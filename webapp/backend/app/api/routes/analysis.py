"""Analysis endpoints.

Provides wind plant operational assessment analysis capabilities.
"""

import logging
from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from app.models.schemas import (
    AEPRequest, 
    AnalysisResponse,
    ElectricalLossesRequest,
    WakeLossesRequest,
    TurbineIdealEnergyRequest,
    EYAGapAnalysisRequest
)
from app.services.openoa_service import openoa_service
from app.services.file_storage import FileStorage

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
        
        # Get file path if file_id provided
        file_path = FileStorage.get_file_path(request.file_id) if request.file_id else None
        
        # Run the analysis
        result = openoa_service.run_aep_analysis_simple(
            iterations=request.iterations,
            file_path=file_path
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
                "type": "electrical_losses",
                "name": "Electrical Losses",
                "description": "Estimate electrical losses in the wind plant",
                "status": "available",
                "endpoint": "/api/v1/analysis/electrical-losses"
            },
            {
                "type": "wake_losses",
                "name": "Wake Losses",
                "description": "Internal wake loss estimation",
                "status": "available",
                "endpoint": "/api/v1/analysis/wake-losses"
            },
            {
                "type": "turbine_ideal_energy",
                "name": "Turbine Ideal Energy",
                "description": "Long-term turbine ideal energy estimation",
                "status": "available",
                "endpoint": "/api/v1/analysis/turbine-ideal-energy"
            },
            {
                "type": "eya_gap",
                "name": "EYA Gap Analysis",
                "description": "Compare actual vs expected AEP from energy yield assessment",
                "status": "available",
                "endpoint": "/api/v1/analysis/eya-gap"
            }
        ]
    }


@router.post(
    "/electrical-losses",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Run Electrical Losses Analysis",
    description="Estimates electrical losses in the wind plant collection and transmission system.",
)
async def run_electrical_losses_analysis(request: ElectricalLossesRequest) -> AnalysisResponse:
    """Run electrical losses analysis.
    
    Analyzes SCADA data to estimate electrical losses including transformer,
    collection system, and transmission losses.
    
    Args:
        request: Electrical losses analysis configuration.
        
    Returns:
        AnalysisResponse: Analysis result with loss estimates.
        
    Raises:
        HTTPException: If analysis fails.
    """
    analysis_id = f"elec_losses_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:6]}"
    
    try:
        logger.info(f"Starting electrical losses analysis {analysis_id}")
        
        result = openoa_service.run_electrical_losses_analysis(
            loss_threshold_pct=request.loss_threshold_pct
        )
        
        logger.info(f"Electrical losses analysis {analysis_id} completed successfully")
        
        return AnalysisResponse(
            id=analysis_id,
            status="completed",
            result=result,
            created_at=datetime.now(),
            completed_at=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Electrical losses analysis {analysis_id} failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Electrical losses analysis failed: {str(e)}"
        )


@router.post(
    "/wake-losses",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Run Wake Losses Analysis",
    description="Estimates internal wake losses in the wind plant.",
)
async def run_wake_losses_analysis(request: WakeLossesRequest) -> AnalysisResponse:
    """Run wake losses analysis.
    
    Analyzes turbine-to-turbine wake effects and estimates energy losses
    due to internal wakes.
    
    Args:
        request: Wake losses analysis configuration.
        
    Returns:
        AnalysisResponse: Analysis result with wake loss estimates.
        
    Raises:
        HTTPException: If analysis fails.
    """
    analysis_id = f"wake_losses_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:6]}"
    
    try:
        logger.info(f"Starting wake losses analysis {analysis_id}")
        
        result = openoa_service.run_wake_losses_analysis(
            bin_width=request.bin_width
        )
        
        logger.info(f"Wake losses analysis {analysis_id} completed successfully")
        
        return AnalysisResponse(
            id=analysis_id,
            status="completed",
            result=result,
            created_at=datetime.now(),
            completed_at=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Wake losses analysis {analysis_id} failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Wake losses analysis failed: {str(e)}"
        )


@router.post(
    "/turbine-ideal-energy",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Run Turbine Ideal Energy Analysis",
    description="Calculates long-term gross energy for turbines under ideal conditions.",
)
async def run_turbine_ideal_energy_analysis(request: TurbineIdealEnergyRequest) -> AnalysisResponse:
    """Run turbine ideal energy analysis.
    
    Estimates the ideal energy production of turbines based on long-term
    wind conditions and power curve performance.
    
    Args:
        request: Turbine ideal energy analysis configuration.
        
    Returns:
        AnalysisResponse: Analysis result with ideal energy estimates.
        
    Raises:
        HTTPException: If analysis fails.
    """
    analysis_id = f"turbine_ideal_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:6]}"
    
    try:
        logger.info(f"Starting turbine ideal energy analysis {analysis_id}")
        
        result = openoa_service.run_turbine_ideal_energy_analysis(
            use_lt_distribution=request.use_lt_distribution
        )
        
        logger.info(f"Turbine ideal energy analysis {analysis_id} completed successfully")
        
        return AnalysisResponse(
            id=analysis_id,
            status="completed",
            result=result,
            created_at=datetime.now(),
            completed_at=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Turbine ideal energy analysis {analysis_id} failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Turbine ideal energy analysis failed: {str(e)}"
        )


@router.post(
    "/eya-gap",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Run EYA Gap Analysis",
    description="Compares actual AEP against expected AEP from energy yield assessment.",
)
async def run_eya_gap_analysis(request: EYAGapAnalysisRequest) -> AnalysisResponse:
    """Run EYA gap analysis.
    
    Compares the measured/calculated AEP against the expected AEP from
    the pre-construction energy yield assessment to identify performance gaps.
    
    Args:
        request: EYA gap analysis configuration with expected AEP.
        
    Returns:
        AnalysisResponse: Analysis result with gap metrics.
        
    Raises:
        HTTPException: If analysis fails.
    """
    analysis_id = f"eya_gap_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:6]}"
    
    try:
        logger.info(f"Starting EYA gap analysis {analysis_id}")
        
        result = openoa_service.run_eya_gap_analysis(
            expected_aep_gwh=request.expected_aep_gwh
        )
        
        logger.info(f"EYA gap analysis {analysis_id} completed successfully")
        
        return AnalysisResponse(
            id=analysis_id,
            status="completed",
            result=result,
            created_at=datetime.now(),
            completed_at=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"EYA gap analysis {analysis_id} failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"EYA gap analysis failed: {str(e)}"
        )
