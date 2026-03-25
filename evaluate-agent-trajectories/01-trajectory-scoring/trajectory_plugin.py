"""Trajectory capture plugin for Strands Agents.

Captures every tool call (name, input, output, duration, status) during
agent execution using the HookProvider protocol. The captured trajectory
can then be evaluated with TrajectoryEvaluator.

Based on: TRACE (arxiv.org/abs/2602.21230)
"""

import time
from strands import Agent, tool
from strands.hooks import HookProvider, HookRegistry
from strands.hooks.events import (
    BeforeInvocationEvent,
    AfterInvocationEvent,
    BeforeToolCallEvent,
    AfterToolCallEvent,
)


class TrajectoryPlugin(HookProvider):
    """Captures the full trajectory of an agent invocation.

    Usage:
        tracker = TrajectoryPlugin()
        agent = Agent(tools=[...], hooks=[tracker])
        agent("Do something")
        print(tracker.trajectory)  # List of tool call records
    """

    def __init__(self):
        self.trajectory = []
        self._pending = {}
        self._start_time = None

    def register_hooks(self, registry: HookRegistry, **kwargs) -> None:
        registry.add_callback(BeforeInvocationEvent, self._on_start)
        registry.add_callback(AfterInvocationEvent, self._on_end)
        registry.add_callback(BeforeToolCallEvent, self._on_before_tool)
        registry.add_callback(AfterToolCallEvent, self._on_after_tool)

    def _on_start(self, event: BeforeInvocationEvent) -> None:
        self.trajectory = []
        self._pending = {}
        self._start_time = time.time()

    def _on_end(self, event: AfterInvocationEvent) -> None:
        self.total_duration = time.time() - self._start_time if self._start_time else 0

    def _on_before_tool(self, event: BeforeToolCallEvent) -> None:
        tool_id = event.tool_use["toolUseId"]
        self._pending[tool_id] = time.time()

    def _on_after_tool(self, event: AfterToolCallEvent) -> None:
        tool_id = event.tool_use["toolUseId"]
        start = self._pending.pop(tool_id, time.time())
        duration_ms = (time.time() - start) * 1000

        # Extract text output from tool result
        output_text = ""
        for content in event.result.get("content", []):
            if "text" in content:
                output_text += content["text"]

        self.trajectory.append({
            "tool": event.tool_use["name"],
            "input": event.tool_use.get("input", {}),
            "output": output_text[:200],
            "status": event.result.get("status", "unknown"),
            "duration_ms": round(duration_ms, 1),
            "had_error": event.exception is not None,
        })

    @property
    def tool_names(self) -> list[str]:
        """List of tool names called in order."""
        return [t["tool"] for t in self.trajectory]

    @property
    def failed_calls(self) -> list[dict]:
        """Tool calls that failed."""
        return [t for t in self.trajectory if t["had_error"] or t["status"] == "error"]

    @property
    def duplicate_calls(self) -> list[str]:
        """Tools called more than once."""
        from collections import Counter
        counts = Counter(self.tool_names)
        return [name for name, count in counts.items() if count > 1]

    def summary(self) -> dict:
        """Return a summary for display."""
        return {
            "total_calls": len(self.trajectory),
            "tools_used": self.tool_names,
            "failed_calls": len(self.failed_calls),
            "duplicate_calls": self.duplicate_calls,
            "total_duration_ms": round(self.total_duration * 1000, 1) if hasattr(self, "total_duration") else 0,
        }

    def display(self) -> None:
        """Print the trajectory in a readable format."""
        print(f"\n📋 Trajectory ({len(self.trajectory)} tool calls):\n")
        for i, t in enumerate(self.trajectory, 1):
            icon = "✅" if not t["had_error"] else "❌"
            print(f"  {i}. {icon} {t['tool']} ({t['duration_ms']:.0f}ms)")
            print(f"     Input:  {t['input']}")
            print(f"     Output: {t['output'][:80]}...")

        s = self.summary()
        print(f"\n📊 Summary:")
        print(f"   Total calls: {s['total_calls']}")
        print(f"   Failed: {s['failed_calls']}")
        print(f"   Duplicates: {s['duplicate_calls'] or 'None'}")


# --- Demo tools ---

@tool
def search_flights(origin: str, destination: str, date: str) -> str:
    """Search for available flights between two cities."""
    return (
        f"Flights from {origin} to {destination} on {date}:\n"
        f"1. BA117 - 7:00 PM to 7:00 AM - $450\n"
        f"2. DL1 - 9:30 PM to 9:30 AM - $520"
    )


@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"Weather in {city}: 18C, partly cloudy, 20% rain chance."


@tool
def book_hotel(hotel_name: str, check_in: str, check_out: str) -> str:
    """Book a hotel room."""
    return f"Booking confirmed: {hotel_name}, {check_in} to {check_out}. Confirmation #H12345."


@tool
def get_currency_exchange(from_currency: str, to_currency: str, amount: float) -> str:
    """Convert between currencies."""
    return f"{amount} {from_currency} = {amount * 0.92:.2f} {to_currency}"


if __name__ == "__main__":
    from strands.models.openai import OpenAIModel

    tracker = TrajectoryPlugin()
    agent = Agent(
        model=OpenAIModel(model_id="gpt-4o-mini"),
        tools=[search_flights, get_weather, book_hotel, get_currency_exchange],
        hooks=[tracker],
        system_prompt="You are a travel assistant. Use tools to answer questions.",
    )

    print("=" * 60)
    print("TRAJECTORY CAPTURE DEMO")
    print("=" * 60)

    result = agent("Find flights from NYC to London and check the weather there")
    print(f"\nAgent response:\n{result}")
    tracker.display()
