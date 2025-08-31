"""
Utility functions for preprocessing datasets.

This module provides helper functions to:
1. Clean numeric columns (convert strings to numbers, handle NaN).
2. Standardize column names.
3. Handle missing values safely.

These preprocessing functions are used across services
before running business logic or ML models.

Author: Amal Prasad Trivedi
"""

import pandas as pd
import numpy as np


# ---------------------------
# NUMERIC CLEANING
# ---------------------------

def clean_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert all numeric-looking columns to numeric dtype.
    Handles strings like "NaN", "unknown", "-", etc.

    Args:
        df (pd.DataFrame): Input DataFrame

    Returns:
        pd.DataFrame: Cleaned DataFrame with numeric values converted
    """
    for col in df.columns:
        # Try converting column to numeric
        df[col] = pd.to_numeric(df[col], errors="ignore")

        # If conversion fails, leave it as string
        if df[col].dtype == object:
            # Replace common placeholders with NaN
            df[col] = df[col].replace(
                ["NaN", "nan", "NULL", "null", "None", "-", ""], np.nan
            )

            # Try numeric conversion again
            df[col] = pd.to_numeric(df[col], errors="ignore")

    return df


# ---------------------------
# HANDLE MISSING VALUES
# ---------------------------

def fill_missing(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
    """
    Fill missing values in numeric columns.

    Args:
        df (pd.DataFrame): Input DataFrame
        strategy (str): Strategy for filling values ("mean", "median", "zero")

    Returns:
        pd.DataFrame: DataFrame with missing values filled
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        if strategy == "mean":
            df[col] = df[col].fillna(df[col].mean())
        elif strategy == "median":
            df[col] = df[col].fillna(df[col].median())
        elif strategy == "zero":
            df[col] = df[col].fillna(0)
        else:
            raise ValueError("Invalid strategy. Use 'mean', 'median', or 'zero'.")

    return df


# ---------------------------
# COLUMN NAME STANDARDIZATION
# ---------------------------

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names by:
    - Stripping whitespace
    - Converting to lowercase
    - Replacing spaces with underscores

    Args:
        df (pd.DataFrame): Input DataFrame

    Returns:
        pd.DataFrame: DataFrame with standardized column names
    """
    df.columns = (
        df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")
    )
    return df
