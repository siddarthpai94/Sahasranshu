"""Pydantic settings for sahasranshu."""

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings."""

    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    log_level: str = "INFO"
    cache_dir: Path = Path(".cache")
    enable_cache: bool = True
    output_dir: Path = Path("results/")

    class Config:
        env_file = ".env"
        case_sensitive = False
