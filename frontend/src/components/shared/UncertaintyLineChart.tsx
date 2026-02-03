import { ResponsiveLine } from '@nivo/line'
import { memo, useState, useEffect } from 'react'
import type { LineChartSeries } from '../../types/charts'
import { useTheme } from '../../hooks/useTheme'

interface UncertaintyLineChartProps {
  data: LineChartSeries[]
  title?: string
}

/**
 * Line chart component for displaying uncertainty ranges over iterations.
 * Built with Nivo for D3-powered visualizations.
 * Fully responsive with adaptive margins and legends.
 */
export const UncertaintyLineChart = memo(function UncertaintyLineChart({
  data,
  title = 'Uncertainty Analysis',
}: UncertaintyLineChartProps) {
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
    ? { top: 20, right: 10, bottom: 90, left: 50 }
    : { top: 20, right: 120, bottom: 60, left: 70 }

  return (
    <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-3 shadow-sm sm:p-6">
      {title && <h3 className="mb-3 text-base font-semibold text-slate-900 dark:text-slate-100 sm:mb-4 sm:text-lg">{title}</h3>}
      <div className="h-64 sm:h-80">
        <ResponsiveLine
          data={data}
          margin={chartMargins}
          xScale={{ type: 'point' }}
          yScale={{
            type: 'linear',
            min: 'auto',
            max: 'auto',
            stacked: false,
            reverse: false,
          }}
          curve="monotoneX"
          axisTop={null}
          axisRight={null}
          axisBottom={{
            tickSize: isMobile ? 3 : 5,
            tickPadding: isMobile ? 5 : 8,
            tickRotation: isMobile ? -45 : 0,
            legend: isMobile ? '' : 'Iteration',
            legendOffset: isMobile ? 70 : 45,
            legendPosition: 'middle',
            format: (value) => (Number(value) % (isMobile ? 400 : 200) === 0 ? value : ''),
          }}
          axisLeft={{
            tickSize: isMobile ? 3 : 5,
            tickPadding: isMobile ? 5 : 8,
            tickRotation: 0,
            legend: isMobile ? '' : 'AEP (GWh)',
            legendOffset: isMobile ? -40 : -55,
            legendPosition: 'middle',
            format: (value) => value.toFixed(isMobile ? 0 : 1),
          }}
          colors={{ datum: 'color' }}
          lineWidth={isMobile ? 2 : 3}
          pointSize={isMobile ? 0 : 8}
          pointColor={{ theme: 'background' }}
          pointBorderWidth={isMobile ? 0 : 2}
          pointBorderColor={{ from: 'serieColor' }}
          pointLabelYOffset={-12}
          enableArea={true}
          areaOpacity={isMobile ? 0.1 : 0.15}
          useMesh={true}
          enableSlices={isMobile ? false : 'x'}
          sliceTooltip={({ slice }) => (
            <div className="rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-2 shadow-lg">
              <div className="text-xs font-semibold text-slate-500 dark:text-slate-400">
                Iteration {slice.points[0].data.x}
              </div>
              {slice.points.map((point) => (
                <div key={point.id} className="mt-1 flex items-center gap-2">
                  <div
                    className="h-3 w-3 rounded-full"
                    style={{ backgroundColor: point.seriesColor }}
                  />
                  <span className="text-sm text-slate-700 dark:text-slate-300">{point.seriesId}:</span>
                  <span className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                    {Number(point.data.y).toFixed(2)} GWh
                  </span>
                </div>
              ))}
            </div>
          )}
          legends={[
            {
              anchor: isMobile ? 'bottom' : 'bottom-right',
              direction: isMobile ? 'row' : 'column',
              justify: false,
              translateX: isMobile ? 0 : 110,
              translateY: isMobile ? 70 : 0,
              itemsSpacing: isMobile ? 5 : 2,
              itemDirection: 'left-to-right',
              itemWidth: isMobile ? 70 : 100,
              itemHeight: isMobile ? 18 : 20,
              itemOpacity: 0.85,
              symbolSize: isMobile ? 10 : 14,
              symbolShape: 'circle',
              symbolBorderColor: 'rgba(0, 0, 0, .5)',
              effects: [
                {
                  on: 'hover',
                  style: {
                    itemBackground: 'rgba(0, 0, 0, .03)',
                    itemOpacity: 1,
                  },
                },
              ],
            },
          ]}
          animate={true}
          motionConfig="gentle"
          role="img"
          ariaLabel="Line chart showing uncertainty analysis"
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
            legends: {
              text: {
                fontSize: isMobile ? 9 : 11,
                fill: theme === 'dark' ? '#94a3b8' : '#475569',
                fontWeight: 500,
              },
            },
          }}
        />
      </div>
    </div>
  )
})
