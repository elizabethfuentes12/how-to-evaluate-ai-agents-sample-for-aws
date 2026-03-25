# Safety Scoring: Detecting Harmful Agent Outputs

**Agents may leak PII, give unsafe advice, or violate policies. This demo compares deterministic PII detection (free) vs. LLM safety evaluation (semantic) on 5 test responses with known safety labels.**

Based on: [StepShield](https://arxiv.org/abs/2601.22136) (Jan 2026)

## Files

| File | Purpose |
|------|---------|
| `01-safety-scoring.ipynb` | **Main demo** — PII regex vs LLM safety evaluator comparison |
| `requirements.txt` | Python dependencies |

## Run the Demo

Open `01-safety-scoring.ipynb`. Tests 5 responses (3 safe, 2 unsafe) with both approaches.

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../../LICENSE) file for details.
