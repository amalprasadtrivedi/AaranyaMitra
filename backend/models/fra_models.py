"""
Pydantic models (schemas) for FRA Claims.

These models define the structure of request and response data
for the FRA router and ensure automatic validation.

Author: Amal Prasad Trivedi
"""

from pydantic import BaseModel, Field, conint, confloat
from typing import Optional


# ---------------------------
# REQUEST MODELS
# ---------------------------

class FRAClaimBase(BaseModel):
    """
    Base model for FRA claim containing common fields.
    """
    State_Code: conint(ge=1) = Field(..., description="Numeric code of the state")
    District_Code: conint(ge=1) = Field(..., description="Numeric code of the district")
    Village_ID: conint(ge=1) = Field(..., description="Unique village ID")

    FRA_Type: str = Field(..., description="Type of FRA (e.g., Individual/Community)")

    Claims_Filed: conint(ge=0) = Field(..., description="Number of FRA claims filed")
    Claims_Verified: conint(ge=0) = Field(..., description="Number of claims verified")
    Patas_Granted: conint(ge=0) = Field(..., description="Number of Patas (land titles) granted")

    Area_Claimed_ha: confloat(ge=0) = Field(..., description="Total area claimed in hectares")
    Area_Granted_ha: confloat(ge=0) = Field(..., description="Total area granted in hectares")


class FRAClaimCreate(FRAClaimBase):
    """
    Request model for creating a new FRA claim.
    Inherits all required fields from FRAClaimBase.
    """
    pass


# ---------------------------
# RESPONSE MODELS
# ---------------------------

class FRAClaim(FRAClaimBase):
    """
    Response model for returning FRA claim data.
    """
    id: Optional[int] = Field(None, description="Optional record ID (if available in DB)")


class FRAResponse(BaseModel):
    """
    Standard API response for FRA operations.
    """
    message: str = Field(..., description="Status message for the operation")
    record: FRAClaim
