"""Shared types and enums."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class StanceType(str, Enum):
    """Stance classification."""

    SUPPORTIVE = "supportive"
    CAUTIOUS = "cautious"
    OPPOSED = "opposed"
    NEUTRAL = "neutral"
    UNCLEAR = "unclear"


@dataclass
class PageReference:
    """Reference to a page in a document."""

    doc_id: str
    page_number: int
    section: Optional[str] = None
