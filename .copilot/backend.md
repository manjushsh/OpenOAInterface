# Backend Development Guidelines - FastAPI

## 📋 Overview

The backend is a FastAPI application that exposes OpenOA functionality via REST API endpoints.

**Tech Stack:**
- Python 3.10+
- FastAPI
- Pydantic for validation
- Uvicorn as ASGI server
- Pytest for testing

---

## 📁 Directory Structure

```
backend/
├── app/
│   ├── __init__.py          # Package init with version
│   ├── main.py              # FastAPI app instance, middleware
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/          # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── health.py    # Health check routes
│   │   │   ├── analysis.py  # Analysis endpoints
│   │   │   └── data.py      # Data management
│   │   └── dependencies.py  # Shared dependencies
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Settings from env vars
│   │   └── cors.py          # CORS configuration
│   ├── services/
│   │   ├── __init__.py
│   │   └── openoa_service.py # OpenOA wrapper
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models
│   └── utils/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_health.py
│   └── test_analysis.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── .env.example
└── README.md
```

---

## 🎯 Coding Standards

### File Naming
- Use `snake_case` for all Python files
- Use descriptive names: `openoa_service.py` not `service.py`

### Function/Variable Naming
```python
# Good
def calculate_annual_energy_production():
    wind_speed_data = []
    
# Bad
def calcAEP():
    wsd = []
```

### Type Hints (Required)
```python
from typing import Optional, List
from pydantic import BaseModel

def get_analysis_result(analysis_id: str) -> Optional[AnalysisResult]:
    """Retrieve analysis result by ID."""
    pass

class AnalysisRequest(BaseModel):
    plant_id: str
    start_date: str
    end_date: str
```

### Docstrings (Google Style)
```python
def run_aep_analysis(
    plant_data: PlantData,
    num_iterations: int = 1000
) -> AEPResult:
    """Run Monte Carlo AEP analysis on plant data.
    
    Args:
        plant_data: OpenOA PlantData object with SCADA data.
        num_iterations: Number of Monte Carlo iterations.
        
    Returns:
        AEPResult containing estimated AEP and uncertainty.
        
    Raises:
        AnalysisError: If plant data is invalid or incomplete.
    """
    pass
```

---

## 🛣️ API Design Patterns

### Route Organization
```python
# app/api/routes/analysis.py
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.get("/{analysis_id}")
async def get_analysis(analysis_id: str) -> AnalysisResponse:
    """Get analysis result by ID."""
    pass

@router.post("/aep")
async def run_aep_analysis(request: AEPRequest) -> AnalysisResponse:
    """Run AEP analysis."""
    pass
```

### Response Models
```python
# app/models/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AnalysisResponse(BaseModel):
    """Standard response for analysis results."""
    id: str = Field(..., description="Unique analysis ID")
    status: str = Field(..., description="Analysis status")
    result: Optional[dict] = Field(None, description="Analysis results")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "abc123",
                "status": "completed",
                "result": {"aep_gwh": 150.5, "uncertainty_pct": 5.2},
                "created_at": "2026-02-03T10:30:00Z"
            }
        }
```

### Error Handling
```python
from fastapi import HTTPException

# Use appropriate status codes
raise HTTPException(status_code=404, detail="Analysis not found")
raise HTTPException(status_code=400, detail="Invalid date range")
raise HTTPException(status_code=500, detail="Analysis failed")

# Custom exception handlers in main.py
@app.exception_handler(OpenOAException)
async def openoa_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"OpenOA error: {str(exc)}"}
    )
```

---

## ⚙️ Configuration Management

### Settings Class
```python
# app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # App settings
    app_name: str = "OpenOA API"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    
    # CORS
    cors_origins: list[str] = ["http://localhost:5173"]
    
    # Logging
    log_level: str = "info"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### Environment Variables
```bash
# .env.example
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=["http://localhost:5173"]
LOG_LEVEL=debug
```

---

## 🔌 OpenOA Integration

### Service Layer Pattern
```python
# app/services/openoa_service.py
from typing import Optional
import logging

# Import from installed openoa package
from openoa import PlantData
from openoa.analysis import MonteCarloAEP

logger = logging.getLogger(__name__)

class OpenOAService:
    """Service for interacting with OpenOA library."""
    
    def __init__(self):
        self._sample_data: Optional[PlantData] = None
    
    def get_sample_plant_data(self) -> PlantData:
        """Load and return sample ENGIE plant data."""
        if self._sample_data is None:
            # Load from examples/data
            self._sample_data = self._load_sample_data()
        return self._sample_data
    
    def run_aep_analysis(
        self,
        plant_data: PlantData,
        **kwargs
    ) -> dict:
        """Run AEP analysis and return results."""
        try:
            analysis = MonteCarloAEP(plant_data, **kwargs)
            analysis.run()
            return {
                "aep_gwh": analysis.aep,
                "uncertainty_pct": analysis.uncertainty
            }
        except Exception as e:
            logger.error(f"AEP analysis failed: {e}")
            raise
    
    def _load_sample_data(self) -> PlantData:
        """Load sample data from examples."""
        # Implementation here
        pass

# Singleton instance
openoa_service = OpenOAService()
```

---

## 🧪 Testing Patterns

### Test Structure
```python
# tests/test_health.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestHealthEndpoints:
    """Tests for health check endpoints."""
    
    def test_health_returns_200(self):
        """Health endpoint should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_health_includes_version(self):
        """Health response should include version."""
        response = client.get("/health")
        assert "version" in response.json()
```

### Fixtures
```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)

@pytest.fixture
def sample_plant_data():
    """Sample PlantData for testing."""
    # Return mock or sample data
    pass
```

---

## 🐳 Docker Configuration

### Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app ./app

# Run with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Health Check
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

---

## 📝 Logging

### Logger Setup
```python
# app/main.py
import logging
from app.core.config import get_settings

settings = get_settings()

logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
```

### Usage
```python
logger.info(f"Starting analysis for plant {plant_id}")
logger.debug(f"Analysis parameters: {params}")
logger.error(f"Analysis failed: {error}", exc_info=True)
```

---

## ✅ Code Review Checklist

Before submitting code:

- [ ] Type hints on all functions
- [ ] Docstrings on public functions
- [ ] No hardcoded values (use config)
- [ ] Error handling in place
- [ ] Tests for new functionality
- [ ] No secrets in code
- [ ] Logging for important operations
- [ ] API docs updated (if endpoint changed)
