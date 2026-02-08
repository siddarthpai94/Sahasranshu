# Geminie Hackathon: Devpost Submission Guide

**Theme**: "The Alpha Engine" (Quantitative Precision + Enterprise Value)
**Target Audience**: Judges looking for technical depth + viable business use cases.

**Target Audience**: Judges looking for technical depth + viable business use cases.

---

## Built With

*   **python**: The core backend logic and orchestration.
*   **google-gemini**: The AI reasoning engine (Gemini 3 Pro Preview) for Extraction, Delta Computation, and Hypothesis Generation.
*   **javascript**: High-performance, vanilla JS frontend for the "Terminal" dashboard.
*   **pydantic**: Enforced strict JSON schemas for all LLM outputs to ensure type safety.
*   **pypdf**: Native PDF ingestion preserving page structure.
*   **typer**: CLI framework for the operational pipeline.
*   **uv**: Fast Python package management.
*   **html5** / **css3**: Semantic markup and custom styling for the dashboard.

---

## Inspiration
Global financial markets move trillions of dollars based on small changes in central-bank language. When institutions like the Federal Reserve or RBI release a new policy statement, analysts manually compare it with the previous version to detect shifts in tone, emphasis, or stance.

This process is **slow, subjective, and error-prone**. Human readers anchor on expectations and often miss subtle but important changes that actually move markets.

We asked a simple question:
*What if an AI could instantly measure how policy changed—so the main output isn’t a summary of what was said, but a precise description of what changed?*

That question led to **Sahasranshu**.

## What it does
Sahasranshu is a stateless, manifest-driven analysis engine that converts central-bank policy documents into structured, machine-readable policy deltas.

It does the following:
1.  **Ingests** complex regulatory PDFs while preserving layout, tables, and footnotes.
2.  **Extracts** core policy stances (inflation, labor markets, growth, financial conditions, etc.).
3.  **Compares** the latest document against a reference version to compute a structured change vector:
    *   Direction of change
    *   Magnitude
    *   Confidence score
4.  **Generates hypotheses** explaining why the policy stance shifted (e.g., inflation persistence or labor-market cooling).
5.  **Produces falsifiable predictions** about upcoming economic data that could confirm or disprove the hypothesis.

The output is not prose. It is **structured JSON** designed for quantitative analysis, trading systems, and research workflows.

## How we built it
We designed Sahasranshu as a deterministic, auditable pipeline—essential for finance and compliance use cases.

### AI Core
*   Uses a large-context LLM (Gemini 3 Pro Preview) to analyze full policy documents and historical references together.
*   Enforces strict JSON outputs via schema validation, making results directly usable downstream.

### Backend
*   **Python 3.11** with a custom client that handles retries, rate limits, and deterministic audit logs.
*   Stateless, manifest-driven execution to ensure reproducibility.

### Frontend
*   A lightweight, high-performance **JavaScript dashboard** inspired by professional market terminals.
*   Built without heavy frameworks to stay responsive during market-moving events.

### Delta Engine
*   A dedicated comparison layer that reasons about policy intent, not just wording.
*   Outputs normalized deltas with confidence scores instead of raw text differences.

## Challenges we ran into
### 1. Comparative hallucination
LLMs are good at summarizing single documents, but comparisons can introduce invented differences.
*   **Solution**: We implemented a strict, manifest-driven comparison protocol that feeds document pairs together and explicitly instructs the model to ignore stylistic edits and focus only on **policy intent**.

### 2. Latency vs. depth
Deep reasoning improves accuracy, but market users need results fast.
*   **Solution**: We parallelized pipeline stages and optimized prompts to achieve **sub-10-second** end-to-end execution.

### 3. PDF complexity
Critical policy signals often live in tables, footnotes, and formatting quirks.
*   **Solution**: We relied on native multimodal PDF understanding rather than OCR-first pipelines, preserving structure and meaning more reliably.

## Accomplishments that we’re proud of
*   Built a complete **delta-first pipeline** from PDF ingestion to structured predictions.
*   Achieved reproducible, auditable analysis with a stateless design.
*   Enforced strict **JSON schemas** suitable for quantitative systems.
*   Delivered a fast, terminal-style UI that surfaces policy changes in seconds.
*   Shifted the focus from “summary-first” to change-first analysis.

## What we learned
*   **Change is the highest-value signal** in time-series text.
*   **Structured output is critical**—schema turns insight into something usable.
*   **Delta detection requires specialized prompting** and system design.
*   Native multimodal PDF reasoning is a major advantage for regulatory documents.

## What’s next for Sahasranshu: Delta-First NLP for Central Bank Intelligence
*   **Expand coverage** across global central banks (Fed, ECB, BoE, RBI, and emerging markets).
*   **Build a cross-country policy delta index** tracking stance shifts over time.
*   **Enable automatic ingestion** when new statements, minutes, or speeches are released.
*   **Benchmark delta accuracy** against human analysts and historical market reactions.
*   **Integrate additional artifacts**: speeches, Q&A transcripts, and macro data releases.
*   **Package the system as an API** and enterprise dashboard for funds, research desks, and risk teams.

---

## 2. The Demo Video (2-3 Minutes Script)

**[0:00-0:30] The Hook (The Problem)**
*   *Visual*: Split screen. Left side: A stressed analyst scrolling through two PDFs trying to find differences. Right side: A stock chart plummeting.
*   *Voiceover*: "When the Fed speaks, the world listens. But listening isn't enough. You need to know exactly *what changed* since last month. Manual analysis is too slow and too biased."

**[0:30-1:30] The Solution (The Dashboard)**
*   *Visual*: Show the **Sahasranshu Terminal** (your `web_view`).
*   *Action*:
    1.  Refresh the page as the analysis loads.
    2.  Highlight the **"Delta Analysis"** column. Point out a specific change (e.g., "Inflation: Elevated -> Moderating").
    3.  Highlight the **"Genetic Hypotheses"**. Read one out: "The model predicts this is due to 'labor market cooling' and will be falsified if unemployment drops below 4.0%."

**[1:30-2:30] Under the Hood (The Code + Gemini)**
*   *Visual*: Switch to VS Code. Show `src/sahasranshu/engines/assemble.py`.
*   *Voiceover*: "We built this on Gemini 2.0 Flash. Its massive context window allows us to load entire historical archives into memory. We use a proprietary 'Delta-First' prompting architecture."
*   *Visual*: Show the `docs/system_architecture.md` diagram (the Mermaid graph).
*   *Voiceover*: "The system is stateless and manifest-driven, ensuring that every insight is fully reproducible—critical for institutional finance."

**[2:30-3:00] Conclusion**
*   *Visual*: Back to the Dashboard, showing the "Executive Memo".
*   *Voiceover*: "Sahasranshu isn't just a summarizer. It's an automated quantitative analyst. It turns text into alpha."

---

## 3. Submission Checklist

*   [ ] **Public GitHub Repo**: Ensure `GEMINI_API_KEY` is NOT in your committed code. Use `.env.example`.
*   [ ] **Video Link**: YouTube or Vimeo.
*   [ ] **Screenshots**:
    1.  The Main Terminal View (Full Screen).
    2.  The "Intelligence Memo" (Zoomed in).
    3.  The Architecture Diagram.
*   [ ] **Try it out link**: (Optional) If you deploy it (e.g., Vercel/Render), link it here. Since it's Python, you might need a backend host or just say "Instructions to run locally in README."
