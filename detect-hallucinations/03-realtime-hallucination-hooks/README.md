# Real-Time Hallucination Detection with Strands Hooks

**Post-hoc evaluation catches hallucinations after they reach the user. This demo uses Strands hooks to detect hallucinations during agent execution, checking each response against tool outputs in real-time before delivery.**

Based on research: [StepShield: When, Not Whether to Intervene on Rogue Agents](https://arxiv.org/abs/2601.22136) (Jan 2026)

## The Problem

Standard evaluation runs **after** the agent finishes. In production, a hallucinated response may already be delivered to the user, triggering a bad action, or eroding trust.

You need evaluation that runs **inline** with agent execution.

## The Solution

A `HookProvider` that intercepts the agent lifecycle:

```
Agent receives query
  → Calls search_flights (hook captures: "BA117 $450, DL1 $520")
  → Calls get_weather (hook captures: "Paris 18C cloudy")
  → Generates final response
  → Hook checks: is response grounded in captured tool outputs?
  → ✅ Score 0.85 → deliver to user
  → ⚠️ Score 0.30 → flag as hallucination
```

The hook collects every tool output as "ground truth" and runs a grounding check when the agent produces its final answer.

### Why Strands Hooks

Strands provides typed hook events that fire at every stage of agent execution:

| Event | When | What We Do |
|-------|------|-----------|
| `BeforeInvocationEvent` | Agent starts processing | Reset collected context |
| `AfterToolCallEvent` | Tool returns result | Capture output as ground truth |
| `AfterModelCallEvent` | Model generates response | Check grounding against collected context |

No polling, no wrapper functions. The hook system is built into the agent runtime.

## Files

| File | Purpose |
|------|---------|
| `03-realtime-hallucination-hooks.ipynb` | **Main demo** — Create agent with hook, run queries, watch real-time detection |
| `hallucination_hook.py` | **Standalone hook + demo** — `HallucinationDetector` class and demo tools |
| `requirements.txt` | Python dependencies |

## Run the Demo

### Notebook

Open `03-realtime-hallucination-hooks.ipynb` in Jupyter or VS Code.

### Standalone

```bash
python hallucination_hook.py
```

**Expected output**:

```
--- Query 1: 'Find flights from NYC to London for Friday' ---
✅ Response grounded (score: 0.90)

--- Query 2: 'What's the weather in Paris?' ---
✅ Response grounded (score: 0.85)

DETECTION SUMMARY
  ✅ Check 1: score=0.90, sources=1
  ✅ Check 2: score=0.85, sources=1
```

## How It Works

### Creating the Hook

```python
from hallucination_hook import HallucinationDetector

detector = HallucinationDetector(threshold=0.5)
agent = Agent(tools=[search_flights], hooks=[detector])
```

### Hook Internals

```python
class HallucinationDetector(HookProvider):
    def register_hooks(self, registry, **kwargs):
        registry.add_callback(BeforeInvocationEvent, self._reset)
        registry.add_callback(AfterToolCallEvent, self._collect_tool_output)
        registry.add_callback(AfterModelCallEvent, self._check_grounding)

    def _collect_tool_output(self, event):
        # event.tool_use["name"] → tool name
        # event.result["content"] → tool output
        self.tool_outputs.append(f"[{tool_name}]: {text}")

    def _check_grounding(self, event):
        # Only on final response (stop_reason == "end_turn")
        # Runs OutputEvaluator against collected tool outputs
```

### Accessing Results

```python
# After agent runs
detector.last_check  # Most recent grounding check
detector.checks      # All checks from this session
detector.checks[-1]["grounding_score"]  # Score of last check
```

## Production Considerations

**Latency**: The grounding check adds 1 LLM call after each final response. For latency-sensitive applications, run the check asynchronously and flag hallucinations after delivery.

**Cost**: 1 extra LLM call per agent response. Use a smaller, faster model (Claude Haiku) for the grounding check to minimize cost.

**Threshold tuning**: Start with 0.5 and adjust based on your false positive/negative tolerance. Lower threshold = fewer flags but more missed hallucinations.

## Research Background

- [StepShield](https://arxiv.org/abs/2601.22136) (Jan 2026) — Early Intervention Rate, Intervention Gap, and Tokens Saved metrics for trajectory safety
- [AgentDrift](https://arxiv.org/abs/2603.12564) (Mar 2026) — Standard metrics miss 65-93% of safety issues; trajectory analysis is essential

## Series Complete

You now have 4 approaches to hallucination detection:

| # | Demo | Approach | When | Best For |
|---|------|----------|------|----------|
| 01 | Strands vs RAGAS | Framework comparison | After execution | Choosing your tool |
| 02 | Claim Decomposition | Per-claim verification | After execution | Root cause analysis |
| 03 | **Hooks (this demo)** | **Real-time detection** | **During execution** | **Production guardrails** |

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../../LICENSE) file for details.
