"""
Utility functions for reading and writing CSV files.

This module provides helper functions to:
1. Load CSV files into pandas DataFrames.
2. Save pandas DataFrames back to CSV files.
3. Handle missing files gracefully with proper error messages.

Author: Amal Prasad Trivedi
"""

import os
import pandas as pd
from fastapi import HTTPException


# ---------------------------
# CSV LOADER
# ---------------------------

def load_csv(path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Args:
        path (str): Path to the CSV file

    Returns:
        pd.DataFrame: Loaded dataset

    Raises:
        HTTPException (404): If the file does not exist
        HTTPException (500): If file cannot be read
    """
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"CSV file not found: {path}")

    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading CSV {path}: {str(e)}")


# ---------------------------
# CSV SAVER
# ---------------------------

def save_csv(df: pd.DataFrame, path: str) -> None:
    """
    Save a pandas DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): DataFrame to save
        path (str): Destination CSV file path

    Raises:
        HTTPException (500): If the file cannot be saved
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving CSV {path}: {str(e)}")
