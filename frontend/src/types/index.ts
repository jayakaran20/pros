/**
 * Frontend TypeScript Contracts.
 * Mirrored directly from backend FastAPI Pydantic v2 schemas.
 */

export interface CropPredictionRequest {
  N: number;
  P: number;
  K: number;
  temperature: number;
  humidity: number;
  ph: number;
  rainfall: number;
}

export interface CropPredictionResponse {
  recommended_crop: string;
  confidence_score: number;
}

export interface CropDetail {
  nitrogen: number;
  phosphorous: number;
  potassium: number;
  temperature: number;
  humidity: number;
  ph: number;
  rainfall: number;
}

export interface PredictionHistoryItem {
  id: number;
  task_type: string;
  recommended_crop: string;
  confidence_score: number;
  created_at: string;
  crop_detail: CropDetail | null;
}

export interface PredictionHistoryResponse {
  total_records: number;
  page_size: number;
  skip: number;
  records: PredictionHistoryItem[];
}
