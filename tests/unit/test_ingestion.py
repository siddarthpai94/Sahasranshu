"""Tests for ingestion module."""

import pytest
from sahasranshu.ingestion.cleaning import normalize_whitespace, clean_text


def test_normalize_whitespace():
    """Test whitespace normalization."""
    text = "This  is   a   test\n\n\nwith   spaces"
    normalized = normalize_whitespace(text)
    assert "  " not in normalized
    assert "\n\n\n" not in normalized


def test_clean_text():
    """Test text cleaning."""
    text = "Page 1 of 10\nThis is content\n© 2025"
    cleaned = clean_text(text)
    assert "Page 1" not in cleaned
    assert "©" not in cleaned
