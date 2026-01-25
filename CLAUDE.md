# Project Guidelines

## Commit Rules

- Commit messages must be in English

## Skill Naming Convention

- The skill directory name, SKILL.md `name` field, and plugin name must be identical
- Use lowercase with hyphens (kebab-case), e.g., `mac-notifier`, `mermaid-to-img`
- This ensures consistency between `/skill-name` commands and plugin management
- When renaming a skill, update all three locations:
  1. Directory name
  2. SKILL.md `name` field
  3. `.claude-plugin/marketplace.json` plugin `name` and `skills` path

## README Updates

- When adding a new skill, update both `README.md` (Chinese) and `README_EN.md` (English)
- Add the new skill to the "Available Skills" table in both files

## Skill Description Rules

The `description` field in SKILL.md must include two parts:
1. **What it does**: Brief description of the skill's functionality
2. **When to use**: Tell the agent when to trigger this skill

Example format:
```yaml
description: Convert Mermaid diagrams to images. Use when user wants to export/save/convert Mermaid code to PNG/JPG/SVG/PDF format.
```

Bad example (missing trigger condition):
```yaml
description: Convert Mermaid diagrams to images.
```

## Progressive Disclosure

To reduce token consumption, use progressive disclosure when a skill has many scripts or complex documentation:

1. **For skills with 3+ scripts**: Create a `scripts/INDEX.md` file that briefly describes each script's purpose
2. **Main SKILL.md**: Only include the most common usage and reference INDEX.md for details
3. **Detailed docs**: Put comprehensive documentation in separate files (e.g., `docs/` folder)

Example INDEX.md structure:
```markdown
# Scripts Index

| Script | Purpose |
|--------|---------|
| main.py | Primary entry point for basic usage |
| install.sh | Installation and setup |
| utils.py | Internal utilities (not for direct use) |
```

