# Token and Cost Tracking: Know What Your Agent Costs

**Every agent call consumes tokens. This demo captures input/output/cache tokens and computes cost per query using Strands built-in `result.metrics`.**

Based on: [Don't Break the Cache](https://arxiv.org/abs/2601.06007) (Jan 2026)

## Files

| File | Purpose |
|------|---------|
| `01-token-cost-tracking.ipynb` | **Main demo** — 3 queries with per-query token and cost breakdown |
| `requirements.txt` | Python dependencies |

## Run the Demo

Open `01-token-cost-tracking.ipynb`. Runs 3 queries and shows token usage, latency, and cost.

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../../LICENSE) file for details.
