"""
Router for Decision Support System (DSS) API endpoints.

This module provides REST APIs to:
1. Generate DSS recommendations using ML models
2. Fetch DSS rules from CSV
3. Add new DSS rules

Uses trained models stored in: models/
    - land_use_classifier.pkl
    - water_index_model.pkl
    - productivity_model.pkl

Dataset for rules: data/dss_rules.csv

Author: Amal Prasad Trivedi
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import os
import joblib

# Import utility functions
from backend.utils.file_io import load_csv, save_csv
from backend.utils.preprocessing import clean_numeric

# ---------------------------
# CONFIGURATION
# ---------------------------
DATA_PATH = "data/dss_rules.csv"
MODEL_LAND_USE = "models/land_use_classifier.pkl"
MODEL_WATER = "models/water_index_model.pkl"
MODEL_PRODUCTIVITY = "models/productivity_model.pkl"

router = APIRouter()

# ---------------------------
# LOAD MODELS
# ---------------------------
def load_model(path: str):
    """Helper to load a saved ML model."""
    if not os.path.exists(path):
        raise HTTPException(status_code=500, detail=f"Model file missing: {path}")
    return joblib.load(path)

land_use_model = load_model(MODEL_LAND_USE)
water_model = load_model(MODEL_WATER)
productivity_model = load_model(MODEL_PRODUCTIVITY)

# ---------------------------
# Pydantic Request Model
# ---------------------------
class DSSInput(BaseModel):
    # FRA
    Claims_Filed: int
    Claims_Verified: int
    Patas_Granted: int
    Area_Claimed_ha: float
    Area_Granted_ha: float

    # Assets
    Agri_Land_ha: float
    Forest_Area_ha: float
    WaterBodies_Count: int
    Water_Area_ha: float
    Homesteads_Count: int

    # Socio
    FRA_Households: int
    Tribal_Population: int
    Poverty_Index: float
    Literacy_Rate: float

# ---------------------------
# HELPER FUNCTION: Load Rules
# ---------------------------
def get_rules() -> pd.DataFrame:
    """Load DSS rules dataset."""
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="DSS rules dataset not found")
    df = load_csv(DATA_PATH)
    df = clean_numeric(df)
    return df

# ---------------------------
# API ENDPOINTS
# ---------------------------

@router.post("/recommend")
def recommend_schemes(input_data: DSSInput):
    """
    Generate DSS recommendations using trained ML models.
    Returns:
        - Land Use Prediction
        - Water Index
        - Productivity Index
        - Recommended Schemes (based on heuristic rules)
    """
    data = input_data.dict()

    # Prepare features for each model
    land_features = [
        data["Claims_Filed"],
        data["Claims_Verified"],
        data["Patas_Granted"],
        data["Area_Claimed_ha"],
        data["Area_Granted_ha"],
    ]

    water_features = [
        data["WaterBodies_Count"],
        data["Water_Area_ha"],
        data["Agri_Land_ha"],
    ]

    productivity_features = [
        data["Claims_Filed"],
        data["Claims_Verified"],
        data["Patas_Granted"],
        data["Area_Claimed_ha"],
        data["Area_Granted_ha"],
        data["Agri_Land_ha"],
        data["Forest_Area_ha"],
        data["WaterBodies_Count"],
        data["Water_Area_ha"],
        data["Homesteads_Count"],
        data["FRA_Households"],
        data["Tribal_Population"],
        data["Poverty_Index"],
        data["Literacy_Rate"],
    ]

    # Run predictions
    land_use_pred = land_use_model.predict([land_features])[0]
    water_index = water_model.predict([water_features])[0]
    productivity_index = productivity_model.predict([productivity_features])[0]

    # Simple heuristic-based scheme recommendations
    recommendations = []
    if productivity_index < 40:
        recommendations.append("MGNREGA")
    if water_index < 50:
        recommendations.append("Jal Jeevan Mission")
    if land_use_pred == 1:  # Assume 1 = agriculture land
        recommendations.append("PM-KISAN Yojana")

    return {
        "Land_Use_Prediction": int(land_use_pred),
        "Water_Index": round(float(water_index), 2),
        "Productivity_Index": round(float(productivity_index), 2),
        "Recommended_Schemes": recommendations,
    }


@router.get("/rules")
def get_dss_rules():
    """
    Get all DSS rules from CSV.
    """
    df = get_rules()
    return df.to_dict(orient="records")


@router.post("/add")
def add_dss_rule(record: dict):
    """
    Add a new DSS rule record to the dataset.
    The record must contain fields consistent with data/dss_rules.csv
    """
    df = get_rules()

    new_df = pd.DataFrame([record])
    df = pd.concat([df, new_df], ignore_index=True)

    save_csv(df, DATA_PATH)

    return {"message": "✅ DSS rule added successfully", "record": record}
