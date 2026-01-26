"""Hypothesis schema for mechanism and falsifiers."""

from pydantic import BaseModel
from typing import List


class Hypothesis(BaseModel):
    """Causal hypothesis about policy change."""

    mechanism: str
    description: str
    falsifiers: List[str]
    confidence: float  # 0.0-1.0
