# Software Testing Agent
Author : Brian Cazares

Github : https://github.com/cazaresb/Software_Testing_Agent

## Overview
An intelligent agent (using MCP) that automatically generates, executes, and iterates on test cases to achieve maximum code coverage. This project combines modern AI-assisted development with traditional software engineering practices. Fully integrated using VSCode's Chat features.

### Features:
* Built on Node.js, Maven and Junit for testing.
* JaCoCo Coverage report artifact creation.
* Model Context Protocol servers for development automation.
* Github Workflow for automatic creation and upload of artifacts.
* Custom automation tools for software development workflows: "**AI Code Review Agentt**" "**Specification-Based Testing Generator**"
* Quality Metrics Dashboard that provides comprehensive coverage reports that improves over time.

This project aims to speed up the development process w/ strong software engineering principles, ultimately applicable to real-world development scenarios, with the help of the software testing agent.

As a small demo, this repository contains a run on a Java utility codebase under the directory `/codebase`. 
### Automated Test Improvement
The agent provides automatic test enhancement based on coverage gaps.

The agent handles test failures with debugging and fix generation.

The agent tracks coverage at each iteration of improvement

### Quality Metrics Dashboard
The agent keeps track of its progress as it generates and improves tests by tracking test quality metrics: assertions per test, edge case coverage, and bug fixes.

For example, for each improvement in coverage or bug fixes, a commit is made onto Github by the agent.

Whenever the agent makes a commit to the repo, it will execute the `generate quality metrics dashboard` job.

The following files are created at execution of the workflow job:
* `testing-metrics.json` Instruction + branch coverage countrs and percentages metadata for the MCP agent 
* `testing-dashboard.md` Summarizes coverage and run information on test quality details (assertions, edge cases, bugs fixed).

You can find the dashboard file under `.github/testing-dashboard.md`
## Extension

### Specification-Based Testing Generator
The agent performs boundary value analysis and generates equivalence class test cases.

### AI Code Review Agent
This feature is to come in a later build.

## Output
The agent is instructed to create dashboards / reports on analysis. The files are:
* `testing-dashboard.md`
    * Coverage analysis on the specified respository.
* `ANALYSIS_AND_SPEC_TESTS.md`
    * This document details the comprehensive analysis and specification-based test generation
* `PROJECT_ANALYSIS_RESULTS.md` 
    * The raw statistical results of analysis.

This repo comes pre-loaded w/ samples. Feel free to delete these for clean generation of new files. The agent will automatically generate these when instructed to perform analysis / generation of tests. 
## Installation
Clone the repo with:
```shell
git clone https://github.com/cazaresb/Software_Testing_Agent
```
or use GitHub CLI
```shell
gh repo clone cazaresb/Software_Testing_Agent
```
* This agent was created with VSCode's CoPilot chat feature in mind. You must use VSCode for the base implementation.
* Add your own repo, or test using the codebase included in the repo at Software_Testing_Agent/codebase.
### Working w/ your own Java codebase

**Requirements**
* Java codebase.
* The codebase must be a Maven project.
* The codebase must be configured to produce Jacoco reports. 
* The codebase must have Junit plugin

You can add your own Java codebase by changing the hardcoded .yml file in .github/workflows.

The .yml file currently defaults to this codebase. Change it to your repo's path name or simply its name if inserted as: Software_Testing_Agent/"YourRepoName".

Line 23 of the YML file:
```yml
working-directory: <YourRepoName>
```

For the Model Context Protocol, FastMCP is used. You may view the install instructions at :Link:

* The agent was built with YOLO mode in mind. Use this at your own discretion. You may enable YOLO mode with the following steps: 

Ctrl+Shift+P -> Chat: Settings -> Enable Auto-Approve
* Maven sometimes does not run automatically. The fix to this is to perform the following:

 Ctrl+Alt+P -> Open Auto-Approve Settings -> Add entry "mvn test"

Install the required Python packages:
* FastMCP (extended instructions [link])
```shell
pip install fastmcp
```
* Langchain
```shell
pip install langchain
```
* Javalang
```shell
pip install javalang
```

Now you should be mostly ready to run the Software Testing Agent!

## How to use the agent & demo run
The basic use of this agent is best when you have generated some tests already for your own `Java` codebase. The agent will align itself with the MCP context to improve these tests. Otherwise, the agent will start from scratch after statically analyzing the codebase.

Let's say that the repository I want to automatically create and improve tests on is a repository called `codebase`. I can have the agent work on precisely this with the following:
* Clone this repository and perform all the installation steps mentioned above. For this example, I clone it with the exact name locally `Software_Testing_Agent`
* Once cloned, I need to point the agent to perform its operations on `codebase` (this can be done in multiple ways, this is simply one).
    * Move `codebase` within the `Software_Testing_Agent` directory.
    ```
    Software_Testing_Agent/codebase
    ``` 
    * Change `Line 23` of the .yml file within `.github/worfklows` to point to my directory's name
    ```yml
    working-directory: codebase
    ```

After this, we can create a new repository on GitHub using our local repository. Create a new repository on GitHub and copy the link. Then connect the GitHub repo to your local repo:
``` 
git init -b main
git add .
git commit -m "Initialization"
git remote add origin REMOTE-URL
git push origin main
```
Now, start the FastMCP server to provide utilities to the agent 

```
Software_Testing_Agent> python server.py
```
Now your CoPilot Chat is set up to be a `Software Testing Agent`

You may prompt this agent to perform the operations mentioned in `Overview`. It has access to 
git utilities to automatically push changes to your repository.

In the CoPilot chat, you can select as a tool `Testing Agent`. This is required to ensure the tool uses the utilities provided by the MCP. 

A good first prompt to ensure the agent is communicating / using the utilities properly is:
```
"List all MCP tools"
```
You should see an output such as this
```
I'll list all the MCP (Model Context Protocol) tools available to me in this context:

mcp_testing_agent_analyze_coverage - Analyzes JaCoCo XML reports for Java projects and recommends coverage improvements
mcp_testing_agent_analyze_java_project - Analyzes a Java project and returns classes and method signatures
mcp_testing_agent_auto_test_and_commit - Runs Maven tests, ensures coverage meets a threshold, and automatically stages and commits changes
mcp_testing_agent_generate_junit_tests - Generates JUnit 5 test skeletons based on public method signatures
mcp_testing_agent_generate_spec_based_tests - Generates test cases based on boundary value analysis and equivalence class analysis for a specific method
mcp_testing_agent_git_add_all - Stages all changes with intelligent filtering (excludes build artifacts and temp files)
mcp_testing_agent_git_commit - Creates an automated commit with standardized messages, including coverage statistics
mcp_testing_agent_git_pull_request - Creates a pull request against a specified base branch
mcp_testing_agent_git_push - Pushes changes to a remote repository with upstream configuration
mcp_testing_agent_git_status - Returns clean status, staged changes, and conflicts for a Git repository

These tools are specifically designed for Java project testing, coverage analysis, and Git workflow automation.
```
**IMPORTANT**: If using a CoPilot chat, you must load the prompt manually every session into the chat's memory. Copy everything below the header in `.github/prompts/tester.prompt.md` and paste into the chat. Now the agent is aligned.

Now, I can have my agent automatically test for me. With our current configuration I can have the agent perform a test run and analysis with the following prompt:
```
"Analyze the Java project at software_testing_agent/codebase and run the tests"
```

You should see output such as this:
```
Summary of What's Ready
Created File: SPEC_BASED_TEST_IMPLEMENTATION_GUIDE.md (1,200+ lines)

This guide provides:

✅ 4 Complete Test Suites (JUnit 4 Format)
TypeUtils Spec Tests - 12 test methods

Null handling, identity, superclass assignment
Autoboxing/unboxing, generic types
Equivalence classes mapped with BVA
FastDatePrinter Spec Tests - 15 test methods

Null input, standard formatting, time-only
Epoch, leap year, year boundaries
Timezone handling, DST, locales
FastDateFormat Spec Tests - 16 test methods

3 method variants (Date, Calendar, long)
Consistency tests, thread safety
Performance benchmarking
ConstructorUtils Spec Tests - 14 test methods

Standard classes (String, Integer, Date, ArrayList)
Error cases (abstract, interface, null)
Exception handling
📋 Implementation Structure
Each test includes:

Clear test method naming (spec_##_description)
Specification comment (boundary, equivalence class, expected behavior)
TODO markers for assertion implementation
JavaDoc with BVA context
🎯 Ready-to-Code Format
✅ Coverage Targets Documented
TypeUtils: 35% → 65%+
FastDatePrinter: 29-63% → 70%+
FastDateFormat: 40-60% → 75%+
ConstructorUtils: 60% → 80%+
```
Happy testing! FAQ and Troubleshoting below:

## Frequently Asked Questions & Troubleshooting
***How does the agent integrate with Github workflows?***
The agent interacts with the CI runs on multiple branches within your repository: `feature`, `test-improvement`, and `bugfix`

Here is where the agent will be making commits. PRs into `main` get the same test + coverage gating.

After the agent reaches a coverage threshold (set to 80%), it publishes a simple coverage summary to GitHub Actions 

***How does the "Automated Test Improvement" work?****

The agent has an elaborate feedback loop which has access to rich MCP tools. Essentially, the agent analyzes existing tests & the tests it creates and measures the coverage gaps using the Jacoco report generated at runtime. The agent gracefully attempts to handle test failures with debugging and fix generation.

***What if the codebase the agent is working on has a bug, or the agent creates a bug in a created, how is it handled?***


The agent is instructed to expose bugs in the code, and implements fixes before moving on. It works on these changes within the `bugfix` branch

***My agent cannot find the Jacoco report / complete operations, what do I do?***

The agent relies on the project's configuration to perform most tasks (the exception being static analysis). If the agent fails to find the report, it will attempt to run the tests. However, if Jacoco is not setup, then this will fail.

The agent refers to the absolute path of the codebase it is performing analysis and work on. Ensure you have `Jacoco`, `Maven`, and `Junit` plugins/dependencies required in your codebase's pom.xml file. Your Jacoco plugin must be configured to create a report and Junit dependency for testing.
```xml

<!-- Jacoco Report Dependency -->
<dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.11</version>
      <scope>test</scope>
    </dependency>
  </dependencies>

<plugin> <!-- Jacoco Report Plugin -->
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <version>0.8.12</version> <!-- or the version you prefer -->
      <executions>
        <!-- Attach JaCoCo agent when tests run -->
        <execution>
          <id>prepare-agent</id>
          <goals>
            <goal>prepare-agent</goal>
          </goals>
        </execution>

        <!-- Generate the report after tests -->
        <execution>
          <id>report</id>
          <phase>test</phase> <!-- or verify -->
          <goals>
            <goal>report</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
```

If the tests have not been run yet, then there is no JaCoCo report available yet. You may locally run the tests on the codebase to generate a report, or the agent can do it for you (just ask it). 

Ensure within your `target` folder, a `jacoco` directory exists with a `jacoco.xml` file.
Afterwards, it can re-run analysis with the new JaCoCo report.

***My current tests have build failures, can the agent fix these errors?***

The agent will try its best to fix changes when prompted. The sample `codebase` has a few to demonstrate the adaptability of the agent. However, it is important to provide meaningful prompts to instruct the agent to fix errors. 

**If the codebase has build failures, then a JaCoCO report may not be generated.** This means that analysis cannot be performed.

Use a prompt such as this:
```
"The current codebase has build failures when executing tests, perform static analysis on the tests, propose changes, and revise the tests to improve coverage..."
```

***Does this agent support Junit 4?***

No, but yes. The agent's `MCP` tools are built on `JUnit 5` standards, thus generation of `JUnit 4` is unsupported. 

However, the agent is capable of recognizing `JUnit 4` standard tests, but it is not recommended to use this Software Testing Agent's `MCP` if writing tests in `JUnit 4`