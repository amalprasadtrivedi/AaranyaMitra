# 🌿 AaranyaMitra — AI for Forest Rights & Rural Development

**AaranyaMitra** is an end-to-end, data-driven Decision Support System (DSS) that unifies **FRA claims**, **village asset mapping**, and **socio-economic indicators** to produce **AI-assisted insights and recommendations**.  
The stack is intentionally lightweight and reproducible:

- **Frontend:** Streamlit (multi-page, interactive dashboards)  
- **Backend:** FastAPI (typed REST API with routers/services/models)  
- **Data:** CSV files as a simple “DB”, plus saved ML models (`.pkl`)  
- **ML:** Scikit-learn models for land-use, water index & productivity

> 💡 This README is your single source of truth for setup, data formats, endpoints, development workflow, troubleshooting, and extensibility.

---

## 📁 Project Structure
```text
AaranyaMitra/
│
├── backend/ # FastAPI backend
│ ├── main.py # FastAPI entrypoint (app = FastAPI())
│ ├── routers/ # API route definitions
│ │ ├── fra.py # Endpoints for FRA claims data
│ │ ├── assets.py # Endpoints for asset mapping
│ │ ├── socio_economic.py # Endpoints for socio-economic data
│ │ └── dss.py # Endpoints for DSS recommendations
│ ├── services/ # Business logic & ML models
│ │ ├── fra_service.py
│ │ ├── asset_service.py
│ │ ├── socio_service.py
│ │ └── dss_service.py
│ ├── models/ # Pydantic models (request/response schemas)
│ │ ├── fra_models.py
│ │ ├── asset_models.py
│ │ ├── socio_models.py
│ │ └── dss_models.py
│ ├── utils/ # Utility functions
│ │ ├── file_io.py # Read/write CSV files
│ │ └── preprocessing.py # Data cleaning
│ └── requirements.txt # Backend dependencies
│
├── frontend/ # Streamlit frontend
│ ├── Home.py # Streamlit entrypoint
│ ├── pages/ # Streamlit multipage apps
│ │ ├── 1_FRA_Atlas.py # FRA Atlas visualization
│ │ ├── 2_Asset_Mapping.py # AI-based asset mapping
│ │ ├── 3_SocioEconomic.py # Socio-economic data explorer
│ │ └── 4_DSS.py # DSS recommendations
│ ├── components/ # Reusable UI components
│ │ ├── filters.py # State/district/village filters
│ │ └── charts.py # Charts, maps, tables
│ └── requirements.txt # Frontend dependencies
│
├── data/ # CSV datasets (acts as DB)
│ ├── fra_claims.csv
│ ├── asset_mapping.csv
│ ├── socio_economic.csv
│ ├── village_ids.csv
│ └── dss_rules.csv
│
├── models/ # Trained AI/ML models (saved as .pkl or .pt)
│ ├── land_use_classifier.pkl
│ ├── water_index_model.pkl
│ └── productivity_model.pkl
│
├── docs/ # Documentation & reports
│ ├── project_doc.md
│ └── api_spec.yaml # OpenAPI spec for FastAPI
│
├── tests/ # Unit tests
│ ├── test_backend.py
│ ├── test_frontend.py
│ └── test_dss.py
│
├── .gitignore
├── README.md
└── run.sh # Script to run backend + frontend together
```

## 🔎 What Problem Does It Solve?

Forest-fringe villages often need **transparent** FRA tracking, **grounded** asset inventories (land, forest, water, homestead), and **contextual** socio-economic views (literacy, poverty, tribal demographics). AaranyaMitra:

1. **Aggregates** village-level indicators from CSVs (easy to replace with DB later).
2. **Exposes** a typed REST API for analytics and dashboards.
3. **Predicts** outcomes with pretrained models:
   - Land use class (classification)
   - Water index (regression)
   - Productivity (regression)
4. **Recommends** actions using a lightweight rules engine (CSV-driven).

---

## 🏗️ Architecture Overview

- **FastAPI** layers:
  - `routers/*`: public endpoints (HTTP → business logic)
  - `services/*`: data access, validation, ML inference
  - `models/*`: Pydantic schemas for requests/responses
  - `utils/*`: CSV IO, preprocessing
- **Streamlit** layers:
  - `Home.py`: landing page & navigation
  - `pages/*`: 1) FRA Atlas, 2) Asset Mapping, 3) Socio-Economic, 4) DSS
  - `components/*`: helpers such as dropdown filters and charts
- **Data/Models**:
  - CSVs under `data/` act as a database
  - Trained scikit-learn models under `models/`

> This modular design lets you swap the data store and retrain models independently without breaking the UI or API.

---

## ✅ Prerequisites

- Python **3.10+** (3.11/3.12/3.13 OK)
- `pip` or `pipx`
- (Optional) **virtualenv** or **conda**
- (Optional) **Node/Make** not required

---

## ⚙️ Environment Setup

From the repository root:

```bash
# 1) Create & activate a virtual environment (recommended)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Install backend dependencies
pip install -r backend/requirements.txt

# 3) Install frontend dependencies
pip install -r frontend/requirements.txt
