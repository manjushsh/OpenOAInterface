# Mock vs Real OpenOA Mode

The OpenOA Web API supports two operating modes to provide flexibility during development and production.

## Overview

| Mode | USE_MOCK_DATA | OpenOA Required | Use Case |
|------|---------------|-----------------|----------|
| **Mock** | `true` (default) | ❌ No | Development, demos, testing frontend |
| **Real** | `false` | ✅ Yes | Production, actual wind plant analysis |

## Mock Mode (Default)

**When to use:**
- Developing and testing the frontend
- Demonstrating the API without real data
- CI/CD pipelines where OpenOA isn't installed
- Quick iteration without dependency overhead

**Characteristics:**
- ✅ No OpenOA installation required
- ✅ Fast, deterministic responses
- ✅ Simulated but realistic data structures
- ✅ Perfect for frontend development
- ⚠️ Returns simulated analysis results

**Example response:**
```json
{
  "analysis_type": "monte_carlo_aep_mock",
  "aep_gwh": 145.8,
  "uncertainty_pct": 7.3,
  "iterations": 1000,
  "notes": "Mock analysis for demonstration - USE_MOCK_DATA=True"
}
```

## Real Mode

**When to use:**
- Production environment
- Actual wind plant operational assessment
- Research and analysis with real data
- Validating against real OpenOA results

**Characteristics:**
- ✅ Uses actual OpenOA library
- ✅ Real analysis algorithms
- ✅ Production-ready results
- ⚠️ Requires OpenOA installation
- ⚠️ Requires plant data files
- ⚠️ Slower (actual computations)

**Requirements:**
```bash
# Install OpenOA
pip install openoa

# Verify installation
python -c "import openoa; print(openoa.__version__)"
```

**Example response:**
```json
{
  "analysis_type": "monte_carlo_aep_real",
  "aep_gwh": 147.2,
  "uncertainty_pct": 6.8,
  "iterations": 5000,
  "p50_gwh": 147.2,
  "p95_gwh": 139.1,
  "notes": "Real OpenOA analysis using Monte Carlo AEP method"
}
```

## Switching Modes

### Method 1: Environment Variable (Recommended)

```bash
# .env file
USE_MOCK_DATA=false  # Enable real mode

# Or export directly
export USE_MOCK_DATA=false
```

### Method 2: Configuration File

```python
# app/core/config.py already configured
class Settings(BaseSettings):
    use_mock_data: bool = True  # Change to False for real mode
```

### Method 3: Runtime Override

```bash
# Start with real mode
USE_MOCK_DATA=false uvicorn app.main:app --reload

# Start with mock mode (default)
uvicorn app.main:app --reload
```

## Testing Both Modes

The test suite includes tests for both modes:

```bash
# Run all tests (uses mock mode by default)
pytest

# Run mock mode specific tests
pytest tests/test_mock_mode.py -v

# Check test coverage
pytest --cov=app tests/
```

## API Behavior Differences

### Mock Mode Response
```bash
curl -X POST http://localhost:8000/api/v1/analysis/aep \
  -H "Content-Type: application/json" \
  -d '{"iterations": 1000}'
  
# Returns instantly with mock data
# analysis_type: "monte_carlo_aep_mock"
```

### Real Mode Response
```bash
curl -X POST http://localhost:8000/api/v1/analysis/aep \
  -H "Content-Type: application/json" \
  -d '{"iterations": 5000}'
  
# Takes longer, returns real analysis
# analysis_type: "monte_carlo_aep_real"
```

## Deployment Considerations

### Development/Staging
- **Recommended:** Mock mode (`USE_MOCK_DATA=true`)
- Fast feedback for frontend testing
- No OpenOA installation overhead
- Consistent, reproducible results

### Production
- **Required:** Real mode (`USE_MOCK_DATA=false`)
- Add `openoa` to `requirements.txt`
- Ensure plant data files are available
- Configure appropriate data paths
- Monitor performance (real analysis is compute-intensive)

## Troubleshooting

### "ModuleNotFoundError: No module named 'openoa'"
**Solution:** You're in real mode without OpenOA installed
```bash
# Option 1: Switch to mock mode
export USE_MOCK_DATA=true

# Option 2: Install OpenOA
pip install openoa
```

### Mock data doesn't change with different inputs
**Expected behavior:** Mock mode returns deterministic results based on iteration count formula. This is intentional for consistent testing.

### Real mode returns errors
**Check:**
1. OpenOA is installed: `python -c "import openoa"`
2. Plant data files exist in `examples/data/`
3. Sufficient memory for large iteration counts
4. Valid plant metadata configuration

## Performance Comparison

| Metric | Mock Mode | Real Mode |
|--------|-----------|-----------|
| Response time | ~10-50ms | ~500ms-5s |
| Memory usage | ~50MB | ~200-500MB |
| CPU usage | Minimal | Moderate-High |
| OpenOA dependency | None | Required |
| Data accuracy | Simulated | Actual |

## Best Practices

1. **Development:** Always use mock mode for frontend development
2. **Testing:** Use mock mode in CI/CD pipelines
3. **Staging:** Test real mode with smaller datasets first
4. **Production:** Use real mode with monitoring
5. **Documentation:** Clearly indicate which mode in API responses

## Conclusion

The mock/real toggle provides the best of both worlds:
- **Fast iteration** during development
- **Real results** when you need them
- **Easy switching** via environment variable
- **Safe defaults** (mock mode prevents accidental heavy computation)

For interview demos, **mock mode is recommended** to ensure fast, reliable responses without infrastructure dependencies.
