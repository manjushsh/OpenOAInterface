import { useEffect, useMemo, useState } from 'react'
import { AnalysisForm } from './components/features/analysis/AnalysisForm'
import { ResultPanel } from './components/features/analysis/ResultPanel'
import { StatCard } from './components/features/analysis/StatCard'
import { Header } from './components/layout/Header'
import { PageShell } from './components/layout/PageShell'
import { fetchHealth, runAepAnalysis } from './services/api'
import type { AnalysisResponse, HealthResponse } from './types/api'

const DEFAULT_ITERATIONS = 1000

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    void loadHealth()
    void runAnalysis(DEFAULT_ITERATIONS)
  }, [])

  const stats = useMemo(
    () => [
      {
        label: 'API Status',
        value: health?.status ?? '—',
        hint: health?.timestamp ? new Date(health.timestamp).toLocaleString() : 'Waiting for API',
      },
      {
        label: 'OpenOA Version',
        value: health?.openoa_version ?? '—',
        hint: 'Real mode enabled by default',
      },
      {
        label: 'Last Run',
        value: analysis?.result.iterations ? `${analysis.result.iterations} iters` : '—',
        hint: analysis?.result.analysis_type ?? 'Not started',
      },
    ],
    [health, analysis]
  )

  async function loadHealth() {
    try {
      const response = await fetchHealth()
      setHealth(response)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to reach API')
    }
  }

  async function runAnalysis(iterations: number) {
    setIsLoading(true)
    setError(null)
    try {
      const response = await runAepAnalysis(iterations)
      setAnalysis(response)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <PageShell>
      <Header
        title="OpenOA Demo Dashboard"
        subtitle="Run AEP simulations and inspect OpenOA health in real time."
        badge={health?.environment ?? 'development'}
      />

      <section className="grid gap-4 md:grid-cols-3">
        {stats.map((item) => (
          <StatCard key={item.label} label={item.label} value={item.value} hint={item.hint} />
        ))}
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <AnalysisForm
          defaultIterations={DEFAULT_ITERATIONS}
          onSubmit={runAnalysis}
          isLoading={isLoading}
          apiUrlHint={import.meta.env.VITE_API_URL ?? 'http://localhost:8000'}
          error={error}
        />
        <ResultPanel analysis={analysis} isLoading={isLoading} />
      </section>
    </PageShell>
  )
}

export default App
