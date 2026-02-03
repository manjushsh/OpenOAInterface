"""Pydantic schemas for request/response validation.

All API request and response models are defined here.
"""

from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response schema."""
    
    status: str = Field(..., description="Service health status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=datetime.now, description="Current timestamp")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": "2026-02-03T10:30:00Z"
            }
        }
    }


class InfoResponse(BaseModel):
    """API information response schema."""
    
    name: str = Field(..., description="API name")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Deployment environment")
    openoa_version: Optional[str] = Field(None, description="OpenOA library version")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "OpenOA API",
                "version": "1.0.0",
                "environment": "development",
                "openoa_version": "3.0.0"
            }
        }
    }


class ErrorResponse(BaseModel):
    """Standard error response schema."""
    
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code for client handling")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Resource not found",
                "error_code": "NOT_FOUND",
                "timestamp": "2026-02-03T10:30:00Z"
            }
        }
    }


# Plant Data Schemas

class PlantMetadata(BaseModel):
    """Wind plant metadata schema."""
    
    name: str = Field(..., description="Wind plant name")
    capacity: float = Field(..., description="Total plant capacity in MW")
    num_turbines: int = Field(..., description="Number of turbines")
    latitude: Optional[float] = Field(None, description="Plant latitude")
    longitude: Optional[float] = Field(None, description="Plant longitude")
    asset_list: list[Dict[str, Any]] = Field(default_factory=list, description="List of turbines/assets")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "La Haute Borne",
                "capacity": 10.5,
                "num_turbines": 4,
                "latitude": 49.7,
                "longitude": 3.1,
                "asset_list": [
                    {"name": "R80721", "capacity_kw": 2050}
                ]
            }
        }
    }


class SampleDataSummary(BaseModel):
    """Summary of available sample data."""
    
    plant_name: str = Field(..., description="Name of the sample plant")
    capacity_mw: float = Field(..., description="Plant capacity in MW")
    num_turbines: int = Field(..., description="Number of turbines")
    data_available: bool = Field(..., description="Whether sample data is available")
    description: str = Field(..., description="Description of the sample data")
    analyses_available: list[str] = Field(..., description="Available analysis types")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "plant_name": "La Haute Borne",
                "capacity_mw": 10.5,
                "num_turbines": 4,
                "data_available": True,
                "description": "Sample SCADA data from La Haute Borne wind plant",
                "analyses_available": ["aep", "turbine_ideal_energy", "electrical_losses"]
            }
        }
    }


# Analysis Schemas

class AEPRequest(BaseModel):
    """Request schema for AEP analysis."""
    
    iterations: Optional[int] = Field(1000, description="Number of Monte Carlo iterations", ge=100, le=10000)
    uncertainty_method: Optional[str] = Field("bootstrap", description="Uncertainty quantification method")
    file_id: Optional[str] = Field(None, description="Optional uploaded dataset ID. If None, uses default dataset")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "iterations": 1000,
                "uncertainty_method": "bootstrap",
                "file_id": None
            }
        }
    }


class AEPResult(BaseModel):
    """AEP analysis result schema."""
    
    aep_gwh: float = Field(..., description="Annual energy production in GWh")
    uncertainty_pct: float = Field(..., description="Uncertainty as percentage")
    capacity_factor: float = Field(..., description="Plant capacity factor (%)")
    plant_capacity_mw: float = Field(..., description="Plant capacity in MW")
    analysis_type: str = Field(..., description="Type of analysis performed")
    iterations: int = Field(..., description="Number of iterations performed")
    notes: Optional[str] = Field(None, description="Additional notes about the analysis")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "aep_gwh": 32.34,
                "uncertainty_pct": 5.2,
                "capacity_factor": 35.0,
                "plant_capacity_mw": 10.5,
                "analysis_type": "monte_carlo_aep",
                "iterations": 1000,
                "notes": "Analysis completed successfully"
            }
        }
    }


class ElectricalLossesRequest(BaseModel):
    """Request schema for electrical losses analysis."""
    
    loss_threshold_pct: Optional[float] = Field(5.0, description="Loss threshold percentage", ge=0, le=100)
    file_id: Optional[str] = Field(None, description="Optional uploaded dataset ID. If None, uses default dataset")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "loss_threshold_pct": 5.0,
                "file_id": None
            }
        }
    }


class WakeLossesRequest(BaseModel):
    """Request schema for wake losses analysis."""
    
    bin_width: Optional[float] = Field(1.0, description="Wind speed bin width (m/s)", ge=0.5, le=5.0)
    file_id: Optional[str] = Field(None, description="Optional uploaded dataset ID. If None, uses default dataset")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "bin_width": 1.0,
                "file_id": None
            }
        }
    }


class TurbineIdealEnergyRequest(BaseModel):
    """Request schema for turbine ideal energy analysis."""
    
    use_lt_distribution: Optional[bool] = Field(True, description="Use long-term wind distribution")
    file_id: Optional[str] = Field(None, description="Optional uploaded dataset ID. If None, uses default dataset")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "use_lt_distribution": True,
                "file_id": None
            }
        }
    }


class EYAGapAnalysisRequest(BaseModel):
    """Request schema for EYA gap analysis."""
    
    expected_aep_gwh: float = Field(..., description="Expected AEP from energy yield assessment (GWh)")
    file_id: Optional[str] = Field(None, description="Optional uploaded dataset ID. If None, uses default dataset")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "expected_aep_gwh": 35.0,
                "file_id": None
            }
        }
    }


class AnalysisResponse(BaseModel):
    """Generic analysis response wrapper."""
    
    id: str = Field(..., description="Unique analysis ID")
    status: str = Field(..., description="Analysis status: pending, running, completed, failed")
    result: Optional[Dict[str, Any]] = Field(None, description="Analysis results")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    error: Optional[str] = Field(None, description="Error message if failed")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "aep_20260203_123456",
                "status": "completed",
                "result": {
                    "aep_gwh": 32.34,
                    "uncertainty_pct": 5.2
                },
                "created_at": "2026-02-03T12:34:56Z",
                "completed_at": "2026-02-03T12:35:12Z",
                "error": None
            }
        }
    }
