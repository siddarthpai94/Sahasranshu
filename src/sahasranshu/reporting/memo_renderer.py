"""Render analysis memos to markdown."""

from typing import Any, Dict


def render_memo(analysis: Dict[str, Any]) -> str:
    """Render analysis to markdown memo."""
    memo = "# Sahasranshu Research Memo\n\n"

    # Metadata (could be passed in, but for now just structure)
    memo += "**Date:** [Date]\n"
    memo += "**Subject:** Policy Stance & Delta Analysis\n\n"
    memo += "---\n\n"

    # Executive Summary (placeholder/generated)
    memo += "## Executive Summary\n\n"
    memo += "This memo analyzes the stance of the latest policy statement and compares it with the previous release.\n\n"

    # Stances section
    if analysis.get("stances"):
        memo += "## 1. Canonical Stance Extraction\n\n"
        memo += "| Topic | Stance | Confidence | Evidence |\n"
        memo += "|-------|--------|------------|----------|\n"
        for stance in analysis["stances"]:
            topic = stance.get("topic", "Unknown")
            cat = stance.get("category", "Unclear")
            conf = stance.get("confidence", "N/A")
            ev = stance.get("evidence", "").replace("\n", " ")
            memo += f"| {topic} | **{cat}** | {conf} | {ev} |\n"
        memo += "\n"

    # Deltas section
    if analysis.get("deltas"):
        memo += "## 2. Delta Analysis (vs Prior Meeting)\n\n"
        for delta in analysis["deltas"]:
            topic = delta.get("topic", "Unknown")
            change = delta.get("change_type", "Changed")
            expl = delta.get("explanation", "")
            memo += f"### {topic}: {change.upper()}\n"
            memo += f"> {expl}\n\n"
            if "previous_stance" in delta and "current_stance" in delta:
                memo += f"- **Previous**: {delta['previous_stance']}\n"
                memo += f"- **Current**: {delta['current_stance']}\n\n"

    # Hypotheses section
    if analysis.get("hypotheses"):
        memo += "## 3. Hypotheses & Falsifiers\n\n"
        for hyp in analysis["hypotheses"]:
            mech = hyp.get("mechanism", "Unknown mechanism")
            conf = hyp.get("confidence", "N/A")
            memo += f"### Hypothesis ({conf} confidence)\n"
            memo += f"{mech}\n\n"
            if hyp.get("falsifiers"):
                memo += "**Falsifiers:**\n"
                for falsifier in hyp["falsifiers"]:
                    memo += f"- {falsifier}\n"
            memo += "\n"

    return memo
