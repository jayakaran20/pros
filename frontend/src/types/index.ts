/**
 * Frontend TypeScript Contracts.
 * Mirrored directly from backend Pydantic v2 schemas.
 */

export interface CropPredictionRequest {
  nitrogen: number;
  phosphorus: number;
  potassium: number;
  temperature: number;
  humidity: number;
  ph: number;
  rainfall: number;
}

export interface CropPredictionOption {
  crop: string;
  confidence: number;
}

export interface CropPredictionResponse {
  status: "success" | "error";
  data: {
    recommended_crop: string;
    confidence: number;
    alternative_options: CropPredictionOption[];
    advisory_notes: string;
    model_version: string;
  };
  timestamp: string;
}

export interface SystemHealthResponse {
  status: "healthy" | "degraded" | "unhealthy";
  database_connected: boolean;
  loaded_models: {
    crop_recommendation: boolean;
    disease_detection: boolean;
    yield_prediction: boolean;
  };
  version: string;
}
