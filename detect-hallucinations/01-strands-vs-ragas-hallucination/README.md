# Strands vs RAGAS: Hallucination Detection Head-to-Head

**AI agents fabricate facts when the context is ambiguous. This demo runs the same 5 hallucination test cases through Strands evals and RAGAS, comparing detection accuracy, code complexity, and granularity against known ground truth.**

Based on research: [LSC: A Zero-Shot Metric for Hallucination Detection](https://arxiv.org/abs/2601.19918) (Jan 2026) and [VISTA: Turn-based Claim Verification](https://arxiv.org/abs/2510.27052) (Oct 2025)

## The Problem

Your agent retrieves context from a knowledge base and generates a response. But it may add fabricated details:

- ❌ **Invented entities**: "Virgin Atlantic VS10" when only BA117 and DL1 exist in context
- ❌ **Fabricated attributes**: "Award-winning service with complimentary champagne"
- ❌ **Embellishments**: "Great weather for sightseeing!" when the context only has temperature data

You need a way to detect these hallucinations automatically.

## The Solution: Two Approaches Compared

| Approach | Framework | How It Works |
|----------|-----------|-------------|
| **Rubric-based** | Strands evals | You write a hallucination-focused rubric. LLM judge scores 0-1 based on your criteria. |
| **Claim decomposition** | RAGAS | Automatic: decomposes response into atomic claims, checks each against context. |

```
Strands:  Question + Context + Response + Rubric → LLM Judge → Score (0-1)
RAGAS:    Response → Claim decomposition → Each claim checked → Faithfulness (0-1)
```

Both use OpenAI GPT-4o-mini as the evaluation model.

## Setup

### Prerequisites

- Python 3.10+
- `OPENAI_API_KEY` environment variable set

### Install

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Files

| File | Purpose |
|------|---------|
| `01-strands-vs-ragas-hallucination.ipynb` | **Main demo** — Head-to-head comparison with ground truth verification |
| `test_data.py` | 5 test cases with known labels (2 grounded, 2 hallucinated, 1 mixed) |
| `requirements.txt` | Python dependencies |

## Run the Demo

Open `01-strands-vs-ragas-hallucination.ipynb` in Jupyter or VS Code.

**What it does**:
1. Loads 5 test cases with known ground truth labels
2. Evaluates all 5 with Strands `OutputEvaluator` + hallucination rubric
3. Evaluates all 5 with RAGAS `Faithfulness` + `ResponseGroundedness`
4. Compares both against ground truth at threshold=0.5
5. Prints code complexity comparison table

**Expected output**:

```
GROUND TRUTH VERIFICATION

Case                           Truth           Strands         RAGAS
----------------------------------------------------------------------
  grounded_flights             ✅ grounded     ✅ 0.90         ✅ 1.00
  grounded_weather             ✅ grounded     ✅ 0.85         ✅ 1.00
  hallucinated_awards          ❌ halluc.      ✅ 0.15         ✅ 0.33
  hallucinated_airline         ❌ halluc.      ✅ 0.20         ✅ 0.50
  mixed_embellished            ❌ halluc.      ✅ 0.40         ✅ 0.67

📊 Detection Accuracy (threshold=0.5):
   Strands: 5/5 (100%)
   RAGAS:   4/5 (80%)
```

*Scores will vary across runs. The key insight is how each framework handles the edge cases.*

## How It Works

### Strands Approach: Custom Rubric

```python
from strands_evals import Experiment, Case
from strands_evals.evaluators import OutputEvaluator
from strands.models.openai import OpenAIModel

evaluator = OutputEvaluator(
    rubric="Score 1.0 if grounded in context. Score 0.0 if fabricated.",
    model=OpenAIModel(model_id="gpt-4o-mini"),
)

cases = [Case(input=question, expected_output=context)]
experiment = Experiment(cases=cases, evaluators=[evaluator])
reports = experiment.run_evaluations(lambda case: response)
```

**Strengths**: No extra dependencies, full control over criteria, swappable model provider (OpenAI, Bedrock, Anthropic, Ollama).
**Weakness**: Context goes in `expected_output` (workaround), no claim decomposition.

### RAGAS Approach: Purpose-Built Metrics

```python
from ragas import evaluate
from ragas.llms import llm_factory
from ragas.dataset_schema import SingleTurnSample, EvaluationDataset
from ragas.metrics.collections import Faithfulness

llm = llm_factory("bedrock/anthropic.claude-sonnet-4-20250514-v1:0",
                   provider="litellm", client=litellm.completion)

samples = [SingleTurnSample(
    user_input=question, response=response, retrieved_contexts=contexts
)]

result = evaluate(dataset=EvaluationDataset(samples=samples),
                  metrics=[Faithfulness(llm=llm)])
```

**Strengths**: Dedicated `retrieved_contexts` field, automatic claim decomposition, per-claim scores.
**Weakness**: Requires LiteLLM dependency for Bedrock, more setup.

## When to Use Each

| Need | Best Choice |
|------|-------------|
| Already using Strands Agents | **Strands evals** |
| Need per-claim granularity | **RAGAS** |
| Evaluating RAG pipelines | **RAGAS** |
| Full control over criteria | **Strands evals** |
| Need both agent + RAG eval | **Combine them** |

## Research Background

- [LSC: Zero-Shot Hallucination Detection](https://arxiv.org/abs/2601.19918) (Jan 2026) — Span confidence without training data
- [VISTA: Turn-based Claim Verification](https://arxiv.org/abs/2510.27052) (Oct 2025) — Atomic claim decomposition
- [Spilled Energy](https://arxiv.org/abs/2602.18671) (Feb 2026) — Training-free logit-based detection

## Next Steps

- [Demo 02 - Claim Decomposition](../02-claim-decomposition/) — Build claim-level verification with Strands Agents
- [Demo 03 - Real-Time Detection](../03-realtime-hallucination-hooks/) — Detect hallucinations during agent execution with hooks

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../../LICENSE) file for details.
