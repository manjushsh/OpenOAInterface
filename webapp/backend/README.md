# OpenOA Web API - Backend

FastAPI backend for the OpenOA web application, exposing wind plant operational assessment capabilities via REST API.

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Create a virtual environment:**
```bash
cd webapp/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install development dependencies (optional):**
```bash
pip install -r requirements-dev.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env if needed
```

### Running the Application

**Development mode (with hot-reload):**
```bash
uvicorn app.main:app --reload --port 8000
```

**Production mode:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API:** http://localhost:8000
- **Interactive Docs (Swagger):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Package metadata
│   ├── main.py              # FastAPI application
│   ├── api/
│   │   ├── routes/          # API endpoints
│   │   │   ├── health.py    # Health check routes
│   │   │   └── ...
│   │   └── dependencies.py  # Shared dependencies
│   ├── core/
│   │   ├── config.py        # Configuration management
│   │   └── cors.py          # CORS setup
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   ├── services/
│   │   └── openoa_service.py # OpenOA integration
│   └── utils/               # Utility functions
├── tests/
│   ├── conftest.py          # Test fixtures
│   ├── test_health.py       # Health endpoint tests
│   └── ...
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── Dockerfile               # Production Docker image
├── Dockerfile.dev           # Development Docker image
└── README.md                # This file
```

## 🧪 Testing

**Run all tests:**
```bash
pytest
```

**Run with coverage:**
```bash
pytest --cov=app --cov-report=html
```

**Run specific test file:**
```bash
pytest tests/test_health.py -v
```

## 🐳 Docker

**Build and run with Docker:**
```bash
# Development
docker build -f Dockerfile.dev -t openoa-backend:dev .
docker run -p 8000:8000 openoa-backend:dev

# Production
docker build -t openoa-backend:latest .
docker run -p 8000:8000 openoa-backend:latest
```

**Using docker-compose (from webapp/ directory):**
```bash
cd ..  # Go to webapp directory
docker-compose up backend
```

## 📚 API Documentation

### Available Endpoints

#### Health & Info
- `GET /health` - Health check endpoint
- `GET /api/v1/info` - API and OpenOA version information
- `GET /` - Root endpoint with API links

### API Documentation
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

## ⚙️ Configuration

Configuration is managed through environment variables. See [.env.example](.env.example) for available options.

### Key Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Environment name |
| `DEBUG` | `false` | Enable debug mode |
| `LOG_LEVEL` | `info` | Logging level |
| `CORS_ORIGINS` | `["http://localhost:5173"]` | Allowed CORS origins |
| `USE_MOCK_DATA` | `true` | Use mock data (true) or real OpenOA (false) |

### Mock vs Real OpenOA Mode

The backend supports two modes:

**Mock Mode (USE_MOCK_DATA=true)** - Default
- Returns simulated analysis results
- No OpenOA installation required
- Perfect for demos and frontend development
- Fast and deterministic

**Real Mode (USE_MOCK_DATA=false)**
- Uses actual OpenOA library
- Requires OpenOA installation: `pip install openoa`
- Returns real analysis results
- Requires plant data files

To switch modes:
```bash
# In .env file
USE_MOCK_DATA=false  # For real OpenOA

# Or as environment variable
export USE_MOCK_DATA=false
uvicorn app.main:app --reload
```

## 🔧 Development

### Code Quality

**Format code:**
```bash
black app tests
isort app tests
```

**Lint code:**
```bash
flake8 app tests
mypy app
```

**Run all quality checks:**
```bash
black app tests && isort app tests && flake8 app tests && mypy app
```

### Adding New Endpoints

1. Create a new route file in `app/api/routes/`
2. Define Pydantic schemas in `app/models/schemas.py`
3. Create service logic in `app/services/` if needed
4. Add tests in `tests/`
5. Include the router in `app/main.py`

## 🚀 Deployment

### Render.com

The application is configured for deployment on Render.com. See [../render.yaml](../render.yaml) for configuration.

**Environment variables to set in Render:**
- `ENVIRONMENT=production`
- `CORS_ORIGINS=["https://openoa-frontend.onrender.com"]`
- `LOG_LEVEL=info`

### Local Production Simulation

```bash
ENVIRONMENT=production uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📖 Guidelines

For detailed coding standards and best practices, see:
- [Backend Guidelines](../.copilot/backend.md)
- [General Guidelines](../.copilot/instructions.md)

## 🔍 Troubleshooting

**Import errors:**
- Make sure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`

**Port already in use:**
- Use a different port: `uvicorn app.main:app --port 8001`
- Or kill the process using port 8000

**CORS errors:**
- Check `CORS_ORIGINS` in your `.env` file
- Ensure frontend URL is included in the list

## 📝 License

This project is part of OpenOA and uses the BSD 3-Clause License.
