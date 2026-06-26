---
name: design-compliance
description: Enforces that all code modifications, feature implementations, and git commits comply with the core design document (core_design.md).
---

# Design Compliance Skill

Use this skill whenever you are about to:
1. Propose architectural or feature changes.
2. Edit or create source files in the project.
3. Prepare a git commit or write commit messages.

## Execution Rules

### 1. Pre-Commit / Pre-Edit Validation
Before executing any git commits or proposing code edits:
* Open and read the [core_design.md](file:///e:/Projects/ollama-wrapper-mcp/core_design.md) file.
* Review the modified/added lines of code.
* Verify compliance against the following design requirements:
  * **Scope check**: Does the change introduce model downloading/pulling APIs? (If yes, block and report violation).
  * **Security check**: Does the text-generation pathway run prompts through the prompt-injection static scanner?
  * **Architecture check**: Is it written using Python and FastMCP?
  * **Minimal Exposure**: Does it stick to listing, running, and interacting with local models?

### 2. Violation Handling
* If a compliance issue is found, stop and present a warning to the user detailng the violation before writing code or committing.
* Format compliance reports as concise bullet points.
