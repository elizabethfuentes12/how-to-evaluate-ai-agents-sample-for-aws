# Tool Selection Accuracy: 3 Ways to Check If Your Agent Picks the Right Tool

**With 10 similar tools available, agents pick the wrong one more often than you think. This demo runs 10 ground-truth queries through a live agent and evaluates selection accuracy with 3 approaches: deterministic, extractors, and LLM-based.**

Based on research: [CCTU: Benchmark for Tool Use under Complex Constraints](https://arxiv.org/abs/2603.15309) (Mar 2026)

## Files

| File | Purpose |
|------|---------|
| `01-tool-selection-accuracy.ipynb` | **Main demo** — 10 queries, 3 evaluation approaches, comparison table |
| `travel_tools.py` | 10 travel agent tools + ground truth mapping |
| `requirements.txt` | Python dependencies |

## Run the Demo

Open `01-tool-selection-accuracy.ipynb`. Runs live agent on 10 queries, then evaluates with ToolCalled (free), extractors (free), and TrajectoryEvaluator (LLM).

## Research Background

- [CCTU](https://arxiv.org/abs/2603.15309) (Mar 2026) — No model achieves >20% under strict constraints
- [CORE](https://arxiv.org/abs/2509.20998) (Sep 2025) — DFA-based path evaluation

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../../LICENSE) file for details.
