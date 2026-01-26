"""Analysis memo schema."""

from pydantic import BaseModel
from typing import List
from datetime import datetime


class Memo(BaseModel):
    """Analysis memo combining stances, deltas, and hypotheses."""

    document_id: str
    document_title: str
    analysis_date: datetime
    stances: List[dict]
    deltas: List[dict] = []
    hypotheses: List[dict] = []
    summary: str
