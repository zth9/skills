---
name: research
description: Ingest sources (files, URLs, code repos) into research wiki with multi-agent analysis. Use when user provides source materials to analyze, wants to add knowledge to the wiki, or says "research", "ingest", "analyze", "add source".
---

# Researcher Research

Ingest and organize sources into the research wiki using multi-agent parallel analysis.

## Source Types

| Source Type | Processing |
|-------------|------------|
| Files (PDF/MD/TXT) | Read from `raw/` directory |
| URLs/Blogs | Use `/web-access` skill to fetch and convert to markdown, save to `raw/` |
| Images | Save to `raw/assets/`, use LLM to interpret content |
| Transcripts/Subtitles | Read text content directly |
| Code Repositories | Clone to repo directory, analyze code files |

## Multi-Agent Workflow

Deploy **3 parallel subagents** with first-principles thinking:

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

## Main-Agent Synthesis

1. Collect results from three subagents
2. Create/update wiki pages:
   - `wiki/source_<title>.md` - Source summary
   - `wiki/entity_<name>.md` - Entity pages
   - `wiki/concept_<name>.md` - Concept pages
3. Add cross-references `[[page_name]]`
4. Update `wiki/index.md`
5. Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | <title>`
6. Output summary of created/updated pages

## Code Repository Handling

- Clone/copy repository to repo directory
- Research phase: Read key code files, understand architecture
- Consult phase: Continue detailed exploration (consult includes research capability)
- Wiki page types: module pages, interface pages, design pattern pages, data flow pages

## Wiki Page Format

### Source Summary (`source_*.md`)
```markdown
---
source: raw/filename
date: YYYY-MM-DD
type: article|paper|code|video|conversation
---
# Source: Title
## Key Points
## Core Arguments
## Related
- [[concept_name]]
- [[entity_name]]
```

### Concept Page (`concept_*.md`)
```markdown
---
type: concept
---
# Concept: Name
## Definition (First Principles)
## Implementation Mechanism
## Evolution (Cross-source Comparison)
## Related Concepts
- [[related_concept]]
```
