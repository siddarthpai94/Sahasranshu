"""JSON parsing and repair utilities."""

import json
import re
from typing import Any


def parse_json_response(response: str) -> Any:
    """Parse JSON (object or array) from LLM response with error handling."""
    # Try to extract both object and array
    obj_match = re.search(r"(\{.*\})", response, re.DOTALL)
    arr_match = re.search(r"(\[.*\])", response, re.DOTALL)

    # Prefer the match that appears earlier in the text (covers array wrapped responses)
    json_match = None
    if obj_match and arr_match:
        json_match = obj_match if obj_match.start() < arr_match.start() else arr_match
    else:
        json_match = obj_match or arr_match

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
