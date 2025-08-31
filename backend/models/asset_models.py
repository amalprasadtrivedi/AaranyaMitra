"""
Pydantic models (schemas) for Asset Mapping.

These models define the structure of request and response data
for the Asset Mapping router and ensure automatic validation.

Author: Amal Prasad Trivedi
"""

from pydantic import BaseModel, Field, conint, confloat
from typing import Optional


# ---------------------------
# REQUEST MODELS
# ---------------------------

class AssetBase(BaseModel):
    """
    Base model for Asset Mapping containing common fields.
    """
    State_Code: conint(ge=1) = Field(..., description="Numeric code of the state")
    District_Code: conint(ge=1) = Field(..., description="Numeric code of the district")
    Village_ID: conint(ge=1) = Field(..., description="Unique village ID")

    Agri_Land_ha: confloat(ge=0) = Field(..., description="Agricultural land in hectares")
    Forest_Area_ha: confloat(ge=0) = Field(..., description="Forest area in hectares")
    WaterBodies_Count: conint(ge=0) = Field(..., description="Number of water bodies")
    Water_Area_ha: confloat(ge=0) = Field(..., description="Total water area in hectares")
    Homesteads_Count: conint(ge=0) = Field(..., description="Number of homestead units")


class AssetCreate(AssetBase):
    """
    Request model for creating a new Asset record.
    Inherits all required fields from AssetBase.
    """
    pass


# ---------------------------
# RESPONSE MODELS
# ---------------------------

class AssetRecord(AssetBase):
    """
    Response model for returning Asset Mapping data.
    """
    id: Optional[int] = Field(None, description="Optional record ID (if available in DB)")


class AssetResponse(BaseModel):
    """
    Standard API response for Asset Mapping operations.
    """
    message: str = Field(..., description="Status message for the operation")
    record: AssetRecord
