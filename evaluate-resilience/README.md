# Evaluate AI Agent Resilience

[![Python](https://img.shields.io/badge/Python-3.10+-green.svg?style=flat-square&logo=python)](https://python.org) [![AWS](https://img.shields.io/badge/AWS-Bedrock-orange.svg?style=flat-square&logo=amazon-aws)](https://aws.amazon.com/bedrock/)

Resilience evaluation checks whether an AI agent still works when the world stops being perfect: a tool times out, an API returns half a response, or a user actively tries to break it. Standard evaluations only test the happy path, so they pass right up until production, where none of those assumptions hold.

This section implements two resilience techniques using [Strands Evals 1.0](https://github.com/strands-agents/evals). Similar patterns apply in other agent frameworks instrumented with OpenTelemetry traces.

> **Requires `strands-agents-evals>=1.0.0`.** Chaos testing and red teaming were introduced in the 1.0 release (June 2026). Install dependencies from inside each demo folder.

## Demos

| Demo | Focus | What it measures | Time |
|------|-------|------------------|------|
| [**01 - Chaos Testing**](./01-chaos-testing/) | Inject corrupted tool data; a guardrail hook (`AfterToolCallEvent`) cross-checks it before the model sees it | Before/after on **correctness** (5/5 → 0/5 bad answers) **and tokens** (~−72%) | 20 min |
| [**02 - Red Teaming**](./02-red-teaming/) | Generate and run multi-turn adversarial attacks (data exfiltration, excessive agency) that escalate across turns, no scripting | Whether the agent defends, the breach *rate* across runs, and the attack's cost | 20 min |

## Key Concepts

**Chaos testing** measures reliability under broken tools. The dangerous failure is not the obvious one (a timeout, garbage types) — a modern model catches those. It's the *plausible* corruption: a believable wrong value the model can't self-detect and reports as fact. The fix is a guardrail hook that validates the tool result at the boundary, in code, before the model sees it. That also keeps verbose junk out of the context window, so it cuts tokens too.

**Red teaming** measures behavior under adversarial pressure. A generator writes multi-turn attack scenarios for the risk categories you care about (data exfiltration, excessive agency) and escalates across turns the way a real attacker would, so you don't script each turn.

**Chaos is bad luck; red teaming is bad intent.** Chaos asks "do broken tools break my agent?" Red teaming asks "does my agent misbehave when someone pushes it?" You want both before you ship.

**One run is not a measurement.** Both demos are stochastic: the same corruption or attack scores differently run to run. Claims here come from N≥4 runs (see each demo's `METHODOLOGY.md`), and where a single contrast isn't stable, the variance itself is the finding.

## Prerequisites

```bash
cd evaluate-resilience
python3 -m venv .venv
source .venv/bin/activate
pip install strands-agents[openai] strands-agents-evals>=1.0.0 boto3 nest-asyncio
```

> Demos default to `gpt-4o-mini` (set `OPENAI_API_KEY`). Switch to Amazon Bedrock with `BedrockModel`; see [Strands Model Providers](https://strandsagents.com/latest/user-guide/concepts/model-providers/).

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../LICENSE) file for details.
