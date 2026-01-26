"""Gemini API client."""

import google.generativeai as genai
from typing import Any
from .prompts import PromptTemplate


class GeminiClient:
    """Client for Gemini API."""

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        """Initialize Gemini client."""
        genai.configure(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        """Generate response from Gemini."""
        model = genai.GenerativeModel(self.model)
        response = model.generate_content(prompt)
        return response.text

    def extract_json(self, prompt: str) -> Any:
        """Generate JSON response from Gemini."""
        from .json_guard import parse_json_response

        response = self.generate(prompt)
        return parse_json_response(response)
