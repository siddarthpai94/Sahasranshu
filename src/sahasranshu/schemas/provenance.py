"""Provenance tracking schema."""

from typing import List, Optional

from pydantic import BaseModel


class Evidence(BaseModel):
    """Evidence for a claim."""

    text: str
    page_number: int
    section: Optional[str] = None


class Provenance(BaseModel):
    """Provenance information for analysis."""

    document_id: str
    document_hash: str
    analysis_version: str
    evidence_chain: List[Evidence]
