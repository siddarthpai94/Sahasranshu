"""Tests for JSON parsing and repair."""

import pytest
from sahasranshu.llm.json_guard import parse_json_response


def test_parse_valid_json():
    """Test parsing valid JSON."""
    response = '{"topic": "Test", "category": "supportive"}'
    result = parse_json_response(response)
    assert result["topic"] == "Test"


def test_parse_json_from_text():
    """Test extracting JSON from text."""
    response = "Here is the result: {\"topic\": \"Test\", \"value\": 123}"
    result = parse_json_response(response)
    assert result["topic"] == "Test"
