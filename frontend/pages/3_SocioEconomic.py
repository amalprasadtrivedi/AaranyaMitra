"""
Streamlit Page 3: Socio-Economic Data Explorer

This page provides:
1. Filters (State, District, Village) for exploring socio-economic indicators.
2. Summary statistics of households, tribal population, poverty, and literacy.
3. Interactive visualizations (bar chart and pie chart).
4. A detailed data table for inspection.
5. AI-inspired insights & recommendations.

Author: Amal Prasad Trivedi
"""

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# PAGE CONFIGURATION
# ---------------------------
st.set_page_config(page_title="Socio-Economic Data", page_icon="👥", layout="wide")

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_socio_data():
    """Load socio-economic dataset from CSV."""
    try:
        file_path = os.path.join(os.getcwd(), "data", "socio_economic.csv")
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error("❌ Socio-economic dataset not found! Ensure data/socio_economic.csv exists.")
        return pd.DataFrame()

df = load_socio_data()


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
    st.title("👥 Socio-Economic Data Explorer")
    st.markdown("---")
    st.markdown(
        f"""
        ### 📍 Selected Region:
        - **State**: `{state}`
        - **District**: `{district}`
        - **Village**: `{village}`

        Explore **households, tribal population, poverty index, and literacy rates** 
        to better understand socio-economic conditions of the region.
        """
    )
    st.markdown("---")

    # ---------------------------
    # SECTION 2: Summary Statistics
    # ---------------------------
    if not filtered_df.empty:
        st.header("📌 Summary Statistics")

        households = int(filtered_df["FRA_Households"].sum())
        tribal_population = int(filtered_df["Tribal_Population"].sum())
        poverty_index = float(filtered_df["Poverty_Index"].mean())
        literacy_rate = float(filtered_df["Literacy_Rate"].mean())

        col1, col2 = st.columns(2)
        col1.metric("🏠 FRA Households", households)
        col2.metric("🧑‍🤝‍🧑 Tribal Population", tribal_population)

        col3, col4 = st.columns(2)
        col3.metric("📉 Poverty Index", f"{poverty_index:.2f} %")
        col4.metric("📚 Literacy Rate", f"{literacy_rate:.2f} %")

        st.markdown("---")

        # ---------------------------
        # SECTION 3: Visual Analysis
        # ---------------------------
        st.header("📊 Visual Analysis")

        col_a, col_b = st.columns(2)

        # Bar chart
        with col_a:
            st.subheader("🏡 Households vs Tribal Population")
            fig, ax = plt.subplots()
            ax.bar(
                ["Households", "Tribal Population"],
                [households, tribal_population],
                color=["#e67e22", "#2980b9"]
            )
            ax.set_ylabel("Count")
            st.pyplot(fig)

        # Pie chart
        with col_b:
            st.subheader("🥧 Poverty vs Literacy Distribution (%)")
            fig2, ax2 = plt.subplots()
            ax2.pie(
                [poverty_index, literacy_rate, 100 - (poverty_index + literacy_rate) if poverty_index + literacy_rate <= 100 else 0],
                labels=["Poverty Index", "Literacy Rate", "Other"],
                autopct="%1.1f%%",
                colors=["#c0392b", "#27ae60", "#95a5a6"],
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
        # SECTION 5: Insights & Recommendations
        # ---------------------------
        st.header("💡 Insights & Recommendations")

        if poverty_index > 40:
            st.error("🚨 High poverty levels detected. Immediate intervention programs are required.")
        else:
            st.success("✅ Poverty levels are manageable.")

        if literacy_rate < 50:
            st.warning("📚 Low literacy rate detected. Adult education and school programs are necessary.")
        else:
            st.info("✨ Literacy levels are at an acceptable level.")

        if tribal_population > (households * 0.5):
            st.warning("🧑‍🤝‍🧑 Majority of population is tribal. Consider specialized welfare schemes.")
        else:
            st.success("🌍 Balanced tribal and non-tribal distribution.")

    else:
        st.warning("⚠️ No records found for the selected filters.")
else:
    st.warning("⚠️ Dataset is empty. Please generate Socio-Economic data first.")



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
