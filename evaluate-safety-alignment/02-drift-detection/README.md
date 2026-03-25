# Drift Detection: When Agents Get Worse Over Turns

**An agent starts safe but degrades as context accumulates. This demo scores each conversation turn and detects safety drift across a 4-turn conversation.**

Based on: [AgentDrift](https://arxiv.org/abs/2603.12564) (Mar 2026) — Standard metrics miss 65-93% of safety issues.

## Files

| File | Purpose |
|------|---------|
| `02-drift-detection.ipynb` | **Main demo** — Per-turn safety scoring with drift analysis |
| `requirements.txt` | Python dependencies |

## Run the Demo

Open `02-drift-detection.ipynb`. Simulates a 4-turn conversation where safety degrades.

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../../LICENSE) file for details.
