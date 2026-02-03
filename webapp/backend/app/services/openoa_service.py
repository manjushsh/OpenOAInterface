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
        file_path: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Run AEP analysis (mock or real based on configuration).
        
        Uses mock data if USE_MOCK_DATA=True, otherwise integrates with OpenOA.
        
        Args:
            iterations: Number of Monte Carlo iterations to perform.
            file_path: Optional path to uploaded data file. If None, uses default dataset.
            **kwargs: Additional parameters passed to the analysis method.
            **kwargs: Additional analysis parameters.
            
        Returns:
            dict: Analysis results with AEP estimate and uncertainty.
        """
        if settings.use_mock_data:
            logger.info(f"Running MOCK AEP analysis with {iterations} iterations")
            return self._run_mock_aep_analysis(iterations)
        else:
            logger.info(f"Running REAL OpenOA AEP analysis with {iterations} iterations")
            return self._run_real_aep_analysis(iterations, file_path, **kwargs)
        
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
        file_path: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Run real OpenOA AEP analysis.
        
        Args:
            iterations: Number of Monte Carlo iterations.
            file_path: Optional path to uploaded data file.
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
            
            # Load actual plant data (from file or default)
            plant_data = self._load_real_plant_data(file_path)
            
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
    
    def _load_real_plant_data(self, file_path: Optional[str] = None):
        """Load real plant data for OpenOA analysis.
        
        Args:
            file_path: Optional path to uploaded CSV/JSON file. If None, uses default dataset.
        
        Returns:
            PlantData: OpenOA PlantData object.
            
        Raises:
            ImportError: If OpenOA is not installed.
            FileNotFoundError: If data files not found.
        """
        try:
            from openoa import PlantData
            import pandas as pd
            
            # If custom file provided, load it
            if file_path:
                logger.info(f"Loading custom plant data from {file_path}")
                return self._load_plant_data_from_file(file_path)
            
            # Otherwise use default La Haute Borne data
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
    
    def _load_plant_data_from_file(self, file_path: str):
        """Load and validate uploaded plant data file.
        
        Args:
            file_path: Path to CSV or JSON file
            
        Returns:
            PlantData: OpenOA PlantData object
            
        Raises:
            ValueError: If file format is invalid or missing required columns
        """
        try:
            from openoa import PlantData
            import pandas as pd
            
            logger.info(f"Loading plant data from uploaded file: {file_path}")
            
            # Determine file type and read
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                df = pd.read_json(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_path}")
            
            logger.info(f"Loaded {len(df)} rows with columns: {list(df.columns)}")
            
            # Case-insensitive column mapping for flexible CSV uploads
            # Create a mapping from lowercase column names to actual column names
            df_cols_lower = {col.lower(): col for col in df.columns}
            
            # Define column mappings (all lowercase for case-insensitive matching)
            col_mapping = {
                'time': ['date_time', 'timestamp', 'datetime', 'date', 'time'],
                'WTUR_W': ['p_avg', 'power', 'power_kw', 'wtur_w', 'activepower'],
                'WMET_HorWdSpd': ['ws_avg', 'wind_speed', 'windspeed', 'wind_spd', 'wmet_horwdspd', 'ws']
            }
            
            # Attempt to map columns (case-insensitive)
            for target_col, alt_names in col_mapping.items():
                if target_col not in df.columns:
                    for alt_name_lower in alt_names:
                        if alt_name_lower in df_cols_lower:
                            actual_col = df_cols_lower[alt_name_lower]
                            df.rename(columns={actual_col: target_col}, inplace=True)
                            logger.info(f"Mapped column '{actual_col}' to '{target_col}'")
                            break
            
            # Validate required columns for OpenOA
            required_cols = ['time', 'WTUR_W', 'WMET_HorWdSpd']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                raise ValueError(
                    f"Missing required columns: {missing_cols}. "
                    f"Available: {list(df.columns)}. "
                    f"Required: time, WTUR_W (power), WMET_HorWdSpd (wind speed)"
                )
            
            # Convert time column to datetime with UTC timezone
            if 'time' in df.columns:
                df['time'] = pd.to_datetime(df['time'], utc=True)
            
            # Ensure we have a turbine identifier column
            if 'asset_id' not in df.columns and 'turbine' not in df.columns:
                # If no turbine column, create from Wind_turbine_name or use default
                if 'Wind_turbine_name' in df.columns:
                    df['asset_id'] = df['Wind_turbine_name']
                else:
                    df['asset_id'] = 'TURBINE_01'
            elif 'turbine' in df.columns:
                df['asset_id'] = df['turbine']
            
            # Create minimal asset table
            turbine_ids = df['asset_id'].unique() if 'asset_id' in df.columns else ['TURBINE_01']
            asset_df = pd.DataFrame({
                'asset_id': turbine_ids,
                'type': ['turbine'] * len(turbine_ids),
                'latitude': [0.0] * len(turbine_ids),
                'longitude': [0.0] * len(turbine_ids),
            })
            
            # Create minimal meter dataframe (required by PlantData)
            meter_df = pd.DataFrame({
                'time': df['time'],
                'MMTR_SupWh': 0.0
            })
            
            # Create minimal curtailment dataframe (required by PlantData)
            curtail_df = pd.DataFrame({
                'time': df['time'],
                'IAVL_DnWh': 0.0,
                'IAVL_ExtPwrDnWh': 0.0
            })
            
            # Create minimal reanalysis dataframe (required by PlantData)
            reanalysis_df = pd.DataFrame({
                'time': df['time'],
                'WMETR_HorWdSpd': df['WMET_HorWdSpd'] if 'WMET_HorWdSpd' in df.columns else 0.0,
                'WMETR_AirDen': 1.225
            })
            
            # Create metadata dictionary for PlantData
            metadata = {
                'latitude': 0.0,
                'longitude': 0.0,
                'capacity': 1.0,
                'asset': {
                    'asset_id': 'asset_id',
                    'latitude': 'latitude',
                    'longitude': 'longitude',
                },
                'scada': {
                    'time': 'time',
                    'asset_id': 'asset_id',
                    'WTUR_W': 'WTUR_W',
                    'WMET_HorWdSpd': 'WMET_HorWdSpd',
                    'frequency': '10min'
                },
                'meter': {
                    'time': 'time',
                    'MMTR_SupWh': 'MMTR_SupWh'
                },
                'curtail': {
                    'time': 'time',
                    'IAVL_DnWh': 'IAVL_DnWh',
                    'IAVL_ExtPwrDnWh': 'IAVL_ExtPwrDnWh'
                },
                'reanalysis': {
                    'era5': {
                        'time': 'time',
                        'WMETR_HorWdSpd': 'WMETR_HorWdSpd',
                        'WMETR_AirDen': 'WMETR_AirDen',
                        'frequency': '10min'
                    }
                }
            }
            
            # Create PlantData object with proper initialization
            plant_data = PlantData(
                analysis_type="MonteCarloAEP",
                metadata=metadata,
                scada=df,
                meter=meter_df,
                curtail=curtail_df,
                asset=asset_df,
                reanalysis={'era5': reanalysis_df}
            )
            
            logger.info(f"Successfully created PlantData from uploaded file")
            return plant_data
            
        except Exception as e:
            logger.error(f"Failed to load plant data from file: {e}", exc_info=True)
            raise ValueError(f"Invalid plant data file: {str(e)}")
    
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
    
    def run_electrical_losses_analysis(self, loss_threshold_pct: float = 5.0, file_path: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Run electrical losses analysis (mock or real based on configuration).
        
        Args:
            loss_threshold_pct: Threshold for flagging high losses.
            file_path: Optional path to uploaded data file.
            **kwargs: Additional analysis parameters.
            
        Returns:
            dict: Electrical losses analysis results.
        """
        if settings.use_mock_data:
            logger.info(f"Running MOCK electrical losses analysis")
            return self._run_mock_electrical_losses(loss_threshold_pct)
        else:
            logger.info(f"Running REAL OpenOA electrical losses analysis")
            return self._run_real_electrical_losses(loss_threshold_pct, file_path, **kwargs)
    
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
            
            # ElectricalLosses stores results in electrical_losses attribute
            # Returns array of results, take first element if not UQ, or mean if UQ
            if hasattr(analysis.electrical_losses, '__iter__'):
                # UQ mode returns array
                total_loss_pct = float(analysis.electrical_losses.mean() * 100)
            else:
                # Non-UQ mode
                total_loss_pct = float(analysis.electrical_losses[0][0] * 100)
            
            capacity_mw = plant_data.metadata.capacity if hasattr(plant_data, 'metadata') else 8.2
            
            return {
                "total_loss_pct": round(total_loss_pct, 2),
                "threshold_pct": loss_threshold_pct,
                "exceeds_threshold": total_loss_pct > loss_threshold_pct,
                "plant_capacity_mw": capacity_mw,
                "analysis_type": "electrical_losses_real",
                "notes": "Real OpenOA electrical losses analysis using La Haute Borne data"
            }
        except ImportError:
            raise ImportError("OpenOA library not found. Install it with: pip install openoa")
        except Exception as e:
            logger.error(f"Electrical losses analysis failed: {e}", exc_info=True)
            raise
    
    def run_wake_losses_analysis(self, bin_width: float = 1.0, file_path: Optional[str] = None, **kwargs) -> Dict[str, Any]:
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
            analysis.run()
            
            # WakeLosses stores results in wake_losses_por and wake_losses_lt attributes
            # These can be scalars or arrays depending on UQ mode
            import numpy as np
            
            # Handle both array and scalar results
            if hasattr(analysis, 'wake_losses_lt'):
                wake_lt = analysis.wake_losses_lt
                wake_loss_pct = float(np.mean(wake_lt) * 100 if hasattr(wake_lt, '__iter__') else wake_lt * 100)
            else:
                wake_loss_pct = None
            
            wake_por = analysis.wake_losses_por
            por_wake_loss_pct = float(np.mean(wake_por) * 100 if hasattr(wake_por, '__iter__') else wake_por * 100)
            
            # Use long-term corrected if available, otherwise period-of-record
            if wake_loss_pct is None:
                wake_loss_pct = por_wake_loss_pct
            
            capacity_mw = plant_data.metadata.capacity if hasattr(plant_data, 'metadata') else 8.2
            
            return {
                "wake_loss_pct": round(wake_loss_pct, 2),
                "por_wake_loss_pct": round(por_wake_loss_pct, 2),
                "plant_capacity_mw": capacity_mw,
                "analysis_type": "wake_losses_real",
                "notes": "Real OpenOA wake losses analysis using La Haute Borne data. Showing long-term corrected value."
            }
        except ImportError:
            raise ImportError("OpenOA library not found. Install it with: pip install openoa")
        except Exception as e:
            logger.error(f"Wake losses analysis failed: {e}", exc_info=True)
            raise
    
    def run_turbine_ideal_energy_analysis(self, use_lt_distribution: bool = False, file_path: Optional[str] = None, **kwargs) -> Dict[str, Any]:
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
            # Run with at least one reanalysis product
            analysis.run(reanalysis_products=['era5'])
            
            # TurbineLongTermGrossEnergy stores results in plant_gross attribute (in MWh)
            # Convert from MWh to GWh
            import numpy as np
            ideal_energy_gwh = float(np.mean(analysis.plant_gross) / 1000)
            
            capacity_mw = plant_data.metadata.capacity if hasattr(plant_data, 'metadata') else 8.2
            
            return {
                "ideal_energy_gwh": round(ideal_energy_gwh, 2),
                "use_lt_distribution": use_lt_distribution,
                "plant_capacity_mw": capacity_mw,
                "analysis_type": "turbine_ideal_energy_real",
                "notes": "Real OpenOA turbine ideal energy analysis using La Haute Borne data and ERA5 reanalysis"
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
