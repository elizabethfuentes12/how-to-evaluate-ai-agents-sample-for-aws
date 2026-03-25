# Variance Analysis: Why One Evaluation Run Is Not Enough

**A single evaluation run can be off by ±0.15. This demo runs the same evaluation 5 times, measures variance, and shows that borderline responses have the highest instability.**

Based on research: [On Randomness in Agentic Evals](https://arxiv.org/abs/2602.07150) (Feb 2026) — 60,000-run study

## The Problem

You run an evaluation: score = 0.75. You set a threshold at 0.70. Pass! But the next run gives 0.65. Fail. The response did not change; only the evaluation randomness did.

## The Solution

Run 5 times. Report mean ± stdev. Make decisions on statistics, not single numbers.

## Files

| File | Purpose |
|------|---------|
| `03-variance-multiple-runs.ipynb` | **Main demo** — 5-run variance test + variance by quality level comparison |
| `requirements.txt` | Python dependencies |

## Run the Demo

Open `03-variance-multiple-runs.ipynb`. Two tests: (1) 5 runs of the same evaluation, (2) variance comparison across good/borderline/bad responses.

## Research Background

- [On Randomness](https://arxiv.org/abs/2602.07150) (Feb 2026) — "Minimum 5 independent runs per task, report pass@k"
- [How to Correctly Report LLM-as-a-Judge](https://arxiv.org/abs/2511.21140) (Feb 2026) — Confidence intervals for evaluation

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../../LICENSE) file for details.
