"""Delta detection engine."""


def detect_deltas(previous_stances: list, current_stances: list) -> list:
    """Detect changes between stance versions."""
    deltas = []

    previous_by_topic = {s["topic"]: s for s in previous_stances}
    current_by_topic = {s["topic"]: s for s in current_stances}

    # Check for removed or changed stances
    for topic, prev_stance in previous_by_topic.items():
        if topic not in current_by_topic:
            deltas.append({"topic": topic, "change_type": "removed"})
        elif prev_stance["category"] != current_by_topic[topic]["category"]:
            deltas.append(
                {
                    "topic": topic,
                    "change_type": "changed",
                    "previous": prev_stance["category"],
                    "current": current_by_topic[topic]["category"],
                }
            )

    # Check for new stances
    for topic in current_by_topic:
        if topic not in previous_by_topic:
            deltas.append({"topic": topic, "change_type": "new"})

    return deltas
