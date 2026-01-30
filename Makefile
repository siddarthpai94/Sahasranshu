.PHONY: help install test test-cov lint type-check format clean

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make test          - Run tests"
	@echo "  make test-cov      - Run tests with coverage"
	@echo "  make lint          - Run linters (ruff, black, isort)"
	@echo "  make type-check    - Run mypy type checking"
	@echo "  make format        - Format code (black, isort)"
	@echo "  make clean         - Clean build artifacts"

install:
	uv sync

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src/sahasranshu --cov-report=html --cov-report=term

lint:
	ruff check src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

type-check:
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

pre-commit-install:
	@pre-commit install

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
