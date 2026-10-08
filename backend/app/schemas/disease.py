from typing import List, Optional
from pydantic import BaseModel, Field

class DiseaseDiagnosisResponse(BaseModel):
    crop: str = Field(..., description="Detected crop species (e.g., Tomato, Potato)")
    condition: str = Field(..., description="Diagnosed condition or disease name")
    is_healthy: bool = Field(..., description="True if no disease detected")
    confidence_score: float = Field(..., description="Model confidence percentage (0-100)")
    severity: str = Field(..., description="Low, Medium, or High risk level")
    symptoms: List[str] = Field(..., description="Key visual symptoms")
    treatment_recommendations: List[str] = Field(..., description="Actionable organic or chemical remedies")
    prevention_tips: List[str] = Field(..., description="Preventative agronomy tips")
