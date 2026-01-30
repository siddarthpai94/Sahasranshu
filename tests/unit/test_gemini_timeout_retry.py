import json
from pathlib import Path

import pytest

from sahasranshu.llm.gemini_client import GeminiClient


def test_retry_and_audit_written(tmp_path, monkeypatch):
    client = GeminiClient(
        api_key="fake",
        model="test",
        retries=2,
        backoff_factor=0.0,
        record_responses=False,
        record_path=str(tmp_path),
        audit_enabled=True,
        audit_path=str(tmp_path / "audit.jsonl"),
    )

    calls = {"count": 0}

    def fake_generate(prompt):
        calls["count"] += 1
        if calls["count"] == 1:
            raise TimeoutError("simulated timeout")
        return '{"ok": 1}'

    monkeypatch.setattr(client, "generate", fake_generate)

    parsed = client.extract_json('{"probe": 1}')
    assert parsed == {"ok": 1}

    # Audit file should have at least two entries (failure then success)
    audit_file = Path(client.audit_path)
    assert audit_file.exists()
    lines = audit_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) >= 2
    entries = [json.loads(l) for l in lines]
    assert any(not e.get("success", True) for e in entries)
    assert any(e.get("success", False) is False for e in entries) or any(
        e.get("success", True) for e in entries
    )


def test_exhaust_retries_raises(tmp_path, monkeypatch):
    client = GeminiClient(
        api_key="fake",
        model="test",
        retries=1,
        backoff_factor=0.0,
        audit_enabled=True,
        audit_path=str(tmp_path / "audit.jsonl"),
    )

    def always_fail(prompt):
        raise RuntimeError("boom")

    monkeypatch.setattr(client, "generate", always_fail)

    with pytest.raises(RuntimeError):
        client.extract_json('{"probe": 1}')

    # Audit file should have entries for the failed attempts
    audit_file = Path(client.audit_path)
    assert audit_file.exists()
    lines = audit_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) >= 1
