# How to Evaluate AI Agents

[![License](https://img.shields.io/badge/License-MIT--0-blue.svg?style=for-the-badge)](LICENSE) [![Python](https://img.shields.io/badge/Python-3.10+-green.svg?style=for-the-badge&logo=python)](https://python.org) [![AWS](https://img.shields.io/badge/AWS-Bedrock-orange.svg?style=for-the-badge&logo=amazon-aws)](https://aws.amazon.com/bedrock/) [![Strands](https://img.shields.io/badge/Strands_Agents-blue.svg?style=for-the-badge)](https://strandsagents.com)

*Research-backed evaluation techniques for AI agents -- from LLM-as-judge to trajectory scoring, hallucination detection, and cost-performance analysis, implemented as working code demos.*

> **Note:** This guide assumes familiarity with AI agents, tool calling, and Python. Similar evaluation patterns can be applied in LangGraph, PydanticAI, AutoGen, or other agent frameworks.

---

## Projects

| Project | Description | Papers |
|---------|-------------|--------|
| [**evaluate-with-llm-judges**](./evaluate-with-llm-judges/) | Rubric-based evaluation, bias detection, statistical calibration | ![Autorubric](https://img.shields.io/badge/-Autorubric-purple) ![SCOPE](https://img.shields.io/badge/-SCOPE-purple) ![Grading_Scale](https://img.shields.io/badge/-Grading_Scale-purple) |
| [**evaluate-agent-trajectories**](./evaluate-agent-trajectories/) | Trajectory scoring, risk aggregation, variance analysis | ![TRACE](https://img.shields.io/badge/-TRACE-blue) ![TRACER](https://img.shields.io/badge/-TRACER-blue) ![On_Randomness](https://img.shields.io/badge/-On_Randomness-blue) |
| [**detect-hallucinations**](./detect-hallucinations/) | Zero-shot detection, claim verification, consistency scoring | ![LSC](https://img.shields.io/badge/-LSC-red) ![Spilled_Energy](https://img.shields.io/badge/-Spilled_Energy-red) ![VISTA](https://img.shields.io/badge/-VISTA-red) |
| [**measure-cost-performance**](./measure-cost-performance/) | Cost-quality tradeoffs, caching impact, Pareto analysis | ![KAMI](https://img.shields.io/badge/-KAMI-green) ![Prompt_Caching](https://img.shields.io/badge/-Prompt_Caching-green) ![Multi_Agent_Cost](https://img.shields.io/badge/-Multi_Agent_Cost-green) |
| [**evaluate-tool-use**](./evaluate-tool-use/) | Constraint validation, path correctness, multilingual robustness | ![CCTU](https://img.shields.io/badge/-CCTU-orange) ![CORE](https://img.shields.io/badge/-CORE-orange) ![Lost_in_Execution](https://img.shields.io/badge/-Lost_in_Execution-orange) |
| [**evaluate-safety-alignment**](./evaluate-safety-alignment/) | Trajectory safety, ethical alignment, drift detection | ![StepShield](https://img.shields.io/badge/-StepShield-critical) ![MoralityGym](https://img.shields.io/badge/-MoralityGym-critical) ![AgentDrift](https://img.shields.io/badge/-AgentDrift-critical) |
| [**blog-framework-comparison**](./blog-framework-comparison/) | Code-first comparison: Strands vs PydanticAI vs DeepEval for agent evaluation | ![Blog](https://img.shields.io/badge/-Blog-yellow) ![Notebook](https://img.shields.io/badge/-Notebook-yellow) |

---

## Why Strands Agents?

We evaluated 8 agent frameworks specifically for their ability to support **evaluation demos** -- not just building agents, but instrumenting, measuring, and scoring them. Here is the comparison:

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

### Why Strands wins for this repo (despite PydanticAI scoring 28)

| Factor | Strands Agents | PydanticAI |
|--------|---------------|------------|
| AWS Bedrock integration | Native, first-class | Supported but secondary |
| AgentCore deployment path | Direct compatibility | No path |
| Evaluation SDK | `strands-agents-evals` with TrajectoryEvaluator, OutputEvaluator, GoalSuccessRate, and more | `pydantic-evals` with Datasets, Cases, Evaluators |
| Multi-agent orchestration | Swarm + Graph + Handoffs | Basic delegation only |
| OpenTelemetry | Core dependency (always on) | Via Logfire (optional) |
| Hook system | 10+ typed lifecycle events (BeforeToolCall, AfterModelCall, etc.) | RunContext dependency injection |
| Built-in metrics | Token usage, latency, cycle counts, per-tool timing on every invocation | Via span instrumentation |

**Bottom line:** PydanticAI has a slightly more mature eval library, but Strands provides the tightest integration between agent execution, evaluation instrumentation, and AWS deployment. For a repository targeting AWS Bedrock users with an AgentCore deployment path, Strands is the right choice.

> For the full 8-framework comparison with code examples, see [FRAMEWORK_COMPARISON.md](FRAMEWORK_COMPARISON.md).

---

## Key Research Trends (Oct 2025 - Mar 2026)

This repository implements techniques from 45+ recent papers. The key trends driving the field:

1. **Beyond pass/fail** -- Multi-dimensional trajectory evaluation replaces binary success metrics (TRACE, TRACER, CORE)
2. **Statistical rigor for LLM judges** -- Conformal prediction and hypothesis testing make LLM-as-judge reliable (SCOPE, Noisy but Valid)
3. **Zero-shot hallucination detection** -- Training-free metrics detect hallucinations without labeled data (LSC, Spilled Energy)
4. **Process over outcome** -- How an agent solves a task matters as much as whether it solves it (WebArbiter, CORE)
5. **Cost as first-class metric** -- Composite cost-performance indices for model selection (KAMI, Don't Break the Cache)
6. **Safety requires trajectory analysis** -- Standard metrics miss 65-93% of safety issues (AgentDrift, StepShield)
7. **Variance demands multiple runs** -- 60,000-run study proves pass@k and multiple runs are essential (On Randomness)

> For the full paper catalog with links and relevance scores, see [RESEARCH.md](RESEARCH.md).

---

## Prerequisites

- Python 3.10+ installed locally
- `OPENAI_API_KEY` environment variable
- Basic understanding of AI agents and tool calling

**Model Configuration:**
All demos use OpenAI with GPT-4o-mini by default (requires `OPENAI_API_KEY` environment variable). You can swap to any provider supported by Strands, such as Amazon Bedrock, Anthropic, or Ollama. See [Strands Model Providers](https://strandsagents.com/latest/user-guide/concepts/model-providers/) for configuration.

---

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/elizabethfuentes12/how-to-evaluate-ai-agents-sample-for-aws.git
cd how-to-evaluate-ai-agents-sample-for-aws
```

### 2. Start with LLM-as-Judge
```bash
cd evaluate-with-llm-judges
```

### 3. Explore All Techniques
Each demo folder contains detailed README files and working Jupyter notebooks.

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| [**Strands Agents**](https://strandsagents.com) | AI agent framework with hooks, multi-agent orchestration, and built-in metrics |
| [**strands-agents-evals**](https://pypi.org/project/strands-agents-evals/) | Evaluation SDK: trajectory evaluators, LLM-as-judge, experiment framework |
| [**OpenTelemetry**](https://opentelemetry.io/) | Distributed tracing for agent trajectory capture |

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](http://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file for details.
