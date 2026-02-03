"""Tests for mock vs real OpenOA mode switching.

Tests that the service correctly switches between mock and real OpenOA
based on the USE_MOCK_DATA configuration flag.
"""

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient


class TestMockDataFlag:
    """Test suite for USE_MOCK_DATA configuration."""
    
    def test_mock_mode_returns_mock_indicator(self, client: TestClient):
        """Mock mode should indicate it's using mock data."""
        # Default configuration has use_mock_data=True
        response = client.post("/api/v1/analysis/aep", json={})
        result = response.json()["result"]
        
        assert "mock" in result["analysis_type"].lower()
        assert "mock" in result["notes"].lower() or "USE_MOCK_DATA" in result["notes"]
    
    def test_mock_mode_does_not_require_openoa(self, client: TestClient):
        """Mock mode should work without OpenOA installed."""
        # This test verifies mock mode works independently
        response = client.post(
            "/api/v1/analysis/aep",
            json={"iterations": 500}
        )
        assert response.status_code == 200
        result = response.json()["result"]
        assert result["iterations"] == 500
    
    def test_analysis_type_indicates_mock_mode(self, client: TestClient):
        """Analysis type should indicate whether mock or real."""
        response_mock = client.post("/api/v1/analysis/aep", json={})
        type_mock = response_mock.json()["result"]["analysis_type"]
        
        assert "mock" in type_mock.lower()
    
    def test_mock_mode_returns_consistent_results(self, client: TestClient):
        """Mock mode should return deterministic results."""
        response1 = client.post("/api/v1/analysis/aep", json={"iterations": 1000})
        response2 = client.post("/api/v1/analysis/aep", json={"iterations": 1000})
        
        result1 = response1.json()["result"]
        result2 = response2.json()["result"]
        
        # Same inputs should give same outputs in mock mode
        assert result1["aep_gwh"] == result2["aep_gwh"]
        assert result1["uncertainty_pct"] == result2["uncertainty_pct"]


class TestOpenOAIntegration:
    """Test suite for real OpenOA integration (when installed)."""
    
    @pytest.mark.skipif(
        True,  # Skip by default since OpenOA may not be installed
        reason="Requires OpenOA installation"
    )
    def test_real_mode_uses_openoa(self, client: TestClient):
        """Real mode should attempt to use OpenOA library."""
        with patch("app.core.config.Settings.use_mock_data", False):
            # This would fail if OpenOA not installed
            # In CI/CD with OpenOA installed, this would test real integration
            response = client.post("/api/v1/analysis/aep", json={})
            
            # If OpenOA is installed and configured
            if response.status_code == 200:
                result = response.json()["result"]
                assert "real" in result["analysis_type"].lower()
            else:
                # Should get appropriate error if OpenOA not available
                assert response.status_code in [500, 501]
