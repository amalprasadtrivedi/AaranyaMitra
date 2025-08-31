"""
Streamlit Page 1: FRA Atlas Visualization

This page provides:
1. Filters (State, District, Village) for exploring FRA claims.
2. Summary statistics of FRA claims, verifications, and granted land.
3. Interactive charts (bar and pie).
4. A data table for detailed inspection.
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
st.set_page_config(page_title="FRA Atlas", page_icon="📊", layout="wide")


# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_fra_data():
    """Load FRA claims dataset from CSV."""
    try:
        file_path = os.path.join(os.getcwd(), "data", "fra_claims.csv")
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error("❌ FRA dataset not found! Ensure data/fra_claims.csv exists.")
        return pd.DataFrame()


df = load_fra_data()

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
# FILTERS SECTION
# ---------------------------
st.sidebar.header("🔎 Filters")

if not df.empty:
    # Step 1: State filter
    states = df["State_Code"].unique().tolist()
    state = st.sidebar.selectbox("🏞️ Select State", options=states)

    # Step 2: District filter
    districts = df[df["State_Code"] == state]["District_Code"].unique().tolist()
    district = st.sidebar.selectbox("🏙️ Select District", options=districts)

    # Step 3: Village filter
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
    st.title("📊 FRA Atlas - Claims Overview")
    st.markdown("---")
    st.markdown(
        f"""
        ### 🏞️ Selected Region:
        - **State**: `{state}`
        - **District**: `{district}`
        - **Village**: `{village}`

        Explore the **Forest Rights Act (FRA) claims** data with interactive charts, summaries, and insights.
        """
    )
    st.markdown("---")

    # ---------------------------
    # SECTION 2: Summary Statistics
    # ---------------------------
    if not filtered_df.empty:
        st.header("📌 Summary Statistics")

        total_claims = int(filtered_df["Claims_Filed"].sum())
        verified_claims = int(filtered_df["Claims_Verified"].sum())
        granted_patas = int(filtered_df["Patas_Granted"].sum())
        area_claimed = float(filtered_df["Area_Claimed_ha"].sum())
        area_granted = float(filtered_df["Area_Granted_ha"].sum())

        col1, col2, col3 = st.columns(3)
        col1.metric("📝 Claims Filed", total_claims)
        col2.metric("✅ Claims Verified", verified_claims)
        col3.metric("🏡 Patas Granted", granted_patas)

        col4, col5 = st.columns(2)
        col4.metric("🌱 Area Claimed (ha)", f"{area_claimed:.2f}")
        col5.metric("🌾 Area Granted (ha)", f"{area_granted:.2f}")

        st.markdown("---")

        # ---------------------------
        # SECTION 3: Visual Charts
        # ---------------------------
        st.header("📊 Visual Analysis")

        col_a, col_b = st.columns(2)

        # Bar chart
        with col_a:
            st.subheader("📈 Claims vs Verifications vs Grants")
            fig, ax = plt.subplots()
            ax.bar(["Claims Filed", "Verified", "Patas Granted"],
                   [total_claims, verified_claims, granted_patas],
                   color=["#4CAF50", "#2196F3", "#FF9800"])
            ax.set_ylabel("Count")
            st.pyplot(fig)

        # Pie chart
        with col_b:
            st.subheader("🥧 Area Claimed vs Granted (ha)")
            fig2, ax2 = plt.subplots()
            ax2.pie(
                [area_claimed, area_granted],
                labels=["Claimed", "Granted"],
                autopct="%1.1f%%",
                colors=["#FF7043", "#66BB6A"],
                startangle=90
            )
            ax2.axis("equal")
            st.pyplot(fig2)

        st.markdown("---")

        # ---------------------------
        # SECTION 4: Detailed Data
        # ---------------------------
        st.header("📋 Detailed Data Table")
        st.dataframe(filtered_df, use_container_width=True)

        st.markdown("---")

        # ---------------------------
        # SECTION 5: Insights
        # ---------------------------
        st.header("💡 Insights & Recommendations")

        if granted_patas < (0.5 * verified_claims):
            st.warning("⚠️ A large gap exists between verified claims and granted patta distribution.")
        else:
            st.success("✅ Grant distribution aligns well with verified claims.")

        if area_granted < (0.5 * area_claimed):
            st.error("🚨 Area granted is significantly lower than area claimed. Policy review recommended.")
        else:
            st.info("📊 Claimed vs granted area distribution looks balanced.")

    else:
        st.warning("⚠️ No records found for the selected filters.")
else:
    st.warning("⚠️ Dataset is empty. Please generate FRA data first.")



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
