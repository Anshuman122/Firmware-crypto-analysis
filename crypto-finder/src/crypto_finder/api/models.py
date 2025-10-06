# Hinglish: Pydantic ka use karke API ke liye data models (schemas) define karte hain.
# Isse API requests aur responses validate hote hain.

from pydantic import BaseModel, Field
from typing import List, Optional

class FunctionAnalysisRequest(BaseModel):
    """Ek single function ko analyze karne ke liye request model."""
    name: Optional[str] = "unknown_function"
    size: int = Field(..., gt=0, description="Function ka size bytes me.")
    instruction_count: int = Field(..., gt=0, description="Instructions ka total count.")
    pcode: List[str] = Field(..., description="Function ke P-Code operations ki list.")

class Prediction(BaseModel):
    """Ek single prediction ka result model."""
    label: str = Field(..., description="Predicted label ('crypto' ya 'non-crypto').")
    confidence: float = Field(..., ge=0, le=1, description="Prediction ka confidence score (0 se 1 tak).")

class AnalysisResponse(BaseModel):
    """API se final analysis response."""
    function_name: str
    prediction: Prediction