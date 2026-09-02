# Evaluate AI Agent Tool Use

[![Python](https://img.shields.io/badge/Python-3.10+-green.svg?style=flat-square&logo=python)](https://python.org) [![AWS](https://img.shields.io/badge/AWS-Bedrock-orange.svg?style=flat-square&logo=amazon-aws)](https://aws.amazon.com/bedrock/)

Tool use evaluation measures whether an AI agent selects the right tools and passes correct parameters. A wrong tool call can trigger real-world side effects: booking the wrong hotel, querying the wrong API, or sending data to the wrong service.

This section implements three evaluation techniques, from deterministic checks (zero cost) to LLM-based semantic validation. Similar patterns apply in other agent frameworks such as LangGraph, PydanticAI, or AutoGen.

## Demos

| Demo | Focus | Paper | Time |
|------|-------|-------|------|
| [**01 - Tool Selection Accuracy**](./01-tool-selection-accuracy/) | Compare 3 approaches: deterministic, extractors, and LLM-based tool selection scoring | [CCTU](https://arxiv.org/abs/2603.15309) (Mar 2026) | 20 min |
| [**02 - Constraint Validation**](./02-constraint-validation/) | Validate tool call parameters against business rules (dates, ranges, required fields) | [CCTU](https://arxiv.org/abs/2603.15309) (Mar 2026) | 20 min |
| [**03 - Parameter Correctness**](./03-parameter-correctness/) | Check if tool parameters match user intent (semantic parameter validation) | [Lost in Execution](https://arxiv.org/abs/2601.05366) (Jan 2026) | 15 min |

## Key Concepts

**Tool selection** = Did the agent pick the right tool? With 30 tools available, the agent may call `search_hotels` when it should call `get_hotel_pricing`.

**Constraint validation** = Did the tool parameters respect business rules? A date in the past, a negative price, or a missing required field are constraint violations.

**Parameter correctness** = Did the parameters match what the user asked? If the user asks about "NYC to London" but the agent passes `origin="New York City"`, is that correct? Semantic matching matters.

## Choosing Your Approach

| Need | Approach | Cost | Demo |
|------|----------|:----:|:----:|
| Was a specific tool called? | `ToolCalled` (deterministic) | Free | 01 |
| Were the right tools called in sequence? | `TrajectoryEvaluator` (LLM) | 1 call | 01 |
| Do parameters respect business rules? | Custom constraint checker | Free | 02 |
| Do parameters match user intent? | `OutputEvaluator` (LLM) | 1 call | 03 |

## Prerequisites

```bash
cd evaluate-tool-use
python3 -m venv .venv
source .venv/bin/activate
pip install strands-agents[openai] strands-agents-evals boto3 matplotlib nest-asyncio
```
