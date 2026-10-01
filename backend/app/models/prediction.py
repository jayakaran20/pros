import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class PredictionRecord(Base):
    """Parent table tracking each prediction event."""
    __tablename__ = "prediction_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_type = Column(String(50), default="crop_recommendation", nullable=False)
    recommended_crop = Column(String(100), nullable=False)
    confidence_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # 1-to-1 relationship with the granular soil/climate features
    crop_detail = relationship(
        "CropPredictionDetail",
        back_populates="record",
        uselist=False,
        cascade="all, delete-orphan"
    )

class CropPredictionDetail(Base):
    """Child table storing the 7 exact inputs provided by the user/farmer."""
    __tablename__ = "crop_predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey("prediction_records.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    nitrogen = Column(Float, nullable=False)
    phosphorous = Column(Float, nullable=False)
    potassium = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    ph = Column(Float, nullable=False)
    rainfall = Column(Float, nullable=False)

    record = relationship("PredictionRecord", back_populates="crop_detail")
