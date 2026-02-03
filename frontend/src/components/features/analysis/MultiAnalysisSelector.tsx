import { useState, memo } from 'react'
import type { AnalysisType } from '../../../types/api'

interface MultiAnalysisSelectorProps {
  onRunMultiple: (types: AnalysisType[]) => void
  isLoading: boolean
}

const ANALYSIS_OPTIONS: {
  value: AnalysisType
  label: string
  description: string
  disabled?: boolean
  disabledReason?: string
}[] = [
  {
    value: 'aep_monte_carlo',
    label: 'AEP (Monte Carlo)',
    description: 'Annual Energy Production with uncertainty analysis',
  },
  {
    value: 'electrical_losses',
    label: 'Electrical Losses',
    description: 'Transmission and electrical system losses',
  },
  {
    value: 'wake_losses',
    label: 'Wake Losses',
    description: 'Turbine wake interaction effects',
    disabled: true,
    disabledReason: 'Long-running analysis - use single analysis mode',
  },
  {
    value: 'turbine_ideal_energy',
    label: 'Turbine Ideal Energy',
    description: 'Theoretical maximum energy production',
    disabled: true,
    disabledReason: 'Long-running analysis - use single analysis mode',
  },
  {
    value: 'eya_gap_analysis',
    label: 'EYA Gap Analysis',
    description: 'Compare actual vs expected yield assessment',
  },
]

/**
 * Multi-analysis selector component.
 * Allows users to select and run multiple analysis types simultaneously.
 */
export const MultiAnalysisSelector = memo(function MultiAnalysisSelector({
  onRunMultiple,
  isLoading,
}: MultiAnalysisSelectorProps) {
  const [selectedTypes, setSelectedTypes] = useState<Set<AnalysisType>>(new Set())

  const toggleSelection = (type: AnalysisType) => {
    const option = ANALYSIS_OPTIONS.find((opt) => opt.value === type)
    if (option?.disabled) return // Don't allow selection of disabled options

    const newSelection = new Set(selectedTypes)
    if (newSelection.has(type)) {
      newSelection.delete(type)
    } else {
      newSelection.add(type)
    }
    setSelectedTypes(newSelection)
  }

  const selectAll = () => {
    // Only select non-disabled options
    const enabledOptions = ANALYSIS_OPTIONS.filter((opt) => !opt.disabled).map((opt) => opt.value)
    setSelectedTypes(new Set(enabledOptions))
  }

  const clearAll = () => {
    setSelectedTypes(new Set())
  }

  const handleRunMultiple = () => {
    if (selectedTypes.size > 0) {
      onRunMultiple(Array.from(selectedTypes))
    }
  }

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-xl font-semibold text-slate-900">Multi-Analysis</h2>
          <p className="text-sm text-slate-600">
            Run multiple analyses at once for comprehensive insights
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={selectAll}
            className="text-sm text-blue-600 hover:text-blue-700 focus:outline-none"
            disabled={isLoading}
          >
            Select All
          </button>
          <span className="text-slate-300">|</span>
          <button
            onClick={clearAll}
            className="text-sm text-slate-600 hover:text-slate-700 focus:outline-none"
            disabled={isLoading}
          >
            Clear All
          </button>
        </div>
      </div>

      {/* Warning about disabled analyses */}
      <div className="mt-4 rounded-lg bg-amber-50 border border-amber-200 p-3">
        <div className="flex items-start gap-2">
          <svg
            className="h-5 w-5 flex-shrink-0 text-amber-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
          <div className="text-sm">
            <p className="font-medium text-amber-800">Note about long-running analyses</p>
            <p className="mt-1 text-amber-700">
              Some analyses (Wake Losses, Turbine Ideal Energy) process large datasets and can take
              several minutes. They are disabled in multi-analysis mode to prevent page timeouts.
              Run them individually from the main analysis form instead.
            </p>
          </div>
        </div>
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {ANALYSIS_OPTIONS.map((option) => {
          const isSelected = selectedTypes.has(option.value)
          const isDisabled = option.disabled || isLoading
          return (
            <label
              key={option.value}
              className={`rounded-lg border-2 p-3 transition-all ${
                isDisabled
                  ? 'cursor-not-allowed border-slate-200 bg-slate-50 opacity-60'
                  : isSelected
                    ? 'cursor-pointer border-blue-500 bg-blue-50 shadow-sm'
                    : 'cursor-pointer border-slate-200 bg-white hover:border-slate-300'
              } ${isLoading && !option.disabled ? 'pointer-events-none' : ''}`}
            >
              <div className="flex items-start gap-3">
                <input
                  type="checkbox"
                  checked={isSelected}
                  onChange={() => toggleSelection(option.value)}
                  className="mt-1 h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-2 focus:ring-blue-500 disabled:cursor-not-allowed"
                  disabled={isDisabled}
                />
                <div className="flex-1">
                  <div className="font-medium text-slate-900">
                    {option.label}
                    {option.disabled && (
                      <span className="ml-2 text-xs font-normal text-amber-600">
                        (Disabled)
                      </span>
                    )}
                  </div>
                  <div className="mt-1 text-xs text-slate-600">
                    {option.disabled ? option.disabledReason : option.description}
                  </div>
                </div>
              </div>
            </label>
          )
        })}
      </div>

      <div className="mt-4 flex items-center justify-between gap-4">
        <p className="text-sm text-slate-600">
          <span className="font-semibold text-slate-900">{selectedTypes.size}</span> analysis
          {selectedTypes.size !== 1 ? 'es' : ''} selected
        </p>
        <button
          onClick={handleRunMultiple}
          disabled={isLoading || selectedTypes.size === 0}
          className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-6 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isLoading ? (
            <>
              <svg className="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Running...
            </>
          ) : (
            <>
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
              Run Selected Analyses
            </>
          )}
        </button>
      </div>
    </div>
  )
})
