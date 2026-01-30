"""Prompt templates and contracts."""

from typing import Dict, Any


class PromptTemplate:
    """Base prompt template."""

    def __init__(self, template: str):
        """Initialize template."""
        self.template = template

    def format(self, **kwargs) -> str:
        """Format template with variables."""
        return self.template.format(**kwargs)


# Prompt templates
STANCE_EXTRACTION_PROMPT = PromptTemplate(
    """Analyze the following text and extract all policy stances.

Text:
{text}

Extract stances in JSON format with fields:
- topic: str
- category: "supportive" | "cautious" | "opposed" | "neutral"
- confidence: float (0-1)
- evidence: str

Return only valid JSON."""
)

DELTA_DETECTION_PROMPT = PromptTemplate(
    """Compare these two policy documents and identify changes.

Previous:
{previous}

Current:
{current}

Identify deltas in JSON format with fields:
- topic: str
- change_type: "strengthened" | "weakened" | "reversed" | "new" | "removed"
- previous_stance: str
- current_stance: str
- explanation: str

Return only valid JSON."""
)

HYPOTHESIS_PROMPT = PromptTemplate(
    """Given the following list of deltas (in JSON), generate testable hypotheses explaining each change.

Deltas:
{deltas}

Output JSON array of hypotheses with fields:
- mechanism: str
- falsifiers: list[str]
- confidence: float (0-1)

Return only valid JSON."""
)
