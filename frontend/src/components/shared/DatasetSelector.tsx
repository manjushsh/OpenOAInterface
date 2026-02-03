import { memo } from 'react'

interface Dataset {
  id: string
  name: string
  isDefault: boolean
}

interface DatasetSelectorProps {
  activeDataset: Dataset | null
  onClearDataset: () => void
}

/**
 * Dataset selector component showing active dataset and option to switch back to default.
 */
export const DatasetSelector = memo(function DatasetSelector({
  activeDataset,
  onClearDataset,
}: DatasetSelectorProps) {
  if (!activeDataset) {
    return null
  }

  const isDefault = activeDataset.isDefault
  const borderColor = isDefault ? 'border-slate-200 dark:border-slate-700' : 'border-blue-200 dark:border-blue-700'
  const bgColor = isDefault ? 'bg-slate-50 dark:bg-slate-800' : 'bg-blue-50 dark:bg-blue-900/30'
  const iconColor = isDefault ? 'text-slate-600 dark:text-slate-400' : 'text-blue-600 dark:text-blue-400'
  const titleColor = isDefault ? 'text-slate-900 dark:text-slate-100' : 'text-blue-900 dark:text-blue-100'
  const textColor = isDefault ? 'text-slate-800 dark:text-slate-200' : 'text-blue-800 dark:text-blue-200'
  const subTextColor = isDefault ? 'text-slate-600 dark:text-slate-400' : 'text-blue-700 dark:text-blue-300'

  return (
    <div className={`rounded-lg border-2 ${borderColor} ${bgColor} p-4`}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          <svg
            className={`h-6 w-6 flex-shrink-0 ${iconColor}`}
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <div>
            <h3 className={`font-semibold ${titleColor}`}>
              {isDefault ? 'Using Default Dataset' : 'Using Uploaded Dataset'}
            </h3>
            <p className={`mt-1 text-sm ${textColor}`}>
              Active File: <span className="font-mono font-medium">{activeDataset.name}</span>
            </p>
            <p className={`mt-1 text-xs ${subTextColor}`}>
              All analyses will run on this {isDefault ? 'example' : 'uploaded'} data.
            </p>
          </div>
        </div>
        {!isDefault && (
          <button
            onClick={onClearDataset}
            className="flex-shrink-0 rounded-md bg-blue-100 dark:bg-blue-800 px-3 py-1.5 text-sm font-medium text-blue-900 dark:text-blue-100 transition-colors hover:bg-blue-200 dark:hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-slate-900"
          >
            Use Default
          </button>
        )}
      </div>
    </div>
  )
})
