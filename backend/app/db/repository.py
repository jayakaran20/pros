from sqlalchemy.orm import Session
from app.models.prediction import PredictionRecord, CropPredictionDetail
from typing import Optional, List

class PredictionRepository:
    @staticmethod
    def create_crop_prediction(
        db: Session,
        input_data: dict,
        recommended_crop: str,
        confidence_score: float
    ) -> PredictionRecord:
        """Saves both the high-level prediction record and the detailed input telemetry."""
        record = PredictionRecord(
            task_type="crop_recommendation",
            recommended_crop=recommended_crop,
            confidence_score=confidence_score
        )
        db.add(record)
        db.flush()  # Flush to populate record.id

        detail = CropPredictionDetail(
            record_id=record.id,
            nitrogen=input_data["N"],
            phosphorous=input_data["P"],
            potassium=input_data["K"],
            temperature=input_data["temperature"],
            humidity=input_data["humidity"],
            ph=input_data["ph"],
            rainfall=input_data["rainfall"]
        )
        db.add(detail)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def get_history(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        task_type: Optional[str] = None
    ) -> List[PredictionRecord]:
        """Queries historical predictions ordered from newest to oldest with pagination."""
        query = db.query(PredictionRecord)
        if task_type:
            query = query.filter(PredictionRecord.task_type == task_type)
        return query.order_by(PredictionRecord.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def count_total(db: Session, task_type: Optional[str] = None) -> int:
        query = db.query(PredictionRecord)
        if task_type:
            query = query.filter(PredictionRecord.task_type == task_type)
        return query.count()
