# Trajectory Scoring: Evaluating the Path, Not the Answer

**Two agents produce the same correct answer, but one uses 2 tool calls and the other uses 4 (with duplicates and irrelevant calls). Output-only evaluation scores them equally. This demo compares output-only vs. trajectory evaluation to show why the path matters.**

Based on research: [TRACE: Trajectory-Aware Comprehensive Evaluation](https://arxiv.org/abs/2602.21230) (Feb 2026)

## The Problem

Output-only evaluation (`OutputEvaluator`) is blind to agent behavior. It only sees the final text. If two agents produce the same answer, they get the same score, even if one wasted tokens on irrelevant and duplicate tool calls.

## The Solution: Three Approaches Compared

| Approach | Sees Path | Catches Waste | Auto Capture | Cost |
|----------|:-:|:-:|:-:|---|
| `OutputEvaluator` | ❌ | ❌ | N/A | 1 LLM call |
| `TrajectoryEvaluator` | ✅ | ✅ | ❌ (manual) | 1 LLM call |
| `TrajectoryPlugin` (hooks) | ✅ | ✅ | ✅ | 0 (deterministic) |

## Files

| File | Purpose |
|------|---------|
| `01-trajectory-scoring.ipynb` | **Main demo** — 3 tests comparing output-only vs. trajectory vs. hooks |
| `trajectory_plugin.py` | **Reusable hook** — `TrajectoryPlugin` captures every tool call with timing |
| `requirements.txt` | Python dependencies |

## Run the Demo

Open `01-trajectory-scoring.ipynb`. It runs 3 progressive tests showing why trajectory evaluation matters.

```bash
# Or run the standalone plugin demo
python trajectory_plugin.py
```

## Research Background

- [TRACE](https://arxiv.org/abs/2602.21230) (Feb 2026) — Hierarchical trajectory utility function
- [CORE](https://arxiv.org/abs/2509.20998) (Sep 2025) — DFA-based full-path evaluation

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../../LICENSE) file for details.
