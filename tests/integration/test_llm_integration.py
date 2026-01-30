import os

import pytest

from sahasranshu.config.settings import Settings
from sahasranshu.llm.gemini_client import GeminiClient


@pytest.mark.llm
@pytest.mark.integration
def test_llm_can_return_parseable_json():
    """Minimal integration test that calls the live Gemini API and ensures parseable JSON is returned.

    This test is **gated**: it will be skipped locally if GEMINI_API_KEY is not set. In CI, add the
    secret `GEMINI_API_KEY` and the CI job will run this test.
    """
    api_key = os.getenv("GEMINI_API_KEY") or Settings().gemini_api_key
    if not api_key:
        pytest.skip("GEMINI_API_KEY not configured; skipping live LLM test")

    settings = Settings()
    # Use a modest timeout and limited retries to avoid long CI hangs
    client = GeminiClient(
        api_key=api_key, model=settings.gemini_model, timeout=15, retries=1
    )

    # Ask the model to output only JSON (object or array). The json_guard will parse it.
    prompt = 'Please output only valid JSON (an object or array). Example: {"probe": "llm_integration_test"}'

    parsed = client.extract_json(prompt)

    assert isinstance(
        parsed, (dict, list)
    ), "Expected parsed JSON (dict or list) from Gemini"
