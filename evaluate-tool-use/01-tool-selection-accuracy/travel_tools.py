"""Travel agent tools for tool selection evaluation demos.

10 tools with varying levels of similarity to test whether agents
pick the correct one. Ground truth mapping included.
"""

from strands import tool


@tool
def search_flights(origin: str, destination: str, date: str) -> str:
    """Search for available flights between two cities on a date."""
    return f"Flights {origin}->{destination} on {date}: BA117 $450, DL1 $520"


@tool
def search_flight_prices(origin: str, destination: str) -> str:
    """Compare flight prices across airlines for a route."""
    return f"Price comparison {origin}->{destination}: BA $450, DL $520, UA $480"


@tool
def get_flight_status(flight_number: str) -> str:
    """Check real-time status of a specific flight."""
    return f"Flight {flight_number}: On time, Gate B22, Departure in 2h"


@tool
def search_hotels(city: str, check_in: str, check_out: str) -> str:
    """Search available hotels in a city for given dates."""
    return f"Hotels in {city} ({check_in} to {check_out}): Marriott $200/night, Hilton $180/night"


@tool
def get_hotel_pricing(hotel_name: str) -> str:
    """Get detailed pricing for a specific hotel."""
    return f"{hotel_name}: Standard $200, Deluxe $350, Suite $500 per night"


@tool
def book_hotel(hotel_name: str, check_in: str, check_out: str, guest_name: str) -> str:
    """Book a hotel room for a guest."""
    return f"Booked {hotel_name} for {guest_name}: {check_in} to {check_out}. Conf #H12345"


@tool
def get_weather(city: str) -> str:
    """Get current weather conditions for a city."""
    return f"{city}: 18C, partly cloudy, 20% rain"


@tool
def get_currency_exchange(from_currency: str, to_currency: str, amount: float) -> str:
    """Convert an amount between currencies."""
    return f"{amount} {from_currency} = {amount * 0.92:.2f} {to_currency}"


@tool
def get_travel_documents(nationality: str, destination: str) -> str:
    """Check visa and passport requirements for a trip."""
    return f"{nationality} travelers to {destination}: Passport required, no visa needed for stays under 90 days"


@tool
def cancel_booking(confirmation_number: str) -> str:
    """Cancel an existing booking by confirmation number."""
    return f"Booking {confirmation_number} cancelled. Refund processed in 5-7 business days."


ALL_TOOLS = [
    search_flights, search_flight_prices, get_flight_status,
    search_hotels, get_hotel_pricing, book_hotel,
    get_weather, get_currency_exchange, get_travel_documents, cancel_booking,
]

# Ground truth: which tool should be called for each query
GROUND_TRUTH = [
    ("What flights go from NYC to London next Friday?", "search_flights"),
    ("How much does a flight from NYC to London cost?", "search_flight_prices"),
    ("Is flight BA117 on time?", "get_flight_status"),
    ("Find hotels in Paris for March 20-22", "search_hotels"),
    ("How much does the Marriott cost per night?", "get_hotel_pricing"),
    ("Book the Hilton in Rome for Alex, March 15-18", "book_hotel"),
    ("What's the weather in Tokyo?", "get_weather"),
    ("Convert 500 USD to EUR", "get_currency_exchange"),
    ("Do I need a visa for Spain from the USA?", "get_travel_documents"),
    ("Cancel booking H12345", "cancel_booking"),
]
