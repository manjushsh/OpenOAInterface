/**
 * Type definitions for chart data structures.
 */

export interface BarChartDataPoint {
  category: string
  value: number
  color: string
  [key: string]: string | number
}

export interface LineChartDataPoint {
  x: number | string
  y: number
}

export interface LineChartSeries {
  id: string
  color?: string
  data: LineChartDataPoint[]
}

export interface PieChartDataPoint {
  id: string
  label: string
  value: number
  color?: string
}

export interface AnalysisChartData {
  metrics: BarChartDataPoint[]
  uncertaintyRange?: LineChartSeries[]
  breakdown?: PieChartDataPoint[]
}
