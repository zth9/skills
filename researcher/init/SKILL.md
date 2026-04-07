---
name: researcher:init
description: Initialize a research repository with LLM Wiki structure. Use when user wants to create a new research repository, set up knowledge base structure, or says "init", "initialize", "create repo", "setup research".
---

# Researcher Init

Initialize a research repository with the LLM Wiki structure for persistent knowledge accumulation.

## Repository Structure

The initialized repository will have:

```
<repo>/
├── AGENTS.md          # Wiki schema and conventions (canonical)
├── CLAUDE.md          # -> AGENTS.md symlink
├── GEMINI.md          # -> AGENTS.md symlink
├── raw/               # Source documents (each in its own directory)
│   ├── <source_id_1>/
│   │   ├── content.md
│   │   ├── metadata.json
│   │   └── assets/    # Source-specific images/files
│   └── <source_id_2>/
│       ├── content.md
│       └── metadata.json
└── wiki/
    ├── index.md       # Content catalog
    ├── log.md         # Operation log
    ├── source_*.md    # Source summary pages
    ├── entity_*.md    # Entity pages (people, orgs, products)
    ├── concept_*.md   # Concept pages
    └── analysis_*.md  # Analysis pages (deprecated, use /tmp for consult)
```

**Note**: Each source gets a unique directory `raw/<source_id>/` where `source_id` is `<sanitized_title>_<6_random_chars>`.

## Workflow

1. **Check current directory**:
   - If current directory is NOT a git repository → Initialize wiki structure in current directory (`.`)
   - If current directory IS a git repository → Ask user for repository path (default: `./research`)

2. Run initialization script:
   ```bash
   python scripts/init_repo.py <path>
   ```

3. Confirm structure created and explain next steps

## Path Selection Logic

**Non-git directory** (recommended for dedicated wiki repos):
- Initialize directly in current directory
- The entire directory becomes the wiki repository
- No subdirectory needed

**Git repository** (for project-embedded wikis):
- Create `./research` subdirectory by default
- Keeps wiki separate from project code
- User can specify alternative path if needed

## Next Steps

After initialization:
- Use `/researcher:research <source>` to ingest sources
- Use `/researcher:consult <query>` to query knowledge
