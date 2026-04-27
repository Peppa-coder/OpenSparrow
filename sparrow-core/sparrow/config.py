"""Configuration management with environment variables and YAML support."""

from __future__ import annotations

import secrets
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class SparrowConfig(BaseSettings):
    """OpenSparrow configuration — loaded from env vars, .env, or sparrow.yml."""

    model_config = {"env_prefix": "SPARROW_", "env_file": ".env"}

    # Server
    host: str = "0.0.0.0"
    port: int = 8080
    debug: bool = False

    # Security
    secret_key: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    admin_token: str = Field(default_factory=lambda: secrets.token_urlsafe(24))
    allowed_origins: list[str] = ["*"]

    # Database
    db_path: str = "data/sparrow.db"

    # Workspace
    workspace_root: str = str(Path.home() / "sparrow-workspace")

    # LLM
    llm_provider: Literal["openai", "anthropic", "ollama"] = "ollama"
    llm_model: str = "llama3"
    llm_api_key: str = ""
    llm_base_url: str = "http://localhost:11434"

    # Agent connection
    agent_ws_port: int = 8081

    # Telegram (optional)
    telegram_bot_token: str = ""
    telegram_allowed_users: list[str] = []


def load_config() -> SparrowConfig:
    """Load configuration with sensible defaults."""
    return SparrowConfig()
