import { useMemo } from 'react'
import type { AnalysisResponse } from '../../../types/api'
import { transformAnalysisToChartData } from '../../../utils/chartData'
import { EnergyBreakdownPieChart } from '../../shared/EnergyBreakdownPieChart'
import { MetricsBarChart } from '../../shared/MetricsBarChart'
import { UncertaintyLineChart } from '../../shared/UncertaintyLineChart'

interface AnalysisVisualizationProps {
  analysis: AnalysisResponse | null
  isLoading: boolean
}

/**
 * Comprehensive visualization panel showing analysis results with charts.
 * Displays metrics bar chart, uncertainty line chart, and energy breakdown pie chart.
 */
export function AnalysisVisualization({
  analysis,
  isLoading,
}: AnalysisVisualizationProps) {
  const chartData = useMemo(() => {
    if (!analysis?.result) return null
    return transformAnalysisToChartData(analysis.result)
  }, [analysis])

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="h-80 animate-pulse rounded-xl bg-slate-200 dark:bg-slate-700" />
        <div className="grid gap-6 lg:grid-cols-2">
          <div className="h-80 animate-pulse rounded-xl bg-slate-200 dark:bg-slate-700" />
          <div className="h-80 animate-pulse rounded-xl bg-slate-200 dark:bg-slate-700" />
        </div>
      </div>
    )
  }

  if (!chartData) {
    return (
      <div className="rounded-2xl border border-dashed border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-12 text-center shadow-sm">
        <svg
          className="mx-auto h-12 w-12 text-slate-300 dark:text-slate-600"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
          />
        </svg>
        <h3 className="mt-4 text-sm font-medium text-slate-900 dark:text-slate-100">No Data Available</h3>
        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
          Run an analysis to see visualizations of the results.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Metrics Overview Bar Chart */}
      <MetricsBarChart data={chartData.metrics} title="Key Analysis Metrics" />

      {/* Uncertainty and Breakdown Charts */}
      <div className="grid gap-6 lg:grid-cols-2">
        {chartData.uncertaintyRange && (
          <UncertaintyLineChart
            data={chartData.uncertaintyRange}
            title="Uncertainty Range Over Iterations"
          />
        )}

        {chartData.breakdown && (
          <EnergyBreakdownPieChart data={chartData.breakdown} title="Capacity Utilization" />
        )}
      </div>

      {/* Analysis Metadata */}
      {analysis && (
        <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Analysis Details</h3>
          <dl className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <div>
              <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Analysis ID
              </dt>
              <dd className="mt-1 font-mono text-sm text-slate-700 dark:text-slate-300">{analysis.id}</dd>
            </div>
            <div>
              <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Status
              </dt>
              <dd className="mt-1">
                <span className="inline-flex items-center rounded-full bg-emerald-50 dark:bg-emerald-900/30 px-2.5 py-0.5 text-xs font-semibold text-emerald-700 dark:text-emerald-300">
                  {analysis.status}
                </span>
              </dd>
            </div>
            {analysis.result.iterations != null && (
              <div>
                <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                  Iterations
                </dt>
                <dd className="mt-1 text-sm text-slate-700 dark:text-slate-300">
                  {analysis.result.iterations.toLocaleString()}
                </dd>
              </div>
            )}
            <div>
              <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Type
              </dt>
              <dd className="mt-1 text-sm text-slate-700 dark:text-slate-300">{analysis.result.analysis_type}</dd>
            </div>
          </dl>

          {analysis.result.notes && (
            <div className="mt-4 rounded-lg bg-slate-50 dark:bg-slate-900/50 p-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Notes
              </p>
              <p className="mt-1 text-sm text-slate-700 dark:text-slate-300">{analysis.result.notes}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
