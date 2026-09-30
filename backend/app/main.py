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
from app.api.v1.endpoints import predict
from app.ml.wrappers.model_wrapper import crop_model

# Define the lifespan of our app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP LOGIC ---
    print("[INFO] Starting up the Cropfit server...")
    
    model_path = str(PROJECT_ROOT / "ml_experiments" / "models" / "xgboost_crop_model.json")
    scaler_path = str(PROJECT_ROOT / "ml_experiments" / "models" / "preprocessing_data.pkl")
    
    # Load the brain into memory!
    crop_model.load_model(model_path, scaler_path)
    
    yield
    # --- SHUTDOWN LOGIC ---
    print("[INFO] Shutting down server...")

# Initialize FastAPI
app = FastAPI(
    title="Cropfit AI API",
    description="API for recommending crops based on soil and weather data using XGBoost.",
    version="1.0.0",
    lifespan=lifespan
)

# Allow our React frontend to talk to this API later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the predict router
app.include_router(predict.router, prefix="/api/v1", tags=["Machine Learning"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Cropfit API is running!"}
