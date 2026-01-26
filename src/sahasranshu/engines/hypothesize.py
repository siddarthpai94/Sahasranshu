"""Hypothesis generation engine."""


def generate_hypotheses(deltas: list) -> list:
    """Generate causal hypotheses from deltas."""
    hypotheses = []

    for delta in deltas:
        if delta["change_type"] in ["strengthened", "weakened", "reversed"]:
            hypotheses.append(
                {
                    "topic": delta["topic"],
                    "change_type": delta["change_type"],
                    "mechanism": "Placeholder mechanism",
                    "falsifiers": [],
                }
            )

    return hypotheses
