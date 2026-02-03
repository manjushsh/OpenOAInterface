"""Tests for health check endpoints.

These tests verify that the health and info endpoints
return the expected responses.
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Test suite for health check endpoints."""
    
    def test_health_check_returns_200(self, client: TestClient):
        """Health endpoint should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
    
    def test_health_check_returns_healthy_status(self, client: TestClient):
        """Health endpoint should return healthy status."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_health_check_includes_version(self, client: TestClient):
        """Health response should include version."""
        response = client.get("/health")
        data = response.json()
        assert "version" in data
        assert data["version"] == "1.0.0"
    
    def test_health_check_includes_timestamp(self, client: TestClient):
        """Health response should include timestamp."""
        response = client.get("/health")
        data = response.json()
        assert "timestamp" in data
    
    def test_info_endpoint_returns_200(self, client: TestClient):
        """Info endpoint should return 200 OK."""
        response = client.get("/api/v1/info")
        assert response.status_code == status.HTTP_200_OK
    
    def test_info_endpoint_returns_app_info(self, client: TestClient):
        """Info endpoint should return application information."""
        response = client.get("/api/v1/info")
        data = response.json()
        
        assert "name" in data
        assert "version" in data
        assert "environment" in data
        assert data["name"] == "OpenOA API"
        assert data["version"] == "1.0.0"
    
    def test_info_endpoint_includes_openoa_version(self, client: TestClient):
        """Info endpoint should include OpenOA version if available."""
        response = client.get("/api/v1/info")
        data = response.json()
        
        # OpenOA version may or may not be present depending on installation
        assert "openoa_version" in data


class TestRootEndpoint:
    """Test suite for root endpoint."""
    
    def test_root_returns_200(self, client: TestClient):
        """Root endpoint should return 200 OK."""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
    
    def test_root_returns_welcome_message(self, client: TestClient):
        """Root endpoint should return welcome message."""
        response = client.get("/")
        data = response.json()
        
        assert "message" in data
        assert "OpenOA" in data["message"]
    
    def test_root_includes_api_links(self, client: TestClient):
        """Root endpoint should include helpful links."""
        response = client.get("/")
        data = response.json()
        
        assert "docs" in data
        assert "health" in data
        assert data["docs"] == "/docs"
        assert data["health"] == "/health"
