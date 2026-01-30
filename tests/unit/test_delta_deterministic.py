"""Tests for deterministic delta detection."""

from sahasranshu.engines.delta import detect_deltas


def test_detect_new_stance():
    """Test detection of new stances."""
    previous = [{"topic": "Rates", "category": "supportive"}]
    current = [
        {"topic": "Rates", "category": "supportive"},
        {"topic": "Lending", "category": "cautious"},
    ]

    deltas = detect_deltas(previous, current)
    assert any(d["change_type"] == "new" for d in deltas)


def test_detect_changed_stance():
    """Test detection of changed stances."""
    previous = [{"topic": "Rates", "category": "supportive"}]
    current = [{"topic": "Rates", "category": "cautious"}]

    deltas = detect_deltas(previous, current)
    assert any(d["change_type"] == "changed" for d in deltas)
