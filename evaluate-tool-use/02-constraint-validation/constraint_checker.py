"""Constraint validation for tool call parameters.

Checks if tool parameters respect business rules (dates, ranges, required fields)
without needing an LLM. Deterministic, instant, zero cost.

Based on: CCTU (arxiv.org/abs/2603.15309)
"""

from datetime import datetime, date


def validate_tool_call(tool_name: str, params: dict) -> dict:
    """Validate tool call parameters against business rules.

    Returns dict with 'valid' (bool), 'violations' (list of strings).
    """
    violations = []
    validators = VALIDATORS.get(tool_name)

    if not validators:
        return {"valid": True, "violations": [], "tool": tool_name}

    for check_fn in validators:
        error = check_fn(params)
        if error:
            violations.append(error)

    return {
        "valid": len(violations) == 0,
        "violations": violations,
        "tool": tool_name,
        "params": params,
    }


# --- Constraint rules per tool ---

def _check_date_format(params: dict, field: str) -> str | None:
    """Date must be YYYY-MM-DD format."""
    val = params.get(field, "")
    try:
        datetime.strptime(val, "%Y-%m-%d")
        return None
    except (ValueError, TypeError):
        return f"'{field}' must be YYYY-MM-DD format, got '{val}'"


def _check_date_not_past(params: dict, field: str) -> str | None:
    """Date must not be in the past."""
    val = params.get(field, "")
    try:
        d = datetime.strptime(val, "%Y-%m-%d").date()
        if d < date.today():
            return f"'{field}' is in the past ({val})"
        return None
    except (ValueError, TypeError):
        return None  # format check handles this


def _check_checkout_after_checkin(params: dict) -> str | None:
    """check_out must be after check_in."""
    try:
        ci = datetime.strptime(params.get("check_in", ""), "%Y-%m-%d").date()
        co = datetime.strptime(params.get("check_out", ""), "%Y-%m-%d").date()
        if co <= ci:
            return f"'check_out' ({co}) must be after 'check_in' ({ci})"
        return None
    except (ValueError, TypeError):
        return None


def _check_required(params: dict, field: str) -> str | None:
    """Field must be present and non-empty."""
    val = params.get(field)
    if not val or (isinstance(val, str) and not val.strip()):
        return f"'{field}' is required but missing or empty"
    return None


def _check_positive_number(params: dict, field: str) -> str | None:
    """Number must be positive."""
    val = params.get(field)
    if val is not None and (not isinstance(val, (int, float)) or val <= 0):
        return f"'{field}' must be a positive number, got {val}"
    return None


VALIDATORS = {
    "search_flights": [
        lambda p: _check_required(p, "origin"),
        lambda p: _check_required(p, "destination"),
        lambda p: _check_required(p, "date"),
        lambda p: _check_date_format(p, "date"),
        lambda p: _check_date_not_past(p, "date"),
    ],
    "search_hotels": [
        lambda p: _check_required(p, "city"),
        lambda p: _check_required(p, "check_in"),
        lambda p: _check_required(p, "check_out"),
        lambda p: _check_date_format(p, "check_in"),
        lambda p: _check_date_format(p, "check_out"),
        lambda p: _check_date_not_past(p, "check_in"),
        _check_checkout_after_checkin,
    ],
    "book_hotel": [
        lambda p: _check_required(p, "hotel_name"),
        lambda p: _check_required(p, "guest_name"),
        lambda p: _check_required(p, "check_in"),
        lambda p: _check_required(p, "check_out"),
        lambda p: _check_date_format(p, "check_in"),
        lambda p: _check_date_format(p, "check_out"),
        _check_checkout_after_checkin,
    ],
    "get_currency_exchange": [
        lambda p: _check_required(p, "from_currency"),
        lambda p: _check_required(p, "to_currency"),
        lambda p: _check_positive_number(p, "amount"),
    ],
}


if __name__ == "__main__":
    # Quick test
    tests = [
        ("search_flights", {"origin": "NYC", "destination": "London", "date": "2026-04-15"}),
        ("search_flights", {"origin": "NYC", "destination": "London", "date": "2020-01-01"}),
        ("search_flights", {"origin": "", "destination": "London", "date": "bad-date"}),
        ("search_hotels", {"city": "Paris", "check_in": "2026-03-20", "check_out": "2026-03-18"}),
        ("get_currency_exchange", {"from_currency": "USD", "to_currency": "EUR", "amount": -100}),
    ]

    for tool_name, params in tests:
        result = validate_tool_call(tool_name, params)
        icon = "✅" if result["valid"] else "❌"
        print(f"{icon} {tool_name}({params})")
        for v in result["violations"]:
            print(f"   ⚠️  {v}")
