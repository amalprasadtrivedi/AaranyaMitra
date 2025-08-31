"""
Service layer for Decision Support System (DSS).

This file contains business logic for DSS:
1. Load trained ML models (land use, water index, productivity).
2. Generate DSS recommendations from input data.
3. Load DSS rules from dataset.
4. Add new DSS rules.

The router (dss.py) calls these service functions to serve requests.

Author: Amal Prasad Trivedi
"""

import os
import joblib
import pandas as pd
from fastapi import HTTPException

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

# ---------------------------
# LOAD MODELS
# ---------------------------

def load_model(path: str):
    """Helper to load a saved ML model."""
    if not os.path.exists(path):
        raise HTTPException(status_code=500, detail=f"Model file missing: {path}")
    return joblib.load(path)

try:
    land_use_model = load_model(MODEL_LAND_USE)
    water_model = load_model(MODEL_WATER)
    productivity_model = load_model(MODEL_PRODUCTIVITY)
except Exception as e:
    # Fail gracefully if models are missing
    land_use_model, water_model, productivity_model = None, None, None


# ---------------------------
# DSS CORE FUNCTIONS
# ---------------------------

def recommend_schemes(data: dict) -> dict:
    """
    Generate DSS recommendations using trained ML models.

    Args:
        data (dict): Dictionary containing FRA, Asset, and Socio values

    Returns:
        dict: Predictions and scheme recommendations
    """
    if not land_use_model or not water_model or not productivity_model:
        raise HTTPException(status_code=500, detail="❌ DSS models are not loaded")

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

    # Simple heuristic rules for scheme recommendations
    recommendations = []
    if productivity_index < 40:
        recommendations.append("MGNREGA")
    if water_index < 50:
        recommendations.append("Jal Jeevan Mission")
    if land_use_pred == 1:  # Assume 1 = agricultural land
        recommendations.append("PM-KISAN Yojana")

    return {
        "Land_Use_Prediction": int(land_use_pred),
        "Water_Index": round(float(water_index), 2),
        "Productivity_Index": round(float(productivity_index), 2),
        "Recommended_Schemes": recommendations,
    }


def get_rules() -> list:
    """
    Load DSS rules dataset and return as list of records.
    """
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="DSS rules dataset not found")

    df = load_csv(DATA_PATH)
    df = clean_numeric(df)
    return df.to_dict(orient="records")


def add_rule(record: dict) -> dict:
    """
    Add a new DSS rule record to the dataset.

    Args:
        record (dict): Dictionary containing DSS rule

    Returns:
        dict: Confirmation message and added record
    """
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="DSS rules dataset not found")

    df = load_csv(DATA_PATH)

    new_df = pd.DataFrame([record])
    df = pd.concat([df, new_df], ignore_index=True)

    save_csv(df, DATA_PATH)

    return {"message": "✅ DSS rule added successfully", "record": record}
