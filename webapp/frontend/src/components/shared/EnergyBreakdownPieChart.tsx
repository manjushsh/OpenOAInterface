import { ResponsivePie } from '@nivo/pie'
import { memo, useState, useEffect } from 'react'
import type { PieChartDataPoint } from '../../types/charts'
import { useTheme } from '../../hooks/useTheme'

interface EnergyBreakdownPieChartProps {
  data: PieChartDataPoint[]
  title?: string
}

/**
 * Pie chart component for displaying energy production breakdown.
 * Built with Nivo for D3-powered visualizations.
 * Fully responsive with adaptive margins and labels.
 */
export const EnergyBreakdownPieChart = memo(function EnergyBreakdownPieChart({
  data,
  title = 'Energy Breakdown',
}: EnergyBreakdownPieChartProps) {
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
    ? { top: 20, right: 10, bottom: 100, left: 10 }
    : { top: 20, right: 20, bottom: 80, left: 20 }

  return (
    <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-3 shadow-sm sm:p-6">
      {title && <h3 className="mb-3 text-base font-semibold text-slate-900 dark:text-slate-100 sm:mb-4 sm:text-lg">{title}</h3>}
      <div className="h-64 sm:h-80">
        <ResponsivePie
          data={data}
          margin={chartMargins}
          innerRadius={isMobile ? 0.5 : 0.6}
          padAngle={isMobile ? 0.5 : 1}
          cornerRadius={isMobile ? 3 : 4}
          activeOuterRadiusOffset={isMobile ? 6 : 10}
          colors={{ datum: 'data.color' }}
          borderWidth={isMobile ? 1 : 2}
          borderColor={{
            from: 'color',
            modifiers: [['darker', 0.3]],
          }}
          arcLinkLabelsSkipAngle={isMobile ? 15 : 8}
          arcLinkLabelsTextColor={theme === 'dark' ? '#94a3b8' : '#64748b'}
          arcLinkLabelsThickness={isMobile ? 1 : 2}
          arcLinkLabelsColor={{ from: 'color' }}
          enableArcLinkLabels={!isMobile}
          arcLabelsSkipAngle={isMobile ? 20 : 15}
          arcLabelsTextColor="#ffffff"
          arcLabel={(d) => `${d.value.toFixed(isMobile ? 0 : 1)}%`}
          valueFormat={(value) => `${value.toFixed(1)}%`}
          tooltip={({ datum }) => (
            <div className="rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-2 shadow-lg">
              <div className="flex items-center gap-2">
                <div className="h-3 w-3 rounded-full" style={{ backgroundColor: datum.color }} />
                <span className="text-sm font-medium text-slate-900 dark:text-slate-100">{datum.label}</span>
              </div>
              <div className="mt-1 text-lg font-semibold text-slate-700 dark:text-slate-300">
                {datum.value.toFixed(1)}%
              </div>
            </div>
          )}
          legends={[
            {
              anchor: 'bottom',
              direction: isMobile ? 'column' : 'row',
              justify: false,
              translateX: 0,
              translateY: isMobile ? 80 : 60,
              itemsSpacing: isMobile ? 4 : 10,
              itemWidth: isMobile ? 120 : 100,
              itemHeight: isMobile ? 16 : 20,
              itemTextColor: theme === 'dark' ? '#94a3b8' : '#475569',
              itemDirection: 'left-to-right',
              itemOpacity: 1,
              symbolSize: isMobile ? 10 : 14,
              symbolShape: 'circle',
              effects: [
                {
                  on: 'hover',
                  style: {
                    itemTextColor: theme === 'dark' ? '#f1f5f9' : '#1e293b',
                    itemOpacity: 1,
                  },
                },
              ],
            },
          ]}
          animate={true}
          motionConfig="gentle"
          role="img"
          aria-label="Pie chart showing energy breakdown"
          theme={{
            labels: {
              text: {
                fontSize: isMobile ? 10 : 12,
                fontWeight: 700,
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
