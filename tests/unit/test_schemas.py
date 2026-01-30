"""Tests for schema validation."""

from sahasranshu.schemas.stance import Stance, StanceCategory


def test_stance_creation():
    """Test stance schema creation."""
    stance = Stance(
        topic="Interest Rates",
        category=StanceCategory.SUPPORTIVE,
        confidence=0.95,
        evidence="The policy supports rate increases.",
    )
    assert stance.topic == "Interest Rates"
    assert stance.category == StanceCategory.SUPPORTIVE
    assert stance.confidence == 0.95
