---
name: git-commits
description: Standards and best practices for writing clean Git commit messages and structuring commits.
---

# Git Commit Best Practices Skill

Use this skill when staging files, writing commit messages, or reviewing repository history.

## The Seven Rules of Git Commits

1. **Use Imperative Mood**: Write the subject line as a command (e.g., `Add feature` or `Fix bug`, not `Added feature` or `Fixes bug`). Completes: *"If applied, this commit will [subject_line]"*.
2. **Limit Subject to 50 Characters**: Keep the summary line concise.
3. **Capitalize the Subject Line**: Always start with a capital letter.
4. **No Period at the End**: Do not end the subject line with a period.
5. **Separate Subject from Body**: Include a blank line between the subject line and the body content.
6. **Wrap Body at 72 Characters**: Prevents horizontal scrolling in terminal logs.
7. **Explain Why and What, Not How**: Focus on the reasoning and context of the changes, rather than explaining the code details directly.

## Conventional Commit Structure

For structured versioning, use:
```text
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
* `feat`: A new feature.
* `fix`: A bug fix.
* `docs`: Documentation updates.
* `refactor`: Code changes that neither fix a bug nor add a feature.
* `style`: Code style updates (formatting, white-space, etc.).
* `test`: Adding or correcting tests.
* `chore`: Maintenance tasks, dependencies, or build config.
