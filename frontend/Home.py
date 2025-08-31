"""
Streamlit Frontend Entrypoint for AaranyaMitra

This is the main entry file for the Streamlit app.
It provides:
1. Sidebar navigation across multiple pages.
2. A visually engaging homepage with multiple sections.
3. Links to each functional module (FRA Atlas, Asset Mapping, Socio-Economic Data, DSS).

Author: Amal Prasad Trivedi
"""

import os
import streamlit as st


# ---------------------------
# PAGE CONFIGURATION
# ---------------------------
st.set_page_config(
    page_title="AaranyaMitra",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


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


# ---------------------------
# HOME PAGE - MULTI SECTION
# ---------------------------

# Title Banner
st.title("🌿 AaranyaMitra - AI for Forest Rights & Rural Development")
st.markdown(
    """
    Welcome to **AaranyaMitra**, a next-generation **Decision Support System (DSS)**  
    designed to empower **communities and policymakers** with **AI-driven insights**  
    on Forest Rights Act (FRA) claims, rural assets, and socio-economic development.  
    """
)

# ---------------------------------
# Section 1: Vision
# ---------------------------------
st.header("🌟 Our Vision")
st.markdown(
    """
    AaranyaMitra envisions **sustainable rural growth** by:
    - 📊 **Analyzing FRA Claims** for fairness & transparency.  
    - 🏡 **Mapping Rural Assets** like land, water, and forest resources.  
    - 👥 **Understanding Socio-Economic Conditions** including literacy, poverty & livelihoods.  
    - 🧠 **Providing AI-Driven Recommendations** for policymakers and villagers alike.  
    """
)
st.info("💡 Goal: Balance *development* with *forest conservation* while uplifting rural communities.")


# ---------------------------------
# Section 2: Features
# ---------------------------------
st.header("🛠️ Key Features")
col1, col2 = st.columns(2)

with col1:
    st.success("🗺️ **FRA Atlas** – Visualize FRA claims, verifications, and granted land.")
    st.success("🏡 **Asset Mapping** – Explore agriculture, water, and homestead resources.")

with col2:
    st.info("👥 **Socio-Economic Explorer** – Analyze poverty, literacy & tribal demographics.")
    st.warning("🧠 **DSS Recommendations** – AI-powered insights for decision-making.")

st.markdown("---")


# ---------------------------------
# Section 3: Why AaranyaMitra?
# ---------------------------------
st.header("🤔 Why AaranyaMitra?")
st.markdown(
    """
    Traditional development models often overlook **local conditions** and **indigenous rights**.  
    AaranyaMitra bridges this gap by combining:  

    - 📑 **Data from FRA claims**  
    - 🛰️ **AI-based land & water mapping**  
    - 📉 **Socio-economic indicators**  
    - 🔮 **Predictive DSS Models**  

    Together, they enable **informed, transparent, and sustainable rural development**.
    """
)


# ---------------------------------
# Section 4: How It Works
# ---------------------------------
st.header("⚙️ How It Works")
steps = [
    "📥 **Data Collection** – FRA claims, rural assets, socio-economic indicators.",
    "🧹 **Preprocessing** – Cleaning & validating the datasets.",
    "🤖 **Machine Learning Models** – Predict land use, water index, productivity.",
    "🧠 **Decision Support System (DSS)** – AI + rules to generate recommendations.",
    "📊 **Interactive Dashboards** – Visual insights for policymakers & villagers."
]
for step in steps:
    st.markdown(f"- {step}")


# ---------------------------------
# Section 5: Get Started
# ---------------------------------
st.header("🚀 Get Started")
st.markdown(
    """
    👉 Use the **sidebar** to explore AaranyaMitra modules:  
    - 🗺️ FRA Atlas  
    - 🏡 Asset Mapping  
    - 👥 Socio-Economic Data Explorer  
    - 🧠 DSS Recommendations  

    Each module provides **interactive dashboards, AI insights, and actionable suggestions**.
    """
)

st.success("✨ Tip: Try the **DSS Module** for AI-driven recommendations tailored to your inputs!")

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

