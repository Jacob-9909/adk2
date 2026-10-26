# adk2

**English** | [한국어](README.ko.md)

Example templates for **graph workflows** (`Workflow`) in Google ADK **2.0 alpha**. Six small agents show sequential, branching, parallel fan-out, human-in-the-loop, and dynamic workflows, and you can try each one in the ADK dev UI.

> ADK 2.0 is in alpha. Use 1.x for production. See [ADK docs — Graph-based workflows](https://google.github.io/adk-docs/workflows/).

## Examples

| Agent | Pattern | What it shows |
|---|---|---|
| [`city_workflow`](agents/city_workflow/agent.py) | Sequential | Generate a city → look up local time (function) → LLM report → done message |
| [`routing_workflow`](agents/routing_workflow/agent.py) | Branching | Classifier LLM → `router` → BUG / CUSTOMER_SUPPORT / LOGISTICS |
| [`mixed_fanout_workflow`](agents/mixed_fanout_workflow/agent.py) | Parallel fan-out | Sequential → parallel fan-out (tuple) → `JoinNode` → summary (no LLM) |
| [`human_input_workflow`](agents/human_input_workflow/agent.py) | Human-in-the-loop | `yield RequestInput(...)` → user reply → follow-up function (`response_schema` is `NumberAnswer`) |
| [`itinerary_feedback_workflow`](agents/itinerary_feedback_workflow/agent.py) | HITL with payload | `ActivitiesList` output → `RequestInput(payload=...)` → `UserFeedback` |
| [`dynamic_workflow_demo`](agents/dynamic_workflow_demo/agent.py) | Dynamic | Only `edges=[(START, orchestrator)]`, then `@node` + `ctx.run_node` + `asyncio.gather` (no LLM) |

## Quick Start

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
cp .env.example .env     # set GEMINI_API_KEY or Vertex AI settings
uv run adk web agents
```

Pick one of the agents above in the dev UI that opens in your browser.

## Credentials

Use one of the two options.

**Option A: Gemini API key (AI Studio)** — set `GEMINI_API_KEY` in `.env`.

**Option B: Vertex AI with a service account**

1. In [IAM](https://console.cloud.google.com/iam-admin/iam), grant the service account **Vertex AI User** (`roles/aiplatform.user`).
2. Create a JSON key and store it outside this repo or in `credentials/` (git-ignored).
3. Set these in `.env`:
   - `GOOGLE_APPLICATION_CREDENTIALS`: absolute path to the key file
   - `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`
   - `GOOGLE_GENAI_USE_VERTEXAI=1`

The app picks up the key through ADC. You do not need `gcloud auth application-default login`.
