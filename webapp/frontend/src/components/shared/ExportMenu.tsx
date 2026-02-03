import { memo } from 'react'
import type { AnalysisResponse } from '../../types/api'
import { exportToCSV, exportToJSON, copyToClipboard } from '../../utils/export'

interface ExportMenuProps {
  analysis: AnalysisResponse | null
  onCopySuccess?: () => void
}

/**
 * Export menu component for downloading analysis results.
 * Supports CSV, JSON, and clipboard copy.
 */
export const ExportMenu = memo(function ExportMenu({
  analysis,
  onCopySuccess,
}: ExportMenuProps) {
  if (!analysis) return null

  const handleCopy = async () => {
    try {
      await copyToClipboard(analysis)
      onCopySuccess?.()
    } catch (error) {
      console.error('Failed to copy to clipboard:', error)
    }
  }

  return (
    <div className="flex flex-wrap gap-2">
      <button
        onClick={() => exportToCSV(analysis)}
        className="inline-flex items-center gap-2 rounded-lg bg-emerald-600 dark:bg-emerald-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-emerald-700 dark:hover:bg-emerald-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 dark:focus:ring-offset-slate-900"
        title="Export as CSV"
      >
        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <span className="hidden sm:inline">Export CSV</span>
        <span className="sm:hidden">CSV</span>
      </button>

      <button
        onClick={() => exportToJSON(analysis)}
        className="inline-flex items-center gap-2 rounded-lg bg-blue-600 dark:bg-blue-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700 dark:hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-slate-900"
        title="Export as JSON"
      >
        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2"
          />
        </svg>
        <span className="hidden sm:inline">Export JSON</span>
        <span className="sm:hidden">JSON</span>
      </button>

      <button
        onClick={handleCopy}
        className="inline-flex items-center gap-2 rounded-lg bg-slate-600 dark:bg-slate-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-slate-700 dark:hover:bg-slate-600 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2 dark:focus:ring-offset-slate-900"
        title="Copy to clipboard"
      >
        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
          />
        </svg>
        <span className="hidden sm:inline">Copy</span>
      </button>
    </div>
  )
})
