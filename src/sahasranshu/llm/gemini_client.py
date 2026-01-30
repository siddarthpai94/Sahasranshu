"""Gemini API client."""

from typing import Any
from pathlib import Path


class GeminiClient:
    """Client for Gemini API."""

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash", record_responses: bool = False, record_path: str = None):
        """Initialize Gemini client.

        Args:
            api_key: Gemini API key
            model: Model name
            record_responses: If True, save raw responses and parsed JSON to disk
            record_path: Directory to store recordings
        """
        # defer configuring the library until generate() to avoid import-time dependency
        self.api_key = api_key
        self.model = model
        self.record_responses = record_responses
        self.record_path = Path(record_path) if record_path else None

        if self.record_responses and self.record_path:
            self.record_path.mkdir(parents=True, exist_ok=True)

    def generate(self, prompt: str) -> str:
        """Generate response from Gemini."""
        # Import lazily so tests don't require the google.generativeai package
        try:
            import google.generativeai as genai
        except Exception as e:
            raise RuntimeError("google.generativeai library is required to call the live Gemini API") from e

        genai.configure(api_key=self.api_key if hasattr(self, "api_key") else None)
        model = genai.GenerativeModel(self.model)
        response = model.generate_content(prompt)
        return response.text

    def extract_json(self, prompt: str) -> Any:
        """Generate JSON response from Gemini and optionally record it."""
        from .json_guard import parse_json_response
        import time
        import json

        response = self.generate(prompt)
        parsed = parse_json_response(response)

        if self.record_responses and self.record_path:
            # create a safe filename using timestamp and a short slug of the prompt
            ts = int(time.time() * 1000)
            slug = "".join(ch if ch.isalnum() else "_" for ch in prompt[:40]).strip("_")
            raw_file = self.record_path / f"{ts}_{slug}_raw.txt"
            parsed_file = self.record_path / f"{ts}_{slug}_parsed.json"
            try:
                raw_file.write_text(response, encoding="utf-8")
                parsed_file.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
            except Exception:
                # swallow any file system errors to avoid breaking pipeline
                pass

        return parsed
