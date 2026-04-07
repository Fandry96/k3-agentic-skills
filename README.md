# k3-agentic-skills

**77 curated AI agent skills + a local semantic search engine powered by Gemma.**

No API keys. No cloud dependency. Your skills, your machine, your vectors.

---

## What's Inside

| Component | Description |
|---|---|
| **`skills/`** | 77 production-grade SKILL.md files for any IDE with agent support (Antigravity, Cursor, Windsurf, Claude Code) |
| **`mrl-indexer/`** | Local semantic search over your skills and docs using EmbeddingGemma-300M |
| **`gemma4/`** | Setup guide for running Gemma 4 26B locally for free inference |

## Quick Start

### 1. Install Skills

Copy the `skills/` directory into your project's `.agent/skills/` folder:

```bash
# Clone
git clone https://github.com/Fandry96/k3-agentic-skills.git

# Copy to your project
cp -r k3-agentic-skills/skills/ your-project/.agent/skills/
```

Your AI coding agent will automatically discover and use them.

### 2. Semantic Search (Optional)

Build a local vector index over your skills and documentation:

```bash
pip install sentence-transformers numpy

# Configure source directories in mrl_index.py, then:
python mrl-indexer/mrl_index.py

# Search
python mrl-indexer/mrl_search.py "how to build RAG with postgres"
```

**Under the hood:**
- **Model:** `google/embeddinggemma-300M` (300M params, <200MB RAM)
- **Vectors:** 768-dim with Matryoshka Representation Learning (MRL)
- **Speed:** ~3.5 embeddings/sec on CPU, sub-15ms per query
- **Cost:** $0 — runs entirely on your machine

### 3. Local Inference with Gemma 4 (Optional)

See [`gemma4/SETUP.md`](gemma4/SETUP.md) for running Gemma 4 26B-A4B locally.

---

## Skills Catalog

### AI & Agents
`ai-agents-architect` · `rag-engineer` · `prompt-engineer` · `langgraph` · `gemini-api-dev` · `mcp-builder` · `deep-research`

### Agentic Orchestration *(NEW)*
`multi-agent-task-orchestrator` · `dispatching-parallel-agents` · `parallel-agents` · `subagent-driven-development` · `loki-mode` · `global-chat-agent-discovery` · `protect-mcp-governance`

### Context & Memory *(NEW)*
`context-compression` · `context-optimization` · `context-degradation` · `context-window-management` · `context-guardian` · `context-driven-development` · `agent-memory-systems` · `hierarchical-agent-memory` · `conversation-memory`

### Frontend
`react-patterns` · `nextjs-best-practices` · `frontend-design` · `frontend-developer` · `react-best-practices` · `design-premium` · `design-luxury` · `design-glassmorphism`

### Backend & Integration
`typescript-pro` · `docker-expert` · `gcp-cloud-run` · `prisma-expert` · `stripe-integration` · `n8n-workflow-patterns` · `auth-implementation-patterns`

### Security & Governance *(NEW)*
`security-auditor` · `find-bugs` · `systematic-debugging` · `codebase-audit-pre-push` · `verification-before-completion` · `tool-use-guardian` · `secrets-management` · `protect-mcp-governance` · `differential-review`

### DevOps & Workflow
`docker-expert` · `gcp-cloud-run` · `github-actions-templates` · `git-pushing` · `git-advanced-workflows` · `using-git-worktrees` · `concise-planning` · `phase-gated-debugging` · `executing-plans`

### Design Systems
`design-premium` · `design-luxury` · `design-glassmorphism` · `design-elegant` · `design-editorial` · `design-corporate`

> See the full list in [`skills/`](skills/).

---

## Architecture: Cognitive Stratification

```
+------------------------------------------------+
|  CLOUD (Gemini 3.1 Pro) -- The Architect       |
|  Complex synthesis, multi-file refactoring,     |
|  strategy, research-to-implementation pivots    |
+------------------------------------------------+
|  LOCAL (Gemma 4 26B-A4B) -- The Worker Bee     |
|  High-volume code gen, sensitive data, offline, |
|  function calling, thinking mode, 256K context  |
+------------------------------------------------+
|  LOCAL (EmbeddingGemma-300M) -- The Librarian  |
|  Semantic search, RAG retrieval, index building |
|  768-dim MRL, <200MB RAM, 3.5 emb/sec          |
+------------------------------------------------+
```

**Matryoshka Representation Learning (MRL):** EmbeddingGemma-300M nests information such that earlier dimensions hold the most critical data. You can truncate 768-dim vectors to 256 or 128 dims for faster search with minimal quality loss.

---

## How Skills Work

Each skill is a markdown file (`SKILL.md`) with YAML frontmatter:

```yaml
---
name: my-skill
description: What this skill does and when to use it.
---

# My Skill

## Instructions
Step-by-step instructions the AI agent follows...
```

AI coding agents (Antigravity, Cursor, Claude Code) read these files and follow the instructions when the skill matches the user's task. Think of them as reusable, shareable prompt templates with structure.

---

## Contributing

1. Fork this repo
2. Add your skill to `skills/your-skill-name/SKILL.md`
3. Follow the YAML frontmatter format above
4. Submit a PR with a description of what the skill does

---

## License

Apache 2.0 — Use freely, modify freely, attribute fairly.

---

**Built with the K3 Agentic Ecosystem** · Powered by Google Gemma
