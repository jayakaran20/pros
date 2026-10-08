import sys
import os
os.environ["DISABLE_SQLALCHEMY_CEXT"] = "1"

from pathlib import Path
from contextlib import asynccontextmanager

# Robustly ensure backend folder is in Python search path
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

PROJECT_ROOT = Path(__file__).resolve().parents[2]

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import setup_logging, get_logger
from app.api.v1.endpoints import predict, history, disease
from app.ml.wrappers.model_wrapper import crop_model
from app.ml.wrappers.vision_wrapper import vision_engine
from app.db.session import engine, Base
import app.models.prediction  # Ensure all ORM models are registered with Base metadata

logger = setup_logging()

# Support configurable ML models directory (for containers and different mount points)
MODELS_DIR = Path(os.getenv("MODELS_DIR", str(PROJECT_ROOT / "ml_experiments" / "models")))

# Define the lifespan of our app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP LOGIC ---
    logger.info("Initializing Cropfit AI Backend...")
    
    # 1. Initialize database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified/created successfully.")

    # 2. Load the Tabular ML brain into memory
    model_path = str(MODELS_DIR / "xgboost_crop_model.json")
    scaler_path = str(MODELS_DIR / "preprocessing_data.pkl")
    crop_model.load_model(model_path, scaler_path)
    logger.info("Crop recommendation model loaded.")

    # 3. Load the Computer Vision Disease Knowledge Base
    disease_classes_path = str(MODELS_DIR / "disease_classes.json")
    onnx_path = str(MODELS_DIR / "mobilenet_disease.onnx")
    vision_engine.load_knowledge_base(disease_classes_path, onnx_path)
    logger.info("Computer Vision disease diagnosis engine loaded.")
    
    yield
    # --- SHUTDOWN LOGIC ---
    logger.info("Shutting down Cropfit AI Backend...")

# Initialize FastAPI
app = FastAPI(
    title="Cropfit AI API",
    description="API for recommending crops (XGBoost) and diagnosing plant leaf diseases (Computer Vision) with persistent SQLite history.",
    version="2.0.0",
    lifespan=lifespan
)

# Global Exception Handler for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server error at {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred.", "error_type": type(exc).__name__}
    )

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(predict.router, prefix="/api/v1", tags=["Crop Recommendation"])
app.include_router(history.router, prefix="/api/v1", tags=["Prediction History"])
app.include_router(disease.router, prefix="/api/v1/diseases", tags=["Leaf Disease Computer Vision"])

@app.get("/", tags=["System"])
def root_check():
    return {"status": "ok", "message": "Cropfit API is running with SQLite Database!"}

@app.get("/api/v1/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "cropfit-backend",
        "version": "2.0.0",
        "database": "connected",
        "crop_model_loaded": crop_model.is_loaded,
        "vision_engine_loaded": vision_engine.is_loaded,
    }


