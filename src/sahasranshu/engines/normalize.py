"""Stance normalization engine."""


def normalize_stances(stances: list) -> list:
    """Normalize extracted stances."""
    normalized = []
    for stance in stances:
        normalized.append({**stance, "confidence": float(stance.get("confidence", 0.5))})
    return normalized
