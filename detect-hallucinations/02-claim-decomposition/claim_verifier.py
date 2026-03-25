"""Claim decomposition and verification for hallucination detection.

Implements VISTA-style atomic claim verification:
1. Decompose a response into individual factual claims
2. Verify each claim against the source context
3. Flag unsupported claims as hallucinations

Based on: VISTA (arxiv.org/abs/2510.27052)
"""

from strands import Agent
from strands.models.openai import OpenAIModel

MODEL_ID = "gpt-4o-mini"


def decompose_claims(response: str, model_id: str = MODEL_ID) -> list[str]:
    """Break a response into atomic factual claims.

    Each claim should be a single verifiable statement.
    Opinions, greetings, and transitions are excluded.
    """
    agent = Agent(
        model=OpenAIModel(model_id=model_id),
        system_prompt=(
            "You are a claim extractor. Given a response, extract every atomic "
            "factual claim as a separate line. Each claim should be a single "
            "verifiable statement of fact.\n\n"
            "Rules:\n"
            "- One claim per line\n"
            "- Skip opinions, greetings, and filler text\n"
            "- Keep claims atomic (one fact each)\n"
            "- Preserve numbers, names, and specific details exactly\n\n"
            "Return ONLY the claims, one per line. No numbering, no bullets."
        ),
    )
    result = agent(f"Extract factual claims from this response:\n\n{response}")
    claims = [line.strip() for line in str(result).strip().split("\n") if line.strip()]
    return claims


def verify_claim(claim: str, context: list[str], model_id: str = MODEL_ID) -> dict:
    """Verify a single claim against the source context.

    Returns dict with 'supported' (bool), 'reason' (str).
    """
    context_text = "\n".join(context)
    agent = Agent(
        model=OpenAIModel(model_id=model_id),
        system_prompt=(
            "You are a fact checker. Given a claim and source context, determine "
            "if the claim is SUPPORTED by the context.\n\n"
            "Rules:\n"
            "- SUPPORTED: The claim can be directly verified from the context\n"
            "- NOT SUPPORTED: The claim contains information not in the context\n\n"
            "Respond with exactly one line:\n"
            "SUPPORTED: <brief reason>\n"
            "or\n"
            "NOT SUPPORTED: <brief reason>"
        ),
    )
    result = str(agent(f"Context:\n{context_text}\n\nClaim: {claim}"))
    supported = result.strip().upper().startswith("SUPPORTED")
    return {"claim": claim, "supported": supported, "reason": result.strip()}


def verify_response(response: str, context: list[str], model_id: str = MODEL_ID) -> dict:
    """Full pipeline: decompose response into claims and verify each.

    Returns dict with 'claims' (list), 'score' (float), 'hallucinated_claims' (list).
    """
    claims = decompose_claims(response, model_id)
    results = []
    for claim in claims:
        result = verify_claim(claim, context, model_id)
        results.append(result)

    supported_count = sum(1 for r in results if r["supported"])
    total = len(results) if results else 1
    score = supported_count / total

    hallucinated = [r for r in results if not r["supported"]]

    return {
        "claims": results,
        "total_claims": total,
        "supported_claims": supported_count,
        "hallucinated_claims": hallucinated,
        "score": score,
    }


if __name__ == "__main__":
    # Quick test
    response = (
        "BA117 departs JFK at 7PM for $450. "
        "It includes complimentary champagne and was rated #1 by TripAdvisor."
    )
    context = ["BA117 departs JFK at 7PM, arrives LHR 7AM, costs $450."]

    print("Response:", response)
    print("Context:", context)
    print()

    result = verify_response(response, context)
    print(f"Score: {result['score']:.2f} ({result['supported_claims']}/{result['total_claims']} claims supported)")
    print()
    for claim in result["claims"]:
        icon = "✅" if claim["supported"] else "❌"
        print(f"  {icon} {claim['claim']}")
        print(f"     {claim['reason']}")
