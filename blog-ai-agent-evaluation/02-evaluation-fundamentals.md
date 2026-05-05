---
title: "AI Agent Evaluation: Stop Silent Failures with LLM-as-Judge and Trajectory Analysis"
published: false
description: "Evaluate AI agents with LLM-as-Judge and trajectory analysis. Catch silent failures binary metrics miss. Code examples and research-backed techniques."
tags: ai, python, tutorial, programming
series: AI Agent Evaluation
cover_image: https://raw.githubusercontent.com/elizabethfuentes12/how-to-evaluate-ai-agents-sample-for-aws/main/blog-ai-agent-evaluation/images/llm-judge-evaluation-pipeline.png
---

AI agents fail silently. They return plausible answers while making unnecessary API calls, hallucinating facts, or following unsafe reasoning paths. Traditional pass/fail metrics catch none of this.

This post covers two fundamental evaluation techniques that catch what binary metrics miss: **LLM-as-Judge** for output quality and **Trajectory Evaluation** for process quality. Both are essential for production-ready agents.

**What You'll Learn:**
- How to implement LLM-as-Judge evaluation with explicit rubrics (5 min setup)
- Why trajectory evaluation catches failures output-only metrics miss
- Code examples in Python using Strands Agents on AWS Bedrock
- How to use Amazon Bedrock AgentCore built-in evaluators for production
- Latest research from April 2026 (WindowsWorld, D3-Gym, CARE framework)

*Published: April 2026*

---

## Why Binary Metrics Fail

Consider these two agents answering "Find flights from NYC to London":

| | Agent A | Agent B |
|---|---|---|
| **Answer** | "BA117 at 7PM ($450), DL1 at 9:30PM ($520)" | "BA117 at 7PM ($450), DL1 at 9:30PM ($520)" |
| **Tool Calls** | `search_flights("NYC", "London")` | `search_flights("NYC", "London")`<br>`get_currency_exchange()`<br>`search_flights("NYC", "London")` (duplicate) |
| **Pass/Fail** | ✅ Pass | ✅ Pass |

Both produce the correct answer. Pass/fail scoring rates them equally. But Agent B wasted tokens on an irrelevant tool and a duplicate call. **Trajectory evaluation catches this. Output-only evaluation does not.**

![AI agent LLM-as-Judge evaluation pipeline diagram: agent output flows through judge LLM with rubric to produce 0-1 score with reasoning, compared to legacy binary pass/fail evaluation](images/llm-judge-evaluation-pipeline.png)

---

## How Does LLM-as-Judge Evaluation Work?

**LLM-as-Judge uses a large language model to score agent outputs against defined criteria, replacing manual review. It provides continuous scores (0.0-1.0) with explanations, unlike binary pass/fail. Research shows explicit rubrics with score thresholds (0.8-1.0 = excellent, 0.5-0.7 = adequate) produce consistent, reproducible evaluation at scale.**

**Paper:** [Autorubric](https://arxiv.org/abs/2603.00077) (March 2026)

### The Problem with Vague Prompts

Most LLM judges use vague prompts like "Is this a good response?" This produces unpredictable scores because the judge decides what "good" means. Research shows vague rubrics lead to **position bias** (preferring the first option) and **verbosity bias** (preferring longer responses).

### The Solution: Explicit Scoring Criteria

Define exact score thresholds in your rubric:

```python
from strands_evals import Experiment, Case
from strands_evals.evaluators import OutputEvaluator

# Define explicit scoring criteria
evaluator = OutputEvaluator(
    rubric=(
        "Rate the travel agent response on a 0 to 1 scale:\n"
        "- 0.8-1.0: Lists specific flights with airline, flight number, times, and price\n"
        "- 0.5-0.7: Provides some useful information but missing key details\n"
        "- 0.2-0.4: Vague response without actionable information\n"
        "- 0.0-0.1: Contains fabricated information or is completely unhelpful"
    ),
    model="gpt-4o-mini",  # Or use AWS Bedrock: us.anthropic.claude-sonnet-4-20250514-v1:0
)

# Create test cases
cases = [
    Case(name="good", input="Find flights NYC to London", 
         expected_output="Specific flights with details"),
    Case(name="vague", input="Find flights NYC to London",
         expected_output="Specific flights with details"),
]

# Run evaluation
def task(case):
    if case.name == "good":
        return "BA117 at 7PM ($450), DL1 at 9:30PM ($520)"
    return "There are several flights available. Prices vary."

experiment = Experiment(cases=cases, evaluators=[evaluator])
reports = experiment.run_evaluations(task)
reports[0].display()
```

**Output:**
```
good:  Score 0.95 - Lists specific flights with all required details
vague: Score 0.30 - Missing specific details about airlines and times
```

### Key Findings from Research

The [Grading Scale paper](https://arxiv.org/abs/2601.03444) (January 2026) tested scoring scales from binary (0/1) to 10-point and found:

- **0-5 scale yields strongest human-LLM alignment** (Pearson correlation 0.89)
- 10-point scales introduce noise without improving precision
- Binary scales miss 73% of quality gradations

**Recommendation:** Use a 0-5 scale (mapped to 0.0-1.0 in code) with explicit criteria at each level.

---

## What Is Trajectory Evaluation?

**Trajectory evaluation scores the step-by-step path an agent takes to reach a solution, not just the final answer. It detects duplicate tool calls, irrelevant actions, and unsafe intermediate steps that output-only evaluation misses. By capturing the sequence of tool invocations, it identifies wasteful or dangerous reasoning patterns before they reach production.**

**Paper:** [TRACE](https://arxiv.org/abs/2602.21230) (February 2026)

### The Problem: Output-Only Evaluation is Blind

Output-only evaluation sees the final answer. It cannot detect:
- Duplicate tool calls (wasted tokens)
- Irrelevant tool calls (wrong reasoning path)
- Unsafe intermediate steps (privacy violations, unauthorized actions)
- Illogical tool order (get_price before search_product)

### The Solution: Evaluate the Path, Not Just the Destination

Trajectory evaluation scores the **step-by-step path** the agent took:

```python
from strands_evals.evaluators import TrajectoryEvaluator

traj_eval = TrajectoryEvaluator(
    rubric=(
        "Rate the tool usage trajectory 0-1:\n"
        "- 0.8-1.0: Only relevant tools called, no duplicates, logical order\n"
        "- 0.5-0.7: Mostly correct but minor inefficiency\n"
        "- 0.2-0.4: Irrelevant tools called or excessive duplicates\n"
        "- 0.0-0.1: Completely wrong tool selection"
    ),
    model="gpt-4o-mini",
)

# Simulate Agent A (efficient) and Agent B (wasteful)
efficient_trajectory = [
    {"name": "search_flights", "args": {"origin": "NYC", "dest": "London"}},
    {"name": "get_weather", "args": {"city": "London"}},
]

wasteful_trajectory = [
    {"name": "search_flights", "args": {"origin": "NYC", "dest": "London"}},
    {"name": "get_currency_exchange", "args": {}},  # irrelevant
    {"name": "search_flights", "args": {"origin": "NYC", "dest": "London"}},  # duplicate
    {"name": "get_weather", "args": {"city": "London"}},
]

cases = [
    Case(name="efficient", input="Find flights and weather", 
         expected_trajectory=["search_flights", "get_weather"]),
    Case(name="wasteful", input="Find flights and weather",
         expected_trajectory=["search_flights", "get_weather"]),
]

def traj_task(case):
    trajectory = efficient_trajectory if case.name == "efficient" else wasteful_trajectory
    return {"output": "BA117 at 7PM, London is 18C", "trajectory": trajectory}

exp = Experiment(cases=cases, evaluators=[traj_eval])
reports = exp.run_evaluations(traj_task)
reports[0].display()
```

**Output:**
```
efficient: Score 0.95 - Clean trajectory, only relevant tools
wasteful:  Score 0.25 - Contains irrelevant tool and duplicate call
```

### Automatic Trajectory Capture with Hooks

In production, you don't manually construct trajectories. Use **Strands hooks** to capture them automatically:

```python
from strands import Agent
from strands.hooks import HookProvider, HookRegistry
from strands.hooks.events import AfterToolCallEvent

class TrajectoryPlugin(HookProvider):
    def __init__(self):
        self.trajectory = []
    
    def on_after_tool_call(self, event: AfterToolCallEvent):
        self.trajectory.append({
            "name": event.tool_use.name,
            "args": event.tool_use.parameters,
            "success": event.exception is None,
        })

tracker = TrajectoryPlugin()
agent = Agent(model="gpt-4o-mini", tools=[...], hooks=[tracker])

# Run the agent
result = agent("Find flights from NYC to London")

# The hook captured everything automatically
print(f"Trajectory: {tracker.trajectory}")
# Output: [{'name': 'search_flights', 'args': {...}, 'success': True}, ...]
```

**Why this matters:** Strands hooks run on **every tool call** with zero configuration. OpenTelemetry tracing is built-in, giving you distributed traces automatically.

---

## Recent Research: What's New in April 2026?

Three papers published this month advance evaluation methodology:

### 1. D3-Gym: Executable Scientific Tasks

**Paper:** [arXiv:2604.27977](https://arxiv.org/abs/2604.27977) (April 30, 2026)

Released 565 scientific tasks with executable environments. Key finding: **87.5% agreement between automated evaluation and human-annotated gold standards**.

**Implication:** LLM-as-Judge can match human evaluation quality when rubrics are well-defined and ground truth is verifiable.

### 2. WindowsWorld: GUI Agent Benchmark

**Paper:** [arXiv:2604.27776](https://arxiv.org/abs/2604.27776) (April 30, 2026)

Tested GUI agents on 181 multi-application professional tasks. Result: **<21% success rate on multi-app tasks**.

**Implication:** Even state-of-the-art agents fail frequently on complex, multi-step tasks. Evaluation must catch these failures before production.

### 3. CARE: Collaborative Agent Reasoning Engineering

**Paper:** [arXiv:2604.28043](https://arxiv.org/abs/2604.28043) (April 30, 2026)

Proposes stage-gated methodology with verification gates at each development stage. Involves subject-matter experts, developers, and helper agents.

**Implication:** Evaluation is not a final step—it should happen at every stage of agent development.

---

## Amazon Bedrock AgentCore: Production-Ready Evaluation

If you're deploying agents to production on AWS, **Amazon Bedrock AgentCore** provides built-in evaluation and observability capabilities designed specifically for agent workflows.

### Built-in Evaluators

AgentCore offers **13 built-in evaluators** that use LLMs as judges:

| Evaluator | What It Measures |
|-----------|-----------------|
| `Builtin.Helpfulness` | Response usefulness and clarity |
| `Builtin.GoalSuccessRate` | Whether the agent achieved the user's goal |
| `Builtin.Correctness` | Factual accuracy of responses |
| `Builtin.ToolSelection` | Quality of tool/action group choices |

**Usage example:**
```bash
# Run evaluation on a trace dataset
agentcore run eval \
  --evaluator "Builtin.Helpfulness" \
  --evaluator "Builtin.GoalSuccessRate" \
  --session-id <session-id>
```

### Automatic Trace Capture

Every AgentCore agent invocation automatically generates a **trace** containing:
- Pre-processing validation
- Orchestration reasoning (rationale for each tool call)
- Tool invocation inputs and outputs
- Post-processing formatting
- Failure details (if any)
- Guardrail interventions

**Enable tracing in API calls:**
```python
import boto3

bedrock_agent_runtime = boto3.client('bedrock-agent-runtime')

response = bedrock_agent_runtime.invoke_agent(
    agentId='your-agent-id',
    agentAliasId='TSTALIASID',  # Use TSTALIASID for testing
    sessionId='session-123',
    inputText='Find flights from NYC to London',
    enableTrace=True  # ← Enables detailed trace capture
)

# Access traces from the response stream
for event in response['completion']:
    if 'trace' in event:
        trace = event['trace']['trace']
        print(f"Reasoning: {trace.get('rationale', {}).get('text', '')}")
```

### CloudWatch Integration

AgentCore agents automatically send logs and metrics to CloudWatch:
- **Invocation logs:** Input, output, latency, token usage
- **Error tracking:** Failures with stack traces
- **Custom metrics:** Success rates, latency percentiles, cost per invocation

**Query traces with CloudWatch Logs Insights:**
```sql
fields @timestamp, sessionId, traceId, invocationType, actionGroupName
| filter invocationType = "ACTION_GROUP"
| stats count() by actionGroupName
```

### When to Use AgentCore vs Strands Evaluation

| Scenario | Use AgentCore | Use Strands Evals |
|----------|:-------------:|:-----------------:|
| Production agents on AWS Bedrock | ✅ | ✅ (compatible) |
| CI/CD evaluation before deploy | ✅ | ✅ |
| Multi-model comparison (GPT, Claude, Gemini) | ❌ | ✅ |
| Custom evaluation logic (external APIs, regex) | ✅ (Lambda) | ✅ (Python) |
| Zero-config tracing | ✅ | ⚠️ (requires hooks) |

**Recommendation:** Use AgentCore built-in evaluators for production monitoring and Strands Evals for pre-deployment testing and multi-framework comparisons.

**Learn more:**
- [Amazon Bedrock Agents User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html?trk=87c4c426-cddf-4799-a299-273337552ad8&sc_channel=el)
- [Agent Observability and Traces](https://docs.aws.amazon.com/bedrock/latest/userguide/trace-events.html?trk=87c4c426-cddf-4799-a299-273337552ad8&sc_channel=el)
- [Testing Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-test.html?trk=87c4c426-cddf-4799-a299-273337552ad8&sc_channel=el)

---

## Combining LLM-as-Judge and Trajectory Evaluation

Production-ready evaluation uses **both** techniques:

| Scenario | Use LLM-as-Judge | Use Trajectory Eval |
|----------|:-:|:-:|
| Agent returns wrong answer | ✅ Catches it | ✅ May catch illogical path |
| Agent returns right answer via wrong path | ❌ Misses it | ✅ Catches it |
| Agent makes unsafe intermediate step | ❌ Misses it | ✅ Catches it |
| Agent output is unprofessional/rude | ✅ Catches it | ❌ Misses it |

**Recommendation:** Run both evaluators in parallel. Use LLM-as-Judge for output quality, trajectory evaluation for process quality.

```python
from strands_evals import Experiment

experiment = Experiment(
    cases=cases,
    evaluators=[
        output_evaluator,     # Scores output quality
        trajectory_evaluator,  # Scores process quality
    ],
)

reports = experiment.run_evaluations(task)

# Access both scores
output_score = reports[0].overall_score
trajectory_score = reports[1].overall_score

# Combine scores (weighted average)
final_score = 0.6 * output_score + 0.4 * trajectory_score
```

---

## Try It Yourself

**Prerequisites:**
- Python 3.10+
- `OPENAI_API_KEY` or AWS Bedrock access

**Install:**
```bash
pip install strands-agents strands-agents-evals boto3
```

**Run the demos:**
```bash
git clone https://github.com/elizabethfuentes12/how-to-evaluate-ai-agents-sample-for-aws.git
cd how-to-evaluate-ai-agents-sample-for-aws

# LLM-as-Judge demo
cd evaluate-with-llm-judges/01-rubric-based-evaluation
jupyter notebook 01-rubric-based-evaluation.ipynb

# Trajectory evaluation demo
cd ../../evaluate-agent-trajectories/01-trajectory-scoring
jupyter notebook 01-trajectory-scoring.ipynb
```

**AWS Bedrock users:** Replace `gpt-4o-mini` with:
```python
from strands.models.bedrock import BedrockModel

model = BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0")
```

---

## Frequently Asked Questions

**Q: How do I choose between LLM-as-Judge and deterministic checks (like "contains '$'")?**

Use deterministic checks for **hard requirements** that can be verified with string matching or regex. Use LLM-as-Judge for **subjective quality** that requires understanding context.

Example: "Must mention a price" → deterministic check. "Is the response helpful?" → LLM-as-Judge.

**Q: What if my agent uses 50+ tools? Does trajectory evaluation scale?**

Yes. Trajectory evaluation looks at the **sequence** of tool calls, not individual tool details. A 50-tool call trajectory is still a single API call to the judge LLM.

Cost per evaluation: ~$0.001-0.003 (GPT-4o-mini) or $0.015-0.045 (Claude Sonnet).

**Q: Can I use trajectory evaluation with LangGraph or AutoGen?**

Yes. Trajectory evaluation only requires the list of tool calls as input. Capture them with LangGraph's `.get_graph().get_state()` or AutoGen's message history, then pass to `TrajectoryEvaluator`.

**Q: How often should I run evaluations?**

- **CI/CD:** Run on every commit with a small test suite (10-20 cases)
- **Staging:** Run full suite (100-500 cases) before production deploy
- **Production:** Sample 1-5% of live traffic and evaluate async

**Q: What's the difference between Strands, PydanticAI, and DeepEval for evaluation?**

See [Blog Post 04: Framework Comparison](./04-framework-comparison.md) for a detailed side-by-side comparison with code examples.

---

## Key Takeaways

1. **Binary metrics miss 73% of quality gradations.** Use continuous scoring (0.0-1.0) with explicit rubrics.

2. **Trajectory evaluation catches issues output-only evaluation misses:** duplicate calls, irrelevant tools, unsafe steps.

3. **The 0-5 scale yields the strongest human-LLM alignment** (0.89 Pearson correlation). Map to 0.0-1.0 in code.

4. **Strands hooks capture trajectories automatically** via `AfterToolCallEvent`. No manual instrumentation needed.

5. **Combine both techniques.** LLM-as-Judge for output quality, trajectory evaluation for process quality.

---

## What's Next?

- **[Part 2: Detecting Agent Failures](./02-detecting-failures.md)** — Hallucination detection and safety alignment
- **[Part 3: Production Metrics](./03-production-metrics.md)** — Cost optimization and tool correctness
- **[Part 4: Framework Comparison](./04-framework-comparison.md)** — Strands vs PydanticAI vs DeepEval

---

## References

- [Autorubric: Unifying Rubric-based LLM Evaluation](https://arxiv.org/abs/2603.00077) (Rao & Callison-Burch, March 2026)
- [TRACE: Trajectory-Aware Comprehensive Evaluation](https://arxiv.org/abs/2602.21230) (February 2026)
- [Grading Scale paper](https://arxiv.org/abs/2601.03444) (January 2026)
- [D3-Gym: Real-World Verifiable Environments](https://arxiv.org/abs/2604.27977) (April 30, 2026)
- [WindowsWorld: GUI Agent Benchmark](https://arxiv.org/abs/2604.27776) (April 30, 2026)
- [CARE: Collaborative Agent Reasoning](https://arxiv.org/abs/2604.28043) (April 30, 2026)
- [Strands Agents Documentation](https://strandsagents.com)
- [Strands Evaluation SDK](https://pypi.org/project/strands-agents-evals/)

---

## Contributing

Found an issue or want to improve this guide? See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## Security

If you discover a security issue, report it via the [AWS vulnerability reporting page](http://aws.amazon.com/security/vulnerability-reporting/). Do not create a public GitHub issue.

---

## License

This content is licensed under the MIT-0 License. See the [LICENSE](../LICENSE) file.
