"""Real-time hallucination detection using Strands hooks.

Intercepts agent outputs after each model call and checks if the response
is grounded in the tool results seen so far. Flags hallucinations before
they reach the end user.

Based on: StepShield (arxiv.org/abs/2601.22136)
"""

from strands import Agent, tool
from strands.hooks import HookProvider, HookRegistry
from strands.hooks.events import (
    AfterToolCallEvent,
    AfterModelCallEvent,
    BeforeInvocationEvent,
)
from strands.models.openai import OpenAIModel
from strands_evals.evaluators import OutputEvaluator
from strands_evals import Experiment, Case

MODEL_ID = "gpt-4o-mini"

GROUNDING_RUBRIC = (
    "Check if the response is grounded in the provided context (tool results).\n"
    "Score 1.0: Every claim is supported by the context.\n"
    "Score 0.0-0.3: Contains fabricated facts not in the context.\n"
    "The context is in the expected_output field."
)


class HallucinationDetector(HookProvider):
    """Captures tool results and checks agent output for hallucinations.

    How it works:
    1. BeforeInvocation: reset state
    2. AfterToolCall: collect tool outputs as "ground truth context"
    3. AfterModelCall: check if final response is grounded in collected context

    If the final response contains claims not supported by tool results,
    it is flagged as a potential hallucination.
    """

    def __init__(self, model_id: str = MODEL_ID, threshold: float = 0.5):
        self.model_id = model_id
        self.threshold = threshold
        self.tool_outputs: list[str] = []
        self.checks: list[dict] = []

    def register_hooks(self, registry: HookRegistry, **kwargs) -> None:
        registry.add_callback(BeforeInvocationEvent, self._reset)
        registry.add_callback(AfterToolCallEvent, self._collect_tool_output)
        registry.add_callback(AfterModelCallEvent, self._check_grounding)

    def _reset(self, event: BeforeInvocationEvent) -> None:
        self.tool_outputs = []

    def _collect_tool_output(self, event: AfterToolCallEvent) -> None:
        """Collect every tool result as ground truth context."""
        tool_name = event.tool_use["name"]
        for content in event.result.get("content", []):
            if "text" in content:
                self.tool_outputs.append(f"[{tool_name}]: {content['text']}")

    def _check_grounding(self, event: AfterModelCallEvent) -> None:
        """After the model produces a final response, check grounding."""
        if not event.stop_response or not self.tool_outputs:
            return

        # Only check on end_turn (final response, not mid-reasoning)
        if event.stop_response.stop_reason != "end_turn":
            return

        # Extract the text from the model's response
        response_text = ""
        for block in event.stop_response.message.get("content", []):
            if "text" in block:
                response_text += block["text"]

        if not response_text:
            return

        context = "\n".join(self.tool_outputs)

        # Run grounding check
        check_case = Case(
            name="grounding_check",
            input=response_text[:200],
            expected_output=context,
        )
        evaluator = OutputEvaluator(rubric=GROUNDING_RUBRIC, model=self.model_id)
        exp = Experiment(cases=[check_case], evaluators=[evaluator])
        reports = exp.run_evaluations(lambda c: response_text)

        score = reports[0].overall_score
        is_grounded = score >= self.threshold

        check_result = {
            "response_preview": response_text[:100],
            "context_sources": len(self.tool_outputs),
            "grounding_score": score,
            "is_grounded": is_grounded,
        }
        self.checks.append(check_result)

        if not is_grounded:
            print(f"\n⚠️  HALLUCINATION DETECTED (score: {score:.2f})")
            print(f"   Response: {response_text[:100]}...")
        else:
            print(f"\n✅ Response grounded (score: {score:.2f})")

    @property
    def last_check(self) -> dict | None:
        return self.checks[-1] if self.checks else None


# --- Demo tools ---

@tool
def search_flights(origin: str, destination: str, date: str) -> str:
    """Search for available flights between two cities."""
    return (
        f"Flights from {origin} to {destination} on {date}:\n"
        f"1. BA117 - Departs 7:00 PM, arrives 7:00 AM - $450\n"
        f"2. DL1 - Departs 9:30 PM, arrives 9:30 AM - $520"
    )


@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"Weather in {city}: 18C, partly cloudy, 20% rain chance."


def run_demo():
    """Run the real-time hallucination detection demo."""
    detector = HallucinationDetector(threshold=0.5)

    agent = Agent(
        model=OpenAIModel(model_id="gpt-4o-mini"),
        tools=[search_flights, get_weather],
        hooks=[detector],
        system_prompt="You are a travel assistant. Use tools to answer questions.",
    )

    print("=" * 60)
    print("REAL-TIME HALLUCINATION DETECTION WITH HOOKS")
    print("=" * 60)

    # Query 1: Should be grounded (tool has the data)
    print("\n--- Query 1: 'Find flights from NYC to London for Friday' ---")
    agent("Find flights from NYC to London for Friday")

    # Query 2: Should be grounded
    print("\n--- Query 2: 'What's the weather in Paris?' ---")
    agent("What's the weather in Paris?")

    # Summary
    print("\n" + "=" * 60)
    print("DETECTION SUMMARY")
    print("=" * 60)
    for i, check in enumerate(detector.checks):
        icon = "✅" if check["is_grounded"] else "⚠️"
        print(f"  {icon} Check {i+1}: score={check['grounding_score']:.2f}, "
              f"sources={check['context_sources']}")


if __name__ == "__main__":
    run_demo()
