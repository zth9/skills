---
name: researcher:research
description: Ingest sources (files, URLs, code repos) into research wiki with multi-agent analysis. Use when user provides source materials to analyze, wants to add knowledge to the wiki, or says "research", "ingest", "analyze", "add source".
---

# Researcher Research

Ingest and organize sources into the research wiki using multi-agent parallel analysis.

## Multi-Source Support

**When multiple sources are provided**, process them in parallel:

1. **Parse input**: Extract all source identifiers (files, URLs, repos)
2. **Parallel processing**: Launch independent research workflows for each source simultaneously
3. **Each source gets full multi-agent analysis**: 3 subagents (Theory/Practice/Critical) per source
4. **Aggregate results**: Collect all wiki updates and present unified summary

**Example**:
```
/researcher:research https://example.com/article1 https://example.com/article2 ./paper.pdf
```
→ Launches 3 parallel research workflows, each with 3 subagents (9 agents total)

## Source Types

| Source Type | Processing |
|-------------|------------|
| Files (PDF/MD/TXT) | Read from `raw/` directory |
| URLs/Blogs | Use `/web-access` skill to fetch and convert to markdown, save to `raw/` |
| Images | Save to `raw/assets/`, use LLM to interpret content |
| Transcripts/Subtitles | Read text content directly |
| Code Repositories | Clone to repo directory, analyze code files |

## Data Integrity Check

**CRITICAL**: When saving large content (especially from web sources), always verify data completeness:

1. **For tool results saved to temp files** (e.g., `/path/to/tool-results/xxx.txt`):
   - Extract raw data using `jq` or `cat`, NOT manual construction
   - Example: `cat tool-results/xxx.txt | jq -r '.value.textContent' > raw/article.md`

2. **Verify file size after saving**:
   ```bash
   wc -c raw/article.md  # Should match source size
   ```

3. **Only proceed with analysis if verification passes**

See `resources/data-integrity-check.md` for detailed guidelines.

## Multi-Agent Workflow

**For each source**, deploy **3 parallel subagents** with first-principles thinking:

**Agent 1 - Theory Analyst**
- Extract core concepts, principles, models, architecture
- Derive knowledge system from first principles
- Identify key abstractions and design decisions

**Agent 2 - Practice Explorer**
- Focus on implementation details, code examples
- Extract best practices and common patterns
- Analyze performance metrics and engineering tradeoffs

**Agent 3 - Critical Thinker**
- Identify problems, contradictions, limitations
- Flag unresolved challenges and open questions
- Compare pros/cons of different approaches

**Parallelization strategy**:
- Single source: 3 subagents in parallel
- Multiple sources: Launch all sources simultaneously, each with 3 subagents
- Example: 3 sources = 9 subagents running in parallel (3 per source)

## Main-Agent Synthesis

**For each source**, after collecting subagent results:

1. **Generate unique source ID**: `<sanitized_title>_<6_random_chars>` (e.g., `kubernetes_architecture_a3f9d2`)
2. **Create source directory**: `raw/<source_id>/`
3. **Save source content**: 
   - Original content: `raw/<source_id>/content.md` (or `.pdf`, `.txt`, etc.)
   - Metadata: `raw/<source_id>/metadata.json` (URL, date, type, etc.)
4. **Create wiki pages**:
   - `wiki/sources/<source_id>.md` - Source summary with link to `raw/<source_id>/`
   - `wiki/entities/<name>.md` - Entity pages
   - `wiki/concepts/<name>.md` - Concept pages
5. **Add cross-references** `[[page_name]]`
6. **Update** `wiki/index.md`
7. **Append to** `wiki/log.md`: `## [YYYY-MM-DD] ingest | <title> | <source_id>`

**After all sources processed**:
- Present unified summary of all created/updated pages
- Highlight cross-source connections and patterns discovered

## Source Storage Structure

Each source gets its own directory in `raw/`:

```
raw/
├── kubernetes_architecture_a3f9d2/
│   ├── content.md              # Original content
│   ├── metadata.json           # Source metadata
│   └── assets/                 # Source-specific images/files
├── react_hooks_guide_b7e4c1/
│   ├── content.md
│   └── metadata.json
└── assets/                     # Shared assets (deprecated, use source-specific)
```

**Metadata format** (`metadata.json`):
```json
{
  "source_id": "kubernetes_architecture_a3f9d2",
  "title": "Kubernetes Architecture Deep Dive",
  "url": "https://example.com/k8s-arch",
  "type": "article",
  "date_ingested": "2026-04-07",
  "original_format": "html"
}
```

- Clone/copy repository to repo directory
- Research phase: Read key code files, understand architecture
- Consult phase: Continue detailed exploration (consult includes research capability)
- Wiki page types: module pages, interface pages, design pattern pages, data flow pages

## Wiki Page Format

### Source Summary (`wiki/sources/<source_id>.md`)
```markdown
---
source_id: kubernetes_architecture_a3f9d2
source_path: raw/kubernetes_architecture_a3f9d2/
date: YYYY-MM-DD
type: article|paper|code|video|conversation
---
# Source: Title
## Key Points
## Core Arguments
## Related
- [[concepts/container_orchestration]]
- [[entities/kubernetes_foundation]]
```

### Concept Page (`wiki/concepts/<name>.md`)
```markdown
---
type: concept
---
# Concept: Name
## Definition (First Principles)
## Implementation Mechanism
## Evolution (Cross-source Comparison)
## Related Concepts
- [[concepts/related_concept]]
```

### Entity Page (`wiki/entities/<name>.md`)
```markdown
---
type: entity
category: person|organization|product|project
---
# Entity: Name
## Description
## Mentions Across Sources
## Relationships
- [[entities/related_entity]]
```
