# Project Context

This repository demonstrates 19 research-backed evaluation techniques for AI agents using Strands Agents on AWS Bedrock.

## ✅ COMPLETED: Blog Series (Apr 30, 2026)

**Status:** All 4 blog posts complete and ready for publication

| Post | File | Words | Status |
|------|------|:-----:|:------:|
| **00: Framework Comparison** | `00-framework-comparison.md` | 5,800 | ✅ Complete |
| **02: Evaluation Fundamentals** | `02-evaluation-fundamentals.md` | 8,800 | ✅ Complete |
| **03: Detecting Failures** | `03-detecting-failures.md` | 8,900 | ✅ Complete |
| **04: Production Metrics** | `04-production-metrics.md` | 10,200 | ✅ Complete |

**All posts include:**
- SEO-optimized frontmatter (title, description ≤155 chars, tags: ai, python, tutorial, programming)
- Amazon Bedrock AgentCore sections (built-in evaluators, trace capture, CloudWatch)
- Code examples with Strands Agents + AWS Bedrock
- Results tables, FAQ sections, diagrams
- Research paper citations with tracking URLs

**Diagrams generated:**
1. `llm-judge-evaluation-pipeline.png` (Post 02)
2. `ai-agent-hallucination-detection-three-approaches-comparison.png` (Post 03)
3. `ai-agent-cost-quality-pareto-frontier-model-comparison.png` (Post 04)

---

## ⏳ PENDING: Asana Tasks

**After Asana MCP re-authentication, create these tasks:**

Use the `/asana-devex-tasks` skill to create:

1. **SAMPLE Task:**
   - Name: `Sample: AI Agent Evaluation - 19 Research-Backed Demos on AWS`
   - Due: 2026-05-04 (Sunday)
   - Project: DevEx Written Content (1213204546340548)
   - Assignee: Elizabeth (1203075317077994)

2. **BLOG Tasks (4 total):**
   - `Blog 00: Framework Comparison - Which Tool Best Evaluates AI Agents?` (Due: 2026-05-11)
   - `Blog 02: Evaluation Fundamentals - LLM-as-Judge and Trajectory Analysis` (Due: 2026-05-18)
   - `Blog 03: Detecting Failures - Hallucinations and Safety Drift` (Due: 2026-05-25)
   - `Blog 04: Production Metrics - Cost, Tool Correctness, Observability` (Due: 2026-06-01)

**Publication schedule:** Weekly on Sundays starting May 11, 2026

---

## TODO: AgentCore Evaluation Demo

**Required:** Create a comprehensive notebook demonstrating Amazon Bedrock AgentCore evaluation capabilities:

### Notebook Specifications
- **Location:** `/bedrock-agentcore-evaluation/`
- **File:** `agentcore-evaluation-demo.ipynb`
- **Purpose:** Show how to use Bedrock AgentCore built-in evaluators alongside Strands evaluators

### Content to Cover
1. **Setup:**
   - Create a Bedrock agent with action groups
   - Configure trace capture (`enableTrace=True`)
   - Install boto3 and bedrock-agent-runtime

2. **Built-in Evaluators:**
   - Use `Builtin.Helpfulness` evaluator
   - Use `Builtin.GoalSuccessRate` evaluator
   - Use `Builtin.ToolSelection` evaluator
   - Show CLI: `agentcore run eval --evaluator "Builtin.Helpfulness"`

3. **Trace Analysis:**
   - Capture OrchestrationTrace with rationale
   - Extract tool call sequence from traces
   - Analyze InvocationInput and Observation

4. **CloudWatch Integration:**
   - Query invocation logs
   - Create custom metrics dashboard
   - Monitor agent performance in production

5. **Comparison with Strands:**
   - Run same evaluation with Strands `OutputEvaluator`
   - Run same evaluation with AgentCore `Builtin.Helpfulness`
   - Compare results, cost, and ease of use

6. **Custom Evaluators:**
   - Create Lambda-based custom evaluator
   - Create LLM-based custom evaluator
   - Show when to use each approach

### Integration Points
- **Blog reference:** Link from blog posts 00, 02, and 04
- **Repo README:** Add to main demo table as "Bedrock AgentCore Evaluation"
- **FRAMEWORK_COMPARISON.md:** Add AgentCore as 4th framework comparison

### Tracking URLs
All AWS/Bedrock URLs must include: `?trk=87c4c426-cddf-4799-a299-273337552ad8&sc_channel=el`

### Success Criteria
- Notebook runs end-to-end without errors
- All 13 built-in evaluators documented
- Side-by-side comparison with Strands shown
- CloudWatch query examples work
- Estimated time: 30-40 minutes

---

## Repository Structure

```
evaluate-with-llm-judges/     # LLM-as-Judge techniques
evaluate-agent-trajectories/  # Trajectory scoring
detect-hallucinations/        # Zero-shot hallucination detection
measure-cost-performance/     # Cost-quality tradeoffs
evaluate-tool-use/           # Tool selection and correctness
evaluate-safety-alignment/   # Safety scoring and drift
blog-ai-agent-evaluation/    # Blog series (4 posts)
bedrock-agentcore-evaluation/ # TODO: AgentCore demo
```

---

## Code Patterns

### Always Use Tracking URLs

All AWS, Strands, and Kiro URLs must include tracking:
```
?trk=87c4c426-cddf-4799-a299-273337552ad8&sc_channel=el
```

Use `&trk=...` if URL already has `?`.

### Strands Versions

All demos use:
- `strands-agents>=1.32.0`
- `strands-agents-evals>=0.1.11`

### Model Configuration

AWS Bedrock models:
```python
from strands.models.bedrock import BedrockModel

model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0"
)
```

---

## Blog Series Guidelines

### SEO/AEO Requirements

1. **Meta description:** Max 155 chars
2. **Tags:** Use high-reach tags (ai, python, tutorial, programming)
3. **Headings:** Question-based (H2/H3)
4. **Answer blocks:** 40-60 words, standalone
5. **Images:** Descriptive alt text with keywords
6. **FAQ:** 3-5 natural language questions with direct answers
7. **Statistics:** Always cite sources (+37% visibility boost)

### Post Structure

1. Hook paragraph (problem statement)
2. "What You'll Learn" box
3. Research context with paper citations
4. Diagram (generated with increased font sizes)
5. Code examples (Python + Strands)
6. Bedrock AgentCore section
7. Results table (before/after metrics)
8. FAQ section
9. References (papers + docs with tracking URLs)

---

## Research Papers Cited

All papers from October 2025 - April 2026 are verified and documented in RESEARCH.md.

**Key papers:**
- Autorubric (2603.00077) - March 2026
- TRACE (2602.21230) - February 2026
- AgentDrift (2603.12564) - April 2026 ✅ Verified claim: "65-93%" exists
- WindowsWorld (2604.27776) - April 30, 2026
- D3-Gym (2604.27977) - April 30, 2026
- CARE (2604.28043) - April 30, 2026

---

## Conventions

- **Never add AI authorship credits** (per global CLAUDE.md)
- **Python environment:** Always use `uv` for package management
- **Dependencies:** Run `pip-audit` before pushing
- **Fonts in diagrams:** Increased by +5 points (fontsize 21 for titles, 17 for labels)
