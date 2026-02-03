"""Pytest configuration and fixtures.

This file contains shared fixtures and configuration for all tests.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI application.
    
    Returns:
        TestClient: FastAPI test client instance.
    """
    return TestClient(app)


@pytest.fixture
def test_headers() -> dict:
    """Standard headers for API requests.
    
    Returns:
        dict: HTTP headers for testing.
    """
    return {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
