# Trajectory Risk Analysis: Scoring Risk Signals in Agent Behavior

**Trajectory scoring tells you if the path was good. Risk analysis tells you how dangerous it was. This demo computes deterministic risk scores (failures, duplicates, excess calls) from captured trajectories, at zero LLM cost.**

Based on research: [TRACER: Trajectory Risk Aggregation for Critical Episodes](https://arxiv.org/abs/2602.11409) (Feb 2026)

## The Problem

For production monitoring, you need a risk score on every agent invocation. LLM-based evaluation is too slow and expensive for real-time monitoring. You need deterministic risk signals.

## The Solution

A deterministic risk scorer that computes risk from trajectory data:

| Risk Signal | Weight | What It Detects |
|------------|:------:|----------------|
| Failure rate | 40% | Tool calls that returned errors |
| Duplicate rate | 30% | Same tool called multiple times |
| Excess calls | 30% | More calls than expected for the query |

Risk score = weighted average → 🟢 Low (<0.2) | 🟡 Medium (0.2-0.5) | 🔴 High (>0.5)

## Files

| File | Purpose |
|------|---------|
| `02-trajectory-risk-analysis.ipynb` | **Main demo** — Live agent risk analysis + comparison table |
| `requirements.txt` | Python dependencies |

## Run the Demo

Open `02-trajectory-risk-analysis.ipynb`. It uses `TrajectoryPlugin` from Demo 01 to capture live trajectories and compute risk.

## Research Background

- [TRACER](https://arxiv.org/abs/2602.11409) (Feb 2026) — Surprisal, semantic repetition, tool coherence gaps
- [StepShield](https://arxiv.org/abs/2601.22136) (Jan 2026) — Early Intervention Rate and Tokens Saved metrics

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../../LICENSE) file for details.
