# How to Run Sahasranshu

This guide details how to execute the Sahasranshu policy analysis pipeline in various modes.

## 1. Prerequisites

Ensure you have the following installed:
*   **Python 3.11+**
*   **uv**: A fast Python package installer and resolver.
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

## 2. Installation

Install dependencies and set up the virtual environment:

```bash
uv sync
```

## 3. Execution Modes

### A. Mock Mode (No API Key Required)
Useful for testing the pipeline flow without incurring LLM costs or needing credentials. It uses pre-canned data.

```bash
# Run on a sample manifest using mock data
python run_one.py data/US/FED/2024/Dec/manifests/2024-12-18_FOMC_Statement.json --mock
```

### B. Live Mode (Recommended)
The easiest way to run the full analysis is using the provided demo script, which handles environment setup (PYTHONPATH) automatically.

1.  **Set API Key**:
    ```bash
    export GEMINI_API_KEY="your-api-key-here"
    ```

2.  **Run the Demo Script**:
    ```bash
    ./scripts/run_demo.sh
    ```

### C. Manual Execution
If you prefer running manual commands, ensure you set `PYTHONPATH` to include the `src` directory:

```bash
export PYTHONPATH=src
python3 run_one.py data/US/FED/2024/Dec/manifests/2024-12-18_FOMC_Statement.json --use-llm
```

## 4. Running the Full Pipeline

To process a batch of documents (defined by input directory):

```bash
sahasranshu run --input data/samples/ --output results/
```

## 5. Developer Commands

Makefile shortcuts for common tasks:

| Command | Description |
| :--- | :--- |
| `make test` | Run unit tests |
| `make lint` | Check code style (Ruff, Black, Isort) |
| `make format` | Auto-format code |
| `make clean` | Remove build artifacts |
