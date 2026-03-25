# Judge Bias Detection: Position Bias and Verbosity Bias in LLM Judges

**LLM judges have systematic biases that distort evaluation scores. This demo detects position bias (preferring first/last responses) and verbosity bias (preferring longer responses) by scoring identical content in different configurations.**

Based on research: [Am I More Pointwise or Pairwise? Revealing Position Bias in Rubric-Based LLM-as-a-Judge](https://arxiv.org/abs/2602.02219) (Feb 2026)

## The Problem

LLM judges exhibit three common biases:

1. **Position bias** — The judge prefers responses presented at a specific position (first or last). The same response scores differently depending on what came before it.
2. **Verbosity bias** — The judge prefers longer responses, even when the extra length adds no value. A 500-word response with filler scores higher than a 50-word response with the same facts.
3. **Self-enhancement bias** — The judge rates outputs from its own model family higher than equivalent outputs from other models.

Research from the [Position Bias paper](https://arxiv.org/abs/2602.02219) shows that rubric-based evaluation exhibits **latent position bias** where LLMs prefer score options appearing at specific positions in the rubric itself.

## The Solution

**Detection**: Score the same content in different configurations (order, length, context). If scores change, bias is present.

**Mitigation**: Add explicit anti-bias instructions to rubrics and use balanced permutation strategies.

```
❌ Standard rubric:
   "Rate helpfulness 0-1."

✅ Debiased rubric:
   "Rate helpfulness 0-1.
    IMPORTANT: Do NOT reward response length.
    A concise response with all required facts should score
    the same as a verbose response with the same facts."
```

## Files

| File | Purpose |
|------|---------|
| `02-judge-bias-detection.ipynb` | **Main demo** — Position bias test, verbosity bias test, rubric-level mitigation |
| `requirements.txt` | Python dependencies |

## Run the Demo

Open `02-judge-bias-detection.ipynb` in Jupyter or VS Code.

**What it does**:
1. Creates two equal-quality responses with different styles
2. Tests position bias by varying context around responses
3. Tests verbosity bias with same facts at different lengths (70 chars vs 500 chars)
4. Mitigates verbosity bias with explicit anti-bias rubric instructions
5. Measures bias magnitude as score difference

## Research Background

- [Position Bias in Rubric-Based LLM-as-a-Judge](https://arxiv.org/abs/2602.02219) (Feb 2026) — Balanced permutation aggregation strategy
- [Autorubric](https://arxiv.org/abs/2603.00077) (Mar 2026) — Option shuffling and length penalty calibration
- [On Randomness in Agentic Evals](https://arxiv.org/abs/2602.07150) (Feb 2026) — Multiple runs needed due to high variance

## Next Steps

- [Demo 03 - Multi-Judge Ensemble](../03-multi-judge-ensemble/) — Use multiple judge models to reduce bias impact

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../../LICENSE) file for details.
