import React, { useState, useRef } from 'react';
import {
  UploadCloud,
  CheckCircle2,
  AlertTriangle,
  AlertCircle,
  ShieldCheck,
  Stethoscope,
  X,
  FileImage,
  Sparkles
} from 'lucide-react';
import { DiseaseDiagnosisResponse } from '../types';
import { diagnoseDisease, ApiError } from '../services/api';

interface DiseaseDetectionProps {
  onDiagnosisSuccess?: () => void;
}

export const DiseaseDetection: React.FC<DiseaseDetectionProps> = ({ onDiagnosisSuccess }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [diagnosis, setDiagnosis] = useState<DiseaseDiagnosisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (file: File) => {
    if (!file.type.startsWith('image/')) {
      setError('Please upload an image file (JPEG, PNG, or WebP).');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError('Image exceeds maximum allowed size of 10MB.');
      return;
    }

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setError(null);
    setDiagnosis(null);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setPreviewUrl(null);
    setDiagnosis(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;

    setIsLoading(true);
    setError(null);
    setDiagnosis(null);

    try {
      const result = await diagnoseDisease(selectedFile);
      setDiagnosis(result);
      if (onDiagnosisSuccess) {
        onDiagnosisSuccess();
      }
    } catch (err) {
      if (err instanceof ApiError) {
        setError(`Diagnosis Failed (${err.status}): ${err.message}`);
      } else {
        setError('Cannot connect to backend server. Make sure FastAPI is running on port 8000.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Helper to create synthetic leaf samples for quick testing
  const createSampleLeaf = (color: string, filename: string) => {
    const canvas = document.createElement('canvas');
    canvas.width = 224;
    canvas.height = 224;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      // Draw background leaf color
      ctx.fillStyle = color;
      ctx.fillRect(0, 0, 224, 224);

      if (filename.includes('blight')) {
        // Draw necrotic brown concentric spots
        ctx.fillStyle = '#4a2810';
        ctx.beginPath();
        ctx.arc(80, 90, 30, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(140, 150, 40, 0, Math.PI * 2);
        ctx.fill();
      } else if (filename.includes('rust')) {
        // Draw cinnamon-orange rust spots
        ctx.fillStyle = '#b45309';
        for (let i = 0; i < 20; i++) {
          ctx.beginPath();
          ctx.arc(40 + (i * 8), 60 + ((i % 5) * 20), 8, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      canvas.toBlob((blob) => {
        if (blob) {
          const testFile = new File([blob], filename, { type: 'image/jpeg' });
          handleFileSelect(testFile);
        }
      }, 'image/jpeg');
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <div className="header-icon">
          <Stethoscope size={24} className="text-emerald" />
        </div>
        <div>
          <h2>Computer Vision Leaf Pathology</h2>
          <p>Upload a plant leaf photo to diagnose diseases and view organic treatment guidelines</p>
        </div>
      </div>

      {/* Preset Test Leaf Generator */}
      <div className="preset-bar">
        <span className="preset-label">Test with Leaf Samples:</span>
        <div className="preset-tags">
          <button
            type="button"
            className="preset-btn"
            onClick={() => createSampleLeaf('#15803d', 'healthy_leaf.jpg')}
          >
            <span>🟢</span>
            <span>Healthy Leaf Sample</span>
          </button>
          <button
            type="button"
            className="preset-btn"
            onClick={() => createSampleLeaf('#84cc16', 'early_blight_leaf.jpg')}
          >
            <span>🍂</span>
            <span>Early Blight Sample</span>
          </button>
          <button
            type="button"
            className="preset-btn"
            onClick={() => createSampleLeaf('#a3e635', 'corn_rust_leaf.jpg')}
          >
            <span>🌾</span>
            <span>Corn Rust Sample</span>
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="disease-form">
        {/* Upload Dropzone */}
        {!previewUrl ? (
          <div
            className="dropzone"
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="image/jpeg,image/png,image/webp"
              style={{ display: 'none' }}
              onChange={(e) => {
                if (e.target.files && e.target.files[0]) {
                  handleFileSelect(e.target.files[0]);
                }
              }}
            />
            <div className="dropzone-icon">
              <UploadCloud size={44} />
            </div>
            <h3>Drag & drop leaf photograph here</h3>
            <p>or click to browse from your device (JPEG, PNG, WebP up to 10MB)</p>
          </div>
        ) : (
          <div className="preview-container">
            <div className="preview-wrapper">
              <img src={previewUrl} alt="Leaf Preview" className="preview-img" />
              <button
                type="button"
                className="btn-clear-preview"
                onClick={handleClear}
                title="Remove photo"
              >
                <X size={18} />
              </button>
            </div>
            <div className="preview-meta">
              <div className="meta-filename">
                <FileImage size={18} />
                <span>{selectedFile?.name}</span>
              </div>
              <span className="meta-size">
                {selectedFile ? (selectedFile.size / 1024).toFixed(1) : 0} KB
              </span>
            </div>
          </div>
        )}

        {/* Action Button */}
        {previewUrl && (
          <div className="form-actions">
            <button
              type="submit"
              className="btn-primary"
              disabled={isLoading || !selectedFile}
            >
              {isLoading ? (
                <>
                  <div className="spinner" /> Analyzing Leaf Chromatics & Pathology...
                </>
              ) : (
                <>
                  <Sparkles size={18} /> Run AI Disease Diagnosis
                </>
              )}
            </button>
          </div>
        )}
      </form>

      {/* Error Banner */}
      {error && (
        <div className="alert-error">
          <AlertCircle size={20} />
          <div>
            <strong>Diagnosis Error</strong>
            <p>{error}</p>
          </div>
        </div>
      )}

      {/* Diagnosis Report Card */}
      {diagnosis && (
        <div className={`diagnosis-card ${diagnosis.is_healthy ? 'is-healthy' : 'is-diseased'}`}>
          <div className="diagnosis-header">
            <div className="diagnosis-status-badge">
              {diagnosis.is_healthy ? (
                <>
                  <CheckCircle2 size={20} />
                  <span>Healthy Plant</span>
                </>
              ) : (
                <>
                  <AlertTriangle size={20} />
                  <span>Disease Detected</span>
                </>
              )}
            </div>

            <div className={`severity-tag severity-${diagnosis.severity.toLowerCase()}`}>
              Severity: {diagnosis.severity}
            </div>
          </div>

          <div className="diagnosis-main">
            <div>
              <span className="crop-species-label">{diagnosis.crop.toUpperCase()}</span>
              <h3 className="disease-condition-title">{diagnosis.condition}</h3>
            </div>
            <div className="confidence-meter-container">
              <div className="confidence-label">
                <span>Model Confidence</span>
                <span className="confidence-value">{diagnosis.confidence_score.toFixed(1)}%</span>
              </div>
              <div className="confidence-track">
                <div
                  className="confidence-bar"
                  style={{ width: `${Math.min(100, diagnosis.confidence_score)}%` }}
                />
              </div>
            </div>
          </div>

          {/* Clinical Symptoms */}
          <div className="report-section">
            <h4>
              <Stethoscope size={16} /> Observed Symptoms & Diagnostic Indicators
            </h4>
            <ul className="bullet-list">
              {diagnosis.symptoms.map((symptom, i) => (
                <li key={i}>{symptom}</li>
              ))}
            </ul>
          </div>

          {/* Treatment & Action Plan */}
          <div className="report-section">
            <h4>
              <ShieldCheck size={16} /> Prescribed Treatment & Field Remediation
            </h4>
            <ul className="treatment-list">
              {diagnosis.treatment_recommendations.map((treatment, i) => (
                <li key={i}>{treatment}</li>
              ))}
            </ul>
          </div>

          {/* Prevention */}
          {diagnosis.prevention_tips.length > 0 && (
            <div className="report-section">
              <h4>🌱 Preventative Agronomy Practices</h4>
              <ul className="bullet-list">
                {diagnosis.prevention_tips.map((tip, i) => (
                  <li key={i}>{tip}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="result-footer">
            ✓ Logged to SQLite database audit trail under <code>disease_detection</code>.
          </div>
        </div>
      )}
    </div>
  );
};
