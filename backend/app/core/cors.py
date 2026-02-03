"""CORS (Cross-Origin Resource Sharing) configuration.

Configures which origins can access the API from browsers.
"""

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.core.config import get_settings


def setup_cors(app: FastAPI) -> None:
    """Configure CORS middleware for the application.
    
    Args:
        app: FastAPI application instance.
    """
    settings = get_settings()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
        expose_headers=["*"],
    )
