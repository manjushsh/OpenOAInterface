import { useEffect, useMemo, useState } from 'react'
import { AnalysisForm } from './components/features/analysis/AnalysisForm'
import { AnalysisVisualization } from './components/features/analysis/AnalysisVisualization'
import { ComparisonView } from './components/features/analysis/ComparisonView'
// import { MultiAnalysisSelector } from './components/features/analysis/MultiAnalysisSelector'
import { ResultPanel } from './components/features/analysis/ResultPanel'
import { DatasetSelector } from './components/shared/DatasetSelector'
import { FileUpload } from './components/shared/FileUpload'
import { StatCard } from './components/shared/StatCard'
import { Header } from './components/layout/Header'
import { PageShell } from './components/layout/PageShell'
import { fetchHealth, runAepAnalysis, uploadPlantData } from './services/api'
import type { AnalysisResponse, HealthResponse } from './types/api'

const DEFAULT_ITERATIONS = 1000

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null)
  const [comparisonAnalyses, setComparisonAnalyses] = useState<AnalysisResponse[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [uploadSuccess, setUploadSuccess] = useState<string | null>(null)
  const [activeDataset, setActiveDataset] = useState<{
    id: string
    name: string
    isDefault: boolean
  } | null>({ id: 'default', name: 'la-haute-borne-data-2014-2015.csv', isDefault: true })

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
      const file_id = activeDataset?.isDefault ? undefined : activeDataset?.id
      const response = await runAepAnalysis(iterations, file_id)
      setAnalysis(response)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed')
    } finally {
      setIsLoading(false)
    }
  }

  // async function runMultipleAnalyses(types: AnalysisType[]) {
  //   setIsLoading(true)
  //   setError(null)
  //   const results: AnalysisResponse[] = []

  //   try {
  //     // Run each analysis type sequentially with appropriate default parameters
  //     for (const type of types) {
  //       let params: Record<string, unknown> = {}
        
  //       switch (type) {
  //         case 'aep_monte_carlo':
  //           params = { iterations: DEFAULT_ITERATIONS }
  //           break
  //         case 'electrical_losses':
  //           params = { loss_threshold_pct: 5.0 }
  //           break
  //         case 'wake_losses':
  //           params = { bin_width: 1.0 }
  //           break
  //         case 'turbine_ideal_energy':
  //           params = { use_lt_distribution: false }
  //           break
  //         case 'eya_gap_analysis':
  //           params = { expected_aep_gwh: 25.0 } // Default expected AEP
  //           break
  //       }
        
  //       const response = await runAnalysisByType(type, params)
  //       results.push(response)
  //     }
  //     setComparisonAnalyses(results)
  //     // Also set the last one as the current analysis
  //     if (results.length > 0) {
  //       setAnalysis(results[results.length - 1])
  //     }
  //   } catch (err) {
  //     setError(err instanceof Error ? err.message : 'Multi-analysis failed')
  //   } finally {
  //     setIsLoading(false)
  //   }
  // }  

  async function handleFileUpload(file: File) {
    setIsUploading(true)
    setError(null)
    setUploadSuccess(null)

    try {
      const response = await uploadPlantData(file)
      
      // Set as active dataset
      setActiveDataset({
        id: response.file_id,
        name: response.filename,
        isDefault: false
      })
      
      setUploadSuccess(
        `Successfully uploaded ${response.filename} (${response.row_count} rows, ${response.columns.length} columns)`
      )
      // Clear success message after 5 seconds
      setTimeout(() => setUploadSuccess(null), 5000)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed')
    } finally {
      setIsUploading(false)
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

      {/* Active Dataset Indicator */}
      <section>
        <DatasetSelector 
          activeDataset={activeDataset}
          onClearDataset={() => setActiveDataset({ id: 'default', name: 'la-haute-borne-data-2014-2015.csv', isDefault: true })}
        />
      </section>

      {/* Data Visualizations */}
      <section>
        <AnalysisVisualization analysis={analysis} isLoading={isLoading} />
      </section>

      {/* Multi-Analysis Section - Temporarily Disabled */}
      <section>
        {/* <MultiAnalysisSelector onRunMultiple={runMultipleAnalyses} isLoading={isLoading} /> */}
        <div className="rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-6 shadow-sm">
          <div className="mb-4">
            <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100">Multi-Analysis</h2>
            <p className="text-sm text-slate-600 dark:text-slate-400">Run multiple analysis types simultaneously</p>
          </div>
          
          <div className="rounded-lg border-2 border-amber-300 dark:border-amber-600/50 bg-amber-50 dark:bg-amber-950/30 p-4">
            <div className="flex items-start gap-3">
              <svg
                className="h-6 w-6 flex-shrink-0 text-amber-700 dark:text-amber-400"
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
              <div>
                <h3 className="font-semibold text-amber-900 dark:text-amber-100">
                  Feature Temporarily Disabled
                </h3>
                <p className="mt-1 text-sm text-amber-800 dark:text-amber-200">
                  Multi-analysis is currently disabled due to performance considerations. 
                  Please run analyses individually using the form above.
                </p>
                <p className="mt-2 text-xs text-amber-700 dark:text-amber-300">
                  Running multiple analyses simultaneously can take several minutes and may cause 
                  browser timeouts. This feature will be re-enabled once background job processing 
                  is implemented.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* File Upload Section */}
      <section>
        <FileUpload onFileUpload={handleFileUpload} isLoading={isUploading} />
        {uploadSuccess && (
          <div className="mt-2 rounded-lg bg-emerald-50 p-3 text-sm text-emerald-700">
            ✓ {uploadSuccess}
          </div>
        )}
      </section>

      {/* Comparison View */}
      {comparisonAnalyses.length > 0 && (
        <section>
          <ComparisonView
            analyses={comparisonAnalyses}
            onClear={() => setComparisonAnalyses([])}
          />
        </section>
      )}
    </PageShell>
  )
}

export default App
