# Claim Decomposition: Per-Claim Hallucination Verification

**A single hallucination score tells you something is wrong but not what. This demo decomposes agent responses into atomic factual claims and verifies each independently against the source context, identifying exactly which facts are fabricated.**

Based on research: [VISTA: Verification In Sequential Turn-based Assessment](https://arxiv.org/abs/2510.27052) (Oct 2025)

## The Problem

An `OutputEvaluator` score of 0.45 means "the response has issues." But which issues?

- Is it one fabricated claim in an otherwise accurate response?
- Are all the facts wrong?
- Is it a minor embellishment or a complete fabrication?

Without per-claim granularity, you cannot debug or fix the hallucination.

## The Solution

Decompose → Verify → Score:

```
Response: "BA117 costs $450 and includes complimentary champagne"
    ↓ Decompose
Claim 1: "BA117 costs $450"
Claim 2: "BA117 includes complimentary champagne"
    ↓ Verify each against context
✅ Claim 1: SUPPORTED (price matches context)
❌ Claim 2: NOT SUPPORTED (champagne not in context)
    ↓ Score
Score: 1/2 = 0.50 (1 hallucinated claim identified)
```

## Files

| File | Purpose |
|------|---------|
| `02-claim-decomposition.ipynb` | **Main demo** — Decompose, verify, and compare against single-score approach |
| `claim_verifier.py` | **Standalone verifier** — `decompose_claims()`, `verify_claim()`, `verify_response()` |
| `requirements.txt` | Python dependencies |

## Run the Demo

### Notebook

Open `02-claim-decomposition.ipynb` in Jupyter or VS Code.

### Standalone

```bash
python claim_verifier.py
```

**Expected output**:

```
Score: 0.50 (2/4 claims supported)

  ✅ BA117 departs JFK at 7PM
     SUPPORTED: Matches context exactly
  ✅ BA117 costs $450
     SUPPORTED: Price confirmed in context
  ❌ BA117 includes complimentary champagne
     NOT SUPPORTED: Champagne not mentioned in any context
  ❌ BA117 was rated #1 by TripAdvisor
     NOT SUPPORTED: TripAdvisor rating not in context
```

## How It Works

### `decompose_claims(response)` — Extract atomic facts

Uses an LLM to break a response into one verifiable fact per line:

```python
from claim_verifier import decompose_claims

claims = decompose_claims("BA117 costs $450 with free champagne")
# ["BA117 costs $450", "BA117 includes free champagne"]
```

### `verify_claim(claim, context)` — Check one claim

Uses an LLM to determine if a single claim is supported by the context:

```python
from claim_verifier import verify_claim

result = verify_claim("BA117 costs $450", ["BA117: JFK 7PM, $450"])
# {"claim": "BA117 costs $450", "supported": True, "reason": "SUPPORTED: ..."}
```

### `verify_response(response, context)` — Full pipeline

Combines decomposition and verification:

```python
from claim_verifier import verify_response

result = verify_response(response, context)
# {"score": 0.5, "total_claims": 4, "supported_claims": 2, "hallucinated_claims": [...]}
```

## Research Background

- [VISTA](https://arxiv.org/abs/2510.27052) (Oct 2025) — Atomic claim decomposition for conversations, improves over FACTSCORE
- [CiteAudit](https://arxiv.org/abs/2602.23452) (Feb 2026) — Citation faithfulness and evidence alignment
- [HalluMat](https://arxiv.org/abs/2512.22396) (Dec 2025) — Paraphrased consistency scoring

## Next Steps

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
