"""Application configuration management.

Settings are loaded from environment variables with fallback defaults.
"""

import json
from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings from environment variables.
    
    All settings can be overridden via environment variables.
    For example: CORS_ORIGINS='["http://localhost:5173"]'
    """
    
    # Application Settings
    app_name: str = "OpenOA API"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    
    # CORS Settings
    cors_origins: List[str] = ["http://localhost:5173"]
    
    # Logging
    log_level: str = "info"
    
    # API Settings
    api_v1_prefix: str = "/api/v1"
    
    # OpenOA Settings
    use_mock_data: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | List[str]) -> List[str]:
        """Parse CORS origins from string or list.
        
        Handles both JSON string format and list format.
        """
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [origin.strip() for origin in v.split(",")]
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.
    
    Using lru_cache ensures settings are only loaded once.
    """
    return Settings()
