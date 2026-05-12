# DevOps AI Prompts & Integration

This folder contains the core intelligence for orchestrating **DevOps AI Agents**, specifically focused on proactively managing and troubleshooting HestiaCP servers.

Instead of locking our logic to a specific low-code platform, we designed these System Prompts and knowledge bases to be **completely platform-agnostic**. This means you can import these models and plug them into your preferred AI engine:
*   **n8n** (Automation Pipelines)
*   **Dify** / **Flowise** / **LangFlow** (Low-Code LLM Builders)
*   **Node.js / Python** (Your own custom Multi-Agent System / Swarm)

## Recommended Agent Architecture

To maintain the highest level of security and DevOps precision, we recommend separating the workload into two independent modules or agents (Orchestrator/Sentinel Pattern):

*   **1. System Monitor (Passive Statistical Audit)**
    An Agent or Pipeline that performs periodic systemic audits based on your scheduled telemetry (CRON jobs outputting RAM, CPU, Disk, Exim, Hestia status). It determines the infrastructure's health and decides whether active operations are required. This prompt is ideal for ingesting structured data and firing summarized alerts to Telegram, Slack, or Discord if the state becomes **"ALERT"**.

*   **2. DevOps Agent (Active Resolution via SSH)**
    The reactive brain and actual executor of the system. This agent acts conversationally and on-demand, serving as an interactive remote hands tool. Based on its identity (`DevOps-Agent-Prompt.md`) combined with the technical notes found in `/knowledge`, it has full planning autonomy. It requires support for `ReAct` (Reasoning & Action) loops and the injection of a Root SSH connection tool (`run_ssh_command`).

## How to Use
The Markdown files in the `/knowledge` directory should ideally be provided to the Active Agent (DevOps Agent) in a RAG (Retrieval-Augmented Generation) format. Alternatively, they can be statically injected into the Context Window if the model's token limit allows (modern models like `gpt-4o`, `claude-3.5-sonnet`, or `gemini-1.5-pro` handle this perfectly).

Before deploying to your production environment, remember to edit the placeholder tags (like bracketed domains and `<IP>` tags) inside the Prompts to reflect your actual domains and infrastructure realities!
