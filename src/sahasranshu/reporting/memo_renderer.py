"""Render analysis memos to markdown."""

from typing import Dict, Any


def render_memo(analysis: Dict[str, Any]) -> str:
    """Render analysis to markdown memo."""
    memo = "# Analysis Report\n\n"

    # Stances section
    if analysis.get("stances"):
        memo += "## Stances\n\n"
        for stance in analysis["stances"]:
            memo += f"- **{stance.get('topic', 'Unknown')}**: {stance.get('category', 'Unclear')}\n"
        memo += "\n"

    # Deltas section
    if analysis.get("deltas"):
        memo += "## Changes\n\n"
        for delta in analysis["deltas"]:
            memo += f"- {delta.get('topic', 'Unknown')}: {delta.get('change_type', 'Changed')}\n"
        memo += "\n"

    # Hypotheses section
    if analysis.get("hypotheses"):
        memo += "## Hypotheses\n\n"
        for hyp in analysis["hypotheses"]:
            memo += f"- {hyp.get('mechanism', 'Unknown mechanism')}\n"

    return memo
