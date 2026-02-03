export interface HealthResponse {
  status: string
  version: string
  environment?: string
  openoa_version?: string
  timestamp?: string
}

export type AnalysisStatus = 'pending' | 'running' | 'completed' | 'failed'

export interface AnalysisResult {
  aep_gwh: number
  uncertainty_pct: number
  capacity_factor: number
  plant_capacity_mw: number
  analysis_type: string
  iterations: number
  notes?: string
  raw_columns?: string[]
}

export interface AnalysisResponse {
  id: string
  status: AnalysisStatus
  result: AnalysisResult
  created_at?: string
  completed_at?: string
  error: string | null
}
