from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.schemas.disease import DiseaseDiagnosisResponse
from app.ml.wrappers.vision_wrapper import vision_engine
from app.db.session import get_db
from app.models.prediction import PredictionRecord

router = APIRouter()

MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB limit
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}

@router.post(
    "/diagnose",
    response_model=DiseaseDiagnosisResponse,
    status_code=status.HTTP_200_OK,
    summary="Diagnose Plant Leaf Disease"
)
async def diagnose_leaf_disease(
    file: UploadFile = File(..., description="Leaf image file (JPEG or PNG, max 10MB)"),
    db: Session = Depends(get_db)
):
    """
    Receives an uploaded leaf photograph, preprocesses it via computer vision,
    runs deep learning diagnosis, records the diagnosis to SQLite history,
    and returns comprehensive symptoms and treatment guidelines.
    """
    # 1. MIME type validation
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{file.content_type}'. Please upload JPEG, PNG, or WebP images."
        )

    # 2. Read bytes and check size
    image_bytes = await file.read()
    if len(image_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty."
        )

    if len(image_bytes) > MAX_IMAGE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image exceeds maximum allowed size of 10MB."
        )

    # 3. Computer Vision Inference
    try:
        diagnosis = vision_engine.diagnose(image_bytes)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid image content: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vision inference error: {str(e)}"
        )

    # 4. Record to SQLite database under 'disease_detection' audit trail
    try:
        record = PredictionRecord(
            task_type="disease_detection",
            recommended_crop=f"{diagnosis['crop']} - {diagnosis['condition']}",
            confidence_score=diagnosis["confidence_score"]
        )
        db.add(record)
        db.commit()
    except Exception as e:
        print(f"[WARN] Could not persist disease diagnosis to DB: {e}")
        db.rollback()

    return DiseaseDiagnosisResponse(**diagnosis)
