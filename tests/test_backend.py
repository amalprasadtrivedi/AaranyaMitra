"""
Unit Tests for AaranyaMitra Backend

This file uses pytest + FastAPI TestClient to test:
1. Backend server startup.
2. API endpoints for FRA, Assets, Socio-Economic, and DSS.
3. Response status codes (200 OK).
4. Response data structure (JSON format).

Run tests using:
    pytest tests/test_backend.py -v
"""

import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app
from backend.main import app

# Create a test client
client = TestClient(app)


# ---------------------------
# GENERAL HEALTH CHECK
# ---------------------------
def test_root_endpoint():
    """
    Test that the root API health endpoint returns a success message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "AaranyaMitra Backend API is running" in response.json()["message"]


# ---------------------------
# FRA ENDPOINT TESTS
# ---------------------------
def test_fra_get_all():
    """
    Test FRA API: Fetch all FRA claims.
    """
    response = client.get("/fra/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Response should be a list


def test_fra_get_by_village():
    """
    Test FRA API: Fetch FRA claims for a specific village.
    """
    response = client.get("/fra/village/101")  # Example Village_ID
    assert response.status_code in [200, 404]  # Either data exists or 404
    if response.status_code == 200:
        assert isinstance(response.json(), list)


# ---------------------------
# ASSETS ENDPOINT TESTS
# ---------------------------
def test_assets_get_all():
    """
    Test Assets API: Fetch all asset mapping data.
    """
    response = client.get("/assets/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_assets_get_by_village():
    """
    Test Assets API: Fetch asset mapping for a specific village.
    """
    response = client.get("/assets/village/101")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert isinstance(response.json(), list)


# ---------------------------
# SOCIO-ECONOMIC ENDPOINT TESTS
# ---------------------------
def test_socio_get_all():
    """
    Test Socio-Economic API: Fetch all socio-economic data.
    """
    response = client.get("/socio/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_socio_get_by_village():
    """
    Test Socio-Economic API: Fetch socio-economic data for a village.
    """
    response = client.get("/socio/village/101")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert isinstance(response.json(), list)


# ---------------------------
# DSS ENDPOINT TESTS
# ---------------------------
def test_dss_recommendation():
    """
    Test DSS API: Get recommendations by sending sample payload.
    """
    payload = {
        "agri_land": 50,
        "forest_area": 30,
        "water_area": 10,
        "water_bodies": 3,
        "productivity": 70,
        "literacy_rate": 60
    }
    response = client.post("/dss/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert "recommendations" in data
