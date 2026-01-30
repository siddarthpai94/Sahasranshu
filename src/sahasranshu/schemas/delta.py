"""Delta (change detection) schema."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ChangeType(str, Enum):
    """Type of change detected."""

    STRENGTHENED = "strengthened"
    WEAKENED = "weakened"
    REVERSED = "reversed"
    NEW = "new"
    REMOVED = "removed"


class Delta(BaseModel):
    """Change detected between document versions."""

    topic: str
    change_type: ChangeType
    previous_stance: Optional[str] = None
    current_stance: Optional[str] = None
    explanation: str
