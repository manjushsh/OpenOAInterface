"""OpenOA service layer for wind plant analysis.

This module provides a clean interface to the OpenOA library,
handling data loading, analysis execution, and result formatting.
"""

import logging
from typing import Optional, Dict, Any
from pathlib import Path
import json

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class OpenOAService:
    """Service for interacting with OpenOA library.
    
    This service wraps OpenOA functionality and provides a clean
    interface for the API layer. It handles:
    - Loading sample plant data
    - Running various analyses
    - Formatting results for API responses
    """
    
    def __init__(self):
        """Initialize the OpenOA service."""
        self._sample_data: Optional[Any] = None
        self._plant_metadata: Optional[Dict[str, Any]] = None
    
    def get_sample_plant_metadata(self) -> Dict[str, Any]:
        """Get metadata for the sample wind plant.
        
        Returns sample plant metadata from the ENGIE project,
        including turbine information, location, and configuration.
        
        Returns:
            dict: Plant metadata including turbines, capacity, location, etc.
        """
        if self._plant_metadata is not None:
            return self._plant_metadata
        
        try:
            # Load metadata from the examples directory
            metadata_path = self._get_examples_path() / "data" / "plant_meta.json"
            
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    self._plant_metadata = json.load(f)
                logger.info("Loaded plant metadata from file")
            else:
                # Fallback to mock data if file not found
                logger.warning(f"Metadata file not found at {metadata_path}, using mock data")
                self._plant_metadata = self._get_mock_metadata()
            
            return self._plant_metadata
            
        except Exception as e:
            logger.error(f"Failed to load plant metadata: {e}", exc_info=True)
            return self._get_mock_metadata()
    
    def get_sample_data_summary(self) -> Dict[str, Any]:
        """Get a summary of available sample data.
        
        Returns information about the sample dataset including
        date ranges, available sensors, and data completeness.
        
        Returns:
            dict: Summary of sample data availability.
        """
        metadata = self.get_sample_plant_metadata()
        
        return {
            "plant_name": metadata.get("name", "La Haute Borne"),
            "capacity_mw": metadata.get("capacity", 10.5),
            "num_turbines": len(metadata.get("asset_list", [])),
            "data_available": True,
            "description": "Sample SCADA data from La Haute Borne wind plant",
            "analyses_available": [
                "aep",
                "turbine_ideal_energy",
                "electrical_losses",
                "wake_losses"
            ]
        }
    
    def run_aep_analysis_simple(
        self,
        iterations: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """Run AEP analysis (mock or real based on configuration).
        
        Uses mock data if USE_MOCK_DATA=True, otherwise integrates with OpenOA.
        
        Args:
            iterations: Number of Monte Carlo iterations to perform.
            **kwargs: Additional analysis parameters.
            
        Returns:
            dict: Analysis results with AEP estimate and uncertainty.
        """
        if settings.use_mock_data:
            logger.info(f"Running MOCK AEP analysis with {iterations} iterations")
            return self._run_mock_aep_analysis(iterations)
        else:
            logger.info(f"Running REAL OpenOA AEP analysis with {iterations} iterations")
            return self._run_real_aep_analysis(iterations, **kwargs)
        
        # Mock analysis results for demo
        # In production, this would call:
        # from openoa.analysis import MonteCarloAEP
        # analysis = MonteCarloAEP(plant_data, **kwargs)
        # analysis.run()
        
        metadata = self.get_sample_plant_metadata()
        capacity_mw = metadata.get("capacity", 10.5)
        
        # Typical capacity factor for wind is 30-40%
        capacity_factor = 0.35
        hours_per_year = 8760
        
        aep_gwh = (capacity_mw * capacity_factor * hours_per_year) / 1000
        
        return {
            "aep_gwh": round(aep_gwh, 2),
            "uncertainty_pct": 5.2,
            "capacity_factor": round(capacity_factor * 100, 1),
            "plant_capacity_mw": capacity_mw,
            "analysis_type": "monte_carlo_aep",
            "iterations": iterations,
            "notes": "Simplified analysis for demonstration purposes"
        }
    
    def _run_mock_aep_analysis(self, iterations: int) -> Dict[str, Any]:
        """Run mock AEP analysis for demo/testing.
        
        Args:
            iterations: Number of iterations (used in result but not executed).
            
        Returns:
            dict: Mock analysis results.
        """
        metadata = self.get_sample_plant_metadata()
        capacity_mw = metadata.get("capacity", 10.5)
        
        # Typical capacity factor for wind is 30-40%
        capacity_factor = 0.35
        hours_per_year = 8760
        
        aep_gwh = (capacity_mw * capacity_factor * hours_per_year) / 1000
        
        return {
            "aep_gwh": round(aep_gwh, 2),
            "uncertainty_pct": 5.2,
            "capacity_factor": round(capacity_factor * 100, 1),
            "plant_capacity_mw": capacity_mw,
            "analysis_type": "monte_carlo_aep_mock",
            "iterations": iterations,
            "notes": "Mock analysis for demonstration - USE_MOCK_DATA=True"
        }
    
    def _run_real_aep_analysis(
        self,
        iterations: int,
        **kwargs
    ) -> Dict[str, Any]:
        """Run real OpenOA AEP analysis.
        
        Args:
            iterations: Number of Monte Carlo iterations.
            **kwargs: Additional analysis parameters.
            
        Returns:
            dict: Real OpenOA analysis results.
            
        Raises:
            ImportError: If OpenOA is not installed.
            Exception: If analysis fails.
        """
        try:
            # Import OpenOA components
            from openoa import PlantData
            from openoa.analysis import MonteCarloAEP
            
            logger.info("Loading plant data for OpenOA analysis")
            
            # Load actual plant data
            # For now, we'll use a simplified approach
            # In production, you'd load from examples/data or user upload
            plant_data = self._load_real_plant_data()
            
            # Run the analysis
            logger.info("Initializing MonteCarloAEP")
            analysis = MonteCarloAEP(
                plant=plant_data,
                **kwargs
            )
            
            logger.info(f"Running AEP analysis with {iterations} iterations")
            analysis.run(num_sim=iterations, progress_bar=False)
            
            # Extract results - analysis.results is a pandas DataFrame
            results_df = analysis.results
            logger.info(f"Results columns: {list(results_df.columns)}")
            logger.info(f"Results data:\n{results_df}")
            
            # Get the key metrics from the results DataFrame
            # Extract available columns dynamically
            result_dict = results_df.iloc[0].to_dict()
            
            # Get capacity from metadata
            capacity_mw = plant_data.metadata.capacity if hasattr(plant_data, 'metadata') else 8.2  # La Haute Borne is 8.2 MW
            
            # Map to our standard format
            result = {
                "aep_gwh": round(float(result_dict.get('aep_GWh', 0)), 2),
                "uncertainty_pct": round(float(result_dict.get('uncertainty_pct', result_dict.get('uncertainty', 0))), 2),
                "capacity_factor": round(float(result_dict.get('avail_pct', result_dict.get('capacity_factor', 0))), 1),
                "plant_capacity_mw": capacity_mw,
                "analysis_type": "monte_carlo_aep_real",
                "iterations": iterations,
                "notes": "Real OpenOA analysis using Monte Carlo AEP method",
                "raw_columns": list(results_df.columns)  # For debugging
            }
            
            logger.info(f"Analysis complete: AEP = {result['aep_gwh']} GWh")
            return result
            
        except ImportError as e:
            logger.error(f"OpenOA not installed: {e}")
            raise ImportError(
                "OpenOA library not found. Install it with: pip install openoa"
            )
        except Exception as e:
            logger.error(f"OpenOA analysis failed: {e}", exc_info=True)
            raise
    
    def _load_real_plant_data(self):
        """Load real plant data for OpenOA analysis.
        
        Returns:
            PlantData: OpenOA PlantData object.
            
        Raises:
            ImportError: If OpenOA is not installed.
            FileNotFoundError: If data files not found.
        """
        try:
            from openoa import PlantData
            
            # Try to load from examples directory using project_ENGIE helper
            examples_path = self._get_examples_path()
            
            # Import the ENGIE project helper
            import sys
            sys.path.insert(0, str(examples_path))
            
            from project_ENGIE import prepare
            
            logger.info(f"Loading La Haute Borne data from {examples_path}")
            # Use the ENGIE prepare function which handles all data loading
            plant = prepare(
                path=examples_path / "data" / "la_haute_borne",
                return_value="plantdata",
                use_cleansed=False
            )
            return plant
                
        except ImportError as e:
            logger.error(f"OpenOA or dependencies not installed: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to load plant data: {e}")
            raise
    
    def _get_examples_path(self) -> Path:
        """Get the path to the OpenOA examples directory.
        
        Returns:
            Path: Path to examples directory.
        """
        # We're in webapp/backend/app/services, so examples is ../../../../examples
        current_file = Path(__file__)
        # Go up: services -> app -> backend -> webapp -> OpenOA root
        openoa_root = current_file.parent.parent.parent.parent.parent
        examples_dir = openoa_root / "examples"
        return examples_dir
    
    def _get_mock_metadata(self) -> Dict[str, Any]:
        """Get mock plant metadata for when real data is unavailable.
        
        Returns:
            dict: Mock plant metadata.
        """
        return {
            "name": "La Haute Borne (Sample)",
            "capacity": 10.5,
            "num_turbines": 4,
            "latitude": 49.7,
            "longitude": 3.1,
            "asset_list": [
                {"name": "R80721", "capacity_kw": 2050},
                {"name": "R80736", "capacity_kw": 2050},
                {"name": "R80790", "capacity_kw": 3450},
                {"name": "R80711", "capacity_kw": 3000}
            ],
            "note": "Mock metadata - actual data file not found"
        }


# Singleton instance
openoa_service = OpenOAService()
