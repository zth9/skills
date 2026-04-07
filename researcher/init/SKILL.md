---
name: init
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
├── raw/               # Immutable source documents
│   └── assets/        # Images and media files
└── wiki/
    ├── index.md       # Content catalog
    ├── log.md         # Operation log
    ├── source_*.md    # Source summary pages
    ├── entity_*.md    # Entity pages (people, orgs, products)
    ├── concept_*.md   # Concept pages
    └── analysis_*.md  # Analysis pages (consult results)
```

## Workflow

1. Ask user for repository path (default: `./research`)
2. Run initialization script:
   ```bash
   python scripts/init_repo.py <path>
   ```
3. Confirm structure created and explain next steps

## Next Steps

After initialization:
- Use `/researcher:research <source>` to ingest sources
- Use `/researcher:consult <query>` to query knowledge
