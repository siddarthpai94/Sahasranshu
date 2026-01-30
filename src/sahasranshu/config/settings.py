"""Pydantic settings for sahasranshu."""

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3-flash-preview"
    log_level: str = "INFO"
    cache_dir: Path = Path(".cache")
    enable_cache: bool = True
    output_dir: Path = Path("results/")

    # LLM recording options
    llm_record_responses: bool = False
    llm_records_dir: Path = Path("tests/fixtures/gemini_responses")

    # LLM audit / telemetry
    llm_audit_enabled: bool = True
    llm_audit_path: Path = Path(".cache/llm_audit.jsonl")

    class Config:
        env_file = ".env"
        case_sensitive = False
