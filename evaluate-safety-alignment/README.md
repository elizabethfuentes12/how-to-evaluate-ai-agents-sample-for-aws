# Evaluate AI Agent Safety and Alignment

[![Python](https://img.shields.io/badge/Python-3.10+-green.svg?style=flat-square&logo=python)](https://python.org) [![AWS](https://img.shields.io/badge/AWS-Bedrock-orange.svg?style=flat-square&logo=amazon-aws)](https://aws.amazon.com/bedrock/)

Safety evaluation checks whether an AI agent produces harmful, biased, or policy-violating outputs. Research shows that standard metrics miss 65-93% of safety issues ([AgentDrift](https://arxiv.org/abs/2603.12564)). You need trajectory-level analysis to catch them.

This section implements three safety evaluation techniques. Similar patterns apply in other agent frameworks such as LangGraph, PydanticAI, or AutoGen.

## Demos

| Demo | Focus | Paper | Time |
|------|-------|-------|------|
| [**01 - Safety Scoring**](./01-safety-scoring/) | Score agent outputs for harmfulness, PII leakage, and policy compliance | [StepShield](https://arxiv.org/abs/2601.22136) (Jan 2026) | 15 min |
| [**02 - Drift Detection**](./02-drift-detection/) | Detect when agent behavior degrades across conversation turns | [AgentDrift](https://arxiv.org/abs/2603.12564) (Mar 2026) | 20 min |
| [**03 - Guardrail Hooks**](./03-guardrail-hooks/) | Block unsafe outputs in real-time with Strands hooks | [StepShield](https://arxiv.org/abs/2601.22136) (Jan 2026) | 15 min |

## Key Concepts

**Harmfulness** measures whether agent outputs contain toxic, violent, or illegal content. Binary: harmful or not harmful.

**Drift detection** catches gradual degradation. An agent may be safe on turn 1 but produce unsafe recommendations by turn 5 after context accumulates.

**Guardrail hooks** block unsafe outputs before they reach the user. Unlike post-hoc evaluation, guardrails run inline during agent execution.

## Prerequisites

```bash
cd evaluate-safety-alignment
python3 -m venv .venv
source .venv/bin/activate
pip install strands-agents[openai] strands-agents-evals boto3 matplotlib nest-asyncio
```
