"""Shared test data for hallucination detection comparison.

Five test cases with known ground truth: 2 grounded, 2 hallucinated, 1 mixed.
Both Strands and RAGAS evaluate the exact same data.
"""

TEST_CASES = [
    {
        "name": "grounded_flights",
        "question": "What flights are available from NYC to London?",
        "context": [
            "BA117 departs JFK at 7PM, arrives LHR 7AM, costs $450.",
            "DL1 departs JFK at 9:30PM, arrives LHR 9:30AM, costs $520.",
        ],
        "response": (
            "I found 2 flights:\n"
            "1. BA117 - JFK 7PM to LHR 7AM - $450\n"
            "2. DL1 - JFK 9:30PM to LHR 9:30AM - $520"
        ),
        "is_hallucinated": False,
        "explanation": "All facts match the context exactly.",
    },
    {
        "name": "grounded_weather",
        "question": "What's the weather in Paris?",
        "context": [
            "Paris forecast: 18C, partly cloudy, 20% rain chance, west wind 15 km/h.",
        ],
        "response": "Paris: 18C, partly cloudy with a 20% chance of rain. Wind from the west at 15 km/h.",
        "is_hallucinated": False,
        "explanation": "All facts match the context exactly.",
    },
    {
        "name": "hallucinated_awards",
        "question": "What flights are available from NYC to London?",
        "context": [
            "BA117 departs JFK at 7PM, arrives LHR 7AM, costs $450.",
            "DL1 departs JFK at 9:30PM, arrives LHR 9:30AM, costs $520.",
        ],
        "response": (
            "1. BA117 - $450 (Award-winning service with complimentary champagne)\n"
            "2. DL1 - $520 (Recently rated #1 transatlantic airline by TripAdvisor)"
        ),
        "is_hallucinated": True,
        "explanation": "Awards, champagne, and TripAdvisor rating are fabricated.",
    },
    {
        "name": "hallucinated_airline",
        "question": "What flights are available from NYC to London?",
        "context": [
            "BA117 departs JFK at 7PM, arrives LHR 7AM, costs $450.",
            "DL1 departs JFK at 9:30PM, arrives LHR 9:30AM, costs $520.",
        ],
        "response": (
            "1. BA117 - $450\n"
            "2. DL1 - $520\n"
            "3. Virgin Atlantic VS10 - $399 (cheapest with free lounge access)"
        ),
        "is_hallucinated": True,
        "explanation": "Virgin Atlantic VS10 does not exist in the context.",
    },
    {
        "name": "mixed_embellished",
        "question": "What's the weather in Paris?",
        "context": [
            "Paris forecast: 18C, partly cloudy, 20% rain chance, west wind 15 km/h.",
        ],
        "response": (
            "Paris: 18C, partly cloudy with 20% rain chance. "
            "Great weather for sightseeing! The Eiffel Tower area will be "
            "especially pleasant this afternoon."
        ),
        "is_hallucinated": True,
        "explanation": "Sightseeing recommendation and Eiffel Tower claim are not in context.",
    },
]


def get_ground_truth():
    """Return dict of case_name -> is_hallucinated for verification."""
    return {tc["name"]: tc["is_hallucinated"] for tc in TEST_CASES}
