from __future__ import annotations
from fastmcp import FastMCP
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, cast
import json
import shutil

import javalang
from javalang.tree import CompilationUnit
from javalang import tree as jl_tree

############### DATA STRUCTS ##################

@dataclass
class MethodInfo:
    name: str
    return_type: Optional[str]
    parameters: List[Dict[str, str]]
    modifiers: List[str]
    is_static: bool
    is_constructor: bool
@dataclass 
class ClassInfo:
    package: str
    class_name: str
    file_path: str
    methods: List[MethodInfo]

########## HELPERS ###############

def _find_java_sources(project_root: Path) -> List[Path]:
    main_java = project_root / "src" / "main" / "java"
    if main_java.exists():
        return list(main_java.rglob("*.java"))
    return list(project_root.rglob("*.java"))

def _extract_package_and_classes(java_path: Path) -> Optional[ClassInfo]:
    code = java_path.read_text(encoding="utf-8", errors="ignore")

    try:
        cu = cast(CompilationUnit, javalang.parse.parse(code))
    except javalang.parser.JavaSyntaxError:
        return None
    
    pkg_node = getattr(cu, "package", None)
    pkg = pkg_node.name if pkg_node is not None else ""
    
    for _, class_node in cu.filter(jl_tree.ClassDeclaration):
        methods: List[MethodInfo] = []

        # methods
        for m in class_node.methods: # pyright: ignore[reportAttributeAccessIssue]
            modifiers = list(m.modifiers or [])
            is_static = "static" in modifiers

            params: List[Dict[str, str]] = []
            for p in m.parameters:
                param_type = p.type.name
                if p.type.dimensions:
                    param_type += "[]" * len(p.type.dimensions)
                params.append({"name": p.name, "type": param_type})
            
            return_type = m.return_type.name if m.return_type is not None else None

            methods.append(
                MethodInfo(
                    name=m.name,
                    return_type=return_type,
                    parameters=params,
                    modifiers=modifiers,
                    is_static=is_static,
                    is_constructor=False,
                )
            )
        # constructors
        for c in class_node.constructors: # pyright: ignore[reportAttributeAccessIssue]
            modifiers = list(c.modifiers or [])
            is_static = "static" in modifiers

            params: List[Dict[str, str]] = []
            for p in c.parameters:
                param_type = p.type.name
                if p.type.dimensions:
                    param_type += "[]" * len(p.type.dimensions)
                params.append({"name": p.name, "type": param_type})

            methods.append(
                MethodInfo(
                    name=c.name,
                    return_type=None,
                    parameters=params,
                    modifiers=modifiers,
                    is_static=is_static,
                    is_constructor=True,
                )
            )
        
        return ClassInfo(
            package=pkg,
            class_name=class_node.name, # pyright: ignore[reportAttributeAccessIssue]
            file_path=str(java_path),
            methods=methods,
        )
    
    return None

def _analyze_project_internal(project_root: Path) -> Dict[str, Any]:
    sources = _find_java_sources(project_root)
    classes: List[ClassInfo] = []

    for src in sources:
        info = _extract_package_and_classes(src)
        if info is not None:
            classes.append(info)

    classes_dicts = [asdict(c) for c in classes]

    total_methods = sum(len(c.methods) for c in classes)
    public_methods = sum(
        sum(1 for m in c.methods if "public" in m.modifiers)
        for c in classes
    )

    return {
        "project_root": str(project_root),
        "num_java_files": len(sources),
        "num_classes": len(classes),
        "num_methods": total_methods,
        "num_public_methods": public_methods,
        "classes": classes_dicts
    }
################## Coverage Analysis ########################

from typing import Tuple

def _find_jacoco_xml(project_root: Path) -> Optional[Path]:
    report_path = project_root / "target" / "site" / "jacoco" / "jacoco.xml"

    if report_path.exists():
        return report_path
    
    for p in (project_root / "target").rglob("jacoco.xml"):
        return p
    
    return None

def _coverage_from_counters(elem: ET.Element, counter_type: str = "INSTRUCTION") -> Tuple[int, int, float]:
    """
    Read JaCoCo <counter type="INSTRUCTION" missed="X" covered="Y"> and
    return (missed, covered, ratio).
    """
    missed = covered = 0
    for c in elem.findall("counter"):
        if c.attrib.get("type") == counter_type:
            missed = int(c.attrib.get("missed", "0"))
            covered = int(c.attrib.get("covered", "0"))
            break

    total = missed + covered
    ratio = 0.0 if total == 0 else covered / total
    return missed, covered, ratio

def _find_uncovered_lines(method_elem: ET.Element) -> List[int]:
    uncovered: List[int] = []

    for line_elem in method_elem.findall("line"):
        nr = int(line_elem.attrib.get("nr", "0"))
        mi = int(line_elem.attrib.get("mi", "0"))
        ci = int(line_elem.attrib.get("ci", "0"))
        if nr > 0 and mi > 0 and ci == 0:
            uncovered.append(nr)
    return uncovered

def _group_into_ranges(lines: List[int]) -> List[Tuple[int, int]]:
    if not lines:
        return []
    lines = sorted(set(lines))
    ranges: List[Tuple[int, int]] = []
    start = prev = lines[0]
    for n in lines[1:]:
        if n == prev + 1:
            prev = n
            continue
        ranges.append((start, prev))
        start = prev = n
    ranges.append((start, prev))
    return ranges

def _analyze_coverage_internal(jacoco_xml: Path, min_coverage: float = 0.8) -> Dict[str, Any]:
    """
    Parse a JaCoCo XML report, identify under-covered classes/methods,
    and generate improvement recommendations.
    """
    tree = ET.parse(jacoco_xml)
    root = tree.getroot()  # <report>

    classes_summary: List[Dict[str, Any]] = []

    # JaCoCo structure: <report><package><class><method><line>...
    for pkg_elem in root.findall("package"):
        pkg_name_raw = pkg_elem.attrib.get("name", "")  # e.g. "main/price"
        pkg_name = pkg_name_raw.replace("/", ".").strip(".")

        for class_elem in pkg_elem.findall("class"):
            class_name_raw = class_elem.attrib.get("name", "")  # e.g. "main/price/Price"
            sourcefile = class_elem.attrib.get("sourcefilename", "")
            # Best-effort FQN
            simple_name = class_name_raw.split("/")[-1] if class_name_raw else sourcefile.replace(".java", "")
            fqn = f"{pkg_name}.{simple_name}" if pkg_name else simple_name

            missed_instr, covered_instr, instr_ratio = _coverage_from_counters(class_elem, "INSTRUCTION")
            _, _, branch_ratio = _coverage_from_counters(class_elem, "BRANCH")

            methods_info: List[Dict[str, Any]] = []
            total_uncovered_lines = 0

            for method_elem in class_elem.findall("method"):
                m_name = method_elem.attrib.get("name", "")
                desc = method_elem.attrib.get("desc", "")
                line = int(method_elem.attrib.get("line", "0"))

                # Method-level coverage (optional; if missing, defaults to 0/0)
                m_missed_instr, m_covered_instr, m_ratio = _coverage_from_counters(method_elem, "INSTRUCTION")
                uncovered_lines = _find_uncovered_lines(method_elem)
                total_uncovered_lines += len(uncovered_lines)
                ranges = _group_into_ranges(uncovered_lines)

                # Heuristic recommendation
                recs: List[str] = []
                if m_ratio < min_coverage and uncovered_lines:
                    # Very simple heuristics just to give the agent something meaningful to say
                    if m_name.startswith("get") or m_name.startswith("set"):
                        recs.append("Add tests exercising this accessor/mutator with representative field values.")
                    elif "equals" in m_name.lower():
                        recs.append("Add tests for equals() covering same-object, equal-object, and non-equal cases.")
                    elif "toString" in m_name:
                        recs.append("Add tests verifying the toString() output for key object states.")
                    else:
                        recs.append("Add tests that execute all branches and edge cases for this method.")

                    if any("null" in d.lower() for d in [desc]):
                        recs.append("Include tests with null or missing inputs if allowed by the API.")

                methods_info.append(
                    {
                        "name": m_name,
                        "descriptor": desc,
                        "line": line,
                        "instruction_coverage": m_ratio,
                        "uncovered_line_ranges": ranges,
                        "recommendations": recs,
                    }
                )

            class_rec: List[str] = []
            if instr_ratio < min_coverage:
                class_rec.append(
                    f"Increase instruction coverage for {fqn} "
                    f"(current ~{instr_ratio:.0%}); focus on methods with uncovered lines."
                )
            if branch_ratio < min_coverage:
                class_rec.append(
                    f"Add tests to exercise alternate branches in {fqn} (branch coverage ~{branch_ratio:.0%})."
                )
            if total_uncovered_lines == 0 and instr_ratio < 1.0:
                class_rec.append(
                    "JaCoCo reports partial coverage; confirm that helper methods and early returns are tested."
                )

            classes_summary.append(
                {
                    "package": pkg_name,
                    "class_name": simple_name,
                    "fqn": fqn,
                    "source_file": sourcefile,
                    "instruction_coverage": instr_ratio,
                    "branch_coverage": branch_ratio,
                    "uncovered_lines_total": total_uncovered_lines,
                    "methods": methods_info,
                    "recommendations": class_rec,
                }
            )

    # Sort by instruction coverage ascending (worst first)
    classes_summary.sort(key=lambda c: c["instruction_coverage"])

    return {
        "report_file": str(jacoco_xml),
        "classes": classes_summary,
    }

################## JUnit Test Generation ###################

def _package_to_dir(pkg: str) -> str:
    if not pkg: 
        return ""
    return pkg.replace(".", "/")

def _build_test_class_content(class_info: ClassInfo) -> str:
    """
    Generate a simple JUnit 5 test class skeleton for a given ClassInfo.
    """
    pkg_line = f"package {class_info.package};\n\n" if class_info.package else ""

    imports = (
        "import org.junit.jupiter.api.Test;\n"
        "import static org.junit.jupiter.api.Assertions.*;\n\n"
    )

    test_class_name = f"{class_info.class_name}Test"
    lines: List[str] = []

    lines.append(f"public class {test_class_name} {{")
    lines.append("")

    # Generate one test stub per public method
    for m in class_info.methods:
        if "public" not in m.modifiers:
            continue

        method_display_name = m.name
        if m.is_constructor:
            method_display_name = f"{class_info.class_name}Constructor"

        test_method_name = f"test_{method_display_name}"

        lines.append("    @Test")
        lines.append(f"    void {test_method_name}() {{")
        lines.append("        // Arrange")

        # Create an instance for non-static, non-constructor methods
        if not m.is_static and not m.is_constructor:
            lines.append(f"        {class_info.class_name} obj = new {class_info.class_name}();")

        # Parameter TODOs
        for p in m.parameters:
            lines.append(
                f"        // TODO: initialize parameter '{p['name']}' of type '{p['type']}'"
            )

        lines.append("")
        lines.append("        // Act")

        call_prefix = ""
        if not m.is_static and not m.is_constructor:
            call_prefix = "obj."
        elif m.is_static and not m.is_constructor:
            call_prefix = f"{class_info.class_name}."
        # Constructors: keep generic stub
        call = f"{call_prefix}{m.name}("
        call += ", ".join(p["name"] for p in m.parameters)
        call += ")"

        if m.return_type and m.return_type.lower() != "void":
            lines.append(f"        var result = {call};")
        else:
            lines.append(f"        {call};")

        lines.append("")
        lines.append("        // Assert")
        lines.append("        // TODO: add meaningful assertions")
        lines.append("        fail(\"Not yet implemented\");")
        lines.append("    }")
        lines.append("")

    lines.append("}")
    return pkg_line + imports + "\n".join(lines)

def _generate_tests_internal(project_root: Path, overwrite: bool) -> Dict[str, Any]:
    analysis = _analyze_project_internal(project_root)
    class_dicts = analysis["classes"]

    generated_files: List[str] = []
    skipped_files: List[str] = []

    for cdict in class_dicts:
        # cdict is something like:
        # {"package": ..., "class_name": ..., "file_path": ..., "methods": [ { ... }, ... ]}
        # Rebuild MethodInfo objects from the method dicts:
        method_infos = [
            MethodInfo(
                name=m["name"],
                return_type=m["return_type"],
                parameters=m["parameters"],
                modifiers=m["modifiers"],
                is_static=m["is_static"],
                is_constructor=m["is_constructor"],
            )
            for m in cdict["methods"]
        ]

        class_info = ClassInfo(
            package=cdict["package"],
            class_name=cdict["class_name"],
            file_path=cdict["file_path"],
            methods=method_infos,
        )

        # Only create tests for classes that have at least one public method
        if not any("public" in m["modifiers"] for m in cdict["methods"]):
            continue

        src_path = Path(class_info.file_path)

        # Map src/main/java/... to src/test/java/... (or general best effort)
        try:
            _ = src_path.relative_to(project_root / "src" / "main" / "java")
            test_root = project_root / "src" / "test" / "java"
        except ValueError:
            # Fallback: project_root as base
            test_root = project_root / "src" / "test" / "java"

        pkg_dir = _package_to_dir(class_info.package)
        dest_dir = test_root / pkg_dir
        dest_dir.mkdir(parents=True, exist_ok=True)

        test_file = dest_dir / f"{class_info.class_name}Test.java"

        if test_file.exists() and not overwrite:
            skipped_files.append(str(test_file))
            continue

        content = _build_test_class_content(class_info)
        test_file.write_text(content, encoding="utf-8")
        generated_files.append(str(test_file))

    return {
        "project_root": str(project_root),
        "generated_files": generated_files,
        "skipped_files": skipped_files,
        "analysis_summary": {
            "num_classes": analysis["num_classes"],
            "num_public_methods": analysis["num_public_methods"],
        },
    }

############### Maven test execution & parsing of results ######################
def _parse_surefire_reports(reports_dir: Path) -> Dict[str, Any]:
    if not reports_dir.exists():
        return {"suites": [], "summary": {"total_tests": 0, "failures": 0, "errors": 0, "skipped": 0}}

    suites = []
    total_tests = total_failures = total_errors = total_skipped = 0

    for xml_file in reports_dir.glob("TEST-*.xml"):
        tree = ET.parse(xml_file)
        root = tree.getroot()  # <testsuite ...>

        tests = int(root.attrib.get("tests", "0"))
        failures = int(root.attrib.get("failures", "0"))
        errors = int(root.attrib.get("errors", "0"))
        skipped = int(root.attrib.get("skipped", "0"))

        total_tests += tests
        total_failures += failures
        total_errors += errors
        total_skipped += skipped

        cases = []
        for case in root.findall("testcase"):
            cname = case.attrib.get("classname", "")
            name = case.attrib.get("name", "")
            time = case.attrib.get("time", "0")

            status = "passed"
            failure_message = None
            failure_type = None
            failure_text = None

            failure_elem = case.find("failure")
            error_elem = case.find("error")
            skipped_elem = case.find("skipped")

            if failure_elem is not None:
                status = "failure"
                failure_message = failure_elem.attrib.get("message")
                failure_type = failure_elem.attrib.get("type")
                failure_text = (failure_elem.text or "").strip()
            elif error_elem is not None:
                status = "error"
                failure_message = error_elem.attrib.get("message")
                failure_type = error_elem.attrib.get("type")
                failure_text = (error_elem.text or "").strip()
            elif skipped_elem is not None:
                status = "skipped"

            cases.append(
                {
                    "class_name": cname,
                    "test_name": name,
                    "time": time,
                    "status": status,
                    "message": failure_message,
                    "type": failure_type,
                    "details": failure_text,
                }
            )

        suites.append(
            {
                "suite_name": root.attrib.get("name", xml_file.name),
                "file": str(xml_file),
                "tests": tests,
                "failures": failures,
                "errors": errors,
                "skipped": skipped,
                "cases": cases,
            }
        )

    summary = {
        "total_tests": total_tests,
        "failures": total_failures,
        "errors": total_errors,
        "skipped": total_skipped,
    }

    return {"suites": suites, "summary": summary}

def _run_maven_and_parse(project_root: Path, goal: str = "test") -> Dict[str, Any]:
    proc = subprocess.run(
        ["mvn", goal],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    reports_dir = project_root / "target" / "surefire-reports"
    report_data = _parse_surefire_reports(reports_dir)

    return {
        "project_root": str(project_root),
        "maven_goal": goal,
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "reports": report_data,
    }

############### Git Phase 3 helpers ###################

def _run_git(repo_root: Path, args: List[str]) -> subprocess.CompletedProcess:
    """
    Run a git command in the given repository.
    """
    return subprocess.run(
        ["git"] + args,
        cwd=repo_root,
        capture_output=True,
        text=True,
    )


def _parse_git_status_porcelain(repo_root: Path) -> Dict[str, Any]:
    """
    Parse `git status --porcelain=v1` into structured buckets:
    - staged_changes
    - unstaged_changes
    - untracked_files
    - conflicts
    """
    proc = _run_git(repo_root, ["status", "--porcelain=v1"])
    staged: List[Dict[str, str]] = []
    unstaged: List[Dict[str, str]] = []
    untracked: List[str] = []
    conflicts: List[str] = []

    if proc.returncode != 0:
        return {
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "staged_changes": staged,
            "unstaged_changes": unstaged,
            "untracked_files": untracked,
            "conflicts": conflicts,
            "is_clean": False,
        }

    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        # Format: XY <path>
        if line.startswith("??"):
            path = line[3:]
            untracked.append(path)
            continue

        status_x = line[0]
        status_y = line[1]
        path = line[3:]

        if status_x in {"M", "A", "D", "R", "C"}:
            staged.append({"path": path, "status": status_x})
        if status_y in {"M", "D"}:
            unstaged.append({"path": path, "status": status_y})

        # conflict patterns (UU, AA, DD, AU, UD, UA, DU)
        if status_x == "U" or status_y == "U" or (status_x == "A" and status_y == "A") or (status_x == "D" and status_y == "D"):
            conflicts.append(path)

    is_clean = not staged and not unstaged and not untracked

    return {
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "staged_changes": staged,
        "unstaged_changes": unstaged,
        "untracked_files": untracked,
        "conflicts": conflicts,
        "is_clean": is_clean,
    }


# Intelligent filtering for git_add_all
_EXCLUDE_PREFIXES = (
    "target/",
    "build/",
    "out/",
    ".idea/",
    ".vscode/",
    ".gradle/",
    "node_modules/",
)

_EXCLUDE_SUFFIXES = (
    ".class",
    ".log",
    ".tmp",
    ".swp",
    "~",
)
def _is_protected_branch(name: str) -> bool:
    """Branches that should not be committed/pushed to directly."""
    return name in {"main", "master"}

def _should_stage_path(path: str) -> bool:
    """
    Intelligent filter: exclude obvious build artifacts and temp files.
    """
    norm = path.replace("\\", "/")
    for pfx in _EXCLUDE_PREFIXES:
        if norm.startswith(pfx):
            return False
    for sfx in _EXCLUDE_SUFFIXES:
        if norm.endswith(sfx):
            return False
    return True


def _git_status_internal(repo_root: Path) -> Dict[str, Any]:
    return _parse_git_status_porcelain(repo_root)


def _git_add_all_internal(repo_root: Path) -> Dict[str, Any]:
    """
    Stage all changes with intelligent filtering, confirm staging success.
    """
    status_before = _parse_git_status_porcelain(repo_root)
    staged = status_before["staged_changes"]
    unstaged = status_before["unstaged_changes"]
    untracked = status_before["untracked_files"]

    # Collect candidate paths
    candidate_paths: List[str] = []
    skipped_paths: List[str] = []

    for entry in unstaged:
        p = entry["path"]
        if _should_stage_path(p):
            candidate_paths.append(p)
        else:
            skipped_paths.append(p)

    for p in untracked:
        if _should_stage_path(p):
            candidate_paths.append(p)
        else:
            skipped_paths.append(p)

    # Remove duplicates
    candidate_paths = sorted(set(candidate_paths))

    if not candidate_paths:
        return {
            "exit_code": 0,
            "stdout": "",
            "stderr": "",
            "staged_files": [e["path"] for e in staged],
            "skipped_files": skipped_paths,
            "message": "No new changes to stage (or all changes filtered).",
        }

    proc = _run_git(repo_root, ["add"] + candidate_paths)

    # Confirm staging success
    status_after = _parse_git_status_porcelain(repo_root)
    staged_after_paths = {e["path"] for e in status_after["staged_changes"]}
    successfully_staged = [p for p in candidate_paths if p in staged_after_paths]

    return {
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "staged_files": successfully_staged,
        "skipped_files": skipped_paths,
        "remaining_unstaged": status_after["unstaged_changes"],
        "remaining_untracked": status_after["untracked_files"],
    }


def _overall_coverage_summary(repo_root: Path) -> Optional[Dict[str, Any]]:
    """
    Compute overall coverage from JaCoCo if jacoco.xml exists.
    """
    xml_path = _find_jacoco_xml(repo_root)
    if xml_path is None:
        return None

    tree = ET.parse(xml_path)
    root = tree.getroot()

    mi, ci, r_instr = _coverage_from_counters(root, "INSTRUCTION")
    mb, cb, r_branch = _coverage_from_counters(root, "BRANCH")

    return {
        "jacoco_xml": str(xml_path),
        "instruction_missed": mi,
        "instruction_covered": ci,
        "instruction_ratio": r_instr,
        "branch_missed": mb,
        "branch_covered": cb,
        "branch_ratio": r_branch,
    }


def _git_commit_internal(repo_root: Path, message: str) -> Dict[str, Any]:
    """
    Automated commit with standardized messages, including coverage stats
    and branch protection for main/master.
    """
    # Determine current branch
    bproc = _run_git(repo_root, ["rev-parse", "--abbrev-ref", "HEAD"])
    if bproc.returncode != 0:
        return {
            "exit_code": bproc.returncode,
            "stdout": bproc.stdout,
            "stderr": bproc.stderr,
            "commit_hash": None,
            "message": None,
            "coverage": None,
        }
    branch = bproc.stdout.strip()

    # Branch protection: don't allow direct commits to main/master
    if _is_protected_branch(branch):
        return {
            "exit_code": 1,
            "stdout": "",
            "stderr": f"Direct commits to protected branch '{branch}' are blocked. "
                      "Create a feature branch and commit there instead.",
            "commit_hash": None,
            "message": None,
            "coverage": None,
        }

    # Check if there is anything staged
    diff_proc = _run_git(repo_root, ["diff", "--cached", "--quiet"])
    if diff_proc.returncode == 0:
        return {
            "exit_code": 1,
            "stdout": "",
            "stderr": "No staged changes to commit.",
            "commit_hash": None,
            "message": None,
            "coverage": None,
        }

    coverage = _overall_coverage_summary(repo_root)
    # Standardized prefix; human message appended
    base_msg = f"chore(test-agent): {message}".strip()

    if coverage:
        cov_line = (
            f"[coverage] instructions={coverage['instruction_ratio']:.1%}, "
            f"branches={coverage['branch_ratio']:.1%}"
        )
        full_msg = base_msg + "\n\n" + cov_line
    else:
        full_msg = base_msg

    proc = _run_git(repo_root, ["commit", "-m", full_msg])

    commit_hash = None
    if proc.returncode == 0:
        hproc = _run_git(repo_root, ["rev-parse", "HEAD"])
        if hproc.returncode == 0:
            commit_hash = hproc.stdout.strip()

    return {
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "commit_hash": commit_hash,
        "message": full_msg,
        "coverage": coverage,
        "branch": branch,
    }

    coverage = _overall_coverage_summary(repo_root)
    # Standardized prefix; student's free-form message comes after it
    base_msg = f"chore(test-agent): {message}".strip()

    if coverage:
        cov_line = (
            f"[coverage] instructions={coverage['instruction_ratio']:.1%}, "
            f"branches={coverage['branch_ratio']:.1%}"
        )
        full_msg = base_msg + "\n\n" + cov_line
    else:
        full_msg = base_msg

    proc = _run_git(repo_root, ["commit", "-m", full_msg])

    commit_hash = None
    if proc.returncode == 0:
        hproc = _run_git(repo_root, ["rev-parse", "HEAD"])
        if hproc.returncode == 0:
            commit_hash = hproc.stdout.strip()

    return {
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "commit_hash": commit_hash,
        "message": full_msg,
        "coverage": coverage,
    }


def _git_push_internal(repo_root: Path, remote: str) -> Dict[str, Any]:
    """
    Push to remote with upstream configuration; authentication handled by
    git credential helpers. Protects main/master from direct pushes.
    """
    # Current branch
    bproc = _run_git(repo_root, ["rev-parse", "--abbrev-ref", "HEAD"])
    if bproc.returncode != 0:
        return {
            "exit_code": bproc.returncode,
            "stdout": bproc.stdout,
            "stderr": bproc.stderr,
            "remote": remote,
            "branch": None,
            "has_upstream_before": None,
            "ci_hint": None,
        }
    branch = bproc.stdout.strip()

    # Branch protection: encourage PR workflow for main/master
    if _is_protected_branch(branch):
        return {
            "exit_code": 1,
            "stdout": "",
            "stderr": (
                f"Direct pushes to protected branch '{branch}' are blocked. "
                "Push a feature branch and open a pull request instead."
            ),
            "remote": remote,
            "branch": branch,
            "has_upstream_before": None,
            "ci_hint": None,
        }

    # Check for upstream
    up_proc = _run_git(repo_root, ["rev-parse", "--abbrev-ref", "@{u}"])
    has_upstream = up_proc.returncode == 0

    if has_upstream:
        proc = _run_git(repo_root, ["push", remote, branch])
    else:
        proc = _run_git(repo_root, ["push", "-u", remote, branch])

    # CI/CD hint: this branch push typically triggers pipeline if configured
    ci_hint = (
        f"Pushing branch '{branch}' to remote '{remote}' will typically "
        f"trigger the configured CI/CD pipeline for this repository."
    )

    return {
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "remote": remote,
        "branch": branch,
        "has_upstream_before": has_upstream,
        "ci_hint": ci_hint,
    }


def _git_pull_request_internal(
    repo_root: Path,
    base: str,
    title: str,
    body: str,
) -> Dict[str, Any]:
    """
    Create a pull request against the specified base branch using `gh` CLI.
    Includes coverage metadata in the body when available.
    """
    # Ensure gh CLI is available
    if shutil.which("gh") is None:
        return {
            "exit_code": 1,
            "stdout": "",
            "stderr": "`gh` CLI not found. Install GitHub CLI and authenticate (`gh auth login`).",
            "pull_request_url": None,
        }

    # Current branch
    bproc = _run_git(repo_root, ["rev-parse", "--abbrev-ref", "HEAD"])
    if bproc.returncode != 0:
        return {
            "exit_code": bproc.returncode,
            "stdout": bproc.stdout,
            "stderr": bproc.stderr,
            "pull_request_url": None,
        }
    head_branch = bproc.stdout.strip()

    coverage = _overall_coverage_summary(repo_root)
    # Standard templates if title/body are not provided
    if not title:
        title = f"[test-agent] Changes from {head_branch}"

    meta_lines: List[str] = []
    if coverage:
        meta_lines.append(
            f"- Instruction coverage: {coverage['instruction_ratio']:.1%} "
            f"(missed {coverage['instruction_missed']}, covered {coverage['instruction_covered']})"
        )
        meta_lines.append(
            f"- Branch coverage: {coverage['branch_ratio']:.1%} "
            f"(missed {coverage['branch_missed']}, covered {coverage['branch_covered']})"
        )
    if not body:
        body = "Automated pull request created by the Software Testing Agent.\n\n"
        if meta_lines:
            body += "### Coverage summary\n" + "\n".join(meta_lines)
    else:
        if meta_lines:
            body += "\n\n### Coverage summary\n" + "\n".join(meta_lines)

    # Create PR via gh
    proc = subprocess.run(
        [
            "gh",
            "pr",
            "create",
            "--base",
            base,
            "--head",
            head_branch,
            "--title",
            title,
            "--body",
            body,
            "--json",
            "url",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    pr_url = None
    if proc.returncode == 0:
        try:
            data = json.loads(proc.stdout)
            pr_url = data.get("url")
        except Exception:
            pr_url = None

    return {
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "base": base,
        "head": head_branch,
        "title": title,
        "body": body,
        "pull_request_url": pr_url,
    }

def _auto_test_and_commit_internal(
    repo_root: Path,
    message: str,
    coverage_threshold: float,
    maven_goal: str = "test",
) -> Dict[str, Any]:
    """
    Run tests, check coverage, and automatically stage & commit if thresholds are met.
    """
    # 1) Run Maven tests
    test_result = _run_maven_and_parse(repo_root, goal=maven_goal)
    exit_code = test_result["exit_code"]
    summary = test_result["reports"]["summary"] if test_result["reports"] else {
        "total_tests": 0,
        "failures": 0,
        "errors": 0,
        "skipped": 0,
    }

    if exit_code != 0 or summary["failures"] > 0 or summary["errors"] > 0:
        return {
            "stage": "tests",
            "tests": test_result,
            "coverage": None,
            "git_add": None,
            "git_commit": None,
            "status": "tests_failed",
            "reason": "Maven tests failed or reported failures/errors.",
        }

    # 2) Compute coverage
    coverage = _overall_coverage_summary(repo_root)
    if coverage is None:
        return {
            "stage": "coverage",
            "tests": test_result,
            "coverage": None,
            "git_add": None,
            "git_commit": None,
            "status": "no_coverage",
            "reason": "No JaCoCo report found; run mvn verify or ensure JaCoCo is configured.",
        }

    instr_ratio = coverage["instruction_ratio"]
    if instr_ratio < coverage_threshold:
        return {
            "stage": "coverage",
            "tests": test_result,
            "coverage": coverage,
            "git_add": None,
            "git_commit": None,
            "status": "coverage_below_threshold",
            "reason": (
                f"Instruction coverage {instr_ratio:.1%} is below the "
                f"required threshold of {coverage_threshold:.1%}."
            ),
        }

    # 3) Stage changes (intelligent filtering)
    add_result = _git_add_all_internal(repo_root)

    # 4) Commit with standardized message + coverage metadata
    commit_result = _git_commit_internal(repo_root, message)

    return {
        "stage": "committed",
        "tests": test_result,
        "coverage": coverage,
        "git_add": add_result,
        "git_commit": commit_result,
        "status": "ok",
        "reason": None,
    }


############### MCP ###################
mcp = FastMCP("software-tester")



########### Test Gen Tools #########
@mcp.tool()
def analyze_java_project(project_root: str) -> Dict[str, Any]:
    """
    Analyze a Java project and return classes and method signatures.

    Parameters
    ----------
    project_root : str
        Path to the Java project root folder (contains src/main/java).

    Returns
    -------
    dict
        Summary counts and a list of classes with their method signatures.
    """
    root = Path(project_root).expanduser().resolve()
    return _analyze_project_internal(root)

@mcp.tool()
def generate_junit_tests(
    project_root: str,
    overwrite: bool = False,
) -> Dict[str, Any]:
    """
    Generate JUnit 5 test skeletons based on public method signatures.

    Parameters
    ----------
    project_root : str
        Path to the Java project root folder.
    overwrite : bool, default False
        If false, existing *Test.java files are not overwritten.

    Returns
    -------
    dict
        Paths of generated and skipped test files, plus a small analysis summary.
    """
    root = Path(project_root).expanduser().resolve()
    return _generate_tests_internal(root, overwrite=overwrite)

@mcp.tool()
def run_maven_tests(
    project_root: str,
    goal: str = "test",
) -> Dict[str, Any]:
    """
    Run Maven tests in the given project and parse the results.

    Parameters
    ----------
    project_root : str
        Path to the Java project root folder (contains pom.xml).
    goal : str, default "test"
        Maven goal to run (e.g., "test", "verify").

    Returns
    -------
    dict
        Maven exit code/output and structured test results parsed from Surefire reports.
    """
    root = Path(project_root).expanduser().resolve()
    return _run_maven_and_parse(root, goal=goal)

@mcp.tool()
def analyze_coverage(
    project_root: str,
    min_coverage: float = 0.8,
) -> Dict[str, Any]:
    """
    Analyze a JaCoCo XML report for a Java project and recommend coverage improvements.

    Parameters
    ----------
    project_root : str
        Path to the Java project root (directory containing pom.xml / target/).
    min_coverage : float, default 0.8
        Minimum desired coverage ratio (e.g., 0.8 for 80%).

    Returns
    -------
    dict
        {
          "report_file": ".../jacoco.xml",
          "classes": [
             {
               "package": "main.price",
               "class_name": "Price",
               "fqn": "main.price.Price",
               "source_file": "Price.java",
               "instruction_coverage": 0.65,
               "branch_coverage": 0.40,
               "uncovered_lines_total": 12,
               "methods": [
                  {
                    "name": "compareTo",
                    "descriptor": "(Lmain/price/Price;)I",
                    "line": 42,
                    "instruction_coverage": 0.50,
                    "uncovered_line_ranges": [(45, 47)],
                    "recommendations": [
                       "Add tests that execute all branches and edge cases for this method."
                    ]
                  },
                  ...
               ],
               "recommendations": [
                  "Increase instruction coverage for main.price.Price (current ~65%); focus on methods with uncovered lines.",
                  "Add tests to exercise alternate branches in main.price.Price (branch coverage ~40%)."
               ]
             },
             ...
          ]
        }
    """
    root = Path(project_root).expanduser().resolve()
    xml_path = _find_jacoco_xml(root)
    if xml_path is None:
        return {
            "error": f"Could not find jacoco.xml under {root}. "
                     "Make sure you ran `mvn test` or `mvn verify` with the JaCoCo plugin enabled."
        }

    return _analyze_coverage_internal(xml_path, min_coverage=min_coverage)

########### Git Tools #############
@mcp.tool()
def git_status(repository_path: str) -> Dict[str, Any]:
    """
    Return clean status, staged changes, and conflicts for a Git repository.

    Parameters
    ----------
    repository_path : str
        Path to the local Git repository (directory containing .git).

    Returns
    -------
    dict
        {
          "exit_code": int,
          "stdout": str,
          "stderr": str,
          "staged_changes": [ { "path": str, "status": str }, ... ],
          "unstaged_changes": [ { "path": str, "status": str }, ... ],
          "untracked_files": [ str, ... ],
          "conflicts": [ str, ... ],
          "is_clean": bool
        }
    """
    root = Path(repository_path).expanduser().resolve()
    return _git_status_internal(root)


@mcp.tool()
def git_add_all(repository_path: str) -> Dict[str, Any]:
    """
    Stage all changes with intelligent filtering (exclude build artifacts and temp files).
    Confirms staging success.

    Parameters
    ----------
    repository_path : str
        Path to the local Git repository.

    Returns
    -------
    dict
        {
          "exit_code": int,
          "stdout": str,
          "stderr": str,
          "staged_files": [ str, ... ],
          "skipped_files": [ str, ... ],
          "remaining_unstaged": [ { "path": str, "status": str }, ... ],
          "remaining_untracked": [ str, ... ]
        }
    """
    root = Path(repository_path).expanduser().resolve()
    return _git_add_all_internal(root)


@mcp.tool()
def git_commit(repository_path: str, message: str) -> Dict[str, Any]:
    """
    Automated commit with standardized messages, including coverage statistics.

    Parameters
    ----------
    repository_path : str
        Path to the local Git repository.
    message : str
        Human-readable description of the changes.

    Returns
    -------
    dict
        {
          "exit_code": int,
          "stdout": str,
          "stderr": str,
          "commit_hash": Optional[str],
          "message": Optional[str],
          "coverage": Optional[dict]
        }
    """
    root = Path(repository_path).expanduser().resolve()
    return _git_commit_internal(root, message)


@mcp.tool()
def git_push(repository_path: str, remote: str = "origin") -> Dict[str, Any]:
    """
    Push to remote with upstream configuration.
    Authentication is handled by existing git credential helpers.

    Parameters
    ----------
    repository_path : str
        Path to the local Git repository.
    remote : str, default "origin"
        Name of the remote to push to.

    Returns
    -------
    dict
        {
          "exit_code": int,
          "stdout": str,
          "stderr": str,
          "remote": str,
          "branch": str,
          "has_upstream_before": bool
        }
    """
    root = Path(repository_path).expanduser().resolve()
    return _git_push_internal(root, remote)


@mcp.tool()
def git_pull_request(
    repository_path: str,
    base: str = "main",
    title: str = "",
    body: str = "",
) -> Dict[str, Any]:
    """
    Create a pull request against the specified base branch (default: main).
    Uses standardized templates for the title and body and automatically
    includes coverage metadata when available. Returns the pull request URL.

    Parameters
    ----------
    repository_path : str
        Path to the local Git repository.
    base : str, default "main"
        Base branch to create the PR against.
    title : str
        Optional custom title for the PR.
    body : str
        Optional body text for the PR.

    Returns
    -------
    dict
        {
          "exit_code": int,
          "stdout": str,
          "stderr": str,
          "base": str,
          "head": str,
          "title": str,
          "body": str,
          "pull_request_url": Optional[str]
        }
    """
    root = Path(repository_path).expanduser().resolve()
    return _git_pull_request_internal(root, base, title, body)

@mcp.tool()
def auto_test_and_commit(
    repository_path: str,
    message: str,
    coverage_threshold: float = 0.8,
    maven_goal: str = "test",
) -> Dict[str, Any]:
    """
    Run Maven tests, ensure coverage meets a threshold, and if so
    automatically stage and commit changes.

    This ties the Git workflow directly to the testing/coverage workflow.

    Parameters
    ----------
    repository_path : str
        Path to the local Git repository (and Maven project root).
    message : str
        Human-readable description of the changes (used in the commit message).
    coverage_threshold : float, default 0.8
        Required minimum instruction coverage (e.g., 0.8 for 80%).
    maven_goal : str, default "test"
        Maven goal to run (e.g., "test" or "verify").

    Returns
    -------
    dict
        {
          "stage": "tests" | "coverage" | "committed",
          "status": "ok" | "tests_failed" | "no_coverage" | "coverage_below_threshold",
          "reason": Optional[str],
          "tests": {...},      # from _run_maven_and_parse
          "coverage": {...},   # from _overall_coverage_summary or None
          "git_add": {...} | None,
          "git_commit": {...} | None
        }
    """
    root = Path(repository_path).expanduser().resolve()
    return _auto_test_and_commit_internal(root, message, coverage_threshold, maven_goal)


if __name__ == "__main__":
    mcp.run(transport="sse")