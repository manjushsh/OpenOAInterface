import { memo } from 'react'
import type { AnalysisResponse } from '../../../types/api'
import { exportComparisonToCSV } from '../../../utils/export'

interface ComparisonViewProps {
  analyses: AnalysisResponse[]
  onClear?: () => void
}

/**
 * Comparison view for multiple analysis results.
 * Displays side-by-side metrics and allows exporting comparison data.
 */
export const ComparisonView = memo(function ComparisonView({
  analyses,
  onClear,
}: ComparisonViewProps) {
  if (analyses.length === 0) {
    return null
  }

  const handleExportComparison = () => {
    exportComparisonToCSV(analyses)
  }

  // Extract common metrics for comparison
  const metrics = [
    { key: 'aep_gwh', label: 'AEP (GWh)', format: (v: number) => v.toFixed(2) },
    { key: 'uncertainty_pct', label: 'Uncertainty (%)', format: (v: number) => v.toFixed(2) },
    { key: 'capacity_factor', label: 'Capacity Factor (%)', format: (v: number) => v.toFixed(1) },
    {
      key: 'plant_capacity_mw',
      label: 'Capacity (MW)',
      format: (v: number) => v.toFixed(1),
    },
  ]

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-xl font-semibold text-slate-900">Analysis Comparison</h2>
          <p className="text-sm text-slate-600">
            Comparing {analyses.length} analysis{analyses.length !== 1 ? 'es' : ''}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={handleExportComparison}
            className="inline-flex items-center gap-2 rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2"
          >
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            Export Comparison
          </button>
          {onClear && (
            <button
              onClick={onClear}
              className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Horizontal scrollable comparison table */}
      <div className="mt-4 overflow-x-auto">
        <table className="w-full min-w-max border-collapse">
          <thead>
            <tr className="border-b-2 border-slate-200">
              <th className="sticky left-0 bg-white px-4 py-3 text-left text-sm font-semibold text-slate-700">
                Metric
              </th>
              {analyses.map((analysis, index) => (
                <th
                  key={index}
                  className="px-4 py-3 text-left text-sm font-semibold text-slate-700"
                >
                  <div className="flex flex-col gap-1">
                    <span className="rounded-full bg-blue-100 px-2 py-0.5 text-xs font-medium text-blue-700">
                      {analysis.result.analysis_type}
                    </span>
                    <span className="text-xs font-normal text-slate-500">
                      {analysis.created_at
                        ? new Date(analysis.created_at).toLocaleTimeString()
                        : 'N/A'}
                    </span>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {metrics.map((metric) => (
              <tr key={metric.key} className="border-b border-slate-100 hover:bg-slate-50">
                <td className="sticky left-0 bg-white px-4 py-3 text-sm font-medium text-slate-700">
                  {metric.label}
                </td>
                {analyses.map((analysis, index) => {
                  const value = analysis.result[metric.key as keyof typeof analysis.result]
                  return (
                    <td key={index} className="px-4 py-3 text-sm text-slate-900">
                      {typeof value === 'number' ? metric.format(value) : '—'}
                    </td>
                  )
                })}
              </tr>
            ))}
            <tr className="border-b border-slate-100 hover:bg-slate-50">
              <td className="sticky left-0 bg-white px-4 py-3 text-sm font-medium text-slate-700">
                Iterations
              </td>
              {analyses.map((analysis, index) => (
                <td key={index} className="px-4 py-3 text-sm text-slate-900">
                  {analysis.result.iterations}
                </td>
              ))}
            </tr>
            <tr className="hover:bg-slate-50">
              <td className="sticky left-0 bg-white px-4 py-3 text-sm font-medium text-slate-700">
                Status
              </td>
              {analyses.map((analysis, index) => (
                <td key={index} className="px-4 py-3">
                  <span className="inline-block rounded-full bg-emerald-50 px-2 py-0.5 text-xs font-semibold uppercase text-emerald-700">
                    {analysis.status}
                  </span>
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>

      {/* Summary stats */}
      <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {metrics.slice(0, 2).map((metric) => {
          const values = analyses
            .map((a) => a.result[metric.key as keyof typeof a.result])
            .filter((v): v is number => typeof v === 'number')
          if (values.length === 0) return null

          const avg = values.reduce((sum, v) => sum + v, 0) / values.length
          const min = Math.min(...values)
          const max = Math.max(...values)
          const range = max - min

          return (
            <div key={metric.key} className="rounded-lg border border-slate-200 bg-slate-50 p-3">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                {metric.label}
              </p>
              <div className="mt-2 space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-600">Average:</span>
                  <span className="font-semibold text-slate-900">{metric.format(avg)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-600">Range:</span>
                  <span className="font-semibold text-slate-900">{metric.format(range)}</span>
                </div>
                <div className="flex justify-between text-xs text-slate-500">
                  <span>Min: {metric.format(min)}</span>
                  <span>Max: {metric.format(max)}</span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
})
