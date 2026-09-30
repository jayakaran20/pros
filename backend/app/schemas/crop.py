from pydantic import BaseModel, Field

class CropPredictionRequest(BaseModel):
    # Field(...) ensures the user MUST provide these values, and sets realistic validation bounds
    N: float = Field(..., description="Ratio of Nitrogen content in soil", ge=0.0)
    P: float = Field(..., description="Ratio of Phosphorous content in soil", ge=0.0)
    K: float = Field(..., description="Ratio of Potassium content in soil", ge=0.0)
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., description="Relative humidity in percentage", ge=0.0, le=100.0)
    ph: float = Field(..., description="pH value of the soil", ge=0.0, le=14.0)
    rainfall: float = Field(..., description="Rainfall in mm", ge=0.0)

    class Config:
        json_schema_extra = {
            "example": {
                "N": 90.0,
                "P": 42.0,
                "K": 43.0,
                "temperature": 20.8,
                "humidity": 82.0,
                "ph": 6.5,
                "rainfall": 202.9
            }
        }

class CropPredictionResponse(BaseModel):
    recommended_crop: str
    confidence_score: float = Field(..., description="Confidence percentage of the prediction (0-100)")
