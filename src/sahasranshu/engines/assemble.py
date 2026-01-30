"""Pipeline assembly engine."""

from typing import Any, Dict


async def run_pipeline(
    text: str, llm_client, previous_text: str = None
) -> Dict[str, Any]:
    """Run end-to-end analysis pipeline."""
    # Extract stances
    stances = await extract_stances(text, llm_client)

    # Detect deltas if previous version exists
    deltas = []
    if previous_text:
        deltas = await detect_deltas(previous_text, text, llm_client)

    # Add metadata for UI
    analysis["meta"] = {
        "current_date": m.publication_date,
        "previous_date": prev_date.strftime("%Y-%m-%d") if previous_text and 'prev_date' in locals() else "N/A"
    }

    return {"stances": stances, "deltas": deltas, "hypotheses": hypotheses, "meta": analysis["meta"]}


from sahasranshu.llm.prompts import (DELTA_DETECTION_PROMPT, HYPOTHESIS_PROMPT,
                                     STANCE_EXTRACTION_PROMPT)


async def extract_stances(text: str, llm_client) -> list:
    """Extract stances from text using the LLM client."""
    prompt = STANCE_EXTRACTION_PROMPT.format(text=text)
    return llm_client.extract_json(prompt)


async def detect_deltas(previous: str, current: str, llm_client) -> list:
    """Detect deltas between versions using the LLM client."""
    prompt = DELTA_DETECTION_PROMPT.format(previous=previous, current=current)
    return llm_client.extract_json(prompt)


async def generate_hypotheses(deltas: list, llm_client) -> list:
    """Generate hypotheses from deltas using the LLM client."""
    prompt = HYPOTHESIS_PROMPT.format(deltas=deltas)
    return llm_client.extract_json(prompt)
