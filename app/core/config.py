"""
App-wide configuration and settings.
app/core/config.py

Centralizes anything that might change between environments
(your machine vs. someone else's, dev vs. "production") so it's
not hardcoded scattered across the codebase.
"""
import os
from dataclasses import dataclass


@dataclass
class Settings:
    # Which local LLM backend to talk to: "ollama" or "lmstudio".
    # Read from an environment variable if set, otherwise default to ollama.
    llm_backend: str = os.getenv("LLM_BACKEND", "ollama")

    # Base URL for the local LLM server.
    # Ollama defaults to this port when running locally.
    llm_base_url: str = os.getenv("LLM_BASE_URL", "http://localhost:11434")

    # Which model to request from the backend.
    # Change this to whatever model you actually have pulled in Ollama.
    llm_model: str = os.getenv("LLM_MODEL", "llama3.1")

    # Where scaffolded projects get written by default.
    default_output_dir: str = os.getenv("OUTPUT_DIR", "./generated_projects")

    # Toggle: if True, generator falls back to the hardcoded sample
    # projects instead of calling the LLM. Useful for testing without
    # a model running.
    use_llm: bool = os.getenv("USE_LLM", "false").lower() == "true"


# Single shared instance — import this wherever settings are needed,
# rather than creating new Settings() objects everywhere.
settings = Settings()