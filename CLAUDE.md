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
