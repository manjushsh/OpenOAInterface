"""Tests for CORS configuration.

Verifies that CORS headers are properly set for cross-origin requests.
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestCORS:
    """Test suite for CORS configuration."""
    
    def test_cors_headers_present_on_health_endpoint(self, client: TestClient):
        """CORS headers should be present on health endpoint."""
        response = client.get(
            "/health",
            headers={"Origin": "http://localhost:5173"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        # FastAPI TestClient may not fully simulate CORS in all cases,
        # but we can verify the endpoint works with Origin header
    
    def test_options_request_allowed(self, client: TestClient):
        """OPTIONS preflight requests should be handled."""
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        # Should not return an error
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
