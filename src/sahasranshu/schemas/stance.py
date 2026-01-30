"""Stance extraction schema."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class StanceCategory(str, Enum):
    """Stance categories."""

    SUPPORTIVE = "supportive"
    CAUTIOUS = "cautious"
    OPPOSED = "opposed"
    NEUTRAL = "neutral"


class Stance(BaseModel):
    """Extracted stance from a document."""

    topic: str
    category: StanceCategory
    confidence: float  # 0.0-1.0
    evidence: str
    page_reference: Optional[int] = None
    section: Optional[str] = None
