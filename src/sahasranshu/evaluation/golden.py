"""Golden output regression testing."""

from typing import Dict, Any


def load_golden_output(path: str) -> Dict[str, Any]:
    """Load golden output from file."""
    import json

    with open(path) as f:
        return json.load(f)


def compare_with_golden(analysis: Dict[str, Any], golden: Dict[str, Any]) -> bool:
    """Compare analysis output with golden output."""
    return analysis == golden
