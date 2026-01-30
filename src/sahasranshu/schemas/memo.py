"""Analysis memo schema."""

from datetime import datetime
from typing import List

from pydantic import BaseModel


class Memo(BaseModel):
    """Analysis memo combining stances, deltas, and hypotheses."""

    document_id: str
    document_title: str
    analysis_date: datetime
    stances: List[dict]
    deltas: List[dict] = []
    hypotheses: List[dict] = []
    summary: str
