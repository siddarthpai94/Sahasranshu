"""JSON parsing and repair utilities."""

import json
import re
from typing import Any


def parse_json_response(response: str) -> Any:
    """Parse JSON from LLM response with error handling."""
    # Try to extract JSON from response
    json_match = re.search(r"\{.*\}", response, re.DOTALL)

    if json_match:
        json_str = json_match.group()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Attempt repair
            return repair_json(json_str)

    raise ValueError("No valid JSON found in response")


def repair_json(json_str: str) -> Any:
    """Attempt to repair malformed JSON."""
    # Remove trailing commas
    json_str = re.sub(r",\s*([}\]])", r"\1", json_str)
    # Try parsing again
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not repair JSON: {e}")
