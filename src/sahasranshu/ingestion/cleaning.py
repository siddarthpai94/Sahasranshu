"""Text cleaning and normalization."""

import re


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text."""
    # Replace multiple spaces with single space
    text = re.sub(r" +", " ", text)
    # Replace multiple newlines with double newline
    text = re.sub(r"\n\n+", "\n\n", text)
    return text.strip()


def clean_text(text: str) -> str:
    """Clean text for processing."""
    text = normalize_whitespace(text)
    # Remove common header/footer patterns
    lines = text.split("\n")
    cleaned_lines = [
        line
        for line in lines
        if not any(
            pattern in line.lower()
            for pattern in ["page ", "©", "confidential", "draft"]
        )
    ]
    return "\n".join(cleaned_lines)
