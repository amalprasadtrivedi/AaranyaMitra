"""
Streamlit Page 2: Asset Mapping

This page provides:
1. Filters (State, District, Village) for exploring asset resources.
2. Summary statistics of agricultural land, forest, water bodies, and homesteads.
3. Interactive visualizations (bar chart and pie chart).
4. A detailed data table for inspection.
5. Insights & recommendations.

Author: Amal Prasad Trivedi
"""

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# PAGE CONFIGURATION
# ---------------------------
st.set_page_config(page_title="Asset Mapping", page_icon="🌍", layout="wide")

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_asset_data():
    """Load Asset Mapping dataset from CSV."""
    try:
        file_path = os.path.join(os.getcwd(), "data", "asset_mapping.csv")
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error("❌ Asset dataset not found! Ensure data/asset_mapping.csv exists.")
        return pd.DataFrame()

df = load_asset_data()


# ---------------------------
# SIDEBAR NAVIGATION
# ---------------------------
st.sidebar.title("🌿 AaranyaMitra")
st.sidebar.info("AI powered FRA Atlas and WebGIS-based Decision Support System (DSS) for Integrated Monitoring of Forest Rights Act (FRA).")
st.sidebar.markdown("### 📌 Modules")
st.sidebar.success("Navigate using the sidebar")
st.sidebar.markdown(
    """
    - 🗺️ **FRA Atlas**  
    - 🏡 **Asset Mapping**  
    - 👥 **Socio-Economic Data**  
    - 🧠 **DSS Recommendations**
    """
)
st.sidebar.markdown("---")


# ---------------------------
# FILTERS
# ---------------------------
st.sidebar.header("🔎 Filters")

if not df.empty:
    # State filter
    states = df["State_Code"].unique().tolist()
    state = st.sidebar.selectbox("🏞️ Select State", options=states)

    # District filter
    districts = df[df["State_Code"] == state]["District_Code"].unique().tolist()
    district = st.sidebar.selectbox("🏙️ Select District", options=districts)

    # Village filter
    villages = df[(df["State_Code"] == state) & (df["District_Code"] == district)]["Village_ID"].unique().tolist()
    village = st.sidebar.selectbox("🏡 Select Village", options=villages)

    # Filter dataset
    filtered_df = df[
        (df["State_Code"] == state) &
        (df["District_Code"] == district) &
        (df["Village_ID"] == village)
    ]

    # ---------------------------
    # SECTION 1: Title & Intro
    # ---------------------------
    st.title("🌍 Asset Mapping - Village Resources Overview")
    st.markdown("---")
    st.markdown(
        f"""
        ### 📍 Selected Region:
        - **State**: `{state}`
        - **District**: `{district}`
        - **Village**: `{village}`

        This dashboard helps visualize **natural and man-made resources** of villages,
        including agricultural land, forests, water bodies, and homesteads.
        """
    )
    st.markdown("---")

    # ---------------------------
    # SECTION 2: Summary Statistics
    # ---------------------------
    if not filtered_df.empty:
        st.header("📌 Summary Statistics")

        agri_land = float(filtered_df["Agri_Land_ha"].sum())
        forest_area = float(filtered_df["Forest_Area_ha"].sum())
        water_bodies = int(filtered_df["WaterBodies_Count"].sum())
        water_area = float(filtered_df["Water_Area_ha"].sum())
        homesteads = int(filtered_df["Homesteads_Count"].sum())

        col1, col2, col3 = st.columns(3)
        col1.metric("🌱 Agricultural Land (ha)", f"{agri_land:.2f}")
        col2.metric("🌳 Forest Area (ha)", f"{forest_area:.2f}")
        col3.metric("🏠 Homesteads", homesteads)

        col4, col5 = st.columns(2)
        col4.metric("💧 Water Bodies", water_bodies)
        col5.metric("🌊 Water Area (ha)", f"{water_area:.2f}")

        st.markdown("---")

        # ---------------------------
        # SECTION 3: Visual Charts
        # ---------------------------
        st.header("📊 Visual Analysis")

        col_a, col_b = st.columns(2)

        # Bar chart
        with col_a:
            st.subheader("📈 Land & Resource Distribution")
            fig, ax = plt.subplots()
            ax.bar(
                ["Agricultural Land", "Forest Area", "Water Area"],
                [agri_land, forest_area, water_area],
                color=["#4CAF50", "#2E7D32", "#1976D2"]
            )
            ax.set_ylabel("Hectares")
            st.pyplot(fig)

        # Pie chart
        with col_b:
            st.subheader("🥧 Land Use Composition")
            fig2, ax2 = plt.subplots()
            ax2.pie(
                [agri_land, forest_area, water_area],
                labels=["Agricultural Land", "Forest Area", "Water Area"],
                autopct="%1.1f%%",
                colors=["#81C784", "#388E3C", "#64B5F6"],
                startangle=90
            )
            ax2.axis("equal")
            st.pyplot(fig2)

        st.markdown("---")

        # ---------------------------
        # SECTION 4: Detailed Data Table
        # ---------------------------
        st.header("📋 Detailed Data Table")
        st.dataframe(filtered_df, use_container_width=True)

        st.markdown("---")

        # ---------------------------
        # SECTION 5: Insights
        # ---------------------------
        st.header("💡 Insights & Recommendations")

        if forest_area > agri_land:
            st.warning("🌳 Forest area dominates over agricultural land. Sustainable forestry practices should be prioritized.")
        else:
            st.success("🌱 Agriculture is the primary land use. Focus on irrigation and crop productivity.")

        if water_bodies < 5:
            st.error("🚨 Limited water bodies detected. Water conservation projects are highly recommended.")
        else:
            st.info("💧 Sufficient water resources available for the village.")

        if homesteads > 500:
            st.warning("🏠 High number of homesteads may indicate rising population pressure.")
        else:
            st.success("🏡 Homestead distribution looks manageable.")

    else:
        st.warning("⚠️ No records found for the selected filters.")
else:
    st.warning("⚠️ Dataset is empty. Please generate Asset Mapping data first.")


# External Links
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Connect with Developer")
st.sidebar.link_button("🌐 Portfolio", "https://amalprasadtrivediportfolio.vercel.app/")
st.sidebar.link_button("🔗 LinkedIn", "https://www.linkedin.com/in/amalprasadtrivedi-aiml-engineer")
st.sidebar.markdown("---")

# Footer badge
st.sidebar.markdown(
    """
    <style>
    .sidebar-button-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 10px;
    }
    .sidebar-button img {
        width: 100%;
        max-width: 250px;
    }
    </style>
    <div class="sidebar-button-container">
        <a href="https://amalprasadtrivediportfolio.vercel.app/" target="_blank" class="sidebar-button">
            <img src="https://img.shields.io/badge/Created%20by-Amal%20Prasad%20Trivedi-blue">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Footer
st.markdown("---")
st.caption("© 2025 AaranyaMitra | Built with ❤️ by Amal Prasad Trivedi")