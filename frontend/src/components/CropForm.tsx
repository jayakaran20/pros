import React, { useState } from 'react';
import { Sprout, Sparkles, AlertCircle, CheckCircle2, Droplets, Thermometer, Wind, TestTube } from 'lucide-react';
import { CropPredictionRequest, CropPredictionResponse } from '../types';
import { predictCrop, ApiError } from '../services/api';

interface CropFormProps {
  onPredictionSuccess?: () => void;
}

const SAMPLE_PRESETS: { name: string; icon: string; data: CropPredictionRequest }[] = [
  {
    name: 'Rice (Wet & Humid)',
    icon: '🌾',
    data: { N: 90, P: 42, K: 43, temperature: 20.8, humidity: 82.0, ph: 6.5, rainfall: 202.9 }
  },
  {
    name: 'Apple (Cool & Mild)',
    icon: '🍎',
    data: { N: 20, P: 134, K: 199, temperature: 22.6, humidity: 92.3, ph: 5.9, rainfall: 110.5 }
  },
  {
    name: 'Coffee (Tropical Highland)',
    icon: '☕',
    data: { N: 101, P: 28, K: 32, temperature: 26.5, humidity: 58.0, ph: 6.7, rainfall: 158.0 }
  },
  {
    name: 'Maize (Balanced Corn)',
    icon: '🌽',
    data: { N: 78, P: 45, K: 20, temperature: 24.0, humidity: 65.0, ph: 6.2, rainfall: 85.0 }
  }
];

export const CropForm: React.FC<CropFormProps> = ({ onPredictionSuccess }) => {
  const [formData, setFormData] = useState<CropPredictionRequest>({
    N: 90,
    P: 42,
    K: 43,
    temperature: 20.8,
    humidity: 82.0,
    ph: 6.5,
    rainfall: 202.9
  });

  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<CropPredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (field: keyof CropPredictionRequest, value: string) => {
    const num = parseFloat(value);
    setFormData(prev => ({
      ...prev,
      [field]: isNaN(num) ? 0 : num
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await predictCrop(formData);
      setResult(response);
      if (onPredictionSuccess) {
        onPredictionSuccess();
      }
    } catch (err) {
      if (err instanceof ApiError) {
        setError(`Error (${err.status}): ${err.message}`);
      } else {
        setError('Cannot connect to backend server. Make sure FastAPI is running on port 8000.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const applyPreset = (preset: CropPredictionRequest) => {
    setFormData(preset);
    setResult(null);
    setError(null);
  };

  return (
    <div className="card">
      <div className="card-header">
        <div className="header-icon">
          <Sprout size={24} className="text-emerald" />
        </div>
        <div>
          <h2>Soil & Climate Analysis</h2>
          <p>Input your farm parameters to get an AI-powered crop recommendation</p>
        </div>
      </div>

      {/* Preset Buttons */}
      <div className="preset-bar">
        <span className="preset-label">Test with Presets:</span>
        <div className="preset-tags">
          {SAMPLE_PRESETS.map((p, idx) => (
            <button
              key={idx}
              type="button"
              className="preset-btn"
              onClick={() => applyPreset(p.data)}
            >
              <span>{p.icon}</span>
              <span>{p.name}</span>
            </button>
          ))}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="form-grid">
        {/* Soil Nutrients Section */}
        <div className="input-section">
          <h3 className="section-title">
            <TestTube size={18} /> Soil Macro-Nutrients (kg/ha)
          </h3>
          <div className="fields-row">
            <div className="form-group">
              <label>Nitrogen (N)</label>
              <input
                type="number"
                step="0.1"
                min="0"
                value={formData.N}
                onChange={e => handleInputChange('N', e.target.value)}
                required
              />
              <span className="helper-text">Plant growth (0-140)</span>
            </div>

            <div className="form-group">
              <label>Phosphorous (P)</label>
              <input
                type="number"
                step="0.1"
                min="0"
                value={formData.P}
                onChange={e => handleInputChange('P', e.target.value)}
                required
              />
              <span className="helper-text">Root development (5-145)</span>
            </div>

            <div className="form-group">
              <label>Potassium (K)</label>
              <input
                type="number"
                step="0.1"
                min="0"
                value={formData.K}
                onChange={e => handleInputChange('K', e.target.value)}
                required
              />
              <span className="helper-text">Disease resistance (5-205)</span>
            </div>
          </div>
        </div>

        {/* Climate & Weather Section */}
        <div className="input-section">
          <h3 className="section-title">
            <Thermometer size={18} /> Climate & Soil Chemistry
          </h3>
          <div className="fields-grid-2">
            <div className="form-group">
              <label>Temperature (°C)</label>
              <div className="input-with-icon">
                <Thermometer size={16} />
                <input
                  type="number"
                  step="0.1"
                  value={formData.temperature}
                  onChange={e => handleInputChange('temperature', e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label>Relative Humidity (%)</label>
              <div className="input-with-icon">
                <Wind size={16} />
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  max="100"
                  value={formData.humidity}
                  onChange={e => handleInputChange('humidity', e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label>Soil pH (0.0 - 14.0)</label>
              <div className="input-with-icon">
                <TestTube size={16} />
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  max="14"
                  value={formData.ph}
                  onChange={e => handleInputChange('ph', e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label>Rainfall (mm)</label>
              <div className="input-with-icon">
                <Droplets size={16} />
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  value={formData.rainfall}
                  onChange={e => handleInputChange('rainfall', e.target.value)}
                  required
                />
              </div>
            </div>
          </div>
        </div>

        {/* Action Button */}
        <div className="form-actions">
          <button
            type="submit"
            className="btn-primary"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <div className="spinner" /> Analyzing Soil & Climate...
              </>
            ) : (
              <>
                <Sparkles size={18} /> Predict Ideal Crop
              </>
            )}
          </button>
        </div>
      </form>

      {/* Error State */}
      {error && (
        <div className="alert-error">
          <AlertCircle size={20} />
          <div>
            <strong>Prediction Failed</strong>
            <p>{error}</p>
          </div>
        </div>
      )}

      {/* Recommendation Result Card */}
      {result && (
        <div className="result-card">
          <div className="result-badge">
            <CheckCircle2 size={18} className="text-emerald" /> Optimal Match Found
          </div>
          <div className="result-content">
            <div className="crop-title">
              <span className="crop-icon">🌱</span>
              <span className="crop-name">{result.recommended_crop.toUpperCase()}</span>
            </div>
            <div className="confidence-box">
              <div className="confidence-label">
                <span>Model Confidence</span>
                <span className="confidence-value">{result.confidence_score.toFixed(1)}%</span>
              </div>
              <div className="confidence-track">
                <div
                  className="confidence-bar"
                  style={{ width: `${Math.min(100, result.confidence_score)}%` }}
                />
              </div>
            </div>
          </div>
          <p className="result-footer">
            ✓ Successfully logged to SQLite database history table.
          </p>
        </div>
      )}
    </div>
  );
};
