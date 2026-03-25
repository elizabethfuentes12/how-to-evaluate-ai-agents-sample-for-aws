# Research: AI Agent Evaluation Methodologies and Metrics

**Research Period:** October 2025 - March 2026
**Focus:** Academic papers proposing new metrics, frameworks, and benchmarks for evaluating AI agents
**Purpose:** Foundation for research-backed code demos using Strands Agents

---

## Table of Contents

- [Key Trends](#key-trends)
- [Recommended Demo Structure](#recommended-demo-structure)
- [1. LLM-as-Judge](#1-llm-as-judge)
- [2. Agent Trajectory Evaluation](#2-agent-trajectory-evaluation)
- [3. Automated Evaluation Metrics](#3-automated-evaluation-metrics)
- [4. Hallucination Detection Metrics](#4-hallucination-detection-metrics)
- [5. Multi-Agent Evaluation](#5-multi-agent-evaluation)
- [6. Cost-Performance Tradeoffs](#6-cost-performance-tradeoffs)
- [7. Human vs Automated Evaluation](#7-human-vs-automated-evaluation)
- [8. Task Completion Benchmarks](#8-task-completion-benchmarks)
- [9. Tool Use Evaluation](#9-tool-use-evaluation)
- [10. Safety and Alignment Evaluation](#10-safety-and-alignment-evaluation)
- [Evaluation Frameworks Landscape](#evaluation-frameworks-landscape)
- [AWS-Specific Tools](#aws-specific-tools)
- [Top Papers for Code Demos](#top-papers-for-code-demos)

---

## Key Trends

1. **Beyond pass/fail:** The field is moving from binary success metrics toward multi-dimensional trajectory-aware evaluation (TRACE, TRACER, CORE).

2. **Statistical rigor for judges:** Multiple papers (SCOPE, Noisy but Valid, Efficient Inference) bring formal statistical frameworks -- conformal prediction, semiparametric efficiency -- to LLM-as-Judge.

3. **Zero-shot hallucination detection:** New training-free metrics (LSC, Spilled Energy, Contrastive Mahalanobis) enable hallucination detection without labeled data.

4. **Process over outcome:** Process reward models (WebArbiter), trajectory utility functions (TRACE), and full-path evaluation (CORE) emphasize that *how* an agent solves a task matters as much as *whether* it solves it.

5. **Cost-awareness as first-class metric:** KAMI, Don't Break the Cache, and Cost/Accuracy in Multi-Agent Systems formalize cost-performance tradeoffs.

6. **Safety as trajectory analysis:** StepShield, AgentDrift, and STING show safety evaluation requires monitoring entire trajectories -- standard metrics miss 65-93% of safety issues.

7. **Variance and reproducibility:** "On Randomness in Agentic Evals" provides the statistical foundation: multiple runs and pass@k reporting are essential due to high variance.

---

## Recommended Demo Structure

Based on the research, the repository should be organized into these evaluation categories, each mapping to a folder of progressive code demos:

| Category | Demos | Core Papers |
|----------|-------|-------------|
| **evaluate-with-llm-judges** | Rubric-based evaluation, bias detection, statistical calibration | Autorubric, SCOPE, Grading Scale |
| **evaluate-agent-trajectories** | Trajectory scoring, risk aggregation, variance analysis | TRACE, TRACER, On Randomness |
| **detect-hallucinations** | Zero-shot detection, claim verification, consistency scoring | LSC, Spilled Energy, VISTA |
| **measure-cost-performance** | Cost-quality tradeoffs, caching impact, Pareto analysis | KAMI, Don't Break the Cache, Multi-Agent Cost |
| **evaluate-tool-use** | Constraint validation, path correctness, multilingual robustness | CCTU, CORE, Lost in Execution |
| **evaluate-safety-alignment** | Trajectory safety, ethical alignment, drift detection | StepShield, MoralityGym, AgentDrift |

---

## 1. LLM-as-Judge

### 1.1 Autorubric: A Unified Framework for Rubric-Based LLM Evaluation

- **Authors:** Delip Rao, Chris Callison-Burch
- **Date:** March 2026
- **Venue:** arXiv (2603.00077)
- **Key contribution:** Comprehensive open-source framework supporting binary, ordinal, and nominal evaluation criteria with multi-judge ensembles. Addresses position bias via option shuffling and verbosity bias through length penalties.
- **Proposed metrics/methods:** CHARM-100 benchmark, multi-judge ensemble protocol, option shuffling for position bias mitigation, length penalty calibration
- **Link:** https://arxiv.org/abs/2603.00077
- **Relevance score:** 5/5 -- Open-source, directly implementable rubric framework.

### 1.2 SCOPE: Selective Conformal Optimized Pairwise LLM Judging

- **Authors:** Sher Badshah, Ali Emami, Hassan Sajjad
- **Date:** February 2026
- **Venue:** arXiv (2602.13110)
- **Key contribution:** Selective judging framework with finite-sample statistical guarantees using conformal prediction. Introduces Bidirectional Preference Entropy to mitigate miscalibration and systematic bias.
- **Proposed metrics/methods:** Bidirectional Preference Entropy (BPE), conformal prediction-based selective judging, position invariance enforcement
- **Link:** https://arxiv.org/abs/2602.13110
- **Relevance score:** 5/5 -- Novel statistical method with clear implementation path.

### 1.3 Am I More Pointwise or Pairwise? Revealing Position Bias in Rubric-Based LLM-as-a-Judge

- **Authors:** Yuzheng Xu, Tosho Hirasawa, Tadashi Kozuno, et al.
- **Date:** February 2026
- **Venue:** arXiv (2602.02219)
- **Key contribution:** Demonstrates rubric-based evaluation exhibits latent position bias where LLMs prefer score options at specific positions. Proposes balanced permutation strategy.
- **Proposed metrics/methods:** Balanced permutation aggregation strategy, position bias detection protocol
- **Link:** https://arxiv.org/abs/2602.02219
- **Relevance score:** 4/5

### 1.4 Noisy but Valid: Robust Statistical Evaluation of LLMs with Imperfect Judges

- **Authors:** Chen Feng, Minghe Shen, Ananth Balashankar, et al.
- **Date:** January 2026
- **Venue:** arXiv (2601.20913)
- **Key contribution:** Hypothesis testing framework deriving variance-corrected critical thresholds from small calibration sets. Theoretical guarantees for finite-sample Type-I error control.
- **Proposed metrics/methods:** Variance-corrected hypothesis testing, True Positive/False Positive Rate modeling
- **Link:** https://arxiv.org/abs/2601.20913
- **Relevance score:** 4/5

### 1.5 Efficient Inference for Noisy LLM-as-a-Judge Evaluation

- **Authors:** Yiqun T Chen, Sizhu Lu, Sijia Li, et al.
- **Date:** January 2026
- **Venue:** arXiv (2601.05420)
- **Key contribution:** Unifies measurement-error correction and prediction-powered inference through semiparametric efficiency theory.
- **Proposed metrics/methods:** Efficient influence function estimators, semiparametric efficiency bounds
- **Link:** https://arxiv.org/abs/2601.05420
- **Relevance score:** 4/5

### 1.6 How to Correctly Report LLM-as-a-Judge Evaluations

- **Authors:** Chungpa Lee, Thomas Zeng, Jongwon Jeong, et al.
- **Date:** February 2026
- **Venue:** arXiv (2511.21140)
- **Key contribution:** Plug-in framework correcting bias and enabling principled uncertainty quantification. Confidence intervals accounting for test and calibration dataset uncertainty.
- **Proposed metrics/methods:** Bias-corrected confidence intervals, adaptive sample allocation, distribution-shift-robust estimation
- **Link:** https://arxiv.org/abs/2511.21140
- **Relevance score:** 5/5 -- Directly addresses reporting best practices.

### 1.7 Grading Scale Impact on LLM-as-a-Judge

- **Authors:** Weiyue Li, Minda Zhao, Weixuan Dong, et al.
- **Date:** January 2026
- **Venue:** arXiv (2601.03444)
- **Key contribution:** Finds that the 0-5 grading scale yields the strongest human-LLM alignment across six benchmarks.
- **Proposed metrics/methods:** Scale-dependent alignment measurement, demographic subgroup analysis
- **Link:** https://arxiv.org/abs/2601.03444
- **Relevance score:** 4/5 -- Simple, practical finding that improves any judge implementation.

### 1.8 Exploring the Effects of Alignment on Numerical Bias in LLMs

- **Authors:** Ayako Sato, Hwichan Kim, Zhousi Chen, et al.
- **Date:** January 2026
- **Venue:** arXiv (2601.16444)
- **Key contribution:** Instruction and preference tuning increase numerical bias in judge outputs. Evaluates mitigation strategies including temperature scaling and distribution calibration.
- **Proposed metrics/methods:** Temperature scaling, distribution calibration, score range adjustment
- **Link:** https://arxiv.org/abs/2601.16444
- **Relevance score:** 3/5

---

## 2. Agent Trajectory Evaluation

### 2.1 TRACE: Trajectory-Aware Comprehensive Evaluation for Deep Research Agents

- **Authors:** Yanyu Chen, Jiyue Jiang, Jiahong Liu, et al.
- **Date:** February 2026
- **Venue:** arXiv (2602.21230)
- **Key contribution:** Addresses the "high-score illusion" in agent benchmarks by proposing a hierarchical trajectory utility function measuring process efficiency, cognitive quality, and evidence grounding alongside accuracy.
- **Proposed metrics/methods:** Hierarchical trajectory utility function, scaffolded capability assessment, process efficiency metrics, cognitive quality score, evidence grounding score
- **Link:** https://arxiv.org/abs/2602.21230
- **Relevance score:** 5/5 -- Directly implementable multi-dimensional trajectory scorer.

### 2.2 TRACER: Trajectory Risk Aggregation for Critical Episodes

- **Authors:** Sina Tayebati, Divake Kumar, Nastaran Darabi, et al.
- **Date:** February 2026
- **Venue:** arXiv (2602.11409)
- **Key contribution:** Trajectory-level uncertainty metric combining surprisal, semantic repetition, and tool coherence gaps using tail-focused risk aggregation.
- **Proposed metrics/methods:** TRACER metric, surprisal scoring, semantic repetition detection, tool coherence gap measurement, tail-focused risk aggregation
- **Link:** https://arxiv.org/abs/2602.11409
- **Relevance score:** 5/5 -- Highly practical risk-scoring framework.

### 2.3 On Randomness in Agentic Evals

- **Authors:** Bjarni Haukur Bjarnason, Andre Silva, Martin Monperrus
- **Date:** February 2026
- **Venue:** arXiv (2602.07150)
- **Key contribution:** Analyzes variance from 60,000 runs, recommending multiple independent runs per task and pass@k metrics for reliable agent benchmarking.
- **Proposed metrics/methods:** pass@k for agents, variance analysis protocol, minimum-run-count recommendations
- **Link:** https://arxiv.org/abs/2602.07150
- **Relevance score:** 5/5 -- Essential statistical methodology for any evaluation pipeline.

### 2.4 AI Planning Framework for LLM-Based Web Agents

- **Authors:** Orit Shahnovsky, Rotem Dror
- **Date:** March 2026
- **Venue:** arXiv (2603.12710)
- **Key contribution:** Maps agent architectures to planning paradigms and proposes five novel trajectory evaluation metrics validated on 794 human-labeled trajectories.
- **Proposed metrics/methods:** Five trajectory quality metrics, planning paradigm mapping
- **Link:** https://arxiv.org/abs/2603.12710
- **Relevance score:** 4/5

### 2.5 StepShield: When, Not Whether to Intervene on Rogue Agents

- **Authors:** Gloria Felicia, Michael Eniolade, Jinfeng He, et al.
- **Date:** January 2026
- **Venue:** arXiv (2601.22136)
- **Key contribution:** Temporal trajectory safety metrics for detecting violations across 9,213 code agent trajectories.
- **Proposed metrics/methods:** Early Intervention Rate (EIR), Intervention Gap, Tokens Saved metric
- **Link:** https://arxiv.org/abs/2601.22136
- **Relevance score:** 5/5 -- Practical safety monitoring metrics.

### 2.6 ContextBench: Context Retrieval in Coding Agents

- **Authors:** Han Li, Letian Zhu, Bohan Zhang, et al.
- **Date:** February 2026
- **Venue:** arXiv (2602.05892)
- **Key contribution:** Process-oriented evaluation measuring context recall, precision, and efficiency throughout agent trajectories in 1,136 tasks.
- **Proposed metrics/methods:** Context recall, context precision, retrieval efficiency across trajectory steps
- **Link:** https://arxiv.org/abs/2602.05892
- **Relevance score:** 4/5

### 2.7 Replayable Financial Agents: Determinism-Faithfulness Assurance

- **Authors:** Raffi Khatchadourian
- **Date:** January 2026
- **Venue:** arXiv (2601.15322)
- **Key contribution:** DFAH framework measuring trajectory determinism, decision determinism, and evidence-conditioned faithfulness across 4,700+ runs.
- **Proposed metrics/methods:** DFAH framework, trajectory determinism score, decision determinism score, evidence-conditioned faithfulness
- **Link:** https://arxiv.org/abs/2601.15322
- **Relevance score:** 4/5

---

## 3. Automated Evaluation Metrics

### 3.1 CORE: Full-Path Evaluation of LLM Agents Beyond Final State

- **Authors:** Panagiotis Michelakis, Yiannis Hadjiyiannis, Dimitrios Stamoulis
- **Date:** September 2025
- **Venue:** arXiv (2509.20998)
- **Key contribution:** Framework evaluating agent behavior across valid tool-use paths using deterministic finite automata (DFA).
- **Proposed metrics/methods:** Path Correctness, Prefix Criticality, Harmful-Call Rate, Path Efficiency, Path Safety
- **Link:** https://arxiv.org/abs/2509.20998
- **Relevance score:** 5/5 -- DFA-based path evaluation is elegant and highly implementable.

### 3.2 TruthTensor: Evaluating LLMs through Human Imitation on Prediction Markets

- **Authors:** Shirin Shahabi, Spencer Graham, Haruna Isah
- **Date:** January 2026
- **Venue:** arXiv (2601.13545)
- **Key contribution:** Multi-axis evaluation combining accuracy, calibration, narrative stability, and cost efficiency. Replaces static benchmarks with live prediction markets.
- **Proposed metrics/methods:** Multi-axis evaluation (accuracy, calibration, narrative stability, cost efficiency)
- **Link:** https://arxiv.org/abs/2601.13545
- **Relevance score:** 3/5

### 3.3 The Measurement Imbalance in Agentic AI Evaluation

- **Authors:** Kiana Jafari Meimandi, Gabriela Aranguiz-Dias, Grace Ra Kim, et al.
- **Date:** June 2025
- **Venue:** arXiv (2506.02064)
- **Key contribution:** Systematic review revealing evaluation frameworks emphasize technical metrics (83%) while neglecting human-centered (30%) and safety assessments (53%). Proposes balanced evaluation model.
- **Proposed metrics/methods:** Four-axis balanced evaluation model (technical, human-centered, safety, organizational)
- **Link:** https://arxiv.org/abs/2506.02064
- **Relevance score:** 4/5 -- Meta-framework for balanced evaluation design.

---

## 4. Hallucination Detection Metrics

### 4.1 Lowest Span Confidence (LSC): A Zero-Shot Metric for Hallucination Detection

- **Authors:** Yitong Qiao, Licheng Pan, Yu Mi, et al.
- **Date:** January 2026
- **Venue:** arXiv (2601.19918)
- **Key contribution:** Zero-shot hallucination detection via sliding window span likelihood to identify factual uncertainty patterns.
- **Proposed metrics/methods:** Lowest Span Confidence (LSC), sliding window span likelihood
- **Link:** https://arxiv.org/abs/2601.19918
- **Relevance score:** 5/5 -- Zero-shot, no training needed, directly implementable.

### 4.2 Spilled Energy in Large Language Models

- **Authors:** Adrian Robert Minut, Hazem Dewidar, Iacopo Masi
- **Date:** February 2026
- **Venue:** arXiv (2602.18671)
- **Key contribution:** Two training-free metrics derived from output logits for hallucination detection without probe classifiers.
- **Proposed metrics/methods:** Spilled Energy metric, Marginalized Energy metric (both training-free, logit-based)
- **Link:** https://arxiv.org/abs/2602.18671
- **Relevance score:** 5/5 -- Training-free, logit-based, straightforward to implement.

### 4.3 VISTA: Verification In Sequential Turn-based Assessment

- **Authors:** Ashley Lewis, Andrew Perrault, Eric Fosler-Lussier, et al.
- **Date:** October 2025
- **Venue:** arXiv (2510.27052)
- **Key contribution:** Framework decomposing conversational turns into atomic factual claims with verification metrics, improving substantially over FACTSCORE baselines.
- **Proposed metrics/methods:** VISTA framework, atomic claim decomposition, turn-based verification scoring
- **Link:** https://arxiv.org/abs/2510.27052
- **Relevance score:** 5/5 -- Extends FACTSCORE to conversations; highly practical.

### 4.4 CiteAudit: You Cited It, But Did You Read It?

- **Authors:** Zhengqing Yuan, Kaiwen Shi, Zheyuan Zhang, et al.
- **Date:** February 2026
- **Venue:** arXiv (2602.23452)
- **Key contribution:** Unified metrics for citation faithfulness and evidence alignment to detect fabricated scientific references.
- **Proposed metrics/methods:** Citation faithfulness score, evidence alignment metric
- **Link:** https://arxiv.org/abs/2602.23452
- **Relevance score:** 4/5

### 4.5 KGHaluBench: Knowledge Graph-Based Hallucination Benchmark

- **Authors:** Alex Robertson, Huizhi Liang, Mahbub Gani, et al.
- **Date:** February 2026
- **Venue:** arXiv (2602.19643)
- **Key contribution:** Uses knowledge graphs to construct dynamic questions with hallucination metrics normalized by model size.
- **Proposed metrics/methods:** KG-based dynamic questioning, hallucination rate metrics
- **Link:** https://arxiv.org/abs/2602.19643
- **Relevance score:** 4/5

### 4.6 HalluMat: Paraphrased Hallucination Consistency Score

- **Authors:** Bhanu Prakash Vangala, Sajid Mahmud, Pawan Neupane, et al.
- **Date:** December 2025
- **Venue:** arXiv (2512.22396)
- **Key contribution:** Paraphrased Hallucination Consistency Score quantifying inconsistencies across semantically equivalent queries, reducing hallucination rates by 30%.
- **Proposed metrics/methods:** Paraphrased Hallucination Consistency Score (PHCS)
- **Link:** https://arxiv.org/abs/2512.22396
- **Relevance score:** 4/5

### 4.7 Contrastive Mahalanobis Score for Hallucination Detection

- **Authors:** Wenyun Li, Zheng Zhang, Dongmei Jiang, et al.
- **Date:** October 2025
- **Venue:** arXiv (2510.15977)
- **Key contribution:** Models truthful/hallucinated distributions separately using contrastive Mahalanobis distance, achieving 6.55% improvement over baselines.
- **Proposed metrics/methods:** Contrastive Mahalanobis Score
- **Link:** https://arxiv.org/abs/2510.15977
- **Relevance score:** 4/5

---

## 5. Multi-Agent Evaluation

### 5.1 DynaTrust: Dynamic Trust Graphs for Multi-Agent Systems

- **Authors:** Yu Li, Qiang Hu, Yao Zhang, et al.
- **Date:** March 2026
- **Venue:** arXiv (2603.15661)
- **Key contribution:** Dynamic trust graphs to evaluate and isolate compromised agents while maintaining system functionality.
- **Proposed metrics/methods:** Dynamic trust graph scores, sleeper agent detection rate, system functionality preservation metric
- **Link:** https://arxiv.org/abs/2603.15661
- **Relevance score:** 4/5

### 5.2 Cost and Accuracy of Long-Term Memory in Distributed Multi-Agent Systems

- **Authors:** Benedict Wolff, Jacopo Bennati
- **Date:** January 2026
- **Venue:** arXiv (2601.07978)
- **Key contribution:** Evaluates distributed MAS measuring computational, financial, and accuracy metrics with Pareto efficiency framework.
- **Proposed metrics/methods:** Pareto efficiency frontier (cost vs. accuracy), computational cost metrics, financial cost metrics, memory accuracy
- **Link:** https://arxiv.org/abs/2601.07978
- **Relevance score:** 5/5 -- Pareto frontier analysis is directly implementable and visually insightful.

### 5.3 MedMASLab: Benchmarking Multimodal Medical Multi-Agent Systems

- **Authors:** Yunhang Qian, Xiaobin Hu, Jiaquan Yu, et al.
- **Date:** March 2026
- **Venue:** arXiv (2603.09909)
- **Key contribution:** Framework standardizing evaluation of 11 heterogeneous MAS architectures across 24 medical modalities.
- **Proposed metrics/methods:** Unified MAS benchmarking protocol, cross-architecture comparison metrics
- **Link:** https://arxiv.org/abs/2603.09909
- **Relevance score:** 3/5

---

## 6. Cost-Performance Tradeoffs

### 6.1 KAMI: Kamiwaza Agentic Merit Index

- **Authors:** JV Roig
- **Date:** November 2025
- **Venue:** arXiv (2511.08042)
- **Key contribution:** Enterprise benchmark processing 170,000 LLM test items across 35 model configurations, evaluating multi-step tool use with cost-performance tradeoff analysis.
- **Proposed metrics/methods:** KAMI index (composite cost-performance score), token efficiency metrics, enterprise-relevant agentic scoring
- **Link:** https://arxiv.org/abs/2511.08042
- **Relevance score:** 5/5 -- Composite cost-performance index directly implementable for model selection.

### 6.2 The Cost of Dynamic Reasoning

- **Authors:** Jiin Kim, Byeongjun Shin, Jinha Chung, et al.
- **Date:** June 2025 (revised January 2026)
- **Venue:** arXiv (2506.04301)
- **Key contribution:** Analyzes resource usage, latency, energy consumption, and datacenter power demands across agent designs.
- **Proposed metrics/methods:** Resource usage profiling, latency characterization, energy consumption metrics, accuracy-cost tradeoff curves
- **Link:** https://arxiv.org/abs/2506.04301
- **Relevance score:** 4/5

### 6.3 Don't Break the Cache: Prompt Caching for Long-Horizon Agentic Tasks

- **Authors:** Elias Lumer, Faheem Nizar, Akshaya Jangiti, et al.
- **Date:** January 2026
- **Venue:** arXiv (2601.06007)
- **Key contribution:** Caching reduces API costs by 41-80% and improves latency by 13-31% for multi-turn agentic tasks across OpenAI, Anthropic, and Google APIs.
- **Proposed metrics/methods:** Cache hit rate, cost reduction percentage, latency improvement measurement
- **Link:** https://arxiv.org/abs/2601.06007
- **Relevance score:** 5/5 -- Highly practical; easy to implement a caching-aware cost tracker.

---

## 7. Human vs Automated Evaluation

### 7.1 Judge's Verdict: LLM Judge Capability Through Human Agreement

- **Authors:** Steve Han, Gilberto Titericz Junior, Tom Balough, et al.
- **Date:** October 2025
- **Venue:** arXiv (2510.09738)
- **Key contribution:** Two-step evaluation assessing how 54 LLMs replicate human judgment. Distinguishes human-like vs. super-consistent judgment using Cohen's Kappa.
- **Proposed metrics/methods:** Cohen's Kappa agreement analysis, human-like vs. super-consistent classification, 54-model comparison protocol
- **Link:** https://arxiv.org/abs/2510.09738
- **Relevance score:** 4/5

### 7.2 The Illusion of Progress: Re-evaluating Hallucination Detection

- **Authors:** Denis Janiak, Jakub Binkowski, Albert Sawczyn, et al.
- **Date:** August 2025
- **Venue:** arXiv (2508.08285)
- **Key contribution:** ROUGE-based metrics show performance drops of 45.9% when assessed with human-aligned evaluation, exposing flaws in automated hallucination metrics.
- **Proposed metrics/methods:** Human-aligned evaluation protocol, ROUGE gap analysis
- **Link:** https://arxiv.org/abs/2508.08285
- **Relevance score:** 4/5

---

## 8. Task Completion Benchmarks

### 8.1 Terminal-Bench 2.0

- **Authors:** Mike A. Merrill, Alexander G. Shaw, Nicholas Carlini, et al.
- **Date:** January 2026
- **Venue:** arXiv (2601.11868)
- **Key contribution:** Hard benchmark with 89 tasks in terminal environments where frontier models score less than 65%.
- **Proposed metrics/methods:** Terminal task completion rate, difficulty-stratified scoring
- **Link:** https://arxiv.org/abs/2601.11868
- **Relevance score:** 5/5 -- Terminal tasks are directly runnable with Strands Agents.

### 8.2 AgencyBench: 1M-Token Real-World Contexts

- **Authors:** Keyu Li, Junhao Shi, Yang Xiao, et al.
- **Date:** January 2026
- **Venue:** arXiv (2601.11044)
- **Key contribution:** Evaluates 6 agentic capabilities across 32 real-world scenarios with 138 tasks requiring ~90 tool calls and 1M tokens per scenario.
- **Proposed metrics/methods:** 6-capability scoring framework, sandbox-based functional assessment
- **Link:** https://arxiv.org/abs/2601.11044
- **Relevance score:** 5/5 -- Comprehensive real-world benchmark.

### 8.3 WebArbiter: Process Reward Model for Web Navigation

- **Authors:** Yao Zhang, Shijie Tang, Zeyu Li, et al.
- **Date:** January 2026
- **Venue:** arXiv (2601.21872)
- **Key contribution:** Process Reward Model generating structured justifications for web navigation, outperforming GPT-5 by 9.1 points.
- **Proposed metrics/methods:** WebPRMBench, process reward scoring, structured justification generation
- **Link:** https://arxiv.org/abs/2601.21872
- **Relevance score:** 5/5 -- Process reward models are a canonical agent evaluation task.

### 8.4 IDE-Bench

- **Authors:** Spencer Mateega, Jeff Yang, Tiana Costello, et al.
- **Date:** January 2026
- **Venue:** arXiv (2601.20886)
- **Key contribution:** IDE agent evaluation with 80 tasks across eight never-published repositories.
- **Proposed metrics/methods:** Feature implementation rate, bug fix rate, performance optimization metrics
- **Link:** https://arxiv.org/abs/2601.20886
- **Relevance score:** 4/5

### 8.5 CAR-bench: In-Car Voice Assistant Benchmark

- **Authors:** Johannes Kirmayr, Lukas Stappen, Elisabeth Andre
- **Date:** January 2026
- **Venue:** arXiv (2601.22027)
- **Key contribution:** 58 interconnected tools testing consistency, uncertainty handling, and capability awareness.
- **Proposed metrics/methods:** Consistency score, uncertainty handling metric, capability awareness metric
- **Link:** https://arxiv.org/abs/2601.22027
- **Relevance score:** 4/5

### 8.6 LongCLI-Bench

- **Authors:** Yukang Feng, Jianwen Sun, Zelai Yang, et al.
- **Date:** February 2026
- **Venue:** arXiv (2602.14337)
- **Key contribution:** Long-horizon CLI agent benchmark where agents achieve pass rates below 20% on complex tasks.
- **Proposed metrics/methods:** Long-horizon pass rate, CLI command accuracy
- **Link:** https://arxiv.org/abs/2602.14337
- **Relevance score:** 4/5

---

## 9. Tool Use Evaluation

### 9.1 CCTU: Benchmark for Tool Use under Complex Constraints

- **Authors:** Junjie Ye, Guoqiang Zhang, Wenjie Fu, et al.
- **Date:** March 2026
- **Venue:** arXiv (2603.15309)
- **Key contribution:** 200 test cases across 12 constraint categories with executable constraint validation. No model achieves >20% task completion under strict constraints.
- **Proposed metrics/methods:** Executable constraint validation module, 12-category constraint taxonomy, step-level validation
- **Link:** https://arxiv.org/abs/2603.15309
- **Relevance score:** 5/5 -- Constraint-based tool evaluation is directly implementable.

### 9.2 Lost in Execution: Multilingual Robustness of Tool Calling

- **Authors:** Zheng Luo, T Pranav Kutralingam, Ogochukwu N Okoani, et al.
- **Date:** January 2026
- **Venue:** arXiv (2601.05366)
- **Key contribution:** MLCL diagnostic benchmark for multilingual tool calling. Parameter value language mismatch identified as dominant failure mode.
- **Proposed metrics/methods:** MLCL benchmark, parameter value language mismatch detection, cross-lingual tool call accuracy
- **Link:** https://arxiv.org/abs/2601.05366
- **Relevance score:** 4/5

### 9.3 EigenData: Multi-Agent Platform for Function-Calling Data Synthesis and Auditing

- **Authors:** Jiaao Chen, Jingyuan Qi, Mingye Gao, et al.
- **Date:** March 2026
- **Venue:** arXiv (2603.05553)
- **Key contribution:** Outcome-aware evaluation assessing task success via database-state correctness rather than turn-level trajectory matching.
- **Proposed metrics/methods:** Outcome-aware evaluation (database-state correctness), function-calling data auditing pipeline
- **Link:** https://arxiv.org/abs/2603.05553
- **Relevance score:** 4/5

---

## 10. Safety and Alignment Evaluation

### 10.1 MoralityGym: Hierarchical Moral Alignment in Sequential Decision-Making Agents

- **Authors:** Simon Rosen, Siddarth Singh, Ebenezer Gelo, et al.
- **Date:** February 2026
- **Venue:** arXiv (2602.13372)
- **Key contribution:** 98 trolley-dilemma-style environments with "Morality Chains" representing ethical norms as ordered constraints. Decouples task completion from ethical assessment.
- **Proposed metrics/methods:** Morality Metric, Morality Chains framework, ethical constraint ordering
- **Link:** https://arxiv.org/abs/2602.13372
- **Relevance score:** 5/5 -- Gym-style environment, visually compelling and implementable.

### 10.2 AgentDrift: Unsafe Recommendation Drift Under Tool Corruption

- **Authors:** Zekun Wu, Adriano Koshiyama, Sahan Bulathwela, et al.
- **Date:** March 2026
- **Venue:** arXiv (2603.12564)
- **Key contribution:** Paired-trajectory protocol analyzing multi-turn safety failures. Standard metrics miss 65-93% of risk-inappropriate recommendations via information/memory channels.
- **Proposed metrics/methods:** Paired-trajectory safety protocol, drift detection across information/memory channels
- **Link:** https://arxiv.org/abs/2603.12564
- **Relevance score:** 5/5 -- Demonstrates blind spots in standard metrics.

### 10.3 Design Behaviour Codes (DBCs): Taxonomy-Driven Layered Governance Benchmark

- **Authors:** G. Madan Mohan, Veena Kiran Nambiar, Kiranmayee Janardhan
- **Date:** March 2026
- **Venue:** arXiv (2603.04837)
- **Key contribution:** 150-control behavioral governance system with 30-domain risk taxonomy and three-judge ensemble with Fleiss kappa >0.70.
- **Proposed metrics/methods:** Risk Exposure Rate, Fleiss kappa multi-judge agreement, 30-domain risk taxonomy
- **Link:** https://arxiv.org/abs/2603.04837
- **Relevance score:** 4/5

### 10.4 STING: Red-Teaming for Multi-Turn Illicit Task Completion

- **Authors:** Nivya Talokar, Ayush K Tarun, Murari Mandal, et al.
- **Date:** February 2026
- **Venue:** arXiv (2602.16346)
- **Key contribution:** Red-teaming framework measuring multi-turn illicit task completion across six non-English languages.
- **Proposed metrics/methods:** Multi-turn illicit task completion rate, cross-lingual safety evaluation
- **Link:** https://arxiv.org/abs/2602.16346
- **Relevance score:** 4/5

---

## Evaluation Frameworks Landscape

### Tier 1: Established, High-Adoption

| Framework | Stars | Key Evaluation Features | Demo Repo Fit |
|-----------|-------|------------------------|---------------|
| **[Langfuse](https://github.com/langfuse/langfuse)** | 23.6K | LLM-as-judge, user feedback, tracing, prompt versioning | Observability + evaluation combo |
| **[Promptfoo](https://github.com/promptfoo/promptfoo)** | 18.3K | Model comparison, red teaming, CI/CD integration | Side-by-side model evaluation |
| **[Opik](https://github.com/comet-ml/opik)** | 18.4K | Hallucination, moderation, answer relevance, CI/CD | Experiment tracking and A/B testing |
| **[DeepEval](https://github.com/confident-ai/deepeval)** | 14.2K | 30+ metrics (agentic, RAG, safety), pytest plugin | Agent-specific metrics (tool correctness, task completion) |
| **[RAGAS](https://github.com/explodinggradients/ragas)** | 13.1K | RAG metrics, test dataset generation | RAG component evaluation |
| **[Arize Phoenix](https://github.com/Arize-ai/phoenix)** | 9K | LLM benchmarking, agent tracing, RAG evaluation | Observability layer for agent traces |

### Tier 2: Specialized and Emerging

| Framework | Stars | Key Evaluation Features | Demo Repo Fit |
|-----------|-------|------------------------|---------------|
| **[Coze Loop](https://github.com/coze-dev/coze-loop)** | 5.4K | Multi-dimensional prompt/agent testing | Full lifecycle eval pipeline |
| **[Giskard v3](https://github.com/Giskard-AI/giskard-oss)** | 5.2K | Hallucination, prompt injection, bias, PII detection | Safety and security evaluation |
| **[Laminar](https://github.com/lmnr-ai/lmnr)** | 2.7K | 1-line tracing, SQL-based querying, signals | Lightweight observability |
| **[Iris MCP Server](https://github.com/iris-eval/mcp-server)** | 5 | MCP agent evaluation, 12 built-in rules | MCP tool-calling evaluation |

### Tier 3: Academic Benchmarks

| Framework | Stars | Key Evaluation Features |
|-----------|-------|------------------------|
| **[AgentBench](https://github.com/THUDM/AgentBench)** | 3.3K | 5 containerized agent tasks, function calling |
| **[MLGym](https://github.com/facebookresearch/MLGym)** | 591 | AI research agent framework and benchmark |
| **[AgentLab](https://github.com/ServiceNow/AgentLab)** | 541 | Web agent testing and benchmarking |
| **[any-agent](https://github.com/mozilla-ai/any-agent)** | 1.1K | Unified cross-framework agent assessment |

---

## AWS-Specific Tools

### Amazon Bedrock Model Evaluation
- **URL:** https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html
- **Capabilities:** Automatic evaluations, human-based evaluations, judge model evaluations (LLM-as-judge), RAG evaluations
- **Metrics:** Semantic robustness, correctness, response quality

### Amazon Bedrock AgentCore (Preview)
- **URL:** https://aws.amazon.com/bedrock/agentcore/
- **Evaluation Features:** Samples and scores live interactions, assesses correctness/helpfulness/safety/goal-success, real-time CloudWatch dashboards
- **Other:** Persistent memory, tool gateway, secure browser runtime, code interpreter

### Strands Agents SDK
- **URL:** https://github.com/strands-agents/sdk-python
- **Evaluation Status:** No built-in evaluation features. Developers must use external evaluation tools.
- **Opportunity:** This repo can showcase how to connect Strands with DeepEval, Langfuse, or AgentCore evaluators.

---

## Top Papers for Code Demos

Papers with 5/5 relevance score, ordered by recommended demo priority:

| # | Paper | Area | Why It Is a Good Demo |
|---|-------|------|----------------------|
| 1 | **TRACE** (2602.21230) | Trajectory | Hierarchical trajectory utility function -- multi-dimensional scorer |
| 2 | **Autorubric** (2603.00077) | LLM-as-Judge | Open-source rubric framework with bias mitigation |
| 3 | **LSC** (2601.19918) | Hallucination | Zero-shot span confidence -- no training needed |
| 4 | **CORE** (2509.20998) | Automated Metrics | DFA-based full-path evaluation -- elegant and visual |
| 5 | **KAMI** (2511.08042) | Cost-Performance | Composite cost-performance index for model selection |
| 6 | **StepShield** (2601.22136) | Trajectory/Safety | Temporal safety metrics with intervention timing |
| 7 | **TRACER** (2602.11409) | Trajectory | Risk aggregation for agent trajectories |
| 8 | **SCOPE** (2602.13110) | LLM-as-Judge | Conformal prediction for judge calibration |
| 9 | **Spilled Energy** (2602.18671) | Hallucination | Training-free logit-based detection |
| 10 | **VISTA** (2510.27052) | Hallucination | Atomic claim verification for conversations |
| 11 | **CCTU** (2603.15309) | Tool Use | Constraint-validated tool evaluation |
| 12 | **MoralityGym** (2602.13372) | Safety/Alignment | Gym-style ethical evaluation environment |
| 13 | **AgentDrift** (2603.12564) | Safety | Paired-trajectory drift detection |
| 14 | **Don't Break the Cache** (2601.06007) | Cost-Performance | Caching-aware cost/latency measurement |
| 15 | **On Randomness** (2602.07150) | Methodology | Statistical foundation for reliable agent eval |
| 16 | **Terminal-Bench 2.0** (2601.11868) | Task Completion | Terminal tasks directly runnable with Strands |
| 17 | **AgencyBench** (2601.11044) | Task Completion | 1M-token real-world scenarios |
| 18 | **WebArbiter** (2601.21872) | Task Completion | Process reward model for navigation |
| 19 | **How to Report** (2511.21140) | LLM-as-Judge | Confidence intervals and bias correction |
| 20 | **Multi-Agent Cost** (2601.07978) | Multi-Agent | Pareto frontier cost-accuracy analysis |
