# Architecture

## System Overview

Sahasranshu follows a modular pipeline architecture:

```
Input (PDF) → Ingestion → LLM Processing → Analysis → Reporting → Output
```

## Core Components

- **Ingestion**: PDF parsing and page extraction
- **LLM Layer**: Gemini API gateway with caching
- **Engines**: Stance extraction, delta detection, hypothesis generation
- **Reporting**: Markdown memo rendering
- **Evaluation**: Metrics and regression testing

## Data Flow

1. PDF documents are ingested and normalized
2. Text is processed by LLM for stance extraction
3. Changes are detected against previous versions
4. Hypotheses are generated from deltas
5. Results are compiled into analysis memos
6. Output is evaluated against golden standards
