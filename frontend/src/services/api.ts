import {
  CropPredictionRequest,
  CropPredictionResponse,
  PredictionHistoryResponse,
  DiseaseDiagnosisResponse,
} from '../types';

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  (import.meta.env.DEV ? 'http://127.0.0.1:8000/api/v1' : '/api/v1');


export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

export async function predictCrop(
  payload: CropPredictionRequest
): Promise<CropPredictionResponse> {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let errorDetail = 'Failed to get recommendation';
    try {
      const errorJson = await response.json();
      if (errorJson.detail) {
        errorDetail = Array.isArray(errorJson.detail)
          ? errorJson.detail.map((d: { msg?: string }) => d.msg).join(', ')
          : String(errorJson.detail);
      }
    } catch {
      errorDetail = response.statusText;
    }
    throw new ApiError(response.status, errorDetail);
  }

  return response.json();
}

export async function getPredictionHistory(
  skip = 0,
  limit = 20,
  taskType?: string
): Promise<PredictionHistoryResponse> {
  let url = `${API_BASE_URL}/history?skip=${skip}&limit=${limit}`;
  if (taskType) {
    url += `&task_type=${taskType}`;
  }

  const response = await fetch(url, {
    method: 'GET',
  });

  if (!response.ok) {
    throw new ApiError(response.status, 'Failed to fetch prediction history');
  }

  return response.json();
}

export async function diagnoseDisease(
  file: File
): Promise<DiseaseDiagnosisResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/diseases/diagnose`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    let errorDetail = 'Failed to diagnose image';
    try {
      const errorJson = await response.json();
      if (errorJson.detail) {
        errorDetail = String(errorJson.detail);
      }
    } catch {
      errorDetail = response.statusText;
    }
    throw new ApiError(response.status, errorDetail);
  }

  return response.json();
}
