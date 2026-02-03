export interface HealthResponse {
  status: string
  version: string
  environment?: string
  openoa_version?: string
  timestamp?: string
}

export type AnalysisStatus = 'pending' | 'running' | 'completed' | 'failed'

export type AnalysisType =
  | 'aep_monte_carlo'
  | 'electrical_losses'
  | 'wake_losses'
  | 'turbine_ideal_energy'
  | 'eya_gap_analysis'

export interface AnalysisResult {
  analysis_type: string
  notes?: string
  raw_columns?: string[]
  
  // AEP Monte Carlo results
  aep_gwh?: number
  uncertainty_pct?: number
  capacity_factor?: number
  plant_capacity_mw?: number
  iterations?: number
  
  // Electrical Losses results
  total_loss_pct?: number
  
  // Wake Losses results
  wake_loss_pct?: number
  
  // Turbine Ideal Energy results
  ideal_energy_gwh?: number
  
  // EYA Gap Analysis results
  gap_pct?: number
}

export interface AnalysisResponse {
  id: string
  status: AnalysisStatus
  result: AnalysisResult
  created_at?: string
  completed_at?: string
  error: string | null
}
