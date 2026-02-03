import type { ChangeEvent, SyntheticEvent } from 'react'
import { useState } from 'react'

interface AnalysisFormProps {
  defaultIterations: number
  onSubmit: (iterations: number) => Promise<void>
  isLoading: boolean
  apiUrlHint: string
  error: string | null
}

export function AnalysisForm({ defaultIterations, onSubmit, isLoading, apiUrlHint, error }: AnalysisFormProps) {
  const [iterations, setIterations] = useState(defaultIterations)

  async function handleSubmit(event: SyntheticEvent<HTMLFormElement>) {
    event.preventDefault()
    const safeIterations = Math.min(Math.max(iterations, 50), 5000)
    await onSubmit(safeIterations)
  }

  return (
    <form
      className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
      onSubmit={handleSubmit}
    >
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-slate-900">Run Monte Carlo AEP</h2>
          <p className="text-sm text-slate-600">Send a job to the FastAPI backend and OpenOA.</p>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">{apiUrlHint}</span>
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <label className="flex flex-col gap-2">
          <span className="text-sm font-medium text-slate-800">Iterations</span>
          <input
            type="number"
            min={50}
            max={5000}
            value={iterations}
            onChange={(event: ChangeEvent<HTMLInputElement>) => setIterations(Number(event.target.value))}
            className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900 shadow-inner focus:border-slate-400 focus:outline-none"
          />
          <span className="text-xs text-slate-500">Range: 50 - 5000</span>
        </label>

        <div className="flex flex-col gap-2 rounded-lg bg-slate-50 p-3 text-sm text-slate-700">
          <span className="font-semibold text-slate-800">Mode</span>
          <p>Backend is currently running in real OpenOA mode (USE_MOCK_DATA=false).</p>
          <p className="text-xs text-slate-500">Toggle is controlled server-side for safety.</p>
        </div>
      </div>

      {error ? <p className="mt-3 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}

      <div className="mt-6 flex items-center gap-3">
        <button
          type="submit"
          className="inline-flex items-center justify-center rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow hover:bg-slate-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-slate-900 disabled:cursor-not-allowed disabled:opacity-70"
          disabled={isLoading}
        >
          {isLoading ? 'Running…' : 'Run Analysis'}
        </button>
        <span className="text-xs text-slate-500">Typical runtime: 10-30 seconds in real mode.</span>
      </div>
    </form>
  )
}
