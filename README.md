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
## Install
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

## How to use the agent
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

You may prompt this agent to perform the operations mentioned in `Overview`. It has access to git utilities to automatically push changes to your repository.

## Extensions

### Specification-Based Testing Generator


### AI Code Review Agent

## Frequently Asked Questions
***How does the agent integrate with Github workflows?***
The agent interacts with the CI runs on multiple branches within your repository: `feature`, `test-improvement`, and `bugfix`

Here is where the agent will be making commits. PRs into `main` get the same test + coverage gating.

After the agent reaches a coverage threshold (set to 80%), it publishes a simple coverage summary to GitHub Actions 

***How does the "Automated Test Improvement" work?****

The agent has an elaborate feedback loop which has access to rich MCP tools. Essentially, the agent analyzes existing tests & the tests it creates and measures the coverage gaps using the Jacoco report generated at runtime. The agent gracefully attempts to handle test failures with debugging and fix generation.

***What if the codebase the agent is working on has a bug, or the agent creates a bug in a created, how is it handled?***


The agent is instructed to expose bugs in the code, and implements fixes before moving on. It works on these changes within the `bugfix` branch
