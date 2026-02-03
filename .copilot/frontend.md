# Frontend Development Guidelines - React + TypeScript

## 📋 Overview

The frontend is a React application built with Vite and TypeScript that provides a user interface for OpenOA analysis capabilities.

**Tech Stack:**
- React 19+
- TypeScript (strict mode)
- Vite for build tooling
- Tailwind CSS for styling
- React Router for navigation
- Axios or Fetch for API calls
- Recharts for data visualization

---

## 📁 Directory Structure

```
frontend/
├── src/
│   ├── components/           # Reusable UI components
│   │   ├── common/           # Generic components
│   │   │   ├── Button/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Button.test.tsx
│   │   │   │   └── index.ts
│   │   │   ├── Card/
│   │   │   ├── Loading/
│   │   │   └── ErrorBoundary/
│   │   ├── layout/           # Layout components
│   │   │   ├── Header/
│   │   │   ├── Sidebar/
│   │   │   └── Footer/
│   │   └── features/         # Feature-specific components
│   │       ├── Dashboard/
│   │       └── Analysis/
│   ├── pages/                # Page components (routes)
│   │   ├── Home.tsx
│   │   ├── Dashboard.tsx
│   │   └── Analysis.tsx
│   ├── services/             # API and external services
│   │   ├── api.ts            # Axios instance
│   │   └── analysisService.ts
│   ├── hooks/                # Custom React hooks
│   │   ├── useApi.ts
│   │   └── useAnalysis.ts
│   ├── types/                # TypeScript types/interfaces
│   │   ├── api.ts
│   │   └── analysis.ts
│   ├── utils/                # Utility functions
│   │   ├── formatters.ts
│   │   └── validators.ts
│   ├── constants/            # App constants
│   │   └── index.ts
│   ├── App.tsx               # Main app component
│   ├── main.tsx              # Entry point
│   └── index.css             # Global styles
├── public/
│   └── favicon.ico
├── tests/
│   └── setup.ts
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
├── .env.example
└── README.md
```

---

## 🎯 Coding Standards

### File Naming
- Components: `PascalCase.tsx` (e.g., `AnalysisCard.tsx`)
- Utilities/hooks: `camelCase.ts` (e.g., `useAnalysis.ts`)
- Types: `camelCase.ts` (e.g., `analysis.ts`)
- Test files: `ComponentName.test.tsx`

### Component Naming
```tsx
// Good - PascalCase, descriptive
export function AnalysisResultCard() {}
export function WindSpeedChart() {}

// Bad
export function analysisCard() {}
export function Chart1() {}
```

### TypeScript Usage (Strict)
```tsx
// Always define props interface
interface AnalysisCardProps {
  title: string;
  value: number;
  unit: string;
  trend?: 'up' | 'down' | 'stable';
  onClick?: () => void;
}

// Use interface for objects, type for unions/primitives
type AnalysisStatus = 'pending' | 'running' | 'completed' | 'failed';

interface AnalysisResult {
  id: string;
  status: AnalysisStatus;
  aepGwh: number;
  uncertaintyPct: number;
}
```

---

## 🧩 Component Patterns

### Functional Components
```tsx
// src/components/features/Analysis/AnalysisCard.tsx
import { memo } from 'react';

interface AnalysisCardProps {
  title: string;
  value: number;
  unit: string;
  isLoading?: boolean;
}

/**
 * Card component displaying a single analysis metric.
 */
export const AnalysisCard = memo(function AnalysisCard({
  title,
  value,
  unit,
  isLoading = false,
}: AnalysisCardProps) {
  if (isLoading) {
    return <div className="animate-pulse bg-gray-200 h-24 rounded-lg" />;
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-sm font-medium text-gray-500">{title}</h3>
      <p className="mt-2 text-3xl font-semibold text-gray-900">
        {value.toFixed(2)} <span className="text-lg">{unit}</span>
      </p>
    </div>
  );
});
```

### Component Exports
```tsx
// src/components/features/Analysis/index.ts
export { AnalysisCard } from './AnalysisCard';
export { AnalysisForm } from './AnalysisForm';
export { AnalysisResults } from './AnalysisResults';
```

### Container/Presenter Pattern
```tsx
// Container - handles logic and data
// src/pages/Dashboard.tsx
export function Dashboard() {
  const { data, isLoading, error } = useAnalysisData();
  
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  
  return <DashboardView data={data} />;
}

// Presenter - handles display only
// src/components/features/Dashboard/DashboardView.tsx
interface DashboardViewProps {
  data: AnalysisData;
}

export function DashboardView({ data }: DashboardViewProps) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {/* Pure presentation */}
    </div>
  );
}
```

---

## 🔌 API Integration

### API Client Setup
```tsx
// src/services/api.ts
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds for long-running analyses
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);
```

### Service Functions
```tsx
// src/services/analysisService.ts
import { apiClient } from './api';
import type { AnalysisResult, AEPRequest } from '../types/analysis';

export const analysisService = {
  /**
   * Run AEP analysis on plant data.
   */
  async runAEP(request: AEPRequest): Promise<AnalysisResult> {
    const { data } = await apiClient.post<AnalysisResult>(
      '/api/v1/analysis/aep',
      request
    );
    return data;
  },

  /**
   * Get analysis result by ID.
   */
  async getResult(id: string): Promise<AnalysisResult> {
    const { data } = await apiClient.get<AnalysisResult>(
      `/api/v1/analysis/${id}`
    );
    return data;
  },

  /**
   * Check API health.
   */
  async checkHealth(): Promise<{ status: string }> {
    const { data } = await apiClient.get('/health');
    return data;
  },
};
```

### Custom Hooks
```tsx
// src/hooks/useApi.ts
import { useState, useEffect, useCallback } from 'react';

interface UseApiState<T> {
  data: T | null;
  isLoading: boolean;
  error: Error | null;
}

export function useApi<T>(
  fetchFn: () => Promise<T>,
  deps: unknown[] = []
): UseApiState<T> & { refetch: () => void } {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    isLoading: true,
    error: null,
  });

  const fetchData = useCallback(async () => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }));
    try {
      const data = await fetchFn();
      setState({ data, isLoading: false, error: null });
    } catch (error) {
      setState({ data: null, isLoading: false, error: error as Error });
    }
  }, deps);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { ...state, refetch: fetchData };
}
```

---

## 🎨 Styling with Tailwind

### Tailwind Configuration
```js
// tailwind.config.js
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        },
        // OpenOA brand colors
        openoa: {
          blue: '#1e40af',
          green: '#059669',
        },
      },
    },
  },
  plugins: [],
};
```

### Component Styling Patterns
```tsx
// Use className with template literals for conditional styles
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export function Button({ variant = 'primary', size = 'md', children }: ButtonProps) {
  const baseStyles = 'rounded-lg font-medium transition-colors focus:outline-none focus:ring-2';
  
  const variantStyles = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
  };
  
  const sizeStyles = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]}`}>
      {children}
    </button>
  );
}
```

---

## 🔀 Routing

### React Router Setup
```tsx
// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import { Home } from './pages/Home';
import { Dashboard } from './pages/Dashboard';
import { Analysis } from './pages/Analysis';
import { NotFound } from './pages/NotFound';

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="analysis" element={<Analysis />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

---

## ⚙️ Environment Variables

### Vite Environment Setup
```bash
# .env.example
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=OpenOA Dashboard
```

### Usage in Code
```tsx
// Access env variables with import.meta.env
const apiUrl = import.meta.env.VITE_API_URL;
const appName = import.meta.env.VITE_APP_NAME || 'OpenOA';

// Type definitions
// src/vite-env.d.ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_APP_NAME: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

---

## 🧪 Testing Patterns

### Component Tests
```tsx
// src/components/common/Button/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('applies primary variant styles by default', () => {
    render(<Button>Primary</Button>);
    expect(screen.getByText('Primary')).toHaveClass('bg-primary-600');
  });
});
```

### Test Setup
```tsx
// tests/setup.ts
import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock environment variables
vi.stubEnv('VITE_API_URL', 'http://localhost:8000');
```

---

## 🐳 Docker Configuration

### Dockerfile (Multi-stage build)
```dockerfile
# Build stage
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Nginx Configuration
```nginx
# nginx.conf
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Handle React Router
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location /assets {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## ✅ Code Review Checklist

Before submitting code:

- [ ] TypeScript strict mode passes (no `any` types)
- [ ] Components have prop interfaces defined
- [ ] No console.log statements (use proper logging)
- [ ] Error boundaries for async operations
- [ ] Loading states handled
- [ ] Mobile responsive (test at 375px width)
- [ ] Accessibility (aria labels, keyboard navigation)
- [ ] Tests for new components
- [ ] No hardcoded API URLs (use env vars)
- [ ] No unused imports or variables
