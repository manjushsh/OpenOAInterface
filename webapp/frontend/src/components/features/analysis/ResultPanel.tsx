import type { AnalysisResponse } from '../../../types/api'

interface ResultPanelProps {
  analysis: AnalysisResponse | null
  isLoading: boolean
}

export function ResultPanel({ analysis, isLoading }: ResultPanelProps) {
  if (isLoading) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="h-6 w-40 animate-pulse rounded bg-slate-200" />
        <div className="mt-4 grid grid-cols-2 gap-3">
          {[...Array(4)].map((_, index) => (
            <div key={index} className="h-16 animate-pulse rounded-lg bg-slate-100" />
          ))}
        </div>
      </div>
    )
  }

  if (!analysis) {
    return (
      <div className="rounded-2xl border border-dashed border-slate-200 bg-white p-6 text-sm text-slate-600 shadow-sm">
        <p>No analysis has been run yet. Submit a job to see results.</p>
      </div>
    )
  }

  const { result } = analysis
  const completedAt = analysis.completed_at ?? analysis.created_at
  const completedLabel = completedAt ? new Date(completedAt).toLocaleString() : 'Not available'

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-start justify-between gap-2">
        <div>
          <h2 className="text-xl font-semibold text-slate-900">AEP Results</h2>
          <p className="text-sm text-slate-600">{result.analysis_type}</p>
        </div>
        <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-emerald-700">
          {analysis.status}
        </span>
      </div>

      <dl className="mt-4 grid gap-4 sm:grid-cols-2">
        <Metric label="Net AEP" value={`${result.aep_gwh.toFixed(2)} GWh`} />
        <Metric label="Uncertainty" value={`${result.uncertainty_pct.toFixed(2)} %`} />
        <Metric label="Capacity Factor" value={`${result.capacity_factor.toFixed(1)} %`} />
        <Metric label="Plant Capacity" value={`${result.plant_capacity_mw.toFixed(1)} MW`} />
      </dl>

      <div className="mt-4 rounded-lg bg-slate-50 p-3 text-sm text-slate-700">
        <p className="font-medium text-slate-800">Notes</p>
        <p>{result.notes ?? 'Run completed successfully.'}</p>
        <p className="mt-1 text-xs text-slate-500">Iterations: {result.iterations}</p>
        <p className="mt-1 text-xs text-slate-500">Completed: {completedLabel}</p>
      </div>

      {result.raw_columns?.length ? (
        <div className="mt-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Raw columns</p>
          <div className="mt-2 flex flex-wrap gap-2 text-xs">
            {result.raw_columns.map((item) => (
              <span key={item} className="rounded-full bg-slate-100 px-3 py-1 text-slate-700">
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
    <div className="rounded-lg border border-slate-100 bg-white px-3 py-2 shadow-inner">
      <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500">{label}</dt>
      <dd className="text-lg font-semibold text-slate-900">{value}</dd>
    </div>
  )
}
