"""Health check and readiness endpoints.

These endpoints are used by load balancers, orchestrators,
and monitoring systems to check service health.
"""

import logging
from datetime import datetime

from fastapi import APIRouter, status

from app.models.schemas import HealthResponse, InfoResponse
from app.core.config import get_settings
from app import __version__

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Returns the health status of the API service.",
)
async def health_check() -> HealthResponse:
    """Check if the API is running and healthy.
    
    This endpoint is used by:
    - Load balancers for health checks
    - Monitoring systems for uptime tracking
    - Render.com for deployment health verification
    
    Returns:
        HealthResponse: Current health status and version info.
    """
    logger.debug("Health check requested")
    
    return HealthResponse(
        status="healthy",
        version=__version__,
        timestamp=datetime.now()
    )


@router.get(
    "/api/v1/info",
    response_model=InfoResponse,
    status_code=status.HTTP_200_OK,
    summary="API Information",
    description="Returns general information about the API and OpenOA version.",
)
async def get_info() -> InfoResponse:
    """Get API and OpenOA library information.
    
    Returns:
        InfoResponse: API metadata and version information.
    """
    settings = get_settings()
    
    # Try to get OpenOA version
    openoa_version = None
    try:
        import openoa
        openoa_version = getattr(openoa, "__version__", None)
    except ImportError:
        logger.warning("OpenOA library not found")
    
    return InfoResponse(
        name=settings.app_name,
        version=__version__,
        environment=settings.environment,
        openoa_version=openoa_version
    )
