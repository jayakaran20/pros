import sys
import os
from pathlib import Path
from contextlib import asynccontextmanager

# Robustly ensure backend folder is in Python search path
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

PROJECT_ROOT = Path(__file__).resolve().parents[2]

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import predict, history
from app.ml.wrappers.model_wrapper import crop_model
from app.db.session import engine, Base
import app.models.prediction  # Ensure all ORM models are registered with Base metadata

# Define the lifespan of our app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP LOGIC ---
    print("[INFO] Starting up the Cropfit server...")
    
    # 1. Initialize database tables
    Base.metadata.create_all(bind=engine)
    print("[INFO] Database tables verified/created successfully.")

    # 2. Load the ML brain into memory
    model_path = str(PROJECT_ROOT / "ml_experiments" / "models" / "xgboost_crop_model.json")
    scaler_path = str(PROJECT_ROOT / "ml_experiments" / "models" / "preprocessing_data.pkl")
    crop_model.load_model(model_path, scaler_path)
    
    yield
    # --- SHUTDOWN LOGIC ---
    print("[INFO] Shutting down server...")

# Initialize FastAPI
app = FastAPI(
    title="Cropfit AI API",
    description="API for recommending crops based on soil and weather data using XGBoost with persistent SQLite history.",
    version="1.0.0",
    lifespan=lifespan
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
app.include_router(predict.router, prefix="/api/v1", tags=["Machine Learning"])
app.include_router(history.router, prefix="/api/v1", tags=["Prediction History"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Cropfit API is running with SQLite Database!"}
