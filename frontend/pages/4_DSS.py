"""
Streamlit Page 4: DSS Recommendations

This page provides:
1. User inputs for land, water, and productivity indicators.
2. AI model predictions from pre-trained ML models.
3. DSS rule-based recommendations loaded from CSV.
4. A combined dashboard of predictions + development suggestions.

Author: Amal Prasad Trivedi
"""

import os
import streamlit as st
import pandas as pd
import joblib

# ---------------------------
# PAGE CONFIGURATION
# ---------------------------
st.set_page_config(page_title="DSS Recommendations", page_icon="🧠", layout="wide")

# ---------------------------
# LOAD MODELS
# ---------------------------
@st.cache_resource
def load_models():
    """Load trained ML models from /models directory."""
    models = {}
    try:
        models["land_use"] = joblib.load("models/land_use_classifier.pkl")
        models["water_index"] = joblib.load("models/water_index_model.pkl")
        models["productivity"] = joblib.load("models/productivity_model.pkl")
    except Exception as e:
        st.error(f"❌ Error loading models: {e}")
    return models

# ---------------------------
# LOAD DSS RULES
# ---------------------------
@st.cache_data
def load_rules():
    """Load DSS rules from CSV file."""
    try:
        file_path = os.path.join(os.getcwd(), "data", "dss_rules.csv")
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error("❌ DSS rules file not found! Ensure data/dss_rules.csv exists.")
        return pd.DataFrame()

# ================================
# FEATURE SCHEMA PER MODEL
# ================================
land_use_features = ["agri_land", "forest_area", "water_area", "water_bodies", "productivity"]
water_index_features = ["agri_land", "forest_area", "water_area", "water_bodies", "literacy_rate"]
productivity_features = [
    "FRA_Households", "Tribal_Population", "Poverty_Index", "Literacy_Rate",
    "agri_land", "forest_area", "water_area", "water_bodies",
    "claim_area", "recognized_area", "pending_area", "rejected_area",
    "avg_land_size", "forest_dependence"
]

# ================================
# HELPER FUNCTIONS
# ================================
def prepare_features(df_row, features):
    """Pick required features in correct order for prediction."""
    return [[df_row[feat] for feat in features]]

models = load_models()
rules_df = load_rules()


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
# SECTION 1: Title & Introduction
# ---------------------------
st.title("🧠 DSS Recommendations - AI Powered Insights")
st.markdown("---")
st.markdown(
    """
    Welcome to the **Decision Support System (DSS)** module of 🌿 **AaranyaMitra**.  
    Here, you can input **land, water, and socio-economic indicators** to generate:
    - 🤖 AI model predictions (Land Use, Water Index, Productivity Score)  
    - 📝 Rule-based recommendations from DSS guidelines  
    - 💡 Actionable insights for development  

    ---
    """
)

# ---------------------------
# SECTION 2: User Input Form
# ---------------------------
st.header("✍️ Enter Village Parameters")
st.markdown("Fill in the socio-economic and environmental values for your village:")

with st.form("dss_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        agri_land = st.number_input("🌱 Agricultural Land (ha)", min_value=0.0, step=0.1)
        forest_area = st.number_input("🌳 Forest Area (ha)", min_value=0.0, step=0.1)

    with col2:
        water_area = st.number_input("💧 Water Area (ha)", min_value=0.0, step=0.1)
        water_bodies = st.number_input("🏞️ Water Bodies Count", min_value=0, step=1)

    with col3:
        productivity = st.number_input("🌾 Productivity Index", min_value=0.0, step=0.1)
        literacy_rate = st.number_input("📚 Literacy Rate (%)", min_value=0.0, max_value=100.0, step=0.1)

    submitted = st.form_submit_button("🔍 Analyze")

# ---------------------------
# SECTION 3: AI Model Predictions
# ---------------------------
if submitted:
    st.header("📊 AI Model Predictions")

    predictions = {}
    row = {
        "agri_land": agri_land,
        "forest_area": forest_area,
        "water_area": water_area,
        "water_bodies": water_bodies,
        "productivity": productivity,
        "literacy_rate": literacy_rate,

        # Default values for missing features
        "FRA_Households": 50,
        "Tribal_Population": 200,
        "Poverty_Index": 25,
        "Literacy_Rate": literacy_rate,
        "claim_area": 10,
        "recognized_area": 8,
        "pending_area": 2,
        "rejected_area": 1,
        "avg_land_size": 1.5,
        "forest_dependence": 70
    }

    # Land Use
    try:
        if "land_use" in models:
            X_land = prepare_features(row, land_use_features)
            pred = models["land_use"].predict(X_land)[0]
            predictions["Land Use Class"] = int(pred)
            st.success(f"🌱 Land Use Class → **{pred}**")
    except Exception as e:
        st.error(f"⚠️ Land Use Model Error: {e}")

    # Water Index
    try:
        if "water_index" in models:
            X_water = prepare_features(row, water_index_features)
            pred = models["water_index"].predict(X_water)[0]
            predictions["Water Index"] = float(pred)
            st.info(f"💧 Water Index → **{pred:.2f}**")
    except Exception as e:
        st.error(f"⚠️ Water Index Model Error: {e}")

    # Productivity
    try:
        if "productivity" in models:
            X_prod = prepare_features(row, productivity_features)
            pred = models["productivity"].predict(X_prod)[0]
            predictions["Productivity Score"] = float(pred)
            st.warning(f"🌾 Productivity Score → **{pred:.2f}**")
    except Exception as e:
        st.error(f"⚠️ Productivity Model Error: {e}")

    st.markdown("---")

    # ---------------------------
    # SECTION 4: DSS Rule-Based Recommendations
    # ---------------------------
    st.header("📝 DSS Rule-Based Recommendations")
    if not rules_df.empty:
        recommendations = []
        for _, r in rules_df.iterrows():
            if literacy_rate < r.get("min_literacy", 0) or predictions.get("Productivity Score", 100) < r.get("min_productivity", 0):
                recommendations.append(f"✅ {r['recommendation']}")

        if recommendations:
            for rec in recommendations:
                st.write(rec)
        else:
            st.success("✨ No specific DSS recommendations triggered. Situation looks balanced.")
    else:
        st.warning("⚠️ No DSS rules available for recommendations.")

    st.markdown("---")

    # ---------------------------
    # SECTION 5: Insights Dashboard
    # ---------------------------
    st.header("💡 Insights Dashboard")

    colA, colB, colC = st.columns(3)
    colA.metric("🌱 Agricultural Land", f"{agri_land:.2f} ha")
    colB.metric("💧 Water Area", f"{water_area:.2f} ha")
    colC.metric("📚 Literacy Rate", f"{literacy_rate:.2f}%")

    if predictions:
        colX, colY = st.columns(2)
        colX.metric("🌾 Predicted Productivity Score", f"{predictions.get('Productivity Score', 0):.2f}")
        colY.metric("💧 Predicted Water Index", f"{predictions.get('Water Index', 0):.2f}")

    st.info("📊 These indicators highlight strengths and weaknesses, helping decision makers prioritize interventions.")


# External Links
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
