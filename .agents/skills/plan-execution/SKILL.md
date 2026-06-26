---
name: plan-execution
description: Guidelines for executing tasks from the implementation plan in sequential phases using small, incremental updates.
---

# Plan Execution & Incremental Implementation

Use this skill when executing task items, writing code, or running verification commands outlined in the implementation plan.

## 1. Phased Execution
* **One Phase at a Time**: Focus execution strictly on the active phase. Do not begin coding tasks for Phase N+1 until Phase N is complete and verified.
* **Task Checklist**: Maintain a `task.md` file to track progress of tasks within the current active phase.

## 2. Incremental Changes
* **Avoid Monolithic Edits**: Do not implement multiple large changes at once. Break edits down into small-to-medium-sized commits.
* **Frequent Verification**: Compile, test, and run checks after completing each small step or task to ensure the project remains stable throughout the execution.

## 3. Testing & Evaluations
* **Evaluations & Tests**: Whenever implementing new features or significantly modifying existing ones, write test cases and evaluation scripts:
  * **Major Features**: Require comprehensive unit/integration tests and behavior evaluations.
  * **Medium & Small Features**: Require targeted test cases for the majority of implementations to maintain consistency and functionality.

## 4. Test Failure Reporting & Changelog
* **Changelog Maintenance**: If any automated test fails during development:
  * Log the failure in `test_changelog.md` in the project root.
  * For each entry, specify:
    1. **Failed Test**: Which test function/suite failed.
    2. **Reason**: The root cause of the failure.
    3. **Resolution**: What was changed to resolve the issue.
  * Simply append new failure logs to `test_changelog.md` without requiring the agent to read it at every run.


