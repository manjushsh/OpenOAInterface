"""Tests for data management endpoints.

Tests sample data retrieval and metadata endpoints.
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestDataEndpoints:
    """Test suite for data management endpoints."""
    
    def test_get_sample_data_summary_returns_200(self, client: TestClient):
        """Sample data summary endpoint should return 200 OK."""
        response = client.get("/api/v1/data/sample/summary")
        assert response.status_code == status.HTTP_200_OK
    
    def test_sample_data_summary_structure(self, client: TestClient):
        """Sample data summary should have correct structure."""
        response = client.get("/api/v1/data/sample/summary")
        data = response.json()
        
        # Check required fields
        assert "plant_name" in data
        assert "capacity_mw" in data
        assert "num_turbines" in data
        assert "data_available" in data
        assert "description" in data
        assert "analyses_available" in data
        
        # Check data types
        assert isinstance(data["plant_name"], str)
        assert isinstance(data["capacity_mw"], (int, float))
        assert isinstance(data["num_turbines"], int)
        assert isinstance(data["data_available"], bool)
        assert isinstance(data["analyses_available"], list)
    
    def test_sample_data_summary_has_valid_values(self, client: TestClient):
        """Sample data summary should have valid values."""
        response = client.get("/api/v1/data/sample/summary")
        data = response.json()
        
        assert data["capacity_mw"] > 0
        assert data["num_turbines"] > 0
        assert data["data_available"] is True
        assert len(data["analyses_available"]) > 0
    
    def test_get_plant_metadata_returns_200(self, client: TestClient):
        """Plant metadata endpoint should return 200 OK."""
        response = client.get("/api/v1/data/sample/metadata")
        assert response.status_code == status.HTTP_200_OK
    
    def test_plant_metadata_structure(self, client: TestClient):
        """Plant metadata should have correct structure."""
        response = client.get("/api/v1/data/sample/metadata")
        data = response.json()
        
        # Check required fields
        assert "name" in data
        assert "capacity" in data
        assert "num_turbines" in data
        assert "asset_list" in data
        
        # Check data types
        assert isinstance(data["name"], str)
        assert isinstance(data["capacity"], (int, float))
        assert isinstance(data["num_turbines"], int)
        assert isinstance(data["asset_list"], list)
    
    def test_plant_metadata_has_turbines(self, client: TestClient):
        """Plant metadata should include turbine information."""
        response = client.get("/api/v1/data/sample/metadata")
        data = response.json()
        
        assert data["num_turbines"] > 0
        assert len(data["asset_list"]) == data["num_turbines"]
    
    def test_plant_metadata_includes_location(self, client: TestClient):
        """Plant metadata may include location data."""
        response = client.get("/api/v1/data/sample/metadata")
        data = response.json()
        
        # Latitude and longitude are optional
        if "latitude" in data:
            assert isinstance(data["latitude"], (int, float))
            assert -90 <= data["latitude"] <= 90
        
        if "longitude" in data:
            assert isinstance(data["longitude"], (int, float))
            assert -180 <= data["longitude"] <= 180
