"""
Service layer for Socio-Economic Data.

This file contains business logic for handling socio-economic data:
1. Load and clean socio-economic dataset.
2. Get all socio-economic records.
3. Filter socio-economic data by state/district/village.
4. Add new socio-economic records.

The router (socio_economic.py) calls these service functions.

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
DATA_PATH = "data/socio_economic.csv"


# ---------------------------
# CORE FUNCTIONS
# ---------------------------

def get_socio_data() -> pd.DataFrame:
    """
    Load and clean socio-economic dataset.
    Returns a pandas DataFrame.
    """
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="Socio-economic dataset not found")

    df = load_csv(DATA_PATH)
    df = clean_numeric(df)
    return df


def get_all_socio() -> list:
    """
    Get all socio-economic records as a list of dictionaries.
    """
    df = get_socio_data()
    return df.to_dict(orient="records")


def filter_socio(state_code: int = None, district_code: int = None, village_id: int = None) -> list:
    """
    Filter socio-economic dataset by state, district, or village.
    Returns list of matching records.

    Args:
        state_code (int, optional): Filter by state code
        district_code (int, optional): Filter by district code
        village_id (int, optional): Filter by village ID
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


def add_socio(record: dict) -> dict:
    """
    Add a new socio-economic record to the dataset.

    Args:
        record (dict): Dictionary containing socio-economic details

    Required fields:
        State_Code, District_Code, Village_ID,
        FRA_Households, Tribal_Population,
        Poverty_Index, Literacy_Rate

    Returns:
        dict: Confirmation message and added record
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

    # Save updated dataset
    save_csv(df, DATA_PATH)

    return {"message": "✅ Socio-economic record added successfully", "record": record}
