# Framework Comparison: Choosing the Right Agent SDK for Evaluation Demos

**Date:** March 2026
**Decision:** Strands Agents SDK

---

## Overview

We compared 8 agent frameworks to determine which is best suited for building AI agent evaluation demos -- not just building agents, but specifically evaluating them with research-backed metrics.

---

## Adoption and Ecosystem

| Framework | GitHub Stars | PyPI Downloads/Month | License | Maintainer |
|-----------|-------------|---------------------|---------|------------|
| **AutoGen** | ~56K | ~1.2M | MIT | Microsoft |
| **CrewAI** | ~47K | ~5.8M | MIT | Community |
| **LangGraph** | ~27K | ~40M | MIT | LangChain |
| **smolagents** | ~26K | ~446K | Apache-2.0 | Hugging Face |
| **OpenAI Agents SDK** | ~20K | ~18M | MIT | OpenAI |
| **Google ADK** | ~19K | ~4.5M | Apache-2.0 | Google |
| **PydanticAI** | ~16K | ~15M | MIT | Pydantic |
| **Strands Agents** | ~5.4K | ~5.3M | Apache-2.0 | AWS |

---

## Technical Feature Comparison

| Feature | Strands | LangGraph | AutoGen | CrewAI | OpenAI SDK | Google ADK | PydanticAI | smolagents |
|---------|---------|-----------|---------|--------|------------|------------|------------|------------|
| Bedrock Support | Native | Via LangChain | Via extensions | Via LiteLLM | Via LiteLLM | Via config | Native | Via LiteLLM |
| OpenAI Support | Yes | Yes | Yes (primary) | Yes | Native | Yes | Yes | Yes |
| Anthropic Direct | Yes | Yes | Via extensions | Yes | No | Yes | Yes | Yes |
| Local Models | Yes | Yes | Via extensions | Yes | Via LiteLLM | Yes | Yes | Yes |
| OpenTelemetry | Built-in | Via LangSmith | Community | Enterprise | Custom | Built-in | Via Logfire | No |
| Hook System | Rich typed events | Node callbacks | Event messages | Decorators | RunHooks | Tool confirm | RunContext | Minimal |
| Multi-Agent | Swarm + Graph | Graph composition | Groups/Teams | Crews | Handoffs | Hierarchical | Delegation | Manager |
| Built-in Eval | strands-agents-evals | LangSmith (SaaS) | AutoGen Bench | crewai test | Tracing UI | adk eval CLI | pydantic-evals | No |

---

## Evaluation-Specific Scoring (1-5)

| Criterion | Strands | LangGraph | AutoGen | CrewAI | OpenAI SDK | Google ADK | PydanticAI | smolagents |
|-----------|---------|-----------|---------|--------|------------|------------|------------|------------|
| Trajectory Capture | 5 | 4 | 3 | 2 | 4 | 3 | 5 | 2 |
| LLM-as-Judge Patterns | 4 | 4 | 5 | 3 | 3 | 4 | 5 | 2 |
| Hook System for Measurement | 5 | 3 | 3 | 2 | 5 | 2 | 4 | 1 |
| Multi-Model Support | 5 | 4 | 3 | 4 | 3 | 3 | 5 | 4 |
| Eval Community/Ecosystem | 3 | 5 | 4 | 3 | 4 | 3 | 4 | 2 |
| Code Simplicity for Demos | 5 | 2 | 3 | 4 | 4 | 3 | 5 | 4 |
| **TOTAL** | **27** | **22** | **21** | **18** | **23** | **18** | **28** | **15** |

---

## Why Strands Agents

### Decisive advantages for this repository

1. **Dedicated evaluation SDK** (`strands-agents-evals` v0.1.11): TrajectoryEvaluator, OutputEvaluator, HelpfulnessEvaluator, FaithfulnessEvaluator, ToolSelectionAccuracyEvaluator, GoalSuccessRateEvaluator, Experiment framework, and ActorSimulator for multi-turn simulation.

2. **Richest typed hook system**: `BeforeToolCallEvent`, `AfterToolCallEvent`, `BeforeModelCallEvent`, `AfterModelCallEvent`, `BeforeInvocationEvent`, `AfterInvocationEvent`, `MessageAddedEvent`. Dataclass-based, strongly typed, composable -- ideal for building evaluation instrumentation.

3. **Built-in metrics on every invocation**: `EventLoopMetrics` captures token usage (input/output/cache), latency, cycle counts, cycle durations, per-tool timing, and execution traces automatically.

4. **OpenTelemetry as core dependency**: Every agent run produces OTEL-compatible traces out of the box. Export to Langfuse, Jaeger, Datadog, or any OTLP collector without extra wiring.

5. **First-class Bedrock support**: Native provider, tightest integration. Model switching is a one-line change across Bedrock, OpenAI, Anthropic, Gemini, Ollama.

6. **Multi-agent orchestration**: Swarm (autonomous handoffs) and Graph (deterministic DAG) patterns enable complex evaluation scenarios like judge/executor/validator.

7. **Minimal boilerplate**: Agent + tools + evaluation in under 50 lines. Clean, educational demos.

8. **AgentCore path**: Direct deployment path to Amazon Bedrock AgentCore with built-in evaluation (correctness, helpfulness, safety, goal-success).

### Why not PydanticAI (scored 28/30)?

PydanticAI was the closest competitor with `pydantic-evals`. However:
- Not AWS-first; Bedrock support exists but is secondary
- No AgentCore deployment path
- Multi-agent patterns are less mature (no swarm/graph orchestration)
- For an AWS-focused audience, Strands provides a more cohesive story

### Why not LangGraph?

- Eval features live in LangSmith (paid SaaS), not the open-source framework
- Steep learning curve: graph definitions, state schemas, node functions make demos harder to follow
- Heavy abstraction layers hurt educational clarity

### Why not the others?

- **AutoGen**: Major rewrite (v0.2 to v0.4) fragmented the ecosystem; Azure-centric
- **CrewAI**: Testing only supports OpenAI; tracing is enterprise-only
- **OpenAI SDK**: Requires LiteLLM for non-OpenAI models; vendor lock-in perception
- **Google ADK**: Optimized for Gemini; evaluation tightly coupled to Google ecosystem
- **smolagents**: No hooks, callbacks, tracing, or evaluation utilities

---

## Strands Agents Key APIs for Evaluation Demos

### Agent creation

```python
from strands import Agent, tool
from strands.models.bedrock import BedrockModel

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = Agent(
    model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
    tools=[search],
    system_prompt="You are a helpful research assistant.",
)

result = agent("Find recent papers on AI evaluation")
```

### Accessing metrics

```python
result = agent("do something")
m = result.metrics

# Token usage
m.accumulated_usage["inputTokens"]
m.accumulated_usage["outputTokens"]
m.accumulated_usage.get("cacheReadInputTokens", 0)

# Latency
m.accumulated_metrics["latencyMs"]
m.cycle_count
m.cycle_durations  # list of durations per cycle
```

### Hooks for evaluation instrumentation

```python
from strands.agent.hooks import BeforeToolCallEvent, AfterToolCallEvent
from strands.plugins import Plugin, hook

class EvalPlugin(Plugin):
    name = "eval-tracker"

    def __init__(self):
        self.trajectory = []

    @hook
    def before_tool(self, event: BeforeToolCallEvent):
        self.trajectory.append({
            "tool": event.tool_use["name"],
            "input": event.tool_use.get("input"),
            "timestamp": time.time(),
        })

    @hook
    def after_tool(self, event: AfterToolCallEvent):
        self.trajectory[-1]["result"] = event.result
        self.trajectory[-1]["success"] = event.exception is None
        self.trajectory[-1]["duration"] = time.time() - self.trajectory[-1]["timestamp"]
```

### Multi-agent evaluation (judge pattern)

```python
from strands.multiagent import Swarm

executor = Agent(name="executor", system_prompt="Execute the task...")
judge = Agent(name="judge", system_prompt="Evaluate the executor's output...")

swarm = Swarm([executor, judge], entry_point=executor)
result = swarm("Complete and then evaluate this task")
```

---

## Note on framework-agnostic content

This repository uses Strands Agents. Similar evaluation patterns can be applied in LangGraph, PydanticAI, AutoGen, or other agent frameworks. The core evaluation concepts (LLM-as-judge, trajectory scoring, hallucination detection metrics) are framework-independent -- Strands provides the implementation vehicle.
