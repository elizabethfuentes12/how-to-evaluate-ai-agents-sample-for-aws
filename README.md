# Evaluate AI Agents with Strands

[![License](https://img.shields.io/badge/License-MIT--0-blue.svg?style=for-the-badge)](LICENSE) [![Python](https://img.shields.io/badge/Python-3.10+-green.svg?style=for-the-badge&logo=python)](https://python.org) [![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange.svg?style=for-the-badge&logo=amazon-aws)](https://aws.amazon.com/bedrock/) [![Strands Agents](https://img.shields.io/badge/Strands_Agents-blue.svg?style=for-the-badge)](https://strandsagents.com)

AI agents return plausible answers while silently failing: wrong tool selection, hallucinated facts, safety drift. These 19 demos use [Strands Agents](https://strandsagents.com) — the only framework with always-on OpenTelemetry tracing, 10+ typed lifecycle hooks, and a dedicated evaluation SDK — to implement techniques from 45+ research papers (Oct 2025–Mar 2026) covering LLM-as-judge scoring, trajectory analysis, hallucination detection, cost benchmarks, and safety alignment on AWS Bedrock.

> **Note:** Code in this repository is provided "as is" and is not officially supported by Amazon. This sample works with [AWS Bedrock](https://aws.amazon.com/bedrock/). The evaluation concepts apply to agents built with LangGraph, PydanticAI, AutoGen, or other frameworks — but Strands makes the instrumentation significantly simpler.

*Last updated: April 2026*

---

## What Is AI Agent Evaluation?

AI agent evaluation measures whether an agent accomplishes tasks correctly — not just whether it returns an answer, but whether it used the right tools, followed a safe reasoning path, and stayed within cost and accuracy thresholds. Standard pass/fail metrics miss 65–93% of safety issues ([AgentDrift, 2025](RESEARCH.md)). Multi-dimensional evaluation catches silent failures that binary success metrics cannot detect.

---

## Why Is Strands Agents the Best Framework for Evaluation?

We evaluated 8 agent frameworks specifically for their ability to support **evaluation demos** — not just building agents, but instrumenting, measuring, and scoring them. Here is the comparison:

### Evaluation-Specific Scoring (1-5 per criterion, 30 max)

| Criterion | Strands | PydanticAI | OpenAI SDK | LangGraph | AutoGen | Google ADK | CrewAI | smolagents |
|-----------|:-------:|:----------:|:----------:|:---------:|:-------:|:----------:|:------:|:----------:|
| Trajectory Capture | 5 | 5 | 4 | 4 | 3 | 3 | 2 | 2 |
| LLM-as-Judge Patterns | 4 | 5 | 3 | 4 | 5 | 4 | 3 | 2 |
| Hook System for Measurement | 5 | 4 | 5 | 3 | 3 | 2 | 2 | 1 |
| Multi-Model Support | 5 | 5 | 3 | 4 | 3 | 3 | 4 | 4 |
| Eval Community/Ecosystem | 3 | 4 | 4 | 5 | 4 | 3 | 3 | 2 |
| Code Simplicity (for demos) | 5 | 5 | 4 | 2 | 3 | 3 | 4 | 4 |
| **Total** | **27** | **28** | **23** | **22** | **21** | **18** | **18** | **15** |

### Why Strands wins (despite PydanticAI scoring 28)

| Factor | Strands Agents | PydanticAI |
|--------|---------------|------------|
| AWS Bedrock integration | Native, first-class | Supported but secondary |
| AgentCore deployment path | Direct compatibility | No path |
| Evaluation SDK | `strands-agents-evals` with TrajectoryEvaluator, OutputEvaluator, GoalSuccessRate, and more | `pydantic-evals` with Datasets, Cases, Evaluators |
| Multi-agent orchestration | Swarm + Graph + Handoffs | Basic delegation only |
| **OpenTelemetry** | **Core dependency — always on, zero config** | Via Logfire (optional) |
| Hook system | 10+ typed lifecycle events (`BeforeToolCall`, `AfterModelCall`, etc.) | RunContext dependency injection |
| Built-in metrics | Token usage, latency, cycle counts, per-tool timing on every invocation | Via span instrumentation |

**OpenTelemetry is a first-class citizen in Strands** — every agent invocation emits distributed traces automatically with no setup required. This makes trajectory capture, latency measurement, and per-tool timing available out of the box, which is critical for the evaluation demos in this repository.

**Bottom line:** PydanticAI has a slightly more mature eval library, but Strands provides the tightest integration between agent execution, evaluation instrumentation, and AWS deployment. For a repository targeting AWS Bedrock users with an AgentCore deployment path, Strands is the right choice.

> For the full 8-framework comparison with code examples, see [FRAMEWORK_COMPARISON.md](FRAMEWORK_COMPARISON.md).

---

## Projects

| Project | Description | Techniques |
|---------|-------------|------------|
| [**evaluate-with-llm-judges**](./evaluate-with-llm-judges/) | Rubric-based scoring, bias detection, statistical calibration | ![Autorubric](https://img.shields.io/badge/-Autorubric-purple) ![SCOPE](https://img.shields.io/badge/-SCOPE-purple) ![Grading_Scale](https://img.shields.io/badge/-Grading_Scale-purple) |
| [**evaluate-agent-trajectories**](./evaluate-agent-trajectories/) | Trajectory scoring, risk aggregation, variance analysis | ![TRACE](https://img.shields.io/badge/-TRACE-blue) ![TRACER](https://img.shields.io/badge/-TRACER-blue) ![On_Randomness](https://img.shields.io/badge/-On_Randomness-blue) |
| [**detect-hallucinations**](./detect-hallucinations/) | Zero-shot detection, claim verification, consistency scoring | ![LSC](https://img.shields.io/badge/-LSC-red) ![Spilled_Energy](https://img.shields.io/badge/-Spilled_Energy-red) ![VISTA](https://img.shields.io/badge/-VISTA-red) |
| [**measure-cost-performance**](./measure-cost-performance/) | Cost-quality tradeoffs, caching impact, Pareto analysis | ![KAMI](https://img.shields.io/badge/-KAMI-green) ![Prompt_Caching](https://img.shields.io/badge/-Prompt_Caching-green) ![Multi_Agent_Cost](https://img.shields.io/badge/-Multi_Agent_Cost-green) |
| [**evaluate-tool-use**](./evaluate-tool-use/) | Constraint validation, path correctness, multilingual robustness | ![CCTU](https://img.shields.io/badge/-CCTU-orange) ![CORE](https://img.shields.io/badge/-CORE-orange) ![Lost_in_Execution](https://img.shields.io/badge/-Lost_in_Execution-orange) |
| [**evaluate-safety-alignment**](./evaluate-safety-alignment/) | Trajectory safety, ethical alignment, drift detection | ![StepShield](https://img.shields.io/badge/-StepShield-critical) ![MoralityGym](https://img.shields.io/badge/-MoralityGym-critical) ![AgentDrift](https://img.shields.io/badge/-AgentDrift-critical) |
| [**evaluate-resilience**](./evaluate-resilience/) | Chaos testing (corrupted-data guardrails, token savings) and red teaming (multi-turn attacks) | ![Chaos](https://img.shields.io/badge/-Chaos_Testing-orange) ![Red_Team](https://img.shields.io/badge/-Red_Teaming-red) ![Evals_1.0](https://img.shields.io/badge/-Strands_Evals_1.0-blue) |
| [**blog-framework-comparison**](./blog-framework-comparison/) | Code-first comparison: Strands vs PydanticAI vs DeepEval for evaluation | ![Blog](https://img.shields.io/badge/-Blog-yellow) ![Notebook](https://img.shields.io/badge/-Notebook-yellow) |

---

## How Do I Get Started?

### Prerequisites

- Python 3.10+ installed locally
- `OPENAI_API_KEY` environment variable (demos use GPT-4o-mini by default)
- Basic familiarity with AI agents and tool calling

> All demos can be switched to Amazon Bedrock, Anthropic, or Ollama. See [Strands Model Providers](https://strandsagents.com/latest/user-guide/concepts/model-providers/) for configuration.

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/elizabethfuentes12/how-to-evaluate-ai-agents-sample-for-aws.git
cd how-to-evaluate-ai-agents-sample-for-aws

# 2. Install dependencies for a demo
cd evaluate-with-llm-judges
uv pip install -r requirements.txt
```

Open the notebooks in JupyterLab or VS Code. Each demo folder contains its own `requirements.txt` and a detailed `README.md`.

---

## What Evaluation Techniques Are Covered?

Seven key trends from 45+ papers (Oct 2025–Mar 2026) drive this collection:

1. **Beyond pass/fail** — Multi-dimensional trajectory evaluation replaces binary success metrics ([TRACE](RESEARCH.md), [TRACER](RESEARCH.md), [CORE](RESEARCH.md))
2. **Statistical rigor for LLM judges** — Conformal prediction and hypothesis testing make LLM-as-judge reproducible ([SCOPE](RESEARCH.md), [Noisy but Valid](RESEARCH.md))
3. **Zero-shot hallucination detection** — Training-free metrics detect hallucinations without labeled data ([LSC](RESEARCH.md), [Spilled Energy](RESEARCH.md))
4. **Process over outcome** — How an agent solves a task matters as much as whether it solves it ([WebArbiter](RESEARCH.md), [CORE](RESEARCH.md))
5. **Cost as first-class metric** — Composite cost-performance indices guide model selection ([KAMI](RESEARCH.md), [Don't Break the Cache](RESEARCH.md))
6. **Safety requires trajectory analysis** — Standard metrics miss 65–93% of safety issues ([AgentDrift](RESEARCH.md), [StepShield](RESEARCH.md))
7. **Variance demands multiple runs** — A 60,000-run study proves pass@k and multiple runs are essential ([On Randomness](RESEARCH.md))

> For the full paper catalog with links and relevance scores, see [RESEARCH.md](RESEARCH.md).

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| [**Strands Agents**](https://strandsagents.com) | AI agent framework with hooks, multi-agent orchestration, and built-in metrics |
| [**strands-agents-evals**](https://pypi.org/project/strands-agents-evals/) | Evaluation SDK: trajectory evaluators, LLM-as-judge, experiment framework |
| [**OpenTelemetry**](https://opentelemetry.io/) | Distributed tracing for agent trajectory capture — core dependency, always on |

---

## Troubleshooting

| Symptom | Resolution |
|---------|-----------|
| `OPENAI_API_KEY not set` | Export the variable: `export OPENAI_API_KEY=your-key` |
| Notebook kernel crashes on install cell | Run `uv pip install -r requirements.txt` in terminal first, then restart kernel |
| AWS Bedrock access denied | Enable model access in the [Bedrock console](https://console.aws.amazon.com/bedrock/) under Model access |
| `ModuleNotFoundError: strands` | Run `uv pip install strands-agents strands-agents-evals` |
| Chart not rendering | Run `uv pip install matplotlib ipympl` and restart kernel |
| `deepeval` import errors | Each demo has its own dependencies — run `uv pip install -r requirements.txt` from that demo's folder |

---

## Frequently Asked Questions

**What is AI agent evaluation?**
AI agent evaluation measures whether an agent accomplishes tasks correctly — covering tool selection accuracy, reasoning path quality, factual accuracy, cost efficiency, and safety alignment. It goes beyond checking whether the final answer is correct to measuring how the agent got there.

**How do I evaluate an AI agent's tool use?**
The [`evaluate-tool-use`](./evaluate-tool-use/) demos implement constraint validation, parameter correctness checking, and execution path analysis using the CCTU (Comprehensive Code Tool Use) and CORE frameworks from recent research.

**How do I detect hallucinations in my AI agent?**
The [`detect-hallucinations`](./detect-hallucinations/) demos implement zero-shot hallucination detection using LSC (Linear Semantic Consistency) and Spilled Energy metrics — no labeled training data required.

**How can I measure the cost and performance of an AI agent?**
The [`measure-cost-performance`](./measure-cost-performance/) demos track per-call token costs, prompt caching impact, and Pareto-optimal model selection using the KAMI (Key Agent Metrics Index) composite index.

**How do I evaluate a LangGraph agent?**
The evaluation techniques in this repo — trajectory scoring, LLM-as-judge, hallucination detection — apply directly to LangGraph agents. LangGraph supports OpenTelemetry via LangSmith, so trajectory capture works similarly. The demos here are implemented in Strands, but the scoring logic is framework-independent.

**How do I evaluate a PydanticAI agent?**
PydanticAI has its own `pydantic-evals` library with Datasets and Evaluators. The research techniques in this repo (TRACE, SCOPE, KAMI) can be layered on top. See [`blog-framework-comparison`](./blog-framework-comparison/) for a direct code comparison between Strands and PydanticAI evaluation patterns.

**How do I evaluate an AutoGen or CrewAI agent?**
AutoGen and CrewAI score lower on trajectory capture and hook instrumentation (see the scoring table above), which makes fine-grained evaluation harder. The LLM-as-judge and hallucination detection patterns from this repo are still applicable — they only require the agent's final output and intermediate steps as input.

**Does this work with smolagents or Google ADK?**
Yes. The evaluation techniques are model- and framework-agnostic — they evaluate inputs and outputs, not the framework internals. smolagents and Google ADK agents can be wrapped to capture the step data these demos require.

---

## References

- Full paper catalog with links and relevance scores: [RESEARCH.md](RESEARCH.md)
- 8-framework comparison with code examples: [FRAMEWORK_COMPARISON.md](FRAMEWORK_COMPARISON.md)
- Strands Agents documentation: [strandsagents.com](https://strandsagents.com)
- Strands evaluation SDK: [strands-agents-evals on PyPI](https://pypi.org/project/strands-agents-evals/)
- AWS Bedrock documentation: [docs.aws.amazon.com/bedrock](https://docs.aws.amazon.com/bedrock/)

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](http://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file for details.
