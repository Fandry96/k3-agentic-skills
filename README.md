# k3-agentic-skills

**82 curated AI agent skills + a local semantic search engine powered by Gemma.**

No API keys. No cloud dependency. Your skills, your machine, your vectors.

---

## What's New (May 2026)

| Skill | Why it matters |
|---|---|
| 🔥 **`adk-python`** | Verified ADK 2.0 Beta API patterns — LlmAgent, Workflow graph, MCP toolsets, HITL, session state. Built from official docs so your agent doesn't hallucinate the API. |
| 🔥 **`gemini-embedding-2`** | GA April 2026. Natively multimodal (text, image, video, audio, PDF). Replaces `text-embedding-004`. Covers the breaking `task_type` → task prefix migration. |
| **`gemini-deep-research-browser`** | Workflow for building a Gemini Deep Research Gem + launching high-precision research sessions. Template included. |
| **`hestiacp-devops`** | Two-brain Orchestrator+Sentinel AI architecture for autonomous VPS management. Covers PHP-FPM tuning, Exim forensics, post-compromise detection. |
| **`blind-spot-advisor`** | Surfaces compliance, trust, conversion, and strategic risks that implementation plans miss. Runs AFTER planning, BEFORE execution. |

---

## What's Inside

| Component | Description |
|---|---|
| **`skills/`** | 82 production-grade SKILL.md files for any IDE with agent support (Antigravity, Cursor, Windsurf, Claude Code) |
| **`mrl-indexer/`** | Local semantic search over your skills and docs using EmbeddingGemma-300M |
| **`gemma4/`** | Setup guide for running Gemma 4 26B locally for free inference |

---

## Quick Start

### 1. Install Skills

```bash
git clone https://github.com/Fandry96/k3-agentic-skills.git

# Copy to your project
cp -r k3-agentic-skills/skills/ your-project/.agent/skills/
```

Your AI coding agent will automatically discover and use them when the task matches a skill description.

### 2. Semantic Search (Optional)

Build a local vector index to find the right skill for any task:

```bash
pip install sentence-transformers numpy

# Indexes all skills/ automatically — no config needed
python mrl-indexer/mrl_index.py

# Search
python mrl-indexer/mrl_search.py "build a multi-agent RAG pipeline"
```

**Under the hood:**
- **Model:** `google/embeddinggemma-300M` (<200MB RAM, runs on CPU)
- **Vectors:** 768-dim with Matryoshka Representation Learning (MRL)
- **Speed:** ~3.5 embeddings/sec on CPU, sub-15ms per query
- **Cost:** $0

### 3. Local Inference with Gemma 4 (Optional)

See [`gemma4/SETUP.md`](gemma4/SETUP.md) for running Gemma 4 26B-A4B locally (free inference, 256K context, function calling, thinking mode).

---

## Skills Catalog

### 🔥 Google ADK & Gemini (New)
`adk-python` · `gemini-embedding-2` · `gemini-deep-research-browser` · `gemini-api-dev`

### AI & Agents
`ai-agents-architect` · `rag-engineer` · `prompt-engineer` · `langgraph` · `mcp-builder` · `deep-research`

### Agentic Orchestration
`multi-agent-task-orchestrator` · `dispatching-parallel-agents` · `parallel-agents` · `subagent-driven-development` · `loki-mode` · `global-chat-agent-discovery` · `protect-mcp-governance`

### Context & Memory
`context-compression` · `context-optimization` · `context-degradation` · `context-window-management` · `context-guardian` · `context-driven-development` · `agent-memory-systems` · `hierarchical-agent-memory` · `conversation-memory`

### Frontend
`react-patterns` · `react-best-practices` · `nextjs-best-practices` · `nextjs-app-router-patterns` · `frontend-design` · `frontend-developer` · `ui-ux-designer` · `stitch-ui-design`

### Design Systems
`design-premium` · `design-luxury` · `design-glassmorphism` · `design-elegant` · `design-editorial` · `design-corporate`

### Backend & Integration
`typescript-pro` · `docker-expert` · `gcp-cloud-run` · `prisma-expert` · `firebase` · `firebase-data-connect` · `stripe-integration` · `n8n-workflow-patterns` · `auth-implementation-patterns`

### Security & Governance
`security-auditor` · `find-bugs` · `systematic-debugging` · `codebase-audit-pre-push` · `verification-before-completion` · `tool-use-guardian` · `secrets-management` · `differential-review` · `blind-spot-advisor`

### DevOps & Infrastructure
`docker-expert` · `gcp-cloud-run` · `hestiacp-devops` · `github-actions-templates` · `git-pushing` · `git-advanced-workflows` · `using-git-worktrees` · `phase-gated-debugging` · `executing-plans`

### Dev Workflow
`plan-writing` · `concise-planning` · `code-reviewer` · `debugging-strategies` · `brainstorming` · `skill-router` · `create-pr` · `webapp-testing`

### Content & Marketing
`content-marketer` · `copywriting` · `page-cro` · `seo-fundamentals`

> Full list in [`skills/`](skills/).

---

## Architecture: Cognitive Stratification

```
+--------------------------------------------------+
|  CLOUD (Gemini 3.1 Pro) — The Architect          |
|  Complex synthesis, multi-file refactoring,       |
|  strategy, research-to-implementation pivots      |
+--------------------------------------------------+
|  LOCAL (Gemma 4 26B-A4B) — The Worker Bee        |
|  High-volume code gen, sensitive data, offline,   |
|  function calling, thinking mode, 256K context    |
+--------------------------------------------------+
|  LOCAL (EmbeddingGemma-300M) — The Librarian     |
|  Skill semantic search, RAG retrieval, indexing   |
|  768-dim MRL, <200MB RAM, 3.5 emb/sec, $0        |
+--------------------------------------------------+
```

**Note on embeddings:** If you're building RAG with API access, use `gemini-embedding-2` (GA April 2026, multimodal, 3072-dim). For local/offline skill search with zero cost, use EmbeddingGemma-300M via the `mrl-indexer/`.

---

## How Skills Work

Each skill is a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: adk-python
description: "Google Agent Development Kit (ADK) for Python — verified API patterns..."
---

# Google ADK Python — Verified API Skill

## Core Imports (Verified)
from google.adk.agents import LlmAgent
...
```

AI coding agents (Antigravity, Cursor, Claude Code, Windsurf) read these files and follow the instructions when the skill matches the task. Think of them as structured, shareable, version-controlled system prompts.

The `description` field is what agents use for semantic routing — make it dense with trigger keywords.

---

## Highlight: `adk-python` Skill

The ADK Python skill covers verified patterns from [adk.dev](https://adk.dev/) including:

- `LlmAgent`, `SequentialAgent`, `LoopAgent`, `ParallelAgent`
- ADK 2.0 `Workflow` graph with conditional routing
- `McpToolset` + `StdioConnectionParams` for MCP integration
- `FunctionTool` with `ToolContext` state access
- `RequestInput` for Human-in-the-Loop (HITL) nodes
- `InMemorySessionService` + `VertexAiSessionService`
- `before_model_callback` / `after_tool_callback` patterns
- `generate_content_config` with `ThinkingConfig` (thinking levels: minimal/low/medium/high)

All patterns are verified against the live docs. No hallucinated APIs.

---

## Highlight: `gemini-embedding-2` Skill

Covers the GA April 2026 release of Google's natively multimodal embedding model:

- **Breaking change:** `task_type` parameter is gone — replaced by string prefixes in content
- Asymmetric retrieval prefixes: `task: search result | query: ...` vs `title: X | text: Y`
- MRL truncation: 128 / 256 / 512 / 768 / 1536 / 3072 dims
- Multimodal: text + image + video + audio + PDF in one model
- Migration guide from `gemini-embedding-001` and `text-embedding-004`
- Python, JavaScript, and REST examples

---

## Contributing

1. Fork this repo
2. Add your skill to `skills/your-skill-name/SKILL.md`
3. YAML frontmatter: `name`, `description` (make the description dense with trigger keywords)
4. Submit a PR

---

## License

Apache 2.0 — Use freely, modify freely, attribute fairly.

---

**Built with the K3 Agentic Ecosystem** · Powered by Google Gemma & Gemini
