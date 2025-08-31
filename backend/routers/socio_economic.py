"""
Router for Socio-Economic API endpoints.

This module provides REST APIs to:
1. Fetch all socio-economic data from CSV
2. Filter socio-economic data by state, district, or village
3. Add new socio-economic records

The dataset used: data/socio_economic.csv

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
DATA_PATH = "data/socio_economic.csv"
router = APIRouter()

# ---------------------------
# HELPER FUNCTION
# ---------------------------

def get_socio_data() -> pd.DataFrame:
    """Load and clean socio-economic dataset."""
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="Socio-economic dataset not found")
    df = load_csv(DATA_PATH)
    df = clean_numeric(df)
    return df

# ---------------------------
# API ENDPOINTS
# ---------------------------

@router.get("/all")
def get_all_socio():
    """
    Get all socio-economic data.
    Returns the entire dataset as a list of dictionaries.
    """
    df = get_socio_data()
    return df.to_dict(orient="records")


@router.get("/filter")
def filter_socio(
    state_code: Optional[int] = None,
    district_code: Optional[int] = None,
    village_id: Optional[int] = None,
):
    """
    Filter socio-economic data by state, district, or village.
    Example:
        /socio/filter?state_code=23
        /socio/filter?state_code=23&district_code=101
    """
    df = get_socio_data()

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
def add_socio(record: dict):
    """
    Add a new socio-economic record to the dataset.
    The record must contain all required fields:
        State_Code, District_Code, Village_ID,
        FRA_Households, Tribal_Population,
        Poverty_Index, Literacy_Rate
    """
    required_columns = [
        "State_Code",
        "District_Code",
        "Village_ID",
        "FRA_Households",
        "Tribal_Population",
        "Poverty_Index",
        "Literacy_Rate",
    ]

    for col in required_columns:
        if col not in record:
            raise HTTPException(status_code=400, detail=f"Missing field: {col}")

    df = get_socio_data()

    # Append new record
    new_df = pd.DataFrame([record])
    df = pd.concat([df, new_df], ignore_index=True)

    # Save back to CSV
    save_csv(df, DATA_PATH)

    return {"message": "✅ Socio-economic record added successfully", "record": record}
