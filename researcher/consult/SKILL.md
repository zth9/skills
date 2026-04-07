---
name: researcher:consult
description: Query knowledge from research wiki and output comprehensive professional documents. Use when user asks questions about researched topics, wants to synthesize knowledge, or says "consult", "query", "ask", "summarize findings".
---

# Researcher Consult

Query knowledge from the research wiki and synthesize comprehensive professional documents using multi-agent analysis.

## Multi-Agent Analysis Workflow

**REQUIRED**: Always deploy **at least 3 parallel subagents** to analyze from different perspectives:

**Agent 1 - Knowledge Synthesizer**
- Read and synthesize relevant wiki pages
- Connect concepts across different sources
- Build comprehensive knowledge map for the query

**Agent 2 - Deep Diver**
- Explore source documents and code in detail
- Extract specific examples, data, and evidence
- Verify claims and trace back to original sources

**Agent 3 - Critical Analyst**
- Identify gaps, contradictions, and limitations
- Question assumptions and challenge conclusions
- Highlight what's unknown or uncertain

**Optional additional agents** (based on query complexity):
- **Practical Implementer**: Focus on actionable steps and code examples
- **Comparative Analyst**: Compare different approaches and tradeoffs
- **Domain Expert**: Apply domain-specific knowledge and best practices

## Main-Agent Synthesis

After collecting all subagent results:

1. **Integrate perspectives**: Combine insights from all agents
2. **Resolve conflicts**: Address contradictions between agents
3. **Structure output**: Organize into coherent professional document
4. **Add citations**: Link back to wiki pages and sources
5. **Highlight confidence**: Mark areas of certainty vs. uncertainty

## Workflow

### Phase 1: Multi-Agent Parallel Analysis

1. **Identify relevant wiki pages**: Read `wiki/index.md` to find related content
2. **Launch 3+ subagents in parallel**: Each agent independently:
   - Reads identified wiki pages (use grep if needed)
   - Explores source documents and code repos as needed
   - Analyzes from their specific perspective (Synthesizer/Diver/Critic)
   - Produces their findings and insights
3. **Collect agent results**: Wait for all agents to complete

### Phase 2: Main-Agent Synthesis

4. **Integrate perspectives**: Combine insights from all subagents
5. **Resolve conflicts**: Address contradictions and gaps
6. **Synthesize complete professional document**: Structure coherent output
7. **Save to temp directory**: `/tmp/researcher_consult_<topic>_<timestamp>.md`
8. **Append to log**: `wiki/log.md` → `## [YYYY-MM-DD] consult | <query> | /tmp/researcher_consult_<topic>_<timestamp>.md`
9. **Present to user**: Output final document with citations

**Note**: Consult results are saved to `/tmp` (not in wiki) as they are query-specific outputs, not persistent knowledge. The log entry records the query and temp file path for reference.

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

Consult results are saved to `/tmp` with this format:

```markdown
---
type: analysis
query: Original query
date: YYYY-MM-DD
timestamp: YYYY-MM-DD_HH-MM-SS
sources: [source1, source2]
---
# Analysis: Topic
[Complete professional document content]
```

File path: `/tmp/researcher_consult_<topic>_<timestamp>.md`

## Maintenance Operations

**Lint Wiki** (periodic execution):
- Find contradictions between pages
- Identify orphan pages (no inbound links)
- Flag outdated information
- Suggest new research directions

## Notes

- Consult results saved to `/tmp` (not in wiki) as they are query-specific outputs
- Log entry in `wiki/log.md` records query and temp file path for reference
- For code analysis, consult phase can directly read code for detailed exploration
- Images must be saved to `raw/assets/` first, then interpreted by LLM
- Web scraping uses `/web-access` skill
