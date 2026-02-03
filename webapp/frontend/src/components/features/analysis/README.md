# Analysis Chart Components

Data visualization components built with [Nivo](https://nivo.rocks/) (D3-based) for displaying OpenOA analysis results.

## Components

### MetricsBarChart

Bar chart displaying key analysis metrics.

```tsx
import { MetricsBarChart } from './components/features/analysis'

const data = [
  { category: 'AEP (GWh)', value: 32.34, color: '#0ea5e9' },
  { category: 'Uncertainty (%)', value: 5.2, color: '#f59e0b' },
]

<MetricsBarChart data={data} title="Key Analysis Metrics" />
```

### UncertaintyLineChart

Line chart showing uncertainty ranges over iterations.

```tsx
import { UncertaintyLineChart } from './components/features/analysis'

const data = [
  {
    id: 'Mean AEP',
    data: [
      { x: 0, y: 32.34 },
      { x: 100, y: 32.45 },
    ],
  },
]

<UncertaintyLineChart data={data} title="Uncertainty Analysis" />
```

### EnergyBreakdownPieChart

Pie chart showing energy production breakdown.

```tsx
import { EnergyBreakdownPieChart } from './components/features/analysis'

const data = [
  { id: 'actual', label: 'Net Energy', value: 35.0, color: '#0ea5e9' },
  { id: 'losses', label: 'System Losses', value: 5.0, color: '#ef4444' },
]

<EnergyBreakdownPieChart data={data} title="Energy Breakdown" />
```

### AnalysisVisualization

Comprehensive visualization panel combining all charts.

```tsx
import { AnalysisVisualization } from './components/features/analysis'

<AnalysisVisualization analysis={analysisResponse} isLoading={false} />
```

## Utilities

### chartData.ts

Utility functions for transforming analysis results into chart data.

```tsx
import { transformAnalysisToChartData } from './utils/chartData'

const chartData = transformAnalysisToChartData(analysisResult)
// Returns: { metrics, uncertaintyRange, breakdown }
```

## Theming

All charts use consistent theming:
- **Colors**: Tailwind color palette
- **Typography**: Tailwind text styles
- **Spacing**: Consistent margins and padding
- **Animations**: Gentle motion config from Nivo

## Accessibility

- Proper ARIA labels
- Keyboard navigation support
- Color contrast compliance
- Screen reader compatible

## Performance

- Components memoized with `React.memo`
- Chart data memoized with `useMemo`
- Lazy loading supported
- Optimized re-renders
