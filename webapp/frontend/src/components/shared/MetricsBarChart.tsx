import { ResponsiveBar } from '@nivo/bar'
import { memo, useState, useEffect } from 'react'
import type { BarChartDataPoint } from '../../types/charts'
import { useTheme } from '../../hooks/useTheme'

interface MetricsBarChartProps {
  data: BarChartDataPoint[]
  title?: string
}

/**
 * Bar chart component for displaying analysis metrics.
 * Built with Nivo for D3-powered visualizations.
 * Fully responsive with adaptive margins and layout.
 */
export const MetricsBarChart = memo(function MetricsBarChart({
  data,
  title = 'Analysis Metrics',
}: MetricsBarChartProps) {
  const [isMobile, setIsMobile] = useState(false)
  const { theme } = useTheme()

  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 768)
    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  if (!data || data.length === 0) {
    return (
      <div className="flex h-64 items-center justify-center rounded-lg border border-dashed border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50">
        <p className="text-sm text-slate-500 dark:text-slate-400">No data available</p>
      </div>
    )
  }

  const chartMargins = isMobile
    ? { top: 10, right: 10, bottom: 80, left: 50 }
    : { top: 20, right: 30, bottom: 60, left: 70 }

  return (
    <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-3 shadow-sm sm:p-6">
      {title && <h3 className="mb-3 text-base font-semibold text-slate-900 dark:text-slate-100 sm:mb-4 sm:text-lg">{title}</h3>}
      <div className="h-64 sm:h-80">
        <ResponsiveBar
          data={data}
          keys={['value']}
          indexBy="category"
          margin={chartMargins}
          padding={isMobile ? 0.2 : 0.3}
          valueScale={{ type: 'linear' }}
          colors={({ data }) => String(data.color || '#0ea5e9')}
          borderRadius={isMobile ? 4 : 6}
          axisBottom={{
            tickSize: 0,
            tickPadding: isMobile ? 8 : 10,
            tickRotation: isMobile ? -45 : 0,
            legend: '',
            legendPosition: 'middle',
            legendOffset: isMobile ? 60 : 40,
          }}
          axisLeft={{
            tickSize: isMobile ? 3 : 5,
            tickPadding: isMobile ? 5 : 8,
            tickRotation: 0,
            legend: isMobile ? '' : 'Value',
            legendPosition: 'middle',
            legendOffset: isMobile ? -40 : -55,
            format: (value) => {
              // Format based on value range
              if (value >= 100) return `${value.toFixed(0)}`
              if (value >= 10) return `${value.toFixed(1)}`
              return `${value.toFixed(2)}`
            },
          }}
          enableLabel={!isMobile}
          label={(d) => `${Number(d.value).toFixed(1)}`}
          labelSkipWidth={isMobile ? 30 : 20}
          labelSkipHeight={isMobile ? 30 : 20}
          labelTextColor="#ffffff"
          animate={true}
          motionConfig="gentle"
          role="img"
          ariaLabel="Bar chart showing analysis metrics"
          tooltip={({ indexValue, value, color }) => (
            <div className="rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-2 shadow-lg">
              <div className="flex items-center gap-2">
                <div className="h-3 w-3 rounded" style={{ backgroundColor: color }} />
                <span className="text-sm font-medium text-slate-900 dark:text-slate-100">{indexValue}</span>
              </div>
              <div className="mt-1 text-lg font-semibold text-slate-700 dark:text-slate-300">
                {Number(value).toFixed(2)}
              </div>
            </div>
          )}
          theme={{
            axis: {
              ticks: {
                text: {
                  fontSize: isMobile ? 9 : 11,
                  fill: theme === 'dark' ? '#94a3b8' : '#64748b',
                  fontWeight: 500,
                },
              },
              legend: {
                text: {
                  fontSize: isMobile ? 10 : 12,
                  fill: theme === 'dark' ? '#cbd5e1' : '#475569',
                  fontWeight: 600,
                },
              },
            },
            grid: {
              line: {
                stroke: theme === 'dark' ? '#334155' : '#e2e8f0',
                strokeWidth: 1,
              },
            },
            labels: {
              text: {
                fontSize: isMobile ? 10 : 12,
                fontWeight: 700,
              },
            },
          }}
        />
      </div>
    </div>
  )
})
