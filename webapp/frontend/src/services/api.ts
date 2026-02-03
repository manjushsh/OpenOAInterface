import type { AnalysisResponse, HealthResponse } from '../types/api'

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

export async function runAepAnalysis(iterations: number): Promise<AnalysisResponse> {
  return request<AnalysisResponse>('/api/v1/analysis/aep', {
    method: 'POST',
    body: JSON.stringify({ iterations }),
  })
}
