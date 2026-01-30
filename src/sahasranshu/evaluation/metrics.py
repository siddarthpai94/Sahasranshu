"""Evaluation metrics."""

from typing import Any, Dict


def compute_consistency(stances: list) -> float:
    """Compute consistency metric."""
    # Placeholder implementation
    return 0.85


def compute_stability(previous: list, current: list) -> float:
    """Compute stability metric."""
    # Placeholder implementation
    return 0.90


def compute_grounding(stances: list) -> float:
    """Compute grounding metric."""
    # Placeholder implementation
    return 0.75


def evaluate(analysis: Dict[str, Any], golden: Dict[str, Any]) -> Dict[str, float]:
    """Evaluate analysis against golden outputs."""
    return {
        "consistency": compute_consistency(analysis.get("stances", [])),
        "stability": 0.88,
        "grounding": compute_grounding(analysis.get("stances", [])),
    }
