"""FastAPI application factory and configuration.

This is the main entry point for the application.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.cors import setup_cors
from app.api.routes import health
from app.services.file_storage import FileStorage
from app import __version__

# Configure logging
settings = get_settings()
logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events.
    
    Handles startup and shutdown events for the application.
    """
    # Startup
    logger.info(f"Starting {settings.app_name} v{__version__}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"CORS origins: {settings.cors_origins}")
    
    # Clean up old uploaded files on startup
    logger.info("Cleaning up old uploaded files...")
    FileStorage._cleanup_old_files(max_age_hours=24)
    logger.info("File cleanup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="REST API for OpenOA wind plant operational assessment",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Setup CORS
setup_cors(app)

# Include routers
app.include_router(health.router)

# Import additional routers
from app.api.routes import data, analysis, upload

app.include_router(data.router, prefix=settings.api_v1_prefix)
app.include_router(analysis.router, prefix=settings.api_v1_prefix)
app.include_router(upload.router, prefix=settings.api_v1_prefix)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    """Handle unexpected exceptions.
    
    Args:
        request: The request that caused the exception.
        exc: The exception that was raised.
        
    Returns:
        JSONResponse with error details.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_code": "INTERNAL_ERROR"
        }
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information.
    
    Returns:
        dict: Welcome message and API links.
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": __version__,
        "docs": "/docs",
        "health": "/health",
        "api": settings.api_v1_prefix
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
