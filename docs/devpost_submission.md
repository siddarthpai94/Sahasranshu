# Geminie Hackathon: Devpost Submission Guide

**Theme**: "The Alpha Engine" (Quantitative Precision + Enterprise Value)
**Target Audience**: Judges looking for technical depth + viable business use cases.

**Target Audience**: Judges looking for technical depth + viable business use cases.

---

## Built With

*   **python**: The core backend logic and orchestration.
*   **google-gemini**: The AI reasoning engine (Gemini 2.0 Flash) for Extraction, Delta Computation, and Hypothesis Generation.
*   **javascript**: High-performance, vanilla JS frontend for the "Terminal" dashboard.
*   **pydantic**: Enforced strict JSON schemas for all LLM outputs to ensure type safety.
*   **pypdf**: Native PDF ingestion preserving page structure.
*   **typer**: CLI framework for the operational pipeline.
*   **uv**: Fast Python package management.
*   **html5** / **css3**: Semantic markup and custom styling for the dashboard.

---

## Inspiration
Global financial markets move trillions of dollars based on subtle shifts in central-bank language. When the Federal Reserve or RBI releases a statement, analysts often manually compare it to the prior version to detect changes in tone, emphasis, and policy stance.

That workflow is **slow, qualitative, and biased**. People anchor on expectations and can miss small but meaningful shifts.

We asked a simple question: *what if an AI could quantify policy change instantly—so the primary output isn’t a summary of what was said, but a structured measure of what changed?*

That idea became **Sahasranshu**.

## What it does
Sahasranshu is a stateless, manifest-driven analysis engine that turns central-bank PDFs into machine-readable “policy deltas.”

It:
1.  **Ingests** complex regulatory PDFs while preserving page structure and tables.
2.  **Extracts** key policy stances (e.g., inflation, labor market, growth, financial conditions).
3.  **Compares** the current document against a reference version to compute a structured “change vector” across stances (direction + magnitude + confidence).
4.  **Generates hypotheses** for what may have caused the change (e.g., “inflation persistence” or “labor market cooling”).
5.  **Produces falsifiable predictions** for upcoming economic data releases that could confirm or refute the hypothesis.

The output is not prose—it is **structured JSON** designed for quantitative workflows.

## How we built it
We designed Sahasranshu as a functional pipeline to maximize reproducibility and auditability—critical for finance and compliance.

### AI Core (Gemini 2.0 Flash)
*   **Large context window**: Enabled full documents (and supporting history) to be analyzed together, instead of relying on lossy chunking.
*   **Native JSON mode**: Enforced strict **Pydantic** schemas so stance and delta objects can be consumed directly by downstream systems.

### Backend
*   **Python 3.11** with a custom `GeminiClient` that implements exponential backoff, rate-limit handling, and deterministic audit logs.

### Frontend
*   A high-performance **Vanilla JavaScript** dashboard inspired by the Bloomberg Terminal.
*   We avoided heavy frameworks to keep interaction snappy during high-volatility market events.

### Delta Engine
*   A dedicated comparison engine that explicitly reasons about changes in intent (not just wording), then outputs normalized deltas with confidence scores.

## Challenges we ran into
### Comparative hallucination
LLMs are strong at summarizing one document, but comparisons can trigger invented differences.
*   **Solution**: We implemented a manifest-driven comparison protocol that always feeds document pairs together with explicit instructions to ignore stylistic edits and focus only on **policy intent**.

### Latency vs. depth
Deep reasoning improves quality, but market users need speed.
*   **Solution**: We parallelized stages (reference loading and stance extraction run concurrently) and optimized prompts for **sub-10-second** end-to-end runs.

### PDF complexity (tables, footnotes, formatting)
Policy caveats often live in the hardest-to-parse parts of documents.
*   **Solution**: We leaned on Gemini’s native multimodal PDF understanding to preserve structure and interpret tables/footnotes more reliably than OCR-first approaches.

## Accomplishments that we're proud of
*   Built a complete “delta-first” pipeline end to end: PDF ingestion → stance extraction → change computation → hypothesis + prediction → structured output.
*   Achieved reproducible, auditable runs using a stateless, manifest-driven design.
*   Enforced strict JSON schemas (Pydantic) for reliability in downstream quantitative systems.
*   Delivered a fast, terminal-style UI that makes policy changes explorable in seconds.
*   Reduced noisy “summary-first” behavior by making change detection the primary objective.

## What we learned
*   **Change is the highest-value signal.** In time-series text, “what changed” matters more than “what it says.”
*   **Schema is strategy.** For fintech use cases, structured outputs are the difference between insight and unusable text.
*   **Comparisons require specialized prompting.** Treating delta detection as a first-class task significantly improves accuracy.
*   **Native multimodal PDF reasoning is a big advantage** for regulatory documents, especially where tables and footnotes matter.

## What's next for Sahasranshu
*   **Expand coverage** beyond one institution: Fed, ECB, BoE, RBI, and major emerging-market central banks.
*   **Build a “policy delta index”** that tracks stance shifts over time and across countries.
*   **Add event-driven workflows**: Automatic ingestion when new statements/minutes/speeches drop.
*   **Integrate more artifacts**: Meeting minutes, speeches, Q&A transcripts, and macro data releases for stronger causal attribution.
*   **Package as an API** + enterprise dashboard for funds, research desks, and risk teams.

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
