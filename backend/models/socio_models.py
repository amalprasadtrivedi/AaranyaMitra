"""
Pydantic models (schemas) for Socio-Economic Data.

These models define the structure of request and response data
for the Socio-Economic router and ensure automatic validation.

Author: Amal Prasad Trivedi
"""

from pydantic import BaseModel, Field, conint, confloat
from typing import Optional


# ---------------------------
# REQUEST MODELS
# ---------------------------

class SocioBase(BaseModel):
    """
    Base model for Socio-Economic Data containing common fields.
    """
    State_Code: conint(ge=1) = Field(..., description="Numeric code of the state")
    District_Code: conint(ge=1) = Field(..., description="Numeric code of the district")
    Village_ID: conint(ge=1) = Field(..., description="Unique village ID")

    FRA_Households: conint(ge=0) = Field(..., description="Number of FRA-eligible households")
    Tribal_Population: conint(ge=0) = Field(..., description="Total tribal population in the village")
    Poverty_Index: confloat(ge=0, le=100) = Field(..., description="Poverty index (0-100 scale)")
    Literacy_Rate: confloat(ge=0, le=100) = Field(..., description="Literacy rate in percentage (0-100)")


class SocioCreate(SocioBase):
    """
    Request model for creating a new Socio-Economic record.
    Inherits all required fields from SocioBase.
    """
    pass


# ---------------------------
# RESPONSE MODELS
# ---------------------------

class SocioRecord(SocioBase):
    """
    Response model for returning Socio-Economic data.
    """
    id: Optional[int] = Field(None, description="Optional record ID (if available in DB)")


class SocioResponse(BaseModel):
    """
    Standard API response for Socio-Economic operations.
    """
    message: str = Field(..., description="Status message for the operation")
    record: SocioRecord
