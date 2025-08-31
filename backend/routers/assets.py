"""
Router for Asset Mapping API endpoints.

This module provides REST APIs to:
1. Fetch all asset mapping data from CSV
2. Filter assets by state, district, or village
3. Add new asset mapping records

The dataset used: data/asset_mapping.csv

Author: Amal Prasad Trivedi
"""

from fastapi import APIRouter, HTTPException
from typing import Optional
import pandas as pd
import os

# Import utility functions
from backend.utils.file_io import load_csv, save_csv
from backend.utils.preprocessing import clean_numeric

# ---------------------------
# CONFIGURATION
# ---------------------------
DATA_PATH = "data/asset_mapping.csv"
router = APIRouter()

# ---------------------------
# HELPER FUNCTION
# ---------------------------

def get_asset_data() -> pd.DataFrame:
    """Load and clean asset mapping dataset."""
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="Asset mapping dataset not found")
    df = load_csv(DATA_PATH)
    df = clean_numeric(df)
    return df

# ---------------------------
# API ENDPOINTS
# ---------------------------

@router.get("/all")
def get_all_assets():
    """
    Get all asset mapping data.
    Returns the entire dataset as a list of dictionaries.
    """
    df = get_asset_data()
    return df.to_dict(orient="records")


@router.get("/filter")
def filter_assets(
    state_code: Optional[int] = None,
    district_code: Optional[int] = None,
    village_id: Optional[int] = None,
):
    """
    Filter asset mapping data by state, district, or village.
    Example:
        /assets/filter?state_code=23
        /assets/filter?state_code=23&district_code=101
    """
    df = get_asset_data()

    if state_code:
        df = df[df["State_Code"] == state_code]
    if district_code:
        df = df[df["District_Code"] == district_code]
    if village_id:
        df = df[df["Village_ID"] == village_id]

    if df.empty:
        raise HTTPException(status_code=404, detail="No records found for given filter")

    return df.to_dict(orient="records")


@router.post("/add")
def add_asset(record: dict):
    """
    Add a new asset mapping record to the dataset.
    The record must contain all required fields:
        State_Code, District_Code, Village_ID,
        Agri_Land_ha, Forest_Area_ha,
        WaterBodies_Count, Water_Area_ha, Homesteads_Count
    """
    required_columns = [
        "State_Code",
        "District_Code",
        "Village_ID",
        "Agri_Land_ha",
        "Forest_Area_ha",
        "WaterBodies_Count",
        "Water_Area_ha",
        "Homesteads_Count",
    ]

    for col in required_columns:
        if col not in record:
            raise HTTPException(status_code=400, detail=f"Missing field: {col}")

    df = get_asset_data()

    # Append new record
    new_df = pd.DataFrame([record])
    df = pd.concat([df, new_df], ignore_index=True)

    # Save back to CSV
    save_csv(df, DATA_PATH)

    return {"message": "✅ Asset record added successfully", "record": record}
