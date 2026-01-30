"""Hypothesis schema for mechanism and falsifiers."""

from typing import List

from pydantic import BaseModel


class Hypothesis(BaseModel):
    """Causal hypothesis about policy change."""

    mechanism: str
    description: str
    falsifiers: List[str]
    confidence: float  # 0.0-1.0
