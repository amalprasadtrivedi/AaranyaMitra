"""
Unit Tests for AaranyaMitra Frontend

Since Streamlit apps are UI-driven, direct page rendering cannot be tested like APIs.
Instead, these tests validate:
1. Existence of Streamlit frontend pages.
2. Data loading from CSV files.
3. Availability of trained ML models (.pkl files).
4. Importing frontend components (filters, charts) without errors.

Run tests using:
    pytest tests/test_frontend.py -v
"""

import os
import pytest
import pandas as pd
import joblib


# ---------------------------
# PATH CONSTANTS
# ---------------------------
FRONTEND_DIR = "frontend/pages"
DATA_DIR = "data"
MODELS_DIR = "models"
COMPONENTS_DIR = "frontend/components"


# ---------------------------
# PAGE EXISTENCE TESTS
# ---------------------------
def test_frontend_pages_exist():
    """
    Test that all expected Streamlit frontend pages exist.
    """
    expected_pages = [
        "1_FRA_Atlas.py",
        "2_Asset_Mapping.py",
        "3_SocioEconomic.py",
        "4_DSS.py"
    ]
    for page in expected_pages:
        assert os.path.exists(os.path.join(FRONTEND_DIR, page)), f"❌ Missing page: {page}"


# ---------------------------
# DATA FILE TESTS
# ---------------------------
@pytest.mark.parametrize("filename", [
    "fra_claims.csv",
    "asset_mapping.csv",
    "socio_economic.csv",
    "dss_rules.csv"
])
def test_data_files_exist_and_load(filename):
    """
    Test that required CSV datasets exist and can be loaded.
    """
    path = os.path.join(DATA_DIR, filename)
    assert os.path.exists(path), f"❌ Missing dataset: {filename}"

    # Try loading the CSV into pandas
    df = pd.read_csv(path)
    assert not df.empty, f"❌ Dataset {filename} is empty!"


# ---------------------------
# MODEL FILE TESTS
# ---------------------------
@pytest.mark.parametrize("filename", [
    "land_use_classifier.pkl",
    "water_index_model.pkl",
    "productivity_model.pkl"
])
def test_model_files_exist_and_load(filename):
    """
    Test that ML model pickle files exist and can be loaded.
    """
    path = os.path.join(MODELS_DIR, filename)
    assert os.path.exists(path), f"❌ Missing model file: {filename}"

    # Try loading the model
    model = joblib.load(path)
    assert model is not None, f"❌ Failed to load model {filename}"


# ---------------------------
# COMPONENT IMPORT TESTS
# ---------------------------
def test_import_filters_component():
    """
    Test importing the filters component.
    """
    try:
        from frontend.components import filters
    except Exception as e:
        pytest.fail(f"❌ Failed to import filters.py: {e}")


def test_import_charts_component():
    """
    Test importing the charts component.
    """
    try:
        from frontend.components import charts
    except Exception as e:
        pytest.fail(f"❌ Failed to import charts.py: {e}")
