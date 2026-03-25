"""Rubric-based evaluation utilities.

Compares vague vs. specific rubrics on the same agent outputs,
measuring how well each rubric separates good from bad responses.
"""

from strands import Agent, tool
from strands_evals import Experiment, Case
from strands_evals.evaluators import OutputEvaluator, Contains


# --- Travel Agent Tools ---

@tool
def search_flights(origin: str, destination: str, date: str) -> str:
    """Search for available flights between two cities on a specific date."""
    return (
        f"Flights from {origin} to {destination} on {date}:\n"
        f"1. BA117 - Departs 7:00 PM, arrives 7:00 AM next day - $450\n"
        f"2. DL1 - Departs 9:30 PM, arrives 9:30 AM next day - $520"
    )


@tool
def get_weather(city: str) -> str:
    """Get current weather conditions for a city."""
    return f"Weather in {city}: 18C (64F), partly cloudy, 20% chance of rain."


# --- Pre-computed responses at different quality levels ---

QUESTION = "Find flights from NYC to London for next Friday"

RESPONSES = {
    "good": (
        "I found 3 flights for next Friday:\n"
        "1. British Airways BA117 - JFK 7:00 PM to LHR 7:00 AM - $450\n"
        "2. Delta DL1 - JFK 9:30 PM to LHR 9:30 AM - $520\n"
        "3. United UA100 - EWR 8:15 PM to LHR 8:15 AM - $480"
    ),
    "mediocre": (
        "There are several flights available from New York to London. "
        "Prices vary depending on the airline and time."
    ),
    "hallucinated": (
        "Virgin Atlantic VS10 at $399 is the cheapest option with free "
        "lounge access and complimentary champagne. Recently rated #1 "
        "transatlantic airline by TripAdvisor."
    ),
}

# --- Rubric definitions ---

VAGUE_RUBRIC = "Is this a good response?"

SPECIFIC_RUBRIC = (
    "Rate the travel agent response on a 0 to 1 scale:\n"
    "- 0.8-1.0: Lists specific flights with airline, flight number, times, and price\n"
    "- 0.5-0.7: Provides some useful information but missing key details\n"
    "- 0.2-0.4: Vague response without actionable information\n"
    "- 0.0-0.1: Contains fabricated information or is completely unhelpful"
)


def run_comparison(model_id: str = "gpt-4o-mini"):
    """Compare vague vs specific rubric on the same responses."""

    cases = [
        Case(name=name, input=QUESTION, expected_output="Specific flights with details")
        for name in RESPONSES
    ]

    def task(case):
        return RESPONSES[case.name]

    # Run with vague rubric
    print("=" * 60)
    print("TEST 1: VAGUE RUBRIC - 'Is this a good response?'")
    print("=" * 60)

    vague_eval = OutputEvaluator(rubric=VAGUE_RUBRIC, model=model_id)
    vague_exp = Experiment(cases=cases, evaluators=[vague_eval])
    vague_reports = vague_exp.run_evaluations(task)

    vague_scores = {}
    for case_result in vague_reports[0].cases:
        name = case_result["case_name"]
        score = case_result.get("score", 0)
        vague_scores[name] = score
        print(f"  {name:15} score: {score:.2f}")

    # Run with specific rubric
    print(f"\n{'=' * 60}")
    print("TEST 2: SPECIFIC RUBRIC - Detailed scoring criteria")
    print("=" * 60)

    specific_eval = OutputEvaluator(rubric=SPECIFIC_RUBRIC, model=model_id)
    specific_exp = Experiment(cases=cases, evaluators=[specific_eval])
    specific_reports = specific_exp.run_evaluations(task)

    specific_scores = {}
    for case_result in specific_reports[0].cases:
        name = case_result["case_name"]
        score = case_result.get("score", 0)
        specific_scores[name] = score
        print(f"  {name:15} score: {score:.2f}")

    # Compare spread
    print(f"\n{'=' * 60}")
    print("COMPARISON: Score Spread (good - hallucinated)")
    print("=" * 60)

    vague_spread = vague_scores.get("good", 0) - vague_scores.get("hallucinated", 0)
    specific_spread = specific_scores.get("good", 0) - specific_scores.get("hallucinated", 0)

    print(f"  Vague rubric spread:    {vague_spread:.2f}")
    print(f"  Specific rubric spread: {specific_spread:.2f}")

    if specific_spread > vague_spread:
        print(f"\n  ✅ Specific rubric separates quality levels better (+{specific_spread - vague_spread:.2f})")
    else:
        print(f"\n  ⚠️  Vague rubric performed unexpectedly well this run")

    return vague_scores, specific_scores


if __name__ == "__main__":
    run_comparison()
