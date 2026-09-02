# Chaos Testing for AI Agents: Stop Trusting Corrupted Tool Data (and Cut Tokens)

**When a tool returns a wrong-but-plausible value buried in a verbose payload, an AI agent reports the bad value as fact and pays tokens to process the junk. One Strands guardrail hook fixes both.** This demo measures the before/after on correctness and token cost with [Strands Agents](https://strandsagents.com) + [Strands Evals 1.0](https://github.com/strands-agents/evals).

*Last updated: 2026-06-20*

## Files

| File | Purpose |
|------|---------|
| `chaos_demo.ipynb` | **Main demo** — before/after on correctness (5/5 → 0/5) and tokens (~−72%), with the agent loop printed and Strands' native token metrics |
| `tools.py` | `get_weather` (Open-Meteo), `search_flights` (Duffel), and `WeatherSanityHook` (the guardrail) |
| `METHODOLOGY.md` | Exactly how the numbers were produced, with measured N=5 results |
| `.env.example` | `OPENAI_API_KEY` (and `DUFFEL_API_KEY` if you use `search_flights`) |
| `requirements.txt` | `strands-agents-evals>=1.0.0` and friends |

## What does the demo show?

A flaky weather API returns `12°C` for Miami in June (real value ~31°C), wrapped in a verbose diagnostic dump. Two things go wrong, and one guardrail fixes both:

| Metric | Before (no guardrail) | After (`WeatherSanityHook`) |
|--------|:---------------------:|:---------------------------:|
| Reports the corrupted value as real | 5 / 5 runs | 0 / 5 runs |
| Avg total tokens | ~1,313 | ~362 (≈ −72%) |

## How does the guardrail work?

Strands fires `AfterToolCallEvent` around every tool call. `WeatherSanityHook` is a `HookProvider` that sees the tool result **before the model does**, range-checks the temperature against an expected band, and on failure replaces the whole payload with a one-line error. That single rewrite both stops the agent trusting a bad value **and** keeps a verbose junk payload out of the context window — correctness and cost from one change. It's the same hook pattern as [`evaluate-safety-alignment/03-guardrail-hooks`](../../evaluate-safety-alignment/03-guardrail-hooks/).

The notebook also runs Strands Evals' built-in `CorruptValues` chaos effect to show the contrast: that effect injects *obvious* garbage (`99999`, `true`, `null`), which the model rejects on its own. The guardrail earns its keep on *plausible* corruption, the case the model can't self-detect.

## Why measure tokens?

Because a guardrail that quarantines a bad, verbose tool result before the model processes it is also a cost optimization. Strands exposes `result.metrics.get_summary()` (token usage + cycle counts) on every invocation, so the demo reads the savings directly — measured, not estimated.

## How do I run it?

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # set OPENAI_API_KEY
```

Open `chaos_demo.ipynb` and run top to bottom. It prints `agent.messages` (the loop) before and after the hook so you can see *why* the answer and the token count change, then measures both across N runs.

> Travel-agent tools adapted, with thanks, from [Ricardo Ceci's `curso-strands-agentcore-2026`](https://github.com/ricardoceci/curso-strands-agentcore-2026).

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../LICENSE) file for details.
