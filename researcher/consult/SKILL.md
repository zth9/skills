---
name: consult
description: Query knowledge from research wiki and output comprehensive professional documents. Use when user asks questions about researched topics, wants to synthesize knowledge, or says "consult", "query", "ask", "summarize findings".
---

# Researcher Consult

Query knowledge from the research wiki and synthesize comprehensive professional documents.

## Workflow

1. Read `wiki/index.md` to find relevant pages
2. Read identified wiki pages (use grep if needed)
3. If needed, perform supplementary exploration of code repos or source documents
4. Synthesize **complete professional document**
5. **Auto-save** as `wiki/analysis_<topic>_<date>.md`
6. Append to `wiki/log.md`: `## [YYYY-MM-DD] consult | <query>`

## Output Document Standards

Based on query type, output complete professional markdown document with applicable content:

- **Code examples and implementation details** (with language-tagged code blocks)
- **Architecture diagrams and flowcharts** (Mermaid diagrams)
- **Technical comparison tables**
- **Best practices and anti-patterns**
- **Performance metrics and benchmarks**
- **Source citations**: `[source_title](wiki/source_title.md)`

## Typical Query Patterns

| Query Type | Output Focus |
|------------|--------------|
| "Current research progress" | Knowledge coverage map, ingested sources list, exploration directions |
| "Actionable measures" | Practice checklist, implementation steps, code examples |
| "Unresolved problems" | Open questions list, known limitations, research gaps |
| "Mental models and frameworks" | Concept hierarchy diagram, core abstractions, thinking frameworks |
| "First principles breakdown" | Layer-by-layer derivation, basic assumptions, reasoning chain |

## Analysis Page Format

```markdown
---
type: analysis
query: Original query
date: YYYY-MM-DD
sources: [source1, source2]
---
# Analysis: Topic
[Complete professional document content]
```

## Maintenance Operations

**Lint Wiki** (periodic execution):
- Find contradictions between pages
- Identify orphan pages (no inbound links)
- Flag outdated information
- Suggest new research directions

## Notes

- All consult results auto-saved as analysis archive
- For code analysis, consult phase can directly read code for detailed exploration
- Images must be saved to `raw/assets/` first, then interpreted by LLM
- Web scraping uses `/web-access` skill
