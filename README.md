# Sahasranshu

Sahasranshu is an intelligent policy analysis system that extracts, tracks, and contextualizes regulatory stances from official documents using advanced language models.

## Overview

This project provides a comprehensive pipeline for:
- **Extracting** regulatory stances from policy documents
- **Tracking** changes (deltas) across document releases
- **Hypothesizing** causal mechanisms and falsifiers
- **Evaluating** consistency, stability, and grounding of outputs

## Features

- Automated PDF ingestion and page-level processing
- LLM-powered stance extraction with evidence grounding
- Change detection and delta analysis
- Comprehensive evaluation metrics
- Reproducible analysis via content hashing
- Regression testing via golden outputs

## Quick Start

### Prerequisites

- Python 3.11+
- uv (package manager)
- Gemini API key (set `GEMINI_API_KEY` environment variable)

### Installation

```bash
git clone <repo-url>
cd sahasranshu
uv sync
```

### Running the Pipeline

```bash
sahasranshu run --input data/samples/ --output results/
```

For more examples, see [examples/](examples/) directory.

## Documentation

- [Architecture](docs/architecture.md) - System design and components
- [Ontology](docs/ontology.md) - Stance taxonomy and definitions
- [Evaluation](docs/evaluation.md) - Metrics and methodology
- [Datasets](docs/datasets.md) - Data sources and provenance
- [Prompts](docs/prompts.md) - Prompt contracts (no secrets)
- [Limitations](docs/limitations.md) - Known constraints

## Project Structure

```
src/sahasranshu/     # Main package
├── config/          # Settings and logging
├── core/            # Shared types, errors, I/O
├── schemas/         # Pydantic models
├── ingestion/       # PDF processing
├── llm/             # LLM gateway & caching
├── engines/         # Core analysis logic
├── reporting/       # Output formatting
├── evaluation/      # Metrics & regression tests
└── tools/           # Utilities
```

## Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test suite
pytest tests/unit/ -v
```

## Contributing

See the main repository for contribution guidelines.

## License

See [LICENSE](LICENSE) file.
