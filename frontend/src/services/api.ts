import {
  CropPredictionRequest,
  CropPredictionResponse,
  PredictionHistoryResponse,
} from '../types';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

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
      // Fallback to response status text
      errorDetail = response.statusText;
    }
    throw new ApiError(response.status, errorDetail);
  }

  return response.json();
}

export async function getPredictionHistory(
  skip = 0,
  limit = 20
): Promise<PredictionHistoryResponse> {
  const response = await fetch(
    `${API_BASE_URL}/history?skip=${skip}&limit=${limit}`,
    {
      method: 'GET',
    }
  );

  if (!response.ok) {
    throw new ApiError(response.status, 'Failed to fetch prediction history');
  }

  return response.json();
}
