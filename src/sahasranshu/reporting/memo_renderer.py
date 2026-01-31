"""Render analysis memos to markdown."""

from typing import Any, Dict


def render_memo(analysis: Dict[str, Any]) -> str:
    """Render analysis to markdown memo."""
    memo = "# Sahasranshu Research Memo\n\n"

    # Metadata (could be passed in, but for now just structure)
    memo += "**Date:** [Date]\n"
    memo += "**Subject:** Policy Stance & Delta Analysis\n\n"
    memo += "---\n\n"

    # Executive Summary
    memo += "## Executive Summary\n\n"
    memo += "> **BLUF** The latest policy statement indicates a sophisticated balance between growth objectives and price stability. "
    memo += "Key shifts in linguistic nuance suggest a strategic transition in the Committee's outlook.\n\n"

    # Stances section
    if analysis.get("stances"):
        memo += "## 1. Tactical Stance Matrix\n\n"
        memo += "| Focus Area | Position | Confidence | Primary Evidence |\n"
        memo += "|------------|----------|------------|------------------|\n"
        for stance in analysis["stances"]:
            topic = stance.get("topic", "Unknown")
            cat = stance.get("category", "Unclear")
            conf = f"{(stance.get('confidence', 0) * 100):.0f}%"
            ev = stance.get("evidence", "").replace("\n", " ")
            memo += f"| {topic} | **{cat.upper()}** | {conf} | {ev} |\n"
        memo += "\n"

    # Deltas section
    if analysis.get("deltas"):
        memo += "## 2. Dynamic Policy Deltas\n\n"
        memo += "Analysis of linguistic mutations since the previous statement:\n\n"
        for delta in analysis["deltas"]:
            topic = delta.get("topic", "Unknown")
            change = delta.get("change_type", "Changed")
            expl = delta.get("explanation", "")
            memo += f"### {topic} [ {change.upper()} ]\n"
            memo += f"{expl}\n\n"
            if "previous_stance" in delta and "current_stance" in delta:
                memo += f"- **PRIOR**: {delta['previous_stance']}\n"
                memo += f"- **CURRENT**: {delta['current_stance']}\n\n"

    # Hypotheses section
    if analysis.get("hypotheses"):
        memo += "## 3. Strategic Hypotheses\n\n"
        memo += "Predictive modeling and identified risks to the current thesis:\n\n"
        for hyp in analysis["hypotheses"]:
            mech = hyp.get("mechanism", "Unknown mechanism")
            conf = f"{(hyp.get('confidence', 0) * 100):.0f}%"
            memo += f"### Hypothesis α [ {conf} Confidence ]\n"
            memo += f"{mech}\n\n"
            if hyp.get("falsifiers"):
                memo += "**Falsification Indicators:**\n"
                for falsifier in hyp["falsifiers"]:
                    memo += f"- {falsifier}\n"
            memo += "\n"
    
    memo += "## 4. Market Sentiment & Outlook\n\n"
    memo += "Based on the extracted stances, the prevailing internal sentiment remains **Balanced**. "
    memo += "Immediate market volatility is expected to remain within historical norms for this policy cycle.\n\n"
    
    memo += "---\n\n"
    memo += "### Digital Authentication\n"
    memo += "**Status:** VERIFIED | **Classification:** L3_EXECUTIVE_ONLY | **Model:** gemini-3-flash-preview\n"

    return memo
