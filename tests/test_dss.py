"""
Unit Tests for AaranyaMitra DSS (Decision Support System)

This file focuses ONLY on testing the DSS system:
1. Valid payloads produce predictions + recommendations.
2. Invalid/missing payloads return proper error responses.
3. Edge cases (extremely high/low values) are handled gracefully.

Run tests using:
    pytest tests/test_dss.py -v
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

# Create a FastAPI test client
client = TestClient(app)


# ---------------------------
# HELPER - VALID PAYLOAD
# ---------------------------
def get_valid_payload():
    """Return a sample valid payload for DSS API testing."""
    return {
        "agri_land": 50,
        "forest_area": 30,
        "water_area": 10,
        "water_bodies": 3,
        "productivity": 70,
        "literacy_rate": 60
    }


# ---------------------------
# TESTS
# ---------------------------
def test_dss_valid_payload():
    """
    Test DSS API with a valid payload.
    Expected: 200 OK + predictions + recommendations.
    """
    response = client.post("/dss/recommend", json=get_valid_payload())
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert "recommendations" in data
    assert isinstance(data["predictions"], dict)
    assert isinstance(data["recommendations"], list)


def test_dss_missing_field():
    """
    Test DSS API with a missing field in the payload.
    Expected: 422 Unprocessable Entity.
    """
    payload = get_valid_payload()
    del payload["literacy_rate"]  # remove required field
    response = client.post("/dss/recommend", json=payload)
    assert response.status_code == 422  # FastAPI validation should fail


def test_dss_invalid_field_type():
    """
    Test DSS API with invalid field types.
    Example: Sending a string instead of a number.
    Expected: 422 validation error.
    """
    payload = get_valid_payload()
    payload["agri_land"] = "fifty"  # invalid type
    response = client.post("/dss/recommend", json=payload)
    assert response.status_code == 422


def test_dss_extreme_values():
    """
    Test DSS API with extreme values to check stability.
    Expected: 200 OK with valid response.
    """
    payload = {
        "agri_land": 1000000,  # extremely high
        "forest_area": 0,      # extremely low
        "water_area": 500000,
        "water_bodies": 999,
        "productivity": 0,
        "literacy_rate": 100
    }
    response = client.post("/dss/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert "recommendations" in data
