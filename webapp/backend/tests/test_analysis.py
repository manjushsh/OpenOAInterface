"""Tests for analysis endpoints.

Tests AEP analysis and other operational assessment endpoints.
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestAnalysisEndpoints:
    """Test suite for analysis endpoints."""
    
    def test_list_analysis_types_returns_200(self, client: TestClient):
        """List analysis types endpoint should return 200 OK."""
        response = client.get("/api/v1/analysis/types")
        assert response.status_code == status.HTTP_200_OK
    
    def test_list_analysis_types_structure(self, client: TestClient):
        """Analysis types list should have correct structure."""
        response = client.get("/api/v1/analysis/types")
        data = response.json()
        
        assert "analyses" in data
        assert isinstance(data["analyses"], list)
        assert len(data["analyses"]) > 0
        
        # Check first analysis type structure
        first_analysis = data["analyses"][0]
        assert "type" in first_analysis
        assert "name" in first_analysis
        assert "description" in first_analysis
        assert "status" in first_analysis
    
    def test_aep_analysis_returns_200(self, client: TestClient):
        """AEP analysis endpoint should return 200 OK."""
        response = client.post(
            "/api/v1/analysis/aep",
            json={"iterations": 1000}
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_aep_analysis_response_structure(self, client: TestClient):
        """AEP analysis response should have correct structure."""
        response = client.post(
            "/api/v1/analysis/aep",
            json={"iterations": 1000}
        )
        data = response.json()
        
        # Check wrapper fields
        assert "id" in data
        assert "status" in data
        assert "result" in data
        assert "created_at" in data
        assert "completed_at" in data
        
        # Check result structure
        assert data["status"] == "completed"
        assert data["result"] is not None
        
        result = data["result"]
        assert "aep_gwh" in result
        assert "uncertainty_pct" in result
        assert "capacity_factor" in result
        assert "plant_capacity_mw" in result
    
    def test_aep_analysis_has_valid_results(self, client: TestClient):
        """AEP analysis should return valid numerical results."""
        response = client.post(
            "/api/v1/analysis/aep",
            json={"iterations": 1000}
        )
        result = response.json()["result"]
        
        # Check values are positive and reasonable
        assert result["aep_gwh"] > 0
        assert result["uncertainty_pct"] > 0
        assert result["capacity_factor"] > 0
        assert result["capacity_factor"] < 100
        assert result["plant_capacity_mw"] > 0
    
    def test_aep_analysis_generates_unique_id(self, client: TestClient):
        """Each AEP analysis should get a unique ID."""
        response1 = client.post("/api/v1/analysis/aep", json={})
        response2 = client.post("/api/v1/analysis/aep", json={})
        
        id1 = response1.json()["id"]
        id2 = response2.json()["id"]
        
        assert id1 != id2
        assert id1.startswith("aep_")
        assert id2.startswith("aep_")
    
    def test_aep_analysis_with_custom_iterations(self, client: TestClient):
        """AEP analysis should accept custom iteration count."""
        response = client.post(
            "/api/v1/analysis/aep",
            json={"iterations": 500}
        )
        assert response.status_code == status.HTTP_200_OK
        
        result = response.json()["result"]
        assert result["iterations"] == 500
    
    def test_aep_analysis_with_default_iterations(self, client: TestClient):
        """AEP analysis should use default iterations if not specified."""
        response = client.post("/api/v1/analysis/aep", json={})
        assert response.status_code == status.HTTP_200_OK
        
        result = response.json()["result"]
        assert "iterations" in result
    
    def test_aep_analysis_validates_iterations_range(self, client: TestClient):
        """AEP analysis should validate iteration count is in valid range."""
        # Too few iterations
        response = client.post(
            "/api/v1/analysis/aep",
            json={"iterations": 50}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Too many iterations  
        response = client.post(
            "/api/v1/analysis/aep",
            json={"iterations": 50000}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
