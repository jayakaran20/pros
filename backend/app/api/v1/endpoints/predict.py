from fastapi import APIRouter, HTTPException
from app.schemas.crop import CropPredictionRequest, CropPredictionResponse
from app.ml.wrappers.model_wrapper import crop_model

router = APIRouter()

@router.post("/predict", response_model=CropPredictionResponse)
def predict_crop(request: CropPredictionRequest):
    """
    Takes soil and weather data, runs it through the ML model, 
    and returns the best crop recommendation.
    """
    try:
        # Convert the Pydantic object to a standard python dictionary
        input_data = request.model_dump()
        
        # Ask the AI model wrapper for a prediction
        crop_name, confidence = crop_model.predict(input_data)
        
        # Return exactly what our schema promised
        return CropPredictionResponse(
            recommended_crop=crop_name,
            confidence_score=round(confidence, 2)
        )
    except Exception as e:
        # If anything fails (like a math error), return a safe 500 error
        raise HTTPException(status_code=500, detail=str(e))
