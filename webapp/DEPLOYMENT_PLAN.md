# OpenOA Web Application - Deployment Plan

## 🎯 Project Overview

**Goal:** Create a web application that exposes OpenOA wind plant analysis capabilities via a URL for interview demo purposes.

**Stack:**
- **Backend:** FastAPI (Python)
- **Frontend:** React.js (TypeScript)
- **Deployment:** Render.com (Free Tier)

---

## 📁 Project Structure

```
webapp/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── health.py  # Health check endpoint
│   │   │   │   ├── analysis.py # OpenOA analysis endpoints
│   │   │   │   └── data.py    # Data upload/management
│   │   │   └── dependencies.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py      # Configuration settings
│   │   │   └── cors.py        # CORS configuration
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── openoa_service.py  # OpenOA integration
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py     # Pydantic models
│   │   └── utils/
│   │       └── __init__.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_health.py
│   │   └── test_analysis.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout/
│   │   │   ├── Dashboard/
│   │   │   └── Analysis/
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   └── Analysis.tsx
│   │   ├── services/
│   │   │   └── api.ts         # API client
│   │   ├── hooks/
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── .env.example
│
├── render.yaml                 # Render.com deployment config
├── docker-compose.yml          # Local development
├── .copilot/                   # Copilot instructions
│   ├── instructions.md
│   ├── backend.md
│   └── frontend.md
└── DEPLOYMENT_PLAN.md          # This file
```

---

## 🚀 Implementation Phases

### Phase 1: Foundation (MVP) ✅ START HERE
**Goal:** Get something working end-to-end

| Component | Feature | Priority |
|-----------|---------|----------|
| Backend | Health check endpoint (`/health`) | P0 |
| Backend | Basic info endpoint (`/api/v1/info`) | P0 |
| Backend | CORS configuration | P0 |
| Frontend | Basic React app with Vite | P0 |
| Frontend | Home page with API connection test | P0 |
| Deploy | Both services running on Render.com | P0 |

**Success Criteria:** 
- Frontend loads at `https://openoa-frontend.onrender.com`
- Backend responds at `https://openoa-backend.onrender.com/health`
- Frontend successfully calls backend API

---

### Phase 2: Core Features
**Goal:** Expose basic OpenOA functionality

| Component | Feature | Priority |
|-----------|---------|----------|
| Backend | Sample data endpoint (ENGIE demo data) | P1 |
| Backend | Basic AEP analysis endpoint | P1 |
| Frontend | Dashboard layout with navigation | P1 |
| Frontend | Display sample wind plant data | P1 |
| Frontend | Show analysis results with charts | P1 |

---

### Phase 3: Enhanced Features
**Goal:** Rich demo experience

| Component | Feature | Priority |
|-----------|---------|----------|
| Backend | Multiple analysis types (TIE, Electrical Losses) | P2 |
| Backend | Data upload capability | P2 |
| Frontend | Interactive data visualization (Recharts/D3) | P2 |
| Frontend | Analysis configuration form | P2 |
| Frontend | Export results | P2 |

---

## 🛠️ Technology Choices

### Backend - FastAPI
```
Why FastAPI?
✅ Native Python - seamless OpenOA integration
✅ Automatic OpenAPI/Swagger documentation
✅ Async support for better performance
✅ Type hints with Pydantic validation
✅ Easy to test and maintain
```

### Frontend - React + Vite + TypeScript
```
Why This Stack?
✅ React - You're already familiar with it
✅ Vite - Fast dev server, optimized builds
✅ TypeScript - Type safety, better IDE support
✅ Tailwind CSS - Rapid styling
✅ Recharts - Data visualization for wind data
```

### Deployment - Render.com
```
Why Render?
✅ Free tier (750 hours/month)
✅ Simple deployment from GitHub
✅ Auto-deploys on push
✅ render.yaml for infrastructure-as-code
✅ No Terraform complexity needed
```

---

## 📋 Render.com Deployment Configuration

### Service URLs (after deployment)
- **Backend:** `https://openoa-backend.onrender.com`
- **Frontend:** `https://openoa-frontend.onrender.com`

### Free Tier Limitations
| Resource | Limit | Impact |
|----------|-------|--------|
| Web Services | 750 hrs/month | Enough for demo |
| RAM | 512 MB | May need optimization |
| Cold Start | ~30 seconds | First request slow |
| Sleep | After 15 min inactivity | Expected for free tier |

### Mitigation Strategies
1. **Cold Start:** Add loading indicator on frontend
2. **Sleep:** Use health check to wake up services
3. **RAM:** Keep dependencies minimal

---

## 🔧 Local Development Setup

### Prerequisites
```bash
# Python 3.10+
python --version

# Node.js 18+
node --version

# Docker (optional, for containerized dev)
docker --version
```

### Quick Start
```bash
# Clone and navigate
cd webapp

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

### Environment Variables

**Backend (.env)**
```
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:5173
LOG_LEVEL=debug
```

**Frontend (.env)**
```
VITE_API_URL=http://localhost:8000
```

---

## 📊 API Endpoints (Phase 1)

### Health & Info
```
GET  /health              → {"status": "healthy"}
GET  /api/v1/info         → {"name": "OpenOA API", "version": "1.0.0"}
GET  /docs                → Swagger UI
```

### Future Endpoints
```
GET  /api/v1/sample-data         → Sample wind plant data
POST /api/v1/analysis/aep        → Run AEP analysis
GET  /api/v1/analysis/{id}       → Get analysis results
```

---

## ✅ Definition of Done - Phase 1

- [ ] Backend runs locally with health endpoint
- [ ] Frontend runs locally and displays content
- [ ] Frontend can call backend API successfully
- [ ] Both deployed to Render.com
- [ ] URLs accessible publicly
- [ ] README with setup instructions
- [ ] Swagger docs accessible at /docs

---

## 🎯 Interview Demo Talking Points

1. **Architecture:** Clean separation of frontend/backend
2. **Technology Choices:** Modern stack, industry standard
3. **Deployment:** Infrastructure-as-code with render.yaml
4. **Testing:** Unit tests for critical paths
5. **Documentation:** API docs auto-generated
6. **Scalability:** Easy to add features
7. **OpenOA Integration:** Exposing scientific library as web service

---

## 📚 Next Steps

1. **Create backend foundation** (FastAPI + health endpoints)
2. **Create frontend foundation** (React + Vite + API connection)
3. **Test locally** (both services communicating)
4. **Deploy to Render** (push to GitHub → auto-deploy)
5. **Verify URLs work** (celebrate! 🎉)
6. **Add OpenOA features** (Phase 2)
