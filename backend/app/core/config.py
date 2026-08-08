import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Interview Agent"
    VERSION: str = "1.0.0"
    ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]

    # Data File Paths
    CURRICULUM_PATH: str = "app/data/curriculum.json"
    CANDIDATE_PATH: str = "app/data/candidate.json"

    # LLM Settings
    LLM_PROVIDER: str = "mock"  # Options: 'mock', 'gemini', 'openai', 'claude'
    LLM_API_KEY: str = ""
    LLM_MODEL_NAME: str = "gemini-1.5-flash"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 500

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
