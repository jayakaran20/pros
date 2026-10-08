import React, { useState } from 'react';
import { Sprout, History, Sparkles, Layers, ShieldCheck, Stethoscope } from 'lucide-react';
import { CropForm } from './components/CropForm';
import { DiseaseDetection } from './components/DiseaseDetection';
import { HistoryDashboard } from './components/HistoryDashboard';
import './App.css';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'recommend' | 'disease' | 'history'>('recommend');
  const [refreshTrigger, setRefreshTrigger] = useState<number>(0);

  const handleActionSuccess = () => {
    // Increment trigger so history dashboard refreshes when visited
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="app-container">
      {/* Top Navigation Bar */}
      <header className="navbar">
        <div className="nav-brand">
          <div className="brand-logo">
            <Sprout size={26} className="text-white" />
          </div>
          <div>
            <div className="brand-title">
              <span>Cropfit</span>
              <span className="badge-version">v2.0 Vision AI</span>
            </div>
            <p className="brand-tagline">AI-Powered Agronomy, Soil Analytics & Leaf Pathology</p>
          </div>
        </div>

        <div className="nav-status">
          <span className="status-dot" />
          <span className="status-text">FastAPI + XGBoost + Vision AI Online</span>
        </div>
      </header>

      {/* Main Container */}
      <main className="main-content">
        {/* Navigation Tabs */}
        <div className="tab-bar">
          <button
            type="button"
            className={`tab-btn ${activeTab === 'recommend' ? 'active' : ''}`}
            onClick={() => setActiveTab('recommend')}
          >
            <Sparkles size={18} />
            <span>Crop Recommendation</span>
          </button>

          <button
            type="button"
            className={`tab-btn ${activeTab === 'disease' ? 'active' : ''}`}
            onClick={() => setActiveTab('disease')}
          >
            <Stethoscope size={18} />
            <span>Leaf Disease Detection</span>
          </button>

          <button
            type="button"
            className={`tab-btn ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            <History size={18} />
            <span>Database History</span>
          </button>
        </div>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === 'recommend' ? (
            <div className="recommend-view">
              <CropForm onPredictionSuccess={handleActionSuccess} />
            </div>
          ) : activeTab === 'disease' ? (
            <div className="disease-view">
              <DiseaseDetection onDiagnosisSuccess={handleActionSuccess} />
            </div>
          ) : (
            <div className="history-view">
              <HistoryDashboard refreshTrigger={refreshTrigger} />
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-tech">
            <span><Layers size={14} /> Full Stack Monolith</span>
            <span>•</span>
            <span>React 18 + TypeScript</span>
            <span>•</span>
            <span>FastAPI REST</span>
            <span>•</span>
            <span>XGBoost + MobileNet Vision</span>
            <span>•</span>
            <span>SQLite + SQLAlchemy</span>
          </div>
          <div className="footer-status">
            <ShieldCheck size={14} className="text-emerald" /> Vision AI V2 Operational
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
