"""
Reusable Filter Components for AaranyaMitra Frontend

This module provides:
1. Sidebar filters for selecting State → District → Village.
2. A reusable function that takes a DataFrame and applies filters.
3. Returns the filtered DataFrame and selected filter values.

Author: Amal Prasad Trivedi
"""

import streamlit as st
import pandas as pd


def apply_filters(df: pd.DataFrame, page_name: str = "Data"):
    """
    Apply sidebar filters (State, District, Village) to a given dataset.

    Args:
        df (pd.DataFrame): Input DataFrame with columns [State_Code, District_Code, Village_ID].
        page_name (str): The page name for context (displayed in sidebar header).

    Returns:
        tuple: (filtered_df, state, district, village)
    """

    if df.empty:
        st.warning(f"⚠️ No data available for {page_name}.")
        return df, None, None, None

    # Sidebar header
    st.sidebar.header(f"🔎 {page_name} Filters")

    # --- State filter ---
    states = sorted(df["State_Code"].dropna().unique().tolist())
    state = st.sidebar.selectbox("Select State", options=states)

    # --- District filter ---
    districts = sorted(df[df["State_Code"] == state]["District_Code"].dropna().unique().tolist())
    district = st.sidebar.selectbox("Select District", options=districts)

    # --- Village filter ---
    villages = sorted(
        df[(df["State_Code"] == state) & (df["District_Code"] == district)]["Village_ID"].dropna().unique().tolist()
    )
    village = st.sidebar.selectbox("Select Village", options=villages)

    # --- Apply filters ---
    filtered_df = df[
        (df["State_Code"] == state)
        & (df["District_Code"] == district)
        & (df["Village_ID"] == village)
    ]

    return filtered_df, state, district, village
