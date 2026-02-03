"""Analysis endpoints.

Provides wind plant operational assessment analysis capabilities.
"""

import logging
from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from app.models.schemas import AEPRequest, AEPResult, AnalysisResponse
from app.services.openoa_service import openoa_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.post(
    "/aep",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Run AEP Analysis",
    description="Performs Annual Energy Production (AEP) analysis on sample wind plant data.",
)
async def run_aep_analysis(request: AEPRequest) -> AnalysisResponse:
    """Run Annual Energy Production (AEP) analysis.
    
    Executes a Monte Carlo AEP analysis on the sample wind plant data
    and returns estimated annual energy production with uncertainty.
    
    Args:
        request: AEP analysis configuration parameters.
        
    Returns:
        AnalysisResponse: Analysis result with AEP estimates.
        
    Raises:
        HTTPException: If analysis fails.
    """
    analysis_id = f"aep_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:6]}"
    
    try:
        logger.info(f"Starting AEP analysis {analysis_id}")
        logger.debug(f"Analysis parameters: {request.model_dump()}")
        
        # Run the analysis
        result = openoa_service.run_aep_analysis_simple(
            iterations=request.iterations
        )
        
        logger.info(f"AEP analysis {analysis_id} completed successfully")
        
        return AnalysisResponse(
            id=analysis_id,
            status="completed",
            result=result,
            created_at=datetime.now(),
            completed_at=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"AEP analysis {analysis_id} failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AEP analysis failed: {str(e)}"
        )


@router.get(
    "/types",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="List Available Analysis Types",
    description="Returns a list of available analysis types and their descriptions.",
)
async def list_analysis_types() -> dict:
    """List available analysis types.
    
    Returns information about all available wind plant analysis types,
    including required parameters and expected outputs.
    
    Returns:
        dict: Available analysis types with descriptions.
    """
    return {
        "analyses": [
            {
                "type": "aep",
                "name": "Annual Energy Production",
                "description": "Monte Carlo AEP analysis with uncertainty quantification",
                "status": "available",
                "endpoint": "/api/v1/analysis/aep"
            },
            {
                "type": "tie",
                "name": "Turbine Ideal Energy",
                "description": "Long-term turbine ideal energy estimation",
                "status": "coming_soon",
                "endpoint": None
            },
            {
                "type": "electrical_losses",
                "name": "Electrical Losses",
                "description": "Estimate electrical losses in the wind plant",
                "status": "coming_soon",
                "endpoint": None
            },
            {
                "type": "wake_losses",
                "name": "Wake Losses",
                "description": "Internal wake loss estimation",
                "status": "coming_soon",
                "endpoint": None
            }
        ]
    }
