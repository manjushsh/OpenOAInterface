import { useState } from 'react'
import type { AnalysisResponse } from '../../../types/api'
import { ExportMenu } from '../../shared/ExportMenu'

interface ResultPanelProps {
  analysis: AnalysisResponse | null
  isLoading: boolean
}

export function ResultPanel({ analysis, isLoading }: ResultPanelProps) {
  const [copySuccess, setCopySuccess] = useState(false)

  const handleCopySuccess = () => {
    setCopySuccess(true)
    setTimeout(() => setCopySuccess(false), 2000)
  }

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-6 shadow-sm">
        <div className="h-6 w-40 animate-pulse rounded bg-slate-200 dark:bg-slate-700" />
        <div className="mt-4 grid grid-cols-2 gap-3">
          {[...Array(4)].map((_, index) => (
            <div key={index} className="h-16 animate-pulse rounded-lg bg-slate-100 dark:bg-slate-900/50" />
          ))}
        </div>
      </div>
    )
  }

  if (!analysis) {
    return (
      <div className="rounded-2xl border border-dashed border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-6 text-sm text-slate-600 dark:text-slate-400 shadow-sm">
        <p>No analysis has been run yet. Submit a job to see results.</p>
      </div>
    )
  }

  const { result } = analysis
  const completedAt = analysis.completed_at ?? analysis.created_at
  const completedLabel = completedAt ? new Date(completedAt).toLocaleString() : 'Not available'

  // Dynamically determine which metrics to display based on available data
  const metrics: Array<{ label: string; value: string }> = []
  
  if (result.aep_gwh != null) {
    metrics.push({ label: 'Net AEP', value: `${result.aep_gwh.toFixed(2)} GWh` })
  }
  if (result.ideal_energy_gwh != null) {
    metrics.push({ label: 'Ideal Energy', value: `${result.ideal_energy_gwh.toFixed(2)} GWh` })
  }
  if (result.total_loss_pct != null) {
    metrics.push({ label: 'Electrical Losses', value: `${result.total_loss_pct.toFixed(2)} %` })
  }
  if (result.wake_loss_pct != null) {
    metrics.push({ label: 'Wake Losses', value: `${result.wake_loss_pct.toFixed(2)} %` })
  }
  if (result.gap_pct != null) {
    metrics.push({ label: 'Gap', value: `${result.gap_pct.toFixed(2)} %` })
  }
  if (result.uncertainty_pct != null) {
    metrics.push({ label: 'Uncertainty', value: `${result.uncertainty_pct.toFixed(2)} %` })
  }
  if (result.capacity_factor != null) {
    metrics.push({ label: 'Capacity Factor', value: `${result.capacity_factor.toFixed(1)} %` })
  }
  if (result.plant_capacity_mw != null) {
    metrics.push({ label: 'Plant Capacity', value: `${result.plant_capacity_mw.toFixed(1)} MW` })
  }

  // Get title based on analysis type
  const getTitle = () => {
    const type = result.analysis_type.toLowerCase()
    if (type.includes('aep')) return 'AEP Results'
    if (type.includes('electrical')) return 'Electrical Losses Results'
    if (type.includes('wake')) return 'Wake Losses Results'
    if (type.includes('turbine')) return 'Turbine Ideal Energy Results'
    if (type.includes('eya') || type.includes('gap')) return 'EYA Gap Analysis Results'
    return 'Analysis Results'
  }

  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-6 shadow-sm">
      <div className="flex items-start justify-between gap-2">
        <div>
          <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100">{getTitle()}</h2>
          <p className="text-sm text-slate-600 dark:text-slate-400">{result.analysis_type}</p>
        </div>
        <span className="rounded-full bg-emerald-50 dark:bg-emerald-900/30 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-emerald-700 dark:text-emerald-300">
          {analysis.status}
        </span>
      </div>

      {/* Export menu with copy success notification */}
      <div className="mt-4">
        <ExportMenu analysis={analysis} onCopySuccess={handleCopySuccess} />
        {copySuccess && (
          <p className="mt-2 text-sm text-emerald-600 dark:text-emerald-400">✓ Copied to clipboard!</p>
        )}
      </div>

      {metrics.length > 0 && (
        <dl className="mt-4 grid gap-4 sm:grid-cols-2">
          {metrics.map((metric) => (
            <Metric key={metric.label} label={metric.label} value={metric.value} />
          ))}
        </dl>
      )}

      <div className="mt-4 rounded-lg bg-slate-50 dark:bg-slate-900/50 p-3 text-sm text-slate-700 dark:text-slate-300">
        <p className="font-medium text-slate-800 dark:text-slate-200">Notes</p>
        <p>{result.notes ?? 'Run completed successfully.'}</p>
        {result.iterations != null && (
          <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">Iterations: {result.iterations}</p>
        )}
        <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">Completed: {completedLabel}</p>
      </div>

      {result.raw_columns?.length ? (
        <div className="mt-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">Raw columns</p>
          <div className="mt-2 flex flex-wrap gap-2 text-xs">
            {result.raw_columns.map((item) => (
              <span key={item} className="rounded-full bg-slate-100 dark:bg-slate-700 px-3 py-1 text-slate-700 dark:text-slate-300">
                {item}
              </span>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  )
}

interface MetricProps {
  label: string
  value: string
}

function Metric({ label, value }: MetricProps) {
  return (
    <div className="rounded-lg border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-2 shadow-inner">
      <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">{label}</dt>
      <dd className="text-lg font-semibold text-slate-900 dark:text-slate-100">{value}</dd>
    </div>
  )
}
