import type { AnalysisResult } from '../types/api'
import type {
  AnalysisChartData,
  BarChartDataPoint,
  LineChartSeries,
  PieChartDataPoint,
} from '../types/charts'

/**
 * Transform analysis result into chart data structures.
 * Dynamically adapts to different analysis types.
 */
export function transformAnalysisToChartData(analysis: AnalysisResult): AnalysisChartData {
  const metrics: BarChartDataPoint[] = []
  
  // Add metrics based on what's available
  if (analysis.aep_gwh != null) {
    metrics.push({
      category: `AEP\n${analysis.aep_gwh.toFixed(1)} GWh`,
      value: analysis.aep_gwh,
      color: '#0ea5e9',
    })
  }
  
  if (analysis.ideal_energy_gwh != null) {
    metrics.push({
      category: `Ideal Energy\n${analysis.ideal_energy_gwh.toFixed(1)} GWh`,
      value: analysis.ideal_energy_gwh,
      color: '#0ea5e9',
    })
  }
  
  if (analysis.total_loss_pct != null) {
    metrics.push({
      category: `Elec. Losses\n${analysis.total_loss_pct.toFixed(1)}%`,
      value: analysis.total_loss_pct,
      color: '#ef4444',
    })
  }
  
  if (analysis.wake_loss_pct != null) {
    metrics.push({
      category: `Wake Losses\n${analysis.wake_loss_pct.toFixed(1)}%`,
      value: analysis.wake_loss_pct,
      color: '#f97316',
    })
  }
  
  if (analysis.gap_pct != null) {
    metrics.push({
      category: `Gap\n${analysis.gap_pct.toFixed(1)}%`,
      value: Math.abs(analysis.gap_pct),
      color: analysis.gap_pct < 0 ? '#ef4444' : '#10b981',
    })
  }
  
  if (analysis.uncertainty_pct != null) {
    metrics.push({
      category: `Uncertainty\n${analysis.uncertainty_pct.toFixed(1)}%`,
      value: analysis.uncertainty_pct,
      color: '#f59e0b',
    })
  }
  
  if (analysis.capacity_factor != null) {
    metrics.push({
      category: `Capacity Factor\n${analysis.capacity_factor.toFixed(1)}%`,
      value: analysis.capacity_factor,
      color: '#10b981',
    })
  }
  
  if (analysis.plant_capacity_mw != null) {
    metrics.push({
      category: `Plant Cap.\n${analysis.plant_capacity_mw.toFixed(1)} MW`,
      value: analysis.plant_capacity_mw,
      color: '#8b5cf6',
    })
  }

  // Generate simulated uncertainty range data for visualization if AEP is available
  const uncertaintyRange: LineChartSeries[] = 
    analysis.aep_gwh != null && analysis.uncertainty_pct != null
      ? generateUncertaintyRange(analysis.aep_gwh, analysis.uncertainty_pct)
      : []

  // Calculate realistic energy breakdown based on capacity factor if available
  const capacityFactor = analysis.capacity_factor ?? 35
  const estimatedLosses = 8.0 // Typical total losses
  const estimatedCurtailment = 2.0 // Typical curtailment
  const unavailability = 5.0 // Typical downtime
  const windAvailability = Math.max(0, 100 - capacityFactor - estimatedLosses - estimatedCurtailment - unavailability)

  const breakdown: PieChartDataPoint[] = [
    {
      id: 'production',
      label: 'Net Production',
      value: capacityFactor,
      color: '#10b981',
    },
    {
      id: 'losses',
      label: 'Electrical Losses',
      value: estimatedLosses,
      color: '#ef4444',
    },
    {
      id: 'curtailment',
      label: 'Curtailment',
      value: estimatedCurtailment,
      color: '#f59e0b',
    },
    {
      id: 'unavailable',
      label: 'Unavailability',
      value: unavailability,
      color: '#64748b',
    },
    {
      id: 'wind',
      label: 'Low Wind',
      value: windAvailability,
      color: '#cbd5e1',
    },
  ]

  return {
    metrics,
    uncertaintyRange,
    breakdown: breakdown.filter((d) => d.value > 0.1), // Remove negligible values
  }
}

/**
 * Generate simulated uncertainty range data for line chart.
 */
function generateUncertaintyRange(
  meanAep: number,
  uncertaintyPct: number
): LineChartSeries[] {
  const uncertaintyValue = (meanAep * uncertaintyPct) / 100
  const numPoints = 20

  const meanSeries: LineChartSeries = {
    id: 'Mean AEP',
    color: '#0ea5e9',
    data: [],
  }

  const upperBoundSeries: LineChartSeries = {
    id: 'Upper Bound',
    color: '#10b981',
    data: [],
  }

  const lowerBoundSeries: LineChartSeries = {
    id: 'Lower Bound',
    color: '#ef4444',
    data: [],
  }

  for (let i = 0; i <= numPoints; i++) {
    const iteration = i * 50
    // Add some simulated variance
    const variance = Math.sin(i * 0.5) * uncertaintyValue * 0.2

    meanSeries.data.push({
      x: iteration,
      y: meanAep + variance,
    })

    upperBoundSeries.data.push({
      x: iteration,
      y: meanAep + uncertaintyValue + variance,
    })

    lowerBoundSeries.data.push({
      x: iteration,
      y: meanAep - uncertaintyValue + variance,
    })
  }

  return [lowerBoundSeries, meanSeries, upperBoundSeries]
}

/**
 * Format number with appropriate precision.
 */
export function formatNumber(value: number, decimals = 2): string {
  return value.toFixed(decimals)
}

/**
 * Format percentage value.
 */
export function formatPercentage(value: number, decimals = 1): string {
  return `${value.toFixed(decimals)}%`
}

/**
 * Format energy value with units.
 */
export function formatEnergy(value: number, unit = 'GWh'): string {
  return `${value.toFixed(2)} ${unit}`
}
