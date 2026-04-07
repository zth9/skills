#!/usr/bin/env python3
"""
Initialize a research repository with the LLM Wiki structure.
"""
import os
import sys
from pathlib import Path
from datetime import datetime

def init_repo(repo_path: str):
    """Initialize the research repository structure."""
    repo = Path(repo_path)

    # Create main directories
    (repo / "raw").mkdir(parents=True, exist_ok=True)
    (repo / "raw" / "assets").mkdir(exist_ok=True)
    (repo / "wiki").mkdir(exist_ok=True)

    # Create index.md
    index_path = repo / "wiki" / "index.md"
    if not index_path.exists():
        index_path.write_text("""# Wiki Index

## Overview
This is the central index of your research wiki. All pages are listed here by category.

## Categories

### Sources
*Source documents and their summaries*

### Entities
*People, organizations, places, products*

### Concepts
*Ideas, theories, frameworks, methodologies*

### Analyses
*Comparisons, syntheses, deep-dives*

---
Last updated: {date}
""".format(date=datetime.now().strftime("%Y-%m-%d")))

    # Create log.md
    log_path = repo / "wiki" / "log.md"
    if not log_path.exists():
        log_path.write_text("""# Research Log

This is a chronological record of all operations on this wiki.

## [{date}] init | Repository initialized

Repository structure created with raw/ and wiki/ directories.

""".format(date=datetime.now().strftime("%Y-%m-%d")))

    # Create AGENTS.md schema (canonical), with CLAUDE.md and GEMINI.md as symlinks
    schema_path = repo / "AGENTS.md"
    if not schema_path.exists():
        schema_path.write_text("""# Research Wiki Schema

## Purpose
This is a personal research wiki maintained by an LLM. The wiki accumulates and organizes knowledge from sources over time.

## Directory Structure

- `raw/` - Immutable source documents (articles, papers, images, data)
- `raw/assets/` - Downloaded images and media from sources
- `wiki/` - LLM-maintained markdown pages
- `wiki/index.md` - Content catalog with links and summaries
- `wiki/log.md` - Chronological operation log

## Page Types

### Source Summaries
- Filename: `wiki/source_<title>.md`
- Content: Key takeaways, main arguments, notable quotes
- Frontmatter: `source`, `date`, `type`

### Entity Pages
- Filename: `wiki/entity_<name>.md`
- Content: Description, mentions across sources, relationships
- Frontmatter: `type: entity`, `category`

### Concept Pages
- Filename: `wiki/concept_<name>.md`
- Content: Definition, evolution across sources, related concepts
- Frontmatter: `type: concept`

### Analysis Pages
- Filename: `wiki/analysis_<topic>.md`
- Content: Synthesis, comparisons, insights
- Frontmatter: `type: analysis`, `sources`

## Workflows

### Ingest Source
1. Read the source document from `raw/`
2. Extract key information and takeaways
3. Create/update source summary page in `wiki/`
4. Update relevant entity and concept pages
5. Add cross-references between pages
6. Update `wiki/index.md` with new entries
7. Append entry to `wiki/log.md`

### Answer Query
1. Read `wiki/index.md` to find relevant pages
2. Read identified pages for detailed information
3. Synthesize answer with citations
4. If answer is valuable, file it as a new analysis page
5. Log the query in `wiki/log.md`

### Lint Wiki
1. Check for contradictions between pages
2. Find orphan pages with no inbound links
3. Identify missing cross-references
4. Suggest new questions or sources to investigate
5. Update stale information

## Conventions

- Use `[[page_name]]` for internal wiki links
- Always cite sources with `[source_title](source_page.md)`
- Keep index.md organized by category
- Log entries format: `## [YYYY-MM-DD] operation | Description`
- Use YAML frontmatter for metadata
""")

    # Create symlinks for other agent CLIs
    for link_name in ["CLAUDE.md", "GEMINI.md"]:
        link_path = repo / link_name
        if not link_path.exists():
            link_path.symlink_to("AGENTS.md")

    print(f"✅ Research repository initialized at: {repo.absolute()}")
    print(f"   - raw/ (source documents)")
    print(f"   - wiki/ (LLM-maintained pages)")
    print(f"   - AGENTS.md (schema and conventions)")
    print(f"   - CLAUDE.md -> AGENTS.md")
    print(f"   - GEMINI.md -> AGENTS.md")

    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python init_repo.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]
    init_repo(repo_path)
