"""
Main entrypoint for the FastAPI backend of AaranyaMitra.

This file:
1. Creates the FastAPI application instance.
2. Includes API routers for different modules:
   - FRA Claims (fra.py)
   - Asset Mapping (assets.py)
   - Socio-Economic Data (socio_economic.py)
   - Decision Support System (dss.py)
3. Configures CORS (so Streamlit frontend can access the backend).
4. Provides a simple root "/" health-check endpoint.

Run this backend server with:
    uvicorn backend.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from backend.routers import fra, assets, socio_economic, dss

# ---------------------------
# CREATE FASTAPI APP
# ---------------------------
app = FastAPI(
    title="AaranyaMitra Backend",
    description="FastAPI backend for FRA Atlas & DSS system",
    version="1.0.0"
)

# ---------------------------
# ENABLE CORS
# ---------------------------
# This allows the frontend (Streamlit running on another port) to call APIs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# ROUTE REGISTRATION
# ---------------------------
# Include routers for different functional modules
app.include_router(fra.router, prefix="/fra", tags=["FRA Claims"])
app.include_router(assets.router, prefix="/assets", tags=["Asset Mapping"])
app.include_router(socio_economic.router, prefix="/socio", tags=["Socio-Economic"])
app.include_router(dss.router, prefix="/dss", tags=["Decision Support System"])

# ---------------------------
# ROOT ENDPOINT
# ---------------------------
@app.get("/")
def root():
    """
    Root health-check endpoint.
    Can be used to verify that the backend server is running.
    """
    return {"message": "✅ AaranyaMitra Backend is running!"}
