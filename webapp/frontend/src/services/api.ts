import type { AnalysisResponse, AnalysisType, HealthResponse } from '../types/api'

const API_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8000'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...init?.headers,
    },
    ...init,
  })

  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || `Request failed with ${response.status}`)
  }

  return response.json() as Promise<T>
}

export async function fetchHealth(): Promise<HealthResponse> {
  return request<HealthResponse>('/health')
}

export async function runAepAnalysis(iterations: number, file_id?: string): Promise<AnalysisResponse> {
  return request<AnalysisResponse>('/api/v1/analysis/aep', {
    method: 'POST',
    body: JSON.stringify({ iterations, file_id }),
  })
}

export async function runAnalysisByType(
  type: AnalysisType,
  params: Record<string, unknown> = {}
): Promise<AnalysisResponse> {
  const endpoints: Record<AnalysisType, string> = {
    aep_monte_carlo: '/api/v1/analysis/aep',
    electrical_losses: '/api/v1/analysis/electrical-losses',
    wake_losses: '/api/v1/analysis/wake-losses',
    turbine_ideal_energy: '/api/v1/analysis/turbine-ideal-energy',
    eya_gap_analysis: '/api/v1/analysis/eya-gap',
  }

  const endpoint = endpoints[type]
  if (!endpoint) {
    throw new Error(`Unknown analysis type: ${type}`)
  }

  return request<AnalysisResponse>(endpoint, {
    method: 'POST',
    body: JSON.stringify(params),
  })
}

export async function uploadPlantData(file: File): Promise<{
  status: string
  message: string
  file_id: string
  filename: string
  file_type: string
  row_count: number
  columns: string[]
  file_size_bytes: number
}> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_URL}/api/v1/upload-plant-data`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || `Upload failed with ${response.status}`)
  }

  return response.json()
}
