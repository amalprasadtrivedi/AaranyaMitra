"""
Service layer for Asset Mapping.

This file contains business logic for handling asset mapping data:
1. Load and clean asset dataset.
2. Get all asset records.
3. Filter assets by state/district/village.
4. Add new asset mapping records.

The router (assets.py) calls these service functions to serve requests.

Author: Amal Prasad Trivedi
"""

import os
import pandas as pd
from fastapi import HTTPException

# Import utility functions
from backend.utils.file_io import load_csv, save_csv
from backend.utils.preprocessing import clean_numeric

# ---------------------------
# CONFIGURATION
# ---------------------------
DATA_PATH = "data/asset_mapping.csv"


# ---------------------------
# CORE FUNCTIONS
# ---------------------------

def get_asset_data() -> pd.DataFrame:
    """
    Load and clean asset mapping dataset.
    Returns a pandas DataFrame.
    """
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="Asset mapping dataset not found")

    df = load_csv(DATA_PATH)
    df = clean_numeric(df)
    return df


def get_all_assets() -> list:
    """
    Get all asset mapping records as a list of dictionaries.
    """
    df = get_asset_data()
    return df.to_dict(orient="records")


def filter_assets(state_code: int = None, district_code: int = None, village_id: int = None) -> list:
    """
    Filter asset mapping dataset by state, district, or village.
    Returns list of matching records.

    Args:
        state_code (int, optional): Filter by state code
        district_code (int, optional): Filter by district code
        village_id (int, optional): Filter by village ID
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


def add_asset(record: dict) -> dict:
    """
    Add a new asset mapping record to the dataset.

    Args:
        record (dict): Dictionary containing asset details

    Required fields:
        State_Code, District_Code, Village_ID,
        Agri_Land_ha, Forest_Area_ha,
        WaterBodies_Count, Water_Area_ha, Homesteads_Count

    Returns:
        dict: Confirmation message and added record
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

    # Save updated dataset
    save_csv(df, DATA_PATH)

    return {"message": "✅ Asset record added successfully", "record": record}
