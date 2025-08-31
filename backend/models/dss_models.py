"""
Pydantic models (schemas) for Decision Support System (DSS).

These models define the structure of:
1. Input data for generating DSS recommendations (ML models).
2. Output format of DSS recommendations.
3. DSS Rules dataset schemas (request/response).

Author: Amal Prasad Trivedi
"""

from pydantic import BaseModel, Field, conint, confloat
from typing import List, Optional


# ---------------------------
# INPUT MODEL FOR DSS
# ---------------------------

class DSSInput(BaseModel):
    """
    Input schema for DSS recommendations.
    Combines FRA, Asset, and Socio-Economic data fields.
    """
    # FRA Features
    Claims_Filed: conint(ge=0) = Field(..., description="Number of FRA claims filed")
    Claims_Verified: conint(ge=0) = Field(..., description="Number of claims verified")
    Patas_Granted: conint(ge=0) = Field(..., description="Number of Patas (land titles) granted")
    Area_Claimed_ha: confloat(ge=0) = Field(..., description="Total area claimed in hectares")
    Area_Granted_ha: confloat(ge=0) = Field(..., description="Total area granted in hectares")

    # Asset Features
    Agri_Land_ha: confloat(ge=0) = Field(..., description="Agricultural land in hectares")
    Forest_Area_ha: confloat(ge=0) = Field(..., description="Forest area in hectares")
    WaterBodies_Count: conint(ge=0) = Field(..., description="Number of water bodies")
    Water_Area_ha: confloat(ge=0) = Field(..., description="Total water area in hectares")
    Homesteads_Count: conint(ge=0) = Field(..., description="Number of homestead units")

    # Socio-Economic Features
    FRA_Households: conint(ge=0) = Field(..., description="Number of FRA-eligible households")
    Tribal_Population: conint(ge=0) = Field(..., description="Total tribal population in the village")
    Poverty_Index: confloat(ge=0, le=100) = Field(..., description="Poverty index (0-100 scale)")
    Literacy_Rate: confloat(ge=0, le=100) = Field(..., description="Literacy rate percentage (0-100)")


# ---------------------------
# OUTPUT MODEL FOR DSS
# ---------------------------

class DSSOutput(BaseModel):
    """
    Output schema for DSS recommendations.
    Contains predictions and suggested schemes.
    """
    Land_Use_Prediction: int = Field(..., description="Predicted land use class (e.g., 0 = forest, 1 = agriculture)")
    Water_Index: float = Field(..., description="Predicted water index score")
    Productivity_Index: float = Field(..., description="Predicted productivity index score")
    Recommended_Schemes: List[str] = Field(..., description="List of recommended government schemes")


# ---------------------------
# DSS RULES MODELS
# ---------------------------

class DSSRuleBase(BaseModel):
    """
    Base schema for DSS rules.
    """
    Rule_ID: Optional[int] = Field(None, description="Unique ID for the DSS rule")
    Condition: str = Field(..., description="Condition description (e.g., Poverty_Index < 40)")
    Recommendation: str = Field(..., description="Scheme recommendation for the condition")


class DSSRuleCreate(DSSRuleBase):
    """
    Request model for creating a new DSS rule.
    """
    pass


class DSSRule(DSSRuleBase):
    """
    Response model for returning DSS rules.
    """
    pass


class DSSRuleResponse(BaseModel):
    """
    Standard API response for DSS rule operations.
    """
    message: str = Field(..., description="Status message for the operation")
    record: DSSRule
