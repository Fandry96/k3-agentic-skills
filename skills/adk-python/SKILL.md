---
name: adk-python
description: "Google Agent Development Kit (ADK) for Python — verified API patterns for building production-grade multi-agent systems. Covers Workflow graphs (ADK 2.0 Beta), LlmAgent, SequentialAgent, LoopAgent, CustomAgent (BaseAgent), MCP integration via McpToolset, FunctionTool, ToolContext state, session management, context compaction, callbacks (before/after agent/model/tool), human input via RequestInput, and the App wrapper. Use when: ADK agent, workflow graph, multi-agent, MCP toolset, HITL, context compaction, session state, agent pipeline."
risk: low
source: "adk.dev official docs (verified May 2026)"
date_added: "2026-05-11"
---

# Google ADK Python — Verified API Skill

> **Source of truth:** `https://adk.dev/` (llms.txt index)
> **ADK 2.0 Beta docs:** `https://adk.dev/workflows/graph-routes/index.md`
> **Install:** `pip install "google-adk[extensions]" --pre` (for 2.0 Beta features)

## Core Imports (Verified)

```python
# Agents
from google.adk.agents import LlmAgent          # Primary LLM-powered agent
from google.adk.agents import BaseAgent          # For custom agents
# Alias: Agent = LlmAgent (from google.adk.agents.llm_agent import Agent)

# Workflow Agents (ADK 1.x — stable)
from google.adk.agents import SequentialAgent    # Runs sub-agents in order
from google.adk.agents import LoopAgent          # Repeats sub-agents until exit
from google.adk.agents import ParallelAgent      # Runs sub-agents concurrently

# Graph Workflows (ADK 2.0 Beta)
from google.adk import Workflow                  # Graph-based workflow
from google.adk import Event                     # Node output events
from google.adk.events import RequestInput       # Human-in-the-loop node
from google.adk.workflow import JoinNode         # Fan-out/fan-in join

# Tools
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

# Sessions & State
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

# Context Compaction
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.apps.llm_event_summarizer import LlmEventSummarizer
from google.adk.models import Gemini
```

## Agent Types

### LlmAgent (Primary)

```python
root_agent = LlmAgent(
    model='gemini-flash-latest',
    name='my_agent',
    instruction='Help the user with their task.',
    tools=[my_function_tool, my_mcp_toolset],
    # Optional:
    # output_key='result',     # Store output in state["result"]
    # sub_agents=[child_a],    # For delegation
)
```

### SequentialAgent (Stable)

Runs sub-agents one after another. No LLM needed.

```python
pipeline = SequentialAgent(
    name="my_pipeline",
    sub_agents=[agent_a, agent_b, agent_c]
)
```

### LoopAgent (Stable)

Repeats sub-agents until max iterations or an agent signals exit.

```python
quality_loop = LoopAgent(
    name="quality_gate",
    sub_agents=[drafter_agent, critic_agent],
    max_iterations=3  # CRITICAL: Always set this
)
```

## ADK 2.0 Beta: Graph-Based Workflows (`Workflow`)

> ⚠️ ADK 2.0 Beta. Do not use in production.

The `Workflow` class defines deterministic directed graphs using an `edges` array. **There is NO `WorkflowAgent`, `add_node()`, or `add_edge()` method.** The graph is fully declarative.

### Basic Sequential Graph

```python
from google.adk import Workflow

root_agent = Workflow(
    name="sequential_workflow",
    edges=[("START", task_A_node, task_B_node)],
)
```

### Conditional Routing

```python
from google.adk import Workflow, Event

def router(node_input: str):
    """Return an Event with a route value to branch."""
    if "urgent" in node_input:
        return Event(route="URGENT_PATH")
    return Event(route="NORMAL_PATH")

root_agent = Workflow(
    name="routing_workflow",
    edges=[
        ("START", task_A, router),
        (router, {
            "URGENT_PATH": urgent_handler,
            "NORMAL_PATH": normal_handler,
        }),
    ],
)
```

### Human-in-the-Loop (HITL)

```python
from google.adk.events import RequestInput
from google.adk import Workflow

def ask_user():
    """Pause execution and request human input."""
    yield RequestInput(message="Select branch (1, 2, or 3):")

def process_input(node_input):
    """Process the human's response."""
    return Event(output=f"User chose: {node_input}")

root_agent = Workflow(
    name="hitl_workflow",
    edges=[("START", ask_user, process_input)],
)
```

### RequestInput Options

```python
yield RequestInput(
    message="Enter your choice:",           # Text prompt
    payload=some_data_dict,                 # Structured data context
    response_schema=MyPydanticModel,        # Expected response format
)
```

### Parallel Fan-Out + Join

```python
from google.adk.workflow import JoinNode

my_join = JoinNode(name="my_join")

root_agent = Workflow(
    name="parallel_workflow",
    edges=[
        ("START", task_A, my_join),
        ("START", task_B, my_join),
        ("START", task_C, my_join),
        (my_join, final_task),
    ],
)
```

### Nested Workflows

```python
root_agent = Workflow(
    name="parent_workflow",
    edges=[
        ("START", task_A, router),
        (router, {
            "RUN_WORKFLOW_B": child_workflow_B,
            "RUN_WORKFLOW_C": child_workflow_C,
        }),
    ],
)
```

## Tools

### FunctionTool (Plain Python Function)

```python
# ADK auto-discovers tools from plain functions.
# Include in agent's tools list directly — no decorator needed.
def get_weather(city: str) -> dict:
    """Get weather for a city."""
    return {"city": city, "temp": "72°F"}

agent = LlmAgent(
    model='gemini-flash-latest',
    name='weather_agent',
    tools=[get_weather],  # ADK wraps it automatically
)
```

### ToolContext (State Access Inside Tools)

```python
from google.adk.tools import ToolContext

def my_tool(query: str, tool_context: ToolContext) -> dict:
    """Tool with access to session state."""
    # Read state
    count = tool_context.state.get('call_count', 0)
    # Write state (recorded in event state_delta)
    tool_context.state['call_count'] = count + 1
    return {"result": query, "calls": count + 1}
# NOTE: Do NOT include tool_context in the docstring.
# It is injected automatically by the ADK framework.
```

### McpToolset (Connect to MCP Servers)

```python
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

agent = LlmAgent(
    model='gemini-flash-latest',
    name='mcp_agent',
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='node',
                    args=['path/to/mcp-server.js'],
                ),
            ),
            # Optional: filter specific tools
            # tool_filter=['tool_name_1', 'tool_name_2']
        )
    ],
)
```

For remote MCP servers (HTTP/SSE):
```python
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://example.com/mcp",
        headers={"Authorization": "Bearer ..."}
    )
)
```

## Sessions & State

### State Prefixes (Scope)

| Prefix | Scope | Persisted Across |
|---|---|---|
| `state["key"]` | Session-scoped | Current session only |
| `state["app:key"]` | App-scoped | All sessions in app |
| `state["user:key"]` | User-scoped | All sessions for user |
| `state["temp:key"]` | Temporary | Current invocation only |

### Templating in Instructions

```python
agent = LlmAgent(
    name="greeter",
    instruction="Hello {user_name}, you have {task_count} tasks.",
    # {user_name} and {task_count} are resolved from session state
)
```

### Runner (Execution)

```python
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()
session = await session_service.create_session(
    state={}, app_name='my_app', user_id='user1'
)

runner = Runner(
    app_name='my_app',
    agent=root_agent,
    session_service=session_service,
)

events = runner.run_async(
    session_id=session.id,
    user_id=session.user_id,
    new_message=content,
)
async for event in events:
    print(event)
```

## Context Compaction (Anti-Amnesia)

Prevents context explosion during long sessions via sliding-window summarization.

```python
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.apps.llm_event_summarizer import LlmEventSummarizer
from google.adk.models import Gemini

app = App(
    name='my-agent',
    root_agent=root_agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=3,  # Compress every 3 invocations
        overlap_size=1,         # Keep 1 event overlap for continuity
        summarizer=LlmEventSummarizer(
            llm=Gemini(model="gemini-flash-latest")
        ),
    ),
)
```

## Callbacks (Before/After Hooks)

Six callback types for observability and control:

| Callback | Signature | Blocking Behavior |
|---|---|---|
| `before_agent_callback` | `(callback_context) -> Optional[Content]` | Returning Content **bypasses entire agent run** |
| `after_agent_callback` | `(callback_context) -> Optional[Content]` | Appends additional response content |
| `before_model_callback` | `(callback_context) -> Optional[LlmRequest]` | Modify the prompt before LLM call |
| `after_model_callback` | `(callback_context) -> Optional[LlmResponse]` | Modify or replace LLM response |
| `before_tool_callback` | `(tool, args, tool_context) -> Optional[dict]` | Returning a dict **skips tool execution** and uses that dict as result |
| `after_tool_callback` | `(tool, args, tool_context, result) -> Optional[dict]` | Returning a dict **replaces** the original tool output |

Callbacks are set on the `LlmAgent`:

```python
def policy_guard(tool, args, tool_context):
    """Block tool if kill-list word detected."""
    if "DROP TABLE" in str(args):
        return {"error": "BLOCKED by policy"}  # Skips tool
    return None  # Proceed normally

agent = LlmAgent(
    model='gemini-flash-latest',
    name='guarded_agent',
    before_tool_callback=policy_guard,
    after_tool_callback=my_after_tool_fn,
)
```

### Tool Confirmation Flow

For high-stakes tools, ADK supports manual approval:

```python
# When a tool requires confirmation, the runner emits
# a function call event for `adk_request_confirmation`.
# The client must respond with a FunctionResponse
# containing the user's approve/deny decision.
```

> ⚠️ **Server-side tools** (GoogleSearchTool, VertexAiSearchTool) do NOT trigger
> `before_tool_callback` or `after_tool_callback` — they execute inside the Gemini
> service. This is a critical blindspot for audit logging and security guardrails.

## Custom Agents (BaseAgent)

For arbitrary orchestration logic beyond Sequential/Loop/Parallel:

```python
from google.adk.agents import BaseAgent

class MyCustomAgent(BaseAgent):
    my_sub_agent: LlmAgent  # Declare sub-agents as attributes

    async def _run_async_impl(self, ctx):
        """Override this to define custom execution logic."""
        # Run sub-agents and yield their events
        async for event in self.my_sub_agent.run_async(ctx):
            yield event
```

Key rules:
- Must inherit from `BaseAgent`
- Must implement `_run_async_impl` as an async generator
- Pass sub-agents to `super().__init__(sub_agents=[...])` for framework discovery

## Sharp Edges (from Deep Research)

| Issue | Impact | Workaround |
|---|---|---|
| MCP stdio 5-second hardcoded timeout (v1.2.x) | Long-running tool calls fail | Custom session manager to extend timeout |
| `Workflow` inherits `BaseNode`, not `BaseAgent` | `after_agent_callback` **silently no-ops** on Workflow roots | Use node-level callbacks or custom wrapper |
| Server-side tools skip callbacks | GoogleSearchTool/VertexAiSearchTool bypass `before_tool_callback` | Implement audit at model callback level |
| JoinNode hangs if upstream fails | Workflow stuck indefinitely | Ensure every fan-out node has error fallback output |
| Session state Pickle→JSON migration (v1.22) | Old Pickle-format DBs incompatible | Re-create sessions or migrate schema |
| `--pre` flag doesn't override 1.x | `pip install google-adk --pre` fails if 1.x installed | Use `pip install google-adk --pre --force` |
| Workflow incompatible with live streaming | Graph workflows can't use real-time session modes | Use LlmAgent for live streaming use cases |

## PolicyEvaluator (Governance)

ADK integrates with governance engines via the `PolicyEvaluator` protocol. The `ADKPolicyEvaluator` is a YAML-configurable engine wired into `before_tool_callback`.

**Key principle: Monotonic Narrowing** — when a parent agent delegates to a sub-agent, the sub-agent's permissions (tools, max iterations) are always a **subset** of the parent's. A sub-agent can never escalate privileges.

```yaml
# Example k3_policy.yaml (wired via before_tool_callback)
policies:
  - name: "kill_list"
    scope: ["*"]
    action: "reject"
    condition: "output contains banned_word"
  - name: "api_key_leak"
    scope: ["*"]
    action: "reject"
    condition: "output matches AIzaSy.*"
```

## Migration: ADK 1.x → 2.0

- **Python 3.10+** required (1.x supported 3.9)
- **Install:** `pip install google-adk --pre --force`
- **`Workflow` replaces nested `SequentialAgent`/`LoopAgent`** — but they can coexist (1.x agents work as nodes in 2.0 graphs)
- **Session DB schema changed** from Pickle blobs to queryable JSON
- **`Optional` parameters removed** from builders for type safety
- **Security fix in v2.0.1** — upgrade is mandatory for enterprise

## CLI Commands

```bash
adk web                  # Launch debug web UI
adk web --no-reload      # Windows fix for subprocess transport error
adk run <agent_dir>      # Run agent from command line
adk api_server           # Start API server for Cloud Run deployment
```

## Related Skills

Works with: `mcp-builder`, `gemini-api-dev`, `gemini-embedding-2`, `ai-agents-architect`

## Deep Research Source

Full 41-source technical reference: `forge-references/agentic/ADK-2.0-Technical-Reference-Guide.md`
