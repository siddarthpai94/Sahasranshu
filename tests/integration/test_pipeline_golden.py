import asyncio
import json
from pathlib import Path

import pytest

from sahasranshu.engines import assemble


class MockLLM:
    """A minimal mock LLM client that returns canned JSON based on the prompt."""

    def __init__(self, mapping: dict):
        self.mapping = mapping

    def extract_json(self, prompt: str):
        # very simple heuristic: look for keywords in prompt
        if "Extract stances" in prompt or "Extract stances" in prompt:
            return self.mapping["stances"]
        if "Compare these two policy documents" in prompt:
            return self.mapping["deltas"]
        if "Given the following list of deltas" in prompt:
            return self.mapping["hypotheses"]
        return {}


@pytest.mark.integration
def test_pipeline_golden():
    fixtures = json.loads(Path("tests/fixtures/golden_analysis.json").read_text())

    mock = MockLLM(fixtures)

    text = "Recent indicators suggest that economic activity has continued to expand at a solid pace. Inflation has made progress..."
    prev_text = "Previous statement text indicating tightening bias."

    analysis = asyncio.get_event_loop().run_until_complete(
        assemble.run_pipeline(text=text, llm_client=mock, previous_text=prev_text)
    )

    # Load golden expected
    expected = fixtures

    assert analysis["stances"] == expected["stances"]
    assert analysis["deltas"] == expected["deltas"]
    assert analysis["hypotheses"] == expected["hypotheses"]
