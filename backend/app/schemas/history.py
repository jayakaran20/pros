import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class CropDetailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nitrogen: float
    phosphorous: float
    potassium: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

class PredictionHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_type: str
    recommended_crop: str
    confidence_score: float
    created_at: datetime.datetime
    crop_detail: Optional[CropDetailSchema] = None

class PredictionHistoryResponse(BaseModel):
    total_records: int
    page_size: int
    skip: int
    records: List[PredictionHistoryItem]
