---
name: skill-creation
description: Rules, best practices, and directory structures for creating and managing custom agent skills in Google Antigravity.
---

# Custom Skill Creation & Governance

Use this skill when designing, generating, or modifying agent skills under customization roots.

## 1. Skill Folder Structure
Skills are stored inside a dedicated directory under a customization root (e.g., `.agents/skills/<skill-name>/`):
```text
.agents/skills/<skill-name>/
├── SKILL.md                 # Required: Entry point and instructions
├── scripts/                 # Optional: Helper utilities/scripts
├── examples/                # Optional: Reference examples
├── resources/               # Optional: Fixed assets or templates
└── references/              # Optional: Documentation > 500 lines
```

## 2. SKILL.md Formatting
Every skill entry point must be named exactly `SKILL.md` and begin with YAML frontmatter:
```yaml
---
name: skill-identifier
description: Clear trigger phrase. Explains when the skill should be activated.
---
# Skill Title
Detailed instructions, workflow steps, and best practices.
```

## 3. Best Practices & Guidelines
* **Progressive Disclosure**: Keep the main `SKILL.md` instructions under 500 lines. Offload long manuals or extra logs to the `references/` subdirectory to conserve context window tokens.
* **Effective Descriptions**: Since only the frontmatter `name` and `description` are scanned during initial planning, write descriptions that clearly declare when and why to activate the skill.
* **Proactive Caution**: Always obtain explicit user confirmation before modifying shared, non-personal, or global team skills to prevent unexpected behavioral churn.
