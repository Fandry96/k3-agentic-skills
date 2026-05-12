---
name: gemini-deep-research-browser
alias: "@dp"
description: "Craft and launch a Gemini Deep Research session via a custom Gem. Use when: @dp, @deep-research, research sprint, investigate topic, market research, technical deep-dive."
risk: safe
source: "K3 Agentic Skills"
date_added: "2026-05-12"
---

# @dp — Gemini Deep Research Skill

**Alias:** `@dp [topic]`

Crafts and launches a Gemini Deep Research session using a custom **Deep Research Architect Gem** that you own.

---

## Setup: Create Your Deep Research Gem (One Time)

1. Go to `https://gemini.google.com/gems/create`
2. Name it: `Deep Research Architect`
3. Paste this system prompt:

```
You are a Deep Research Query Architect. Your job is to transform vague research topics into high-precision Gemini Deep Research queries.

When a user gives you a topic:
1. Identify the core question and 2-3 critical sub-questions
2. Add year scope (current year), domain constraints, and format requests (tables, code examples, comparisons)
3. Recommend source type:
   - Technical/general → No sources needed (web-only)
   - User-provided docs → Google Drive attachment
   - Prior research notes → NotebookLM attachment
4. Output:
   a. The paste-ready research query (3-5 sentences, specific)
   b. Source recommendation with reasoning
   c. A 3-item plan checklist of what good research will cover

Keep queries tight. Vague queries produce vague reports.
```

4. Save the Gem. Copy its URL — that's your `@dp` endpoint.

---

## Workflow (3 Steps)

### Step 1 — Craft the Query (Agent)

Expand the user's topic:
- Add year scope (e.g., "2026"), domain constraints
- Request comparison tables or code examples if technical
- Decide source type:
  - Project docs / specs → **Google Drive**
  - Prior research notebook → **NotebookLM**
  - General / technical research → **None**

Open your Gem URL and drop the topic in. It returns a paste-ready research query + plan checklist.

---

### Step 2 — Launch Deep Research (User)

1. Open a new Gemini chat: `https://gemini.google.com/app`
2. Click **`+`** button left of input → **Tools** → **Deep research**
3. Paste the query from your Gem
4. If sources needed: attach via the Sources button before submitting
5. Submit → review the auto-generated plan → click **Start research**

---

### Step 3 — Retrieve Results (User)

When research completes:
- Export as Google Doc → **Share** → **Export**
- Download as `.docx`
- Convert to Markdown: `python -m markitdown report.docx > report.md`
- Store in your project's research directory

---

## Confirmed UI Notes (May 2026)

| Action | Where |
|---|---|
| Activate Deep Research | `+` button → Tools → "Deep research" |
| Attach Google Drive | Sources button → Drive |
| Edit research plan | "Edit plan" before "Start research" |
| Export report | Share icon → Export to Docs |

---

## Curated @dp Prompt Examples

### ADK / Model Architecture
```
@dp Gemini 3.1 model cascading: Flash-Lite drafter → Flash linter → Pro critic — ADK LoopAgent cost and quality tradeoffs 2026
@dp thinking_level None/Low/Medium/High in Gemini 3.1 — token cost, latency, quality per level for multi-agent pipelines
@dp Gemini Batch Mode 50% discount — async batch processing in ADK for non-realtime generation
@dp ARC-AGI-2 benchmark results — what long-horizon agentic tasks Gemini 3.1 Pro handles vs fails at
```

### RAG / Embeddings
```
@dp sqlite-vec vs pgvector for local vector memory at 10k documents — embedding strategies 2026
@dp Gemini Embedding 2 task prefix patterns vs legacy task_type — migration guide and pitfalls
@dp MRL truncation quality vs storage tradeoffs — 256/768/1536/3072 dims benchmarks 2026
```

### Infrastructure
```
@dp Jules GitHub agent autonomous PR workflows — deduplication, branch hygiene, CI/CD best practices 2026
@dp Docker dynamic MCP server pattern — runtime secret injection from GCP Secret Manager
@dp ADK DatabaseSessionService SQLite session persistence — call replay and failure logging patterns
```

### Market / Business Research
```
@dp [your market] competitive landscape 2026 — pricing, features, differentiators comparison table
@dp [your tech stack] security audit patterns — OWASP Top 10 coverage and remediation 2026
```

---

## Tips

- **Be specific upfront.** "AI agents" → bad. "ADK 2.0 LoopAgent vs LangGraph cycles — Python, 2026, cost benchmarks" → good.
- **Use year scope always.** Deep Research's web index is current; anchor it with "2026" to avoid outdated results.
- **Review the plan.** Before clicking "Start research", Deep Research shows you its research plan. Edit it if a key angle is missing.
- **Export immediately.** Reports expire from the chat. Export to Docs right after completion.
