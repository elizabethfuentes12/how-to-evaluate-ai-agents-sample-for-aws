# Chaos Testing Demo — Methodology and Measured Results

This file documents exactly how the numbers in `chaos_demo.ipynb` were produced, so the
demo's claims are reproducible and honest. LLM behavior varies run to run; this records
what we actually measured and how.

## Setup

- **Model under test:** `gpt-4o-mini` (via `OpenAIModel`)
- **Tool corrupted:** `get_weather` — returns a plausible-but-wrong value (`12.0°C`, real value
  ~31°C) wrapped in a verbose diagnostic dump (retry traces + node logs), simulating a flaky API.
- **Guardrail under test:** `WeatherSanityHook` (in `tools.py`) — fires on `AfterToolCallEvent`,
  range-checks the temperature against an expected seasonal band (25–38°C for Miami in June),
  and on failure replaces the *entire* tool result with a one-line error before the model sees it.
- **Trajectory / token metrics:** Strands native `result.metrics.get_summary()`
  (`accumulated_usage.totalTokens`, `total_cycles`). No LLM judge for the headline numbers.
- **Correctness check:** deterministic regex — did the agent state `12°C` as the forecast
  without flagging it?
- **Package versions:** `strands-agents==1.44.0`, `strands-agents-evals==1.0.0`
- **Date measured:** 2026-06-20

## Measured results (N = 5 runs per condition)

| Condition | Reported the bad value | Avg total tokens | Tool result the model saw |
|-----------|:----------------------:|:----------------:|---------------------------|
| **Before** (no guardrail) | 5 / 5 | ~1,313 | ~5,441 chars (bad value + verbose junk) |
| **After** (`WeatherSanityHook`) | 0 / 5 | ~362 | ~153 chars (one-line error) |

**Headline: correctness 5/5 → 0/5 bad answers; tokens ≈ −72% (1,313 → 362).**

A single representative run measured 1,328 → 355 tokens (−73%); an earlier variant with a
larger junk payload measured −84%. The exact percentage depends on how much garbage the
corrupted tool result carries; the **direction and rough magnitude (~70–80% fewer tokens)** is
the reproducible result, not a single value.

## What we can and cannot claim

**Claim 1 — a guardrail hook fixes a corruption the model can't catch.** A plausible-but-wrong
value (`12°C`) is invisible to the model; it reported it as fact in all 5 baseline runs. The
hook, with an independent expected range, caught it every time (0/5). This is a stable,
deterministic before/after (not an LLM-judge score).

**Claim 2 — the same hook cuts tokens.** Because the hook replaces the verbose corrupted payload
with a one-line error *before* the model processes it, the model ingests far less text. Measured
~−72% total tokens across 5 runs. The savings scale with payload size.

**What we do NOT claim:**
- That Strands' built-in `CorruptValues` effect engaged the agent the same way. It replaces
  values with *obvious* garbage (`99999`, `true`, `null`), which `gpt-4o-mini` rejects on its own
  (shown in the notebook's bonus cell). The dangerous case is *plausible* corruption, which is why
  the main demo injects `12°C` via the tool rather than via `CorruptValues`.
- That a custom `ToolEffect` subclass can inject plausible corruption through `ChaosPlugin`. It
  can't be registered cleanly: `ChaosCase` validates effects against a fixed Pydantic discriminated
  union, so a custom effect tag is rejected. Plausible corruption is therefore injected by the tool
  itself, and the guardrail is a standard `HookProvider`.
- Any single token percentage as exact. Your numbers will differ; the ~70–80% range and the
  5/5 → 0/5 correctness flip are the results.

## Reproduce it

```bash
pip install -r requirements.txt
cp .env.example .env   # set OPENAI_API_KEY (DUFFEL_API_KEY only needed if you add search_flights)
# then run chaos_demo.ipynb top to bottom
```

The notebook prints `agent.messages` (the loop) before and after the hook, the per-run token
metrics, and the N-run aggregate, so every number above is regenerated live.
