# OpenOA Frontend

React + TypeScript + Vite + Tailwind v4 single-page dashboard for the OpenOA demo backend.

## Quick start

```bash
pnpm install
cp .env.example .env        # set VITE_API_URL if different
pnpm dev                    # http://localhost:5173
```

## Scripts

- `pnpm dev` — local development
- `pnpm build` — type-check + production build
- `pnpm lint` — eslint

## Tech choices

- React 19 with functional components
- Tailwind CSS v4 via `@tailwindcss/vite`
- Fetch-based API client (`src/services/api.ts`)
- Lightweight layout + analysis form connected to FastAPI/OpenOA

## Env

`VITE_API_URL` defaults to `http://localhost:8000`. Point it at your deployed backend to demo.
