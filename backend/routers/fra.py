"""
Router for FRA Claims API endpoints.

This module provides REST APIs to:
1. Fetch all FRA claims data from CSV
2. Fetch claims for a specific state, district, or village
3. Add new FRA claim entries (append to CSV)

The dataset used: data/fra_claims.csv

Author: Amal Prasad Trivedi
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
import pandas as pd
import os

# Import utility functions
from backend.utils.file_io import load_csv, save_csv
from backend.utils.preprocessing import clean_numeric

# ---------------------------
# CONFIGURATION
# ---------------------------
DATA_PATH = "data/fra_claims.csv"
router = APIRouter()

# ---------------------------
# HELPER FUNCTION
# ---------------------------

def get_fra_data() -> pd.DataFrame:
    """Load and clean FRA claims dataset."""
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="FRA claims dataset not found")
    df = load_csv(DATA_PATH)
    df = clean_numeric(df)
    return df

# ---------------------------
# API ENDPOINTS
# ---------------------------

@router.get("/all")
def get_all_fra_claims():
    """
    Get all FRA claims data.
    Returns the entire dataset as a list of dictionaries.
    """
    df = get_fra_data()
    return df.to_dict(orient="records")


@router.get("/filter")
def filter_fra_claims(
    state_code: Optional[int] = None,
    district_code: Optional[int] = None,
    village_id: Optional[int] = None,
):
    """
    Filter FRA claims data by state, district, or village.
    Example:
        /fra/filter?state_code=23
        /fra/filter?state_code=23&district_code=101
    """
    df = get_fra_data()

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
def add_fra_claim(record: dict):
    """
    Add a new FRA claim record to the dataset.
    The record must contain all required fields:
        State_Code, District_Code, Village_ID,
        FRA_Type, Claims_Filed, Claims_Verified,
        Patas_Granted, Area_Claimed_ha, Area_Granted_ha
    """
    required_columns = [
        "State_Code",
        "District_Code",
        "Village_ID",
        "FRA_Type",
        "Claims_Filed",
        "Claims_Verified",
        "Patas_Granted",
        "Area_Claimed_ha",
        "Area_Granted_ha",
    ]

    for col in required_columns:
        if col not in record:
            raise HTTPException(status_code=400, detail=f"Missing field: {col}")

    df = get_fra_data()

    # Append new record
    new_df = pd.DataFrame([record])
    df = pd.concat([df, new_df], ignore_index=True)

    # Save back to CSV
    save_csv(df, DATA_PATH)

    return {"message": "✅ Record added successfully", "record": record}
