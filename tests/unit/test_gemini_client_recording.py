import json

from sahasranshu.llm.gemini_client import GeminiClient


def test_extract_json_records(tmp_path):
    # Arrange: make a GeminiClient that records into tmp_path
    client = GeminiClient(
        api_key="fake",
        model="test-model",
        record_responses=True,
        record_path=str(tmp_path),
    )

    # Monkeypatch the generate method to return a known JSON string
    client.generate = lambda prompt: '{"test": "value", "num": 1}'

    # Act
    parsed = client.extract_json("Test prompt for recording")

    # Assert parsed content
    assert parsed == {"test": "value", "num": 1}

    # Assert that files were written
    files = list(tmp_path.iterdir())
    assert any(p.name.endswith("_raw.txt") for p in files)
    assert any(p.name.endswith("_parsed.json") for p in files)

    # Check contents
    raw = next(p for p in files if p.name.endswith("_raw.txt")).read_text(
        encoding="utf-8"
    )
    parsed_json = json.loads(
        next(p for p in files if p.name.endswith("_parsed.json")).read_text(
            encoding="utf-8"
        )
    )

    assert raw.strip() == '{"test": "value", "num": 1}'
    assert parsed_json == {"test": "value", "num": 1}
