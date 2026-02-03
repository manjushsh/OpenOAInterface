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
                "wake_losses",
                "eya_gap_analysis"
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
        """Locate the examples directory that ships with the backend."""
        current_file = Path(__file__).resolve()

        # Primary expected location: backend/examples
        candidates = [
            current_file.parents[2] / "examples",  # .../backend/examples
            current_file.parents[3] / "examples",  # .../webapp/examples (fallback)
            current_file.parents[4] / "examples",  # .../repo/examples (fallback)
        ]

        for path in candidates:
            if path.exists():
                return path

        searched = ", ".join(str(p) for p in candidates)
        raise FileNotFoundError(f"Examples directory not found. Checked: {searched}")
    
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
    
    def run_electrical_losses_analysis(self, loss_threshold_pct: float = 5.0, **kwargs) -> Dict[str, Any]:
        """Run electrical losses analysis (mock or real based on configuration).
        
        Args:
            loss_threshold_pct: Threshold for flagging high losses.
            **kwargs: Additional analysis parameters.
            
        Returns:
            dict: Electrical losses analysis results.
        """
        if settings.use_mock_data:
            logger.info(f"Running MOCK electrical losses analysis")
            return self._run_mock_electrical_losses(loss_threshold_pct)
        else:
            logger.info(f"Running REAL OpenOA electrical losses analysis")
            return self._run_real_electrical_losses(loss_threshold_pct, **kwargs)
    
    def _run_mock_electrical_losses(self, loss_threshold_pct: float) -> Dict[str, Any]:
        """Mock electrical losses analysis."""
        metadata = self.get_sample_plant_metadata()
        capacity_mw = metadata.get("capacity", 10.5)
        
        # Typical electrical losses are 1-3%
        total_loss_pct = 2.1
        
        return {
            "total_loss_pct": round(total_loss_pct, 2),
            "threshold_pct": loss_threshold_pct,
            "exceeds_threshold": total_loss_pct > loss_threshold_pct,
            "loss_breakdown": {
                "transformer_loss_pct": 0.8,
                "collection_system_loss_pct": 0.9,
                "transmission_loss_pct": 0.4
            },
            "plant_capacity_mw": capacity_mw,
            "analysis_type": "electrical_losses_mock",
            "notes": "Mock analysis for demonstration - USE_MOCK_DATA=True"
        }
    
    def _run_real_electrical_losses(self, loss_threshold_pct: float, **kwargs) -> Dict[str, Any]:
        """Real OpenOA electrical losses analysis."""
        try:
            from openoa.analysis import ElectricalLosses
            
            logger.info("Loading plant data for electrical losses analysis")
            plant_data = self._load_real_plant_data()
            
            logger.info("Initializing ElectricalLosses analysis")
            analysis = ElectricalLosses(plant=plant_data, **kwargs)
            
            logger.info("Running electrical losses analysis")
            analysis.run()
            
            results_df = analysis.results
            result_dict = results_df.iloc[0].to_dict() if not results_df.empty else {}
            
            capacity_mw = plant_data.metadata.capacity if hasattr(plant_data, 'metadata') else 8.2
            total_loss_pct = float(result_dict.get('total_loss_pct', result_dict.get('electrical_losses', 0)))
            
            return {
                "total_loss_pct": round(total_loss_pct, 2),
                "threshold_pct": loss_threshold_pct,
                "exceeds_threshold": total_loss_pct > loss_threshold_pct,
                "plant_capacity_mw": capacity_mw,
                "analysis_type": "electrical_losses_real",
                "notes": "Real OpenOA electrical losses analysis",
                "raw_columns": list(results_df.columns)
            }
        except ImportError:
            raise ImportError("OpenOA library not found. Install it with: pip install openoa")
        except Exception as e:
            logger.error(f"Electrical losses analysis failed: {e}", exc_info=True)
            raise
    
    def run_wake_losses_analysis(self, bin_width: float = 1.0, **kwargs) -> Dict[str, Any]:
        """Run wake losses analysis (mock or real based on configuration).
        
        Args:
            bin_width: Wind speed bin width in m/s.
            **kwargs: Additional analysis parameters.
            
        Returns:
            dict: Wake losses analysis results.
        """
        if settings.use_mock_data:
            logger.info(f"Running MOCK wake losses analysis")
            return self._run_mock_wake_losses(bin_width)
        else:
            logger.info(f"Running REAL OpenOA wake losses analysis")
            return self._run_real_wake_losses(bin_width, **kwargs)
    
    def _run_mock_wake_losses(self, bin_width: float) -> Dict[str, Any]:
        """Mock wake losses analysis."""
        metadata = self.get_sample_plant_metadata()
        capacity_mw = metadata.get("capacity", 10.5)
        
        # Typical wake losses are 5-15%
        wake_loss_pct = 8.5
        
        return {
            "wake_loss_pct": round(wake_loss_pct, 2),
            "bin_width_ms": bin_width,
            "num_turbines": metadata.get("num_turbines", 4),
            "plant_capacity_mw": capacity_mw,
            "analysis_type": "wake_losses_mock",
            "notes": "Mock analysis for demonstration - USE_MOCK_DATA=True"
        }
    
    def _run_real_wake_losses(self, bin_width: float, **kwargs) -> Dict[str, Any]:
        """Real OpenOA wake losses analysis."""
        try:
            from openoa.analysis import WakeLosses
            
            logger.info("Loading plant data for wake losses analysis")
            plant_data = self._load_real_plant_data()
            
            logger.info("Initializing WakeLosses analysis")
            analysis = WakeLosses(plant=plant_data, **kwargs)
            
            logger.info("Running wake losses analysis")
            analysis.run(bin_width=bin_width)
            
            results_df = analysis.results
            result_dict = results_df.iloc[0].to_dict() if not results_df.empty else {}
            
            capacity_mw = plant_data.metadata.capacity if hasattr(plant_data, 'metadata') else 8.2
            wake_loss_pct = float(result_dict.get('wake_loss_pct', result_dict.get('wake_losses', 0)))
            
            return {
                "wake_loss_pct": round(wake_loss_pct, 2),
                "bin_width_ms": bin_width,
                "plant_capacity_mw": capacity_mw,
                "analysis_type": "wake_losses_real",
                "notes": "Real OpenOA wake losses analysis",
                "raw_columns": list(results_df.columns)
            }
        except ImportError:
            raise ImportError("OpenOA library not found. Install it with: pip install openoa")
        except Exception as e:
            logger.error(f"Wake losses analysis failed: {e}", exc_info=True)
            raise
    
    def run_turbine_ideal_energy_analysis(self, use_lt_distribution: bool = True, **kwargs) -> Dict[str, Any]:
        """Run turbine ideal energy analysis (mock or real based on configuration).
        
        Args:
            use_lt_distribution: Whether to use long-term wind distribution.
            **kwargs: Additional analysis parameters.
            
        Returns:
            dict: Turbine ideal energy analysis results.
        """
        if settings.use_mock_data:
            logger.info(f"Running MOCK turbine ideal energy analysis")
            return self._run_mock_turbine_ideal_energy(use_lt_distribution)
        else:
            logger.info(f"Running REAL OpenOA turbine ideal energy analysis")
            return self._run_real_turbine_ideal_energy(use_lt_distribution, **kwargs)
    
    def _run_mock_turbine_ideal_energy(self, use_lt_distribution: bool) -> Dict[str, Any]:
        """Mock turbine ideal energy analysis."""
        metadata = self.get_sample_plant_metadata()
        capacity_mw = metadata.get("capacity", 10.5)
        
        # Calculate ideal energy based on typical values
        hours_per_year = 8760
        ideal_capacity_factor = 0.45  # Higher than actual since it's \"ideal\"
        ideal_energy_gwh = (capacity_mw * ideal_capacity_factor * hours_per_year) / 1000
        
        return {
            "ideal_energy_gwh": round(ideal_energy_gwh, 2),
            "ideal_capacity_factor_pct": round(ideal_capacity_factor * 100, 1),
            "use_lt_distribution": use_lt_distribution,
            "plant_capacity_mw": capacity_mw,
            "num_turbines": metadata.get("num_turbines", 4),
            "analysis_type": "turbine_ideal_energy_mock",
            "notes": "Mock analysis for demonstration - USE_MOCK_DATA=True"
        }
    
    def _run_real_turbine_ideal_energy(self, use_lt_distribution: bool, **kwargs) -> Dict[str, Any]:
        """Real OpenOA turbine ideal energy analysis."""
        try:
            from openoa.analysis import TurbineLongTermGrossEnergy
            
            logger.info("Loading plant data for turbine ideal energy analysis")
            plant_data = self._load_real_plant_data()
            
            logger.info("Initializing TurbineLongTermGrossEnergy analysis")
            analysis = TurbineLongTermGrossEnergy(plant=plant_data, **kwargs)
            
            logger.info("Running turbine ideal energy analysis")
            analysis.run(use_lt_distribution=use_lt_distribution)
            
            results_df = analysis.results
            result_dict = results_df.iloc[0].to_dict() if not results_df.empty else {}
            
            capacity_mw = plant_data.metadata.capacity if hasattr(plant_data, 'metadata') else 8.2
            ideal_energy_gwh = float(result_dict.get('gross_energy_gwh', result_dict.get('ideal_energy', 0)))
            
            return {
                "ideal_energy_gwh": round(ideal_energy_gwh, 2),
                "use_lt_distribution": use_lt_distribution,
                "plant_capacity_mw": capacity_mw,
                "analysis_type": "turbine_ideal_energy_real",
                "notes": "Real OpenOA turbine ideal energy analysis",
                "raw_columns": list(results_df.columns)
            }
        except ImportError:
            raise ImportError("OpenOA library not found. Install it with: pip install openoa")
        except Exception as e:
            logger.error(f"Turbine ideal energy analysis failed: {e}", exc_info=True)
            raise
    
    def run_eya_gap_analysis(self, expected_aep_gwh: float, **kwargs) -> Dict[str, Any]:
        """Run EYA gap analysis comparing actual vs expected AEP.
        
        Args:
            expected_aep_gwh: Expected AEP from energy yield assessment.
            **kwargs: Additional analysis parameters.
            
        Returns:
            dict: EYA gap analysis results.
        """
        if settings.use_mock_data:
            logger.info(f"Running MOCK EYA gap analysis")
            return self._run_mock_eya_gap_analysis(expected_aep_gwh)
        else:
            logger.info(f"Running REAL OpenOA EYA gap analysis")
            return self._run_real_eya_gap_analysis(expected_aep_gwh, **kwargs)
    
    def _run_mock_eya_gap_analysis(self, expected_aep_gwh: float) -> Dict[str, Any]:
        """Mock EYA gap analysis."""
        metadata = self.get_sample_plant_metadata()
        capacity_mw = metadata.get("capacity", 10.5)
        
        # Get actual AEP from our mock AEP analysis
        aep_result = self._run_mock_aep_analysis(1000)
        actual_aep_gwh = aep_result["aep_gwh"]
        
        gap_gwh = actual_aep_gwh - expected_aep_gwh
        gap_pct = (gap_gwh / expected_aep_gwh) * 100
        
        return {
            "expected_aep_gwh": round(expected_aep_gwh, 2),
            "actual_aep_gwh": round(actual_aep_gwh, 2),
            "gap_gwh": round(gap_gwh, 2),
            "gap_pct": round(gap_pct, 2),
            "meets_expectations": gap_pct >= -5,  # Within 5% is acceptable
            "plant_capacity_mw": capacity_mw,
            "analysis_type": "eya_gap_analysis_mock",
            "notes": "Mock analysis for demonstration - USE_MOCK_DATA=True"
        }
    
    def _run_real_eya_gap_analysis(self, expected_aep_gwh: float, **kwargs) -> Dict[str, Any]:
        """Real OpenOA EYA gap analysis."""
        try:
            # First run AEP analysis to get actual AEP
            aep_result = self._run_real_aep_analysis(1000, **kwargs)
            actual_aep_gwh = aep_result["aep_gwh"]
            
            gap_gwh = actual_aep_gwh - expected_aep_gwh
            gap_pct = (gap_gwh / expected_aep_gwh) * 100
            
            return {
                "expected_aep_gwh": round(expected_aep_gwh, 2),
                "actual_aep_gwh": round(actual_aep_gwh, 2),
                "gap_gwh": round(gap_gwh, 2),
                "gap_pct": round(gap_pct, 2),
                "meets_expectations": gap_pct >= -5,
                "analysis_type": "eya_gap_analysis_real",
                "notes": "Real OpenOA EYA gap analysis"
            }
        except ImportError:
            raise ImportError("OpenOA library not found. Install it with: pip install openoa")
        except Exception as e:
            logger.error(f"EYA gap analysis failed: {e}", exc_info=True)
            raise


# Singleton instance
openoa_service = OpenOAService()
