"""Travel-agent tools backed by real APIs, for the chaos testing demo.

These tools call live services so the demo has a verifiable ground truth:
when chaos injects a failure, we can check whether the agent fabricated a
value the API never returned.

- `search_flights`  -> Duffel sandbox API (real one-way offers). Needs DUFFEL_API_KEY.
- `get_weather`     -> Open-Meteo (no auth, real daily forecast).

Adapted, with thanks, from Ricardo Ceci's open course
"curso-strands-agentcore-2026" (clase-1 / clase-4 travel agent):
https://github.com/ricardoceci/curso-strands-agentcore-2026
The Duffel two-step flow and the Open-Meteo geocode-then-forecast pattern
are his; here they are trimmed to what the chaos demo needs.
"""

import os
from typing import Optional

import requests
from strands import tool

# --- Duffel (flights) ---------------------------------------------------------

DUFFEL_API_BASE_URL = "https://api.duffel.com"
DUFFEL_API_VERSION = "v2"


def _duffel_headers() -> dict:
    """Build the headers required by every Duffel request."""
    api_key = os.environ.get("DUFFEL_API_KEY")
    if not api_key:
        raise RuntimeError(
            "DUFFEL_API_KEY is not set. Create a free sandbox token at "
            "https://app.duffel.com (Settings -> API tokens, sandbox) and add "
            "it to your .env file as DUFFEL_API_KEY=duffel_sandbox_..."
        )
    return {
        "Authorization": f"Bearer {api_key}",
        "Duffel-Version": DUFFEL_API_VERSION,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


@tool
def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    cabin_class: str = "economy",
    adults: int = 1,
    max_results: int = 3,
) -> dict:
    """Search for one-way flights using the Duffel sandbox API.

    Use this tool whenever the user asks to find, search, or compare flights.
    Returns the cheapest offers ordered by total price.

    Args:
        origin: Origin airport IATA code (3 letters, e.g. "EZE", "JFK").
        destination: Destination airport IATA code (3 letters, e.g. "MIA").
        departure_date: Departure date in YYYY-MM-DD format.
        cabin_class: One of "economy", "premium_economy", "business", "first".
        adults: Number of adult passengers (default 1).
        max_results: Maximum number of offers to return (default 3).

    Returns:
        A dict with `offers`: a list of flight options, each containing
        `offer_id`, `total_amount`, `currency`, `airline`, `departure_time`,
        `arrival_time`, `duration`, and `stops`.
    """
    payload = {
        "data": {
            "slices": [
                {
                    "origin": origin.upper(),
                    "destination": destination.upper(),
                    "departure_date": departure_date,
                }
            ],
            "passengers": [{"type": "adult"} for _ in range(adults)],
            "cabin_class": cabin_class,
        }
    }

    # return_offers=true makes Duffel include offers in the response,
    # avoiding a second round-trip call.
    response = requests.post(
        f"{DUFFEL_API_BASE_URL}/air/offer_requests",
        headers=_duffel_headers(),
        params={"return_offers": "true"},
        json=payload,
        timeout=30,
    )

    if response.status_code >= 400:
        return {
            "error": "duffel_request_failed",
            "status_code": response.status_code,
            "details": response.text[:500],
        }

    data = response.json().get("data", {})
    offers = data.get("offers", [])
    offers_sorted = sorted(offers, key=lambda o: float(o.get("total_amount", 1e9)))
    return {
        "offer_request_id": data.get("id"),
        "offers": [_simplify_offer(o) for o in offers_sorted[:max_results]],
    }


def _simplify_offer(offer: dict) -> dict:
    """Reduce a Duffel offer to the minimum fields the agent needs."""
    first_slice = offer.get("slices", [{}])[0]
    segments = first_slice.get("segments", [])
    first_segment: Optional[dict] = segments[0] if segments else None
    last_segment: Optional[dict] = segments[-1] if segments else None
    return {
        "offer_id": offer.get("id"),
        "total_amount": offer.get("total_amount"),
        "currency": offer.get("total_currency"),
        "airline": offer.get("owner", {}).get("name"),
        "departure_time": first_segment.get("departing_at") if first_segment else None,
        "arrival_time": last_segment.get("arriving_at") if last_segment else None,
        "duration": first_slice.get("duration"),
        "stops": max(0, len(segments) - 1),
    }


# --- Open-Meteo (weather) -----------------------------------------------------

OPEN_METEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def _resolve_city(city: str) -> Optional[dict]:
    """Resolve a city name to coordinates using Open-Meteo's geocoder."""
    response = requests.get(
        OPEN_METEO_GEOCODING_URL,
        params={"name": city, "count": 1, "format": "json"},
        timeout=15,
    )
    response.raise_for_status()
    results = response.json().get("results", [])
    return results[0] if results else None


def _fetch_weather(city: str, target_date: str) -> dict:
    """Core Open-Meteo lookup. Plain function so both the @tool wrapper and
    the ground-truth capture call the SAME code (no decorator internals)."""
    location = _resolve_city(city)
    if not location:
        return {"error": "city_not_found", "city": city}

    response = requests.get(
        OPEN_METEO_FORECAST_URL,
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
            "start_date": target_date,
            "end_date": target_date,
            "timezone": "auto",
        },
        timeout=15,
    )
    response.raise_for_status()
    daily = response.json().get("daily", {})
    if not daily.get("time"):
        return {"error": "no_forecast_for_date", "city": city, "target_date": target_date}

    return {
        "city": location["name"],
        "country": location.get("country"),
        "date": daily["time"][0],
        "temperature_max_c": daily["temperature_2m_max"][0],
        "temperature_min_c": daily["temperature_2m_min"][0],
        "precipitation_mm": daily["precipitation_sum"][0],
        "summary": _weather_summary(daily["weather_code"][0]),
    }


@tool
def get_weather(city: str, target_date: str) -> dict:
    """Get the daily weather forecast for a city on a specific date.

    Use this tool to enrich a flight recommendation with weather context,
    e.g. so the traveler knows what to pack.

    Args:
        city: City name in any supported language, e.g. "Miami", "Buenos Aires".
        target_date: Date in YYYY-MM-DD format. Must be within the next 16 days.

    Returns:
        A dict with `city`, `country`, `date`, `temperature_max_c`,
        `temperature_min_c`, `precipitation_mm`, `summary`. If the city
        cannot be resolved, returns `{"error": "city_not_found"}`.
    """
    return _fetch_weather(city, target_date)


def _weather_summary(weather_code: int) -> str:
    """Translate a WMO weather code into a short English description."""
    code_map = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle",
        61: "Light rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Light snow", 73: "Moderate snow", 80: "Light rain showers",
        95: "Thunderstorm",
    }
    return code_map.get(weather_code, "Unknown")


def ground_truth_weather(city: str, target_date: str) -> dict:
    """Capture GROUND TRUTH: the real forecast, with no agent and no chaos.

    The demo calls this directly to record what Open-Meteo actually returned,
    then checks whether an agent reported a different value when the tool
    was corrupted under chaos.
    """
    return _fetch_weather(city, target_date)


# --- Guardrail hook: catch corrupted-but-plausible tool data ------------------

import re  # noqa: E402  (kept local to the guardrail section)

from strands.hooks import HookProvider, HookRegistry  # noqa: E402
from strands.hooks.events import AfterToolCallEvent  # noqa: E402


class WeatherSanityHook(HookProvider):
    """Cross-check `get_weather` results against an expected range and quarantine
    the whole payload when the value is wrong.

    This fixes two problems at once, both measured in the notebook:

    1. **Correctness.** A plausible-but-wrong temperature (e.g. 12C for Miami in
       June, when the real value is ~31C) is invisible to the model: it looks
       like a normal number, so the agent reports it as fact. The hook range-checks
       it and, on failure, replaces the result with a short error so the agent
       treats the forecast as unavailable instead of trusting it.
    2. **Token cost.** A flaky API often returns the bad value buried in a verbose
       diagnostic dump (retry traces, node logs). Left alone, that whole blob enters
       the model's context and is paid for in tokens. By replacing the failed result
       with a one-line error *before the model sees it*, the hook also cuts the
       tokens the model has to process.

    The expected range plays the role of an independent sanity source; in a real
    system it might come from a second provider, a historical climatology, or a
    monitoring threshold. The hook fires on `AfterToolCallEvent`, which sees (and
    can rewrite) the tool result before the model does.
    """

    def __init__(self, expected_min_c: float, expected_max_c: float):
        self.expected_min_c = expected_min_c
        self.expected_max_c = expected_max_c

    def register_hooks(self, registry: HookRegistry, **kwargs) -> None:
        registry.add_callback(AfterToolCallEvent, self._validate)

    def _validate(self, event: AfterToolCallEvent) -> None:
        if event.tool_use.get("name") != "get_weather":
            return
        result = event.result
        if not hasattr(result, "get"):
            return
        for block in result.get("content", []):
            text = block.get("text", "")
            match = re.search(r'temperature_max_c["\': ]+(-?\d+\.?\d*)', text)
            value_ok = match is not None and (self.expected_min_c <= float(match.group(1)) <= self.expected_max_c)
            if not value_ok:
                # Quarantine the ENTIRE result: this both stops the agent trusting a
                # bad value AND keeps a verbose garbage payload out of the context window.
                block["text"] = (
                    f"ERROR: weather data failed a range cross-check (expected "
                    f"{self.expected_min_c}-{self.expected_max_c}C for this location and "
                    f"season). Treat the forecast as unavailable; do not report a number."
                )
