# Rubric-Based Evaluation: Teaching LLM Judges to Score Consistently

**AI agents produce outputs that look correct but may be vague, incomplete, or hallucinated. This demo builds LLM-as-Judge evaluators with Strands Agents, comparing vague vs. specific rubrics to show how rubric quality directly determines evaluation reliability.**

Based on research: [Autorubric: A Unified Framework for Rubric-Based LLM Evaluation](https://arxiv.org/abs/2603.00077) (Mar 2026) and [Grading Scale Impact on LLM-as-a-Judge](https://arxiv.org/abs/2601.03444) (Jan 2026)

## The Problem

When you ask an LLM judge "Is this response good?", the judge has no framework for scoring. It defaults to superficial heuristics: longer responses score higher, confident-sounding text scores higher, and scores cluster around 0.7 regardless of actual quality.

Research from the [Autorubric paper](https://arxiv.org/abs/2603.00077) shows that:

1. **Vague rubrics produce random scores** — Without explicit criteria, two runs of the same evaluation produce different scores
2. **Judges reward verbosity** — A 500-word response with fabricated details scores higher than a concise, accurate response
3. **Score compression** — All responses cluster in the 0.6-0.8 range, making it impossible to distinguish good from bad

## The Solution

Define **explicit scoring rubrics** with concrete criteria at each score level. The judge maps responses to specific rubric levels instead of guessing.

```
❌ Vague:    "Is this a good response?"
✅ Specific: "Rate 0-1:
              0.8-1.0: Lists specific flights with airline, number, times, price
              0.5-0.7: Some useful info but missing key details
              0.2-0.4: Vague without actionable information
              0.0-0.1: Contains fabricated information"
```

**Results**: The specific rubric produces 3-5x more score spread between good and bad responses, making it possible to set meaningful quality thresholds.

### Why Strands Agents Makes This Production-Ready

Strands provides `OutputEvaluator` with built-in rubric support and the `Experiment` class for batch evaluation:

```python
evaluator = OutputEvaluator(rubric="your criteria...", model="bedrock-model-id")
experiment = Experiment(cases=test_cases, evaluators=[evaluator])
reports = experiment.run_evaluations(task_function)
reports[0].display()  # Rich table with scores and reasons
```

Mix LLM judges with deterministic checks (zero cost) in the same experiment:

```python
experiment = Experiment(
    cases=cases,
    evaluators=[
        OutputEvaluator(rubric="..."),    # LLM judge (costs tokens)
        Contains(value="$"),               # Deterministic (free, instant)
        ToolCalled(tool_name="search"),    # Deterministic (free, instant)
    ],
)
```

Learn more: [Strands Agents Evaluation](https://strandsagents.com/latest/user-guide/evaluate/)

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
| `01-rubric-based-evaluation.ipynb` | **Main demo** — Progressive notebook: vague vs. specific rubrics, live agent evaluation, multi-evaluator experiments |
| `rubric_evaluator.py` | **Standalone comparison** — Run vague vs. specific rubric comparison from command line |
| `requirements.txt` | Python dependencies |

## Run the Demo

### Notebook (recommended)

Open `01-rubric-based-evaluation.ipynb` in Jupyter, VS Code, or your preferred notebook environment.

**What it does**:
1. Creates 3 test responses: good, mediocre, and hallucinated
2. Evaluates all 3 with a vague rubric ("Is this good?")
3. Evaluates all 3 with a specific rubric (detailed scoring criteria)
4. Compares score spread between approaches
5. Connects a live Strands agent with tools to the evaluator
6. Demonstrates mixed LLM + deterministic evaluators

### Standalone Script

```bash
python rubric_evaluator.py
```

**Expected output**:

```
TEST 1: VAGUE RUBRIC - 'Is this a good response?'
  good            score: 0.70
  mediocre        score: 0.50
  hallucinated    score: 0.60    ← Scores too close together

TEST 2: SPECIFIC RUBRIC - Detailed scoring criteria
  good            score: 0.90
  mediocre        score: 0.30
  hallucinated    score: 0.10    ← Clear separation

COMPARISON: Score Spread (good - hallucinated)
  Vague rubric spread:    0.10
  Specific rubric spread: 0.80
  ✅ Specific rubric separates quality levels better (+0.70)
```

## How It Works

### Step 1: Define Test Cases with Known Quality Levels

```python
from strands_evals import Experiment, Case

cases = [
    Case(name="good",         input="Find flights NYC to London", expected_output="..."),
    Case(name="mediocre",     input="Find flights NYC to London", expected_output="..."),
    Case(name="hallucinated", input="Find flights NYC to London", expected_output="..."),
]
```

### Step 2: Create an LLM Judge with a Rubric

```python
from strands_evals.evaluators import OutputEvaluator

evaluator = OutputEvaluator(
    rubric=(
        "Rate the travel agent response on a 0 to 1 scale:\n"
        "- 0.8-1.0: Lists specific flights with airline, times, and price\n"
        "- 0.5-0.7: Some useful information but missing details\n"
        "- 0.2-0.4: Vague without actionable information\n"
        "- 0.0-0.1: Contains fabricated information"
    ),
    model="us.anthropic.claude-sonnet-4-20250514-v1:0",
)
```

The judge receives:
- The agent's **input** (the question)
- The agent's **output** (the response to score)
- Your **rubric** (the scoring criteria)
- The **expected_output** (optional reference)

It returns a **score** (0.0-1.0) and a **reason** explaining why.

### Step 3: Run Batch Evaluation

```python
experiment = Experiment(cases=cases, evaluators=[evaluator])
reports = experiment.run_evaluations(task_function)
reports[0].display()  # Rich table
```

### Step 4: Mix LLM + Deterministic Evaluators

```python
from strands_evals.evaluators import Contains, ToolCalled

experiment = Experiment(
    cases=cases,
    evaluators=[
        OutputEvaluator(rubric="..."),   # LLM judge: subjective quality
        Contains(value="$"),              # Deterministic: must mention price
        ToolCalled(tool_name="search"),   # Deterministic: must call search
    ],
)
```

Deterministic evaluators run instantly at zero cost. Use them for hard requirements (must contain a price, must call a specific tool) and LLM judges for subjective quality.

## Research Background

This demo implements findings from:
- [Autorubric](https://arxiv.org/abs/2603.00077) (Mar 2026) — Open-source rubric framework with multi-judge ensembles and bias mitigation
- [Grading Scale Impact](https://arxiv.org/abs/2601.03444) (Jan 2026) — The 0-5 scale produces the strongest human-LLM alignment across six benchmarks

## Next Steps

- [Demo 02 - Judge Bias Detection](../02-judge-bias-detection/) — Detect position bias and verbosity bias in LLM judges
- [Demo 03 - Multi-Judge Ensemble](../03-multi-judge-ensemble/) — Use multiple judge models to reduce evaluation variance

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](../../../CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](../../../LICENSE) file for details.
