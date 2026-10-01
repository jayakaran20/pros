from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.crop import CropPredictionRequest, CropPredictionResponse
from app.ml.wrappers.model_wrapper import crop_model
from app.db.session import get_db
from app.db.repository import PredictionRepository

router = APIRouter()

@router.post("/predict", response_model=CropPredictionResponse)
def predict_crop(request: CropPredictionRequest, db: Session = Depends(get_db)):
    """
    Takes soil and weather data, runs it through the ML model,
    saves the prediction event and inputs to the database,
    and returns the best crop recommendation.
    """
    try:
        # Convert Pydantic object to standard dictionary
        input_data = request.model_dump()
        
        # 1. Ask the AI model wrapper for prediction
        crop_name, confidence = crop_model.predict(input_data)
        rounded_confidence = round(confidence, 2)
        
        # 2. Persist to SQLite Database via Repository
        PredictionRepository.create_crop_prediction(
            db=db,
            input_data=input_data,
            recommended_crop=crop_name,
            confidence_score=rounded_confidence
        )
        
        # 3. Return response
        return CropPredictionResponse(
            recommended_crop=crop_name,
            confidence_score=rounded_confidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
