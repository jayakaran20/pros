import React, { useEffect, useState } from 'react';
import { History, RefreshCw, Calendar, Database } from 'lucide-react';
import { PredictionHistoryItem } from '../types';
import { getPredictionHistory } from '../services/api';

interface HistoryDashboardProps {
  refreshTrigger?: number;
}

export const HistoryDashboard: React.FC<HistoryDashboardProps> = ({ refreshTrigger }) => {
  const [history, setHistory] = useState<PredictionHistoryItem[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHistory = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getPredictionHistory(0, 50);
      setHistory(data.records);
      setTotal(data.total_records);
    } catch {
      setError('Could not load prediction history. Ensure the backend server is active.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [refreshTrigger]);

  const formatDate = (isoStr: string) => {
    try {
      const d = new Date(isoStr);
      return d.toLocaleString(undefined, {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return isoStr;
    }
  };

  return (
    <div className="card">
      <div className="card-header history-header">
        <div className="header-icon">
          <History size={24} className="text-emerald" />
        </div>
        <div className="header-info">
          <h2>Prediction Audit Trail</h2>
          <p>
            Persisted in SQLite database (<code>prediction_records</code> & <code>crop_predictions</code>)
          </p>
        </div>
        <div className="header-action">
          <button
            type="button"
            className="btn-secondary"
            onClick={fetchHistory}
            disabled={isLoading}
            title="Refresh History"
          >
            <RefreshCw size={16} className={isLoading ? 'animate-spin' : ''} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {error ? (
        <div className="alert-error">
          <p>{error}</p>
        </div>
      ) : isLoading && history.length === 0 ? (
        <div className="empty-state">
          <div className="spinner-large" />
          <p>Querying SQLite database...</p>
        </div>
      ) : history.length === 0 ? (
        <div className="empty-state">
          <Database size={40} className="text-muted" />
          <h3>No predictions recorded yet</h3>
          <p>Submit your first crop recommendation using the form to see telemetry logged here.</p>
        </div>
      ) : (
        <div className="table-responsive">
          <div className="history-summary">
            Showing <strong>{history.length}</strong> of <strong>{total}</strong> logged predictions
          </div>
          <table className="history-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Timestamp</th>
                <th>Recommended Crop</th>
                <th>Confidence</th>
                <th>Soil (N / P / K)</th>
                <th>Climate (Temp / Hum / Rain)</th>
                <th>pH</th>
              </tr>
            </thead>
            <tbody>
              {history.map(item => (
                <tr key={item.id}>
                  <td className="font-mono text-muted">#{item.id}</td>
                  <td className="text-sm">
                    <span className="flex items-center gap-1">
                      <Calendar size={13} className="text-muted" />
                      {formatDate(item.created_at)}
                    </span>
                  </td>
                  <td>
                    <span className="badge-crop">
                      🌱 {item.recommended_crop}
                    </span>
                  </td>
                  <td>
                    <div className="confidence-pill">
                      <div
                        className="confidence-fill"
                        style={{ width: `${Math.min(100, item.confidence_score)}%` }}
                      />
                      <span>{item.confidence_score.toFixed(1)}%</span>
                    </div>
                  </td>
                  <td className="font-mono text-sm">
                    {item.crop_detail
                      ? `${item.crop_detail.nitrogen} / ${item.crop_detail.phosphorous} / ${item.crop_detail.potassium}`
                      : '—'}
                  </td>
                  <td className="font-mono text-sm">
                    {item.crop_detail
                      ? `${item.crop_detail.temperature.toFixed(1)}°C / ${item.crop_detail.humidity.toFixed(0)}% / ${item.crop_detail.rainfall.toFixed(0)}mm`
                      : '—'}
                  </td>
                  <td className="font-mono text-sm">
                    {item.crop_detail ? item.crop_detail.ph.toFixed(1) : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
