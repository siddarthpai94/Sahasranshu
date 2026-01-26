"""Content hashing for reproducibility."""

import hashlib
from pathlib import Path


def compute_file_hash(path: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def compute_text_hash(text: str) -> str:
    """Compute SHA256 hash of text content."""
    return hashlib.sha256(text.encode()).hexdigest()
