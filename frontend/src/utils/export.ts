import type { AnalysisResponse } from '../types/api'

/**
 * Export analysis results to CSV format.
 */
export function exportToCSV(analysis: AnalysisResponse): void {
  const { result } = analysis
  
  // Create CSV header
  const headers = ['Metric', 'Value', 'Unit']
  
  // Create CSV rows
  const rows: string[][] = []
  
  // Add available metrics
  if (result.aep_gwh != null) rows.push(['AEP', result.aep_gwh.toString(), 'GWh'])
  if (result.uncertainty_pct != null) rows.push(['Uncertainty', result.uncertainty_pct.toString(), '%'])
  if (result.capacity_factor != null) rows.push(['Capacity Factor', result.capacity_factor.toString(), '%'])
  if (result.plant_capacity_mw != null) rows.push(['Plant Capacity', result.plant_capacity_mw.toString(), 'MW'])
  if (result.iterations != null) rows.push(['Iterations', result.iterations.toString(), 'count'])
  rows.push(['Analysis Type', result.analysis_type, ''])
  
  // Add metadata
  rows.push(['', '', ''])
  rows.push(['Analysis ID', analysis.id, ''])
  rows.push(['Status', analysis.status, ''])
  if (analysis.created_at) {
    rows.push(['Created At', new Date(analysis.created_at).toISOString(), ''])
  }
  if (analysis.completed_at) {
    rows.push(['Completed At', new Date(analysis.completed_at).toISOString(), ''])
  }
  if (result.notes) {
    rows.push(['Notes', result.notes, ''])
  }
  
  // Convert to CSV string
  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n')
  
  // Download file
  downloadFile(csvContent, `analysis_${analysis.id}.csv`, 'text/csv')
}

/**
 * Export analysis results to JSON format.
 */
export function exportToJSON(analysis: AnalysisResponse): void {
  const jsonContent = JSON.stringify(analysis, null, 2)
  downloadFile(jsonContent, `analysis_${analysis.id}.json`, 'application/json')
}

/**
 * Helper function to trigger file download.
 */
function downloadFile(content: string, filename: string, mimeType: string): void {
  const blob = new Blob([content], { type: mimeType })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  
  link.href = url
  link.download = filename
  link.style.display = 'none'
  
  document.body.appendChild(link)
  link.click()
  
  // Cleanup
  setTimeout(() => {
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }, 100)
}

/**
 * Copy analysis results to clipboard as JSON.
 */
export async function copyToClipboard(analysis: AnalysisResponse): Promise<void> {
  const jsonContent = JSON.stringify(analysis, null, 2)
  await navigator.clipboard.writeText(jsonContent)
}

/**
 * Export multiple analyses for comparison.
 */
export function exportComparisonToCSV(analyses: AnalysisResponse[]): void {
  if (analyses.length === 0) return
  
  // Create comparison CSV
  const headers = ['Analysis ID', 'Type', 'AEP (GWh)', 'Uncertainty (%)', 'Capacity Factor (%)', 'Iterations', 'Status', 'Created At']
  
  const rows = analyses.map(analysis => [
    analysis.id,
    analysis.result.analysis_type,
    (analysis.result.aep_gwh ?? 0).toString(),
    (analysis.result.uncertainty_pct ?? 0).toString(),
    (analysis.result.capacity_factor ?? 0).toString(),
    (analysis.result.iterations ?? 0).toString(),
    analysis.status,
    analysis.created_at ? new Date(analysis.created_at).toISOString() : '',
  ])
  
  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n')
  
  const timestamp = new Date().toISOString().split('T')[0]
  downloadFile(csvContent, `analysis_comparison_${timestamp}.csv`, 'text/csv')
}
