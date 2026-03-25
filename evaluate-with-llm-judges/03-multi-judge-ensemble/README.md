# Multi-Judge Ensemble: Reducing Evaluation Variance with Multiple Models

**A single LLM judge has biases. This demo uses multiple judge models (Claude Sonnet, Claude Haiku, Amazon Nova) and multiple runs to produce more reliable evaluation scores, measuring inter-judge agreement and score variance.**

Based on research: [Autorubric](https://arxiv.org/abs/2603.00077) (Mar 2026) and [SCOPE: Selective Conformal Optimized Pairwise LLM Judging](https://arxiv.org/abs/2602.13110) (Feb 2026)

## The Problem

A single LLM judge has two sources of unreliability:

1. **Model-specific bias** — Each model has different blind spots. Claude Sonnet may catch hallucinations that Nova misses, and vice versa.
2. **Run-to-run variance** — The same model, same rubric, same input produces different scores across runs due to temperature and sampling.

The [On Randomness paper](https://arxiv.org/abs/2602.07150) analyzed 60,000 agent evaluation runs and found that **a single run is statistically insufficient**. They recommend a minimum of 5 independent runs per task.

## The Solution

**Multi-model ensemble**: Run the same evaluation with 3 different judge models and aggregate scores (mean, median, stdev).

**Multi-run ensemble**: Run the same evaluation 5 times with the same model and measure variance.

```python
# Multi-model: different perspectives on the same response
judges = ["claude-sonnet", "claude-haiku", "amazon-nova"]
scores = [evaluate(response, model=j) for j in judges]
final_score = statistics.median(scores)  # Median ignores outliers
```

**Key finding from Autorubric**: 3-judge ensembles reduce evaluation variance by approximately 40%.

## Files

| File | Purpose |
|------|---------|
| `03-multi-judge-ensemble.ipynb` | **Main demo** — Multi-model ensemble, multi-run variance analysis, disagreement detection |
| `requirements.txt` | Python dependencies |

## Run the Demo

Open `03-multi-judge-ensemble.ipynb` in Jupyter or VS Code.

**What it does**:
1. Scores one response with a subtle hallucination using 3 different Bedrock models
2. Computes mean, median, and standard deviation across judges
3. Runs the same evaluation 5 times with one model to measure run-to-run variance
4. Flags high disagreement as a signal to investigate

**Expected output**:

```
Multi-model ensemble:
  claude-sonnet:  0.60
  claude-haiku:   0.50
  amazon-nova:    0.70

  Mean:   0.60
  Median: 0.60
  Stdev:  0.10

Multi-run (5 runs, same model):
  Run 1: 0.55
  Run 2: 0.60
  Run 3: 0.55
  Run 4: 0.65
  Run 5: 0.60

  Mean:   0.59
  Stdev:  0.039
```

## When to Use Ensembles

A 3-model, 5-run ensemble makes 15x more LLM calls than a single evaluation. Use ensembles for:
- **Deployment gates** — Before shipping a new agent version
- **Regression tests** — After modifying prompts or tools
- **Dispute resolution** — When a single judge score seems wrong

Use single judges for:
- **Development iteration** — Quick feedback during prompt tuning
- **Large-scale screening** — Evaluating thousands of outputs

## Research Background

- [Autorubric](https://arxiv.org/abs/2603.00077) (Mar 2026) — Multi-judge ensemble protocol, 3 judges reduce variance by ~40%
- [SCOPE](https://arxiv.org/abs/2602.13110) (Feb 2026) — Conformal prediction for judge calibration with statistical guarantees
- [On Randomness in Agentic Evals](https://arxiv.org/abs/2602.07150) (Feb 2026) — 60,000-run study proving multiple runs are essential

## Series Complete

You now know how to:
1. ✅ Write effective rubrics (Demo 01)
2. ✅ Detect judge biases (Demo 02)
3. ✅ Build reliable ensembles (Demo 03)

**Next section:** [Evaluate Agent Trajectories](../../evaluate-agent-trajectories/) — Score the step-by-step reasoning path, not the final answer.

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../../LICENSE) file for details.
