"""Request caching for LLM calls."""

import hashlib
import json
from pathlib import Path
from typing import Optional, Any


class LLMCache:
    """Cache for LLM requests and responses."""

    def __init__(self, cache_dir: Path = Path(".cache")):
        """Initialize cache."""
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)

    def _hash_request(self, prompt: str) -> str:
        """Hash request for caching."""
        return hashlib.sha256(prompt.encode()).hexdigest()

    def get(self, prompt: str) -> Optional[Any]:
        """Get cached response."""
        cache_file = self.cache_dir / f"{self._hash_request(prompt)}.json"
        if cache_file.exists():
            with open(cache_file) as f:
                return json.load(f)
        return None

    def set(self, prompt: str, response: Any) -> None:
        """Cache response."""
        cache_file = self.cache_dir / f"{self._hash_request(prompt)}.json"
        with open(cache_file, "w") as f:
            json.dump(response, f)
