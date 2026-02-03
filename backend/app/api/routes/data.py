"""Data management endpoints.

Provides access to sample wind plant data and metadata.
"""

import logging
from fastapi import APIRouter, HTTPException, status

from app.models.schemas import PlantMetadata, SampleDataSummary
from app.services.openoa_service import openoa_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/data", tags=["Data"])


@router.get(
    "/sample/summary",
    response_model=SampleDataSummary,
    status_code=status.HTTP_200_OK,
    summary="Get Sample Data Summary",
    description="Returns a summary of available sample wind plant data.",
)
async def get_sample_data_summary() -> SampleDataSummary:
    """Get summary information about the sample dataset.
    
    Provides details about the available sample wind plant data,
    including plant name, capacity, and available analyses.
    
    Returns:
        SampleDataSummary: Summary of sample data.
        
    Raises:
        HTTPException: If data cannot be loaded.
    """
    try:
        logger.info("Fetching sample data summary")
        summary = openoa_service.get_sample_data_summary()
        return SampleDataSummary(**summary)
        
    except Exception as e:
        logger.error(f"Failed to get sample data summary: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load sample data summary"
        )


@router.get(
    "/sample/metadata",
    response_model=PlantMetadata,
    status_code=status.HTTP_200_OK,
    summary="Get Sample Plant Metadata",
    description="Returns detailed metadata for the sample wind plant.",
)
async def get_sample_plant_metadata() -> PlantMetadata:
    """Get detailed metadata for the sample wind plant.
    
    Returns comprehensive metadata including turbine specifications,
    location, and plant configuration.
    
    Returns:
        PlantMetadata: Plant metadata.
        
    Raises:
        HTTPException: If metadata cannot be loaded.
    """
    try:
        logger.info("Fetching sample plant metadata")
        metadata = openoa_service.get_sample_plant_metadata()
        return PlantMetadata(**metadata)
        
    except Exception as e:
        logger.error(f"Failed to get plant metadata: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load plant metadata"
        )
