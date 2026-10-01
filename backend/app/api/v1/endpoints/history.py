from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repository import PredictionRepository
from app.schemas.history import PredictionHistoryResponse, PredictionHistoryItem

router = APIRouter()

@router.get("/history", response_model=PredictionHistoryResponse)
def get_prediction_history(
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    task_type: Optional[str] = Query(None, description="Filter by task type, e.g. crop_recommendation"),
    db: Session = Depends(get_db)
):
    """
    Fetches paginated prediction history with full input telemetry from the database.
    """
    total = PredictionRepository.count_total(db, task_type=task_type)
    records = PredictionRepository.get_history(db, skip=skip, limit=limit, task_type=task_type)

    return PredictionHistoryResponse(
        total_records=total,
        page_size=len(records),
        skip=skip,
        records=records
    )
