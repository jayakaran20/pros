import { describe, it, expect } from 'vitest';
import { CropPredictionRequest, DiseaseDiagnosisResponse } from '../types';

describe('Frontend Data Contracts & Boundaries', () => {
  it('validates a correct CropPredictionRequest payload structure', () => {
    const validPayload: CropPredictionRequest = {
      N: 90,
      P: 42,
      K: 43,
      temperature: 20.8,
      humidity: 82.0,
      ph: 6.5,
      rainfall: 202.9,
    };

    expect(validPayload.N).toBeGreaterThanOrEqual(0);
    expect(validPayload.ph).toBeGreaterThanOrEqual(0);
    expect(validPayload.ph).toBeLessThanOrEqual(14);
    expect(validPayload.humidity).toBeLessThanOrEqual(100);
  });

  it('validates DiseaseDiagnosisResponse structure', () => {
    const response: DiseaseDiagnosisResponse = {
      crop: 'Tomato',
      condition: 'Early Blight',
      is_healthy: false,
      confidence_score: 92.5,
      severity: 'Medium',
      symptoms: ['Concentric rings'],
      treatment_recommendations: ['Fungicide spray'],
      prevention_tips: ['Crop rotation'],
    };

    expect(response.is_healthy).toBe(false);
    expect(response.confidence_score).toBeGreaterThan(0);
    expect(response.symptoms.length).toBeGreaterThan(0);
    expect(response.treatment_recommendations.length).toBeGreaterThan(0);
  });
});
