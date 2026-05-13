# Measure AI Agent Cost and Performance

[![Python](https://img.shields.io/badge/Python-3.10+-green.svg?style=flat-square&logo=python)](https://python.org) [![AWS](https://img.shields.io/badge/AWS-Bedrock-orange.svg?style=flat-square&logo=amazon-aws)](https://aws.amazon.com/bedrock/)

Cost-performance evaluation measures whether your agent delivers quality results at an acceptable cost. An agent that scores 0.95 on quality but costs $2 per query may be worse than one scoring 0.85 at $0.10.

This section implements three cost-aware evaluation techniques. Similar patterns apply in other agent frameworks such as LangGraph, PydanticAI, or AutoGen.

## Demos

| Demo | Focus | Paper | Time |
|------|-------|-------|------|
| [**01 - Token and Cost Tracking**](./01-token-cost-tracking/) | Capture token usage and compute costs per query using Strands built-in metrics | [Don't Break the Cache](https://arxiv.org/abs/2601.06007) (Jan 2026) | 15 min |
| [**02 - Model Comparison**](./02-model-comparison/) | Compare quality vs. cost across Claude Sonnet, Haiku, and Nova on the same tasks | [KAMI](https://arxiv.org/abs/2511.08042) (Nov 2025) | 20 min |
| [**03 - Cost-Quality Pareto**](./03-cost-quality-pareto/) | Find the optimal model for your quality threshold and budget | [Multi-Agent Cost](https://arxiv.org/abs/2601.07978) (Jan 2026) | 15 min |

## Key Concepts

**Token tracking** captures input tokens, output tokens, and cache read tokens from every agent invocation using Strands built-in `result.metrics`.

**Model comparison** runs the same evaluation tasks across multiple models and plots quality vs. cost.

**Pareto frontier** identifies models where no other model is both cheaper and higher quality. Models on the frontier are the optimal choices.

![Cost-quality Pareto frontier comparing Claude Sonnet, Haiku, and Nova models across quality score and cost per query](../blog-ai-agent-evaluation/images/ai-agent-cost-quality-pareto-frontier-model-comparison.png)

## Prerequisites

```bash
cd measure-cost-performance
python3 -m venv .venv
source .venv/bin/activate
pip install strands-agents strands-agents-evals boto3
```
