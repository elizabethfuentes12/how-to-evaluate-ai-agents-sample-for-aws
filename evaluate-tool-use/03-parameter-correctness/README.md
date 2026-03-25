# Parameter Correctness: Did the Agent Pass What the User Asked?

**Parameters pass validation but do not match user intent: "New York" becomes "JFK", an unmentioned date is assumed. This demo uses LLM-based semantic evaluation to catch intent mismatches that deterministic checks miss.**

Based on research: [Lost in Execution: Multilingual Robustness of Tool Calling](https://arxiv.org/abs/2601.05366) (Jan 2026)

## Files

| File | Purpose |
|------|---------|
| `03-parameter-correctness.ipynb` | **Main demo** — 5 tool calls with known intent issues, semantic evaluation |
| `requirements.txt` | Python dependencies |

## Run the Demo

Open `03-parameter-correctness.ipynb`. Evaluates 5 simulated tool calls for semantic parameter correctness.

## Research Background

- [Lost in Execution](https://arxiv.org/abs/2601.05366) (Jan 2026) — Parameter value language mismatch is dominant failure
- [EigenData](https://arxiv.org/abs/2603.05553) (Mar 2026) — Outcome-aware evaluation via state correctness

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../../LICENSE) file for details.
