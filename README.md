# 🌱 Cropfit — AI-Powered Smart Agriculture Platform

[![CI Pipeline](https://github.com/jayakaran20/pros/actions/workflows/ci.yml/badge.svg)](https://github.com/jayakaran20/pros/actions/workflows/ci.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-Native%20Booster-EB4034)](https://xgboost.readthedocs.io)
[![ONNX Runtime](https://img.shields.io/badge/ONNX%20Runtime-Inference-005CED)](https://onnxruntime.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Cropfit** is an enterprise-grade agronomy intelligence platform combining **Tabular Machine Learning (XGBoost)** for precision crop recommendations and **Computer Vision (MobileNetV3 / ONNX)** for real-time plant leaf disease diagnosis. Designed with a clean layered monolith architecture, persistent SQLite audit trails, Nginx reverse proxying, and automated cloud CI/CD quality gates.

---

## 🏛️ System Architecture

```mermaid
graph TD
    User["Client Web Browser"] -->|HTTP / HTTPS| Nginx["Nginx Reverse Proxy (Port 80 / 3000)"]
    
    subgraph "Docker Orchestration (cropfit-network)"
        Nginx -->|Serves Static UI| SPA["React 18 + Vite SPA (/usr/share/nginx/html)"]
        Nginx -->|Reverse Proxy /api/v1/*| API["FastAPI Uvicorn (Port 8000)"]
        
        subgraph "Application Core & Services"
            API --> AuthMiddleware["CORS & Structured Logging Engine"]
            AuthMiddleware --> PredictRouter["/api/v1/predict (Crop Service)"]
            AuthMiddleware --> HistoryRouter["/api/v1/history (History Service)"]
            AuthMiddleware --> DiseaseRouter["/api/v1/diseases/diagnose (Vision Service)"]
        end
        
        subgraph "Machine Learning Inference Engines"
            PredictRouter -->|7 Features| XGB["Native XGBoost Booster (88.18% Accuracy, ~1.8ms Latency)"]
            DiseaseRouter -->|Multipart JPEG/PNG| ONNX["MobileNetV3 ONNX Engine (11 Botanical Classes)"]
        end
        
        subgraph "Persistence Layer"
            PredictRouter -.->|Save Audit Record| Repo["SQLAlchemy ORM Repository"]
            DiseaseRouter -.->|Save Diagnosis Record| Repo
            HistoryRouter -->|Paginated Query| Repo
            Repo --> DB[("SQLite Database (/app/data/cropfit.db)")]
        end
    end

    DB -.->|Mount| Vol[("Persistent Docker Volume (cropfit_data)")]
```

---

## ✨ Key Features

1. **Precision Crop Recommendation**:
   * Evaluates 7 soil and climate parameters: Nitrogen ($N$), Phosphorus ($P$), Potassium ($K$), Temperature, Humidity, Soil pH, and Rainfall.
   * Powered by a native C++ **XGBoost Booster** serialized without brittle pickle wrappers, delivering sub-2ms inference ($P95 < 50\text{ms}$).
   * Outputs top-ranked crops with exact probability distributions and agronomic guidance.

2. **Computer Vision Plant Disease Diagnosis**:
   * Supports drag-and-drop multipart upload of smartphone leaf photos.
   * Diagnoses conditions across 11 botanical categories (e.g., Tomato Late Blight, Tomato Early Blight, Potato Healthy Foliage).
   * Returns severity level, primary visual symptoms, organic/chemical treatment plans, and preventative agronomy advice.

3. **Persistent Audit History**:
   * Full database audit trail storing every inference request with input features, timestamps, recommendations, and diagnosis metadata.
   * Filterable and paginated history dashboard with 1-click preset testing.

4. **Production DevOps & Cloud Readiness**:
   * **Multi-Stage Dockerfiles**: Lean runtime containers using non-root security (`appuser`).
   * **Docker Compose**: Single-command stack orchestration (`docker compose up --build`).
   * **GitHub Actions CI**: Automated 3-stage pipeline testing backend, frontend, and container builds.
   * **Automated Smoke Testing**: Built-in Python CLI verification testing all endpoints in $<500\text{ ms}$.

---

## 🚀 Quick Start (Local Development)

### Prerequisites
* **Python 3.11+**
* **Node.js 20+**
* **Git**

### 1. Clone & Setup Repository
```bash
git clone https://github.com/jayakaran20/pros.git Cropfit
cd Cropfit
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate   # Windows PowerShell
# source .venv/bin/activate  # macOS / Linux

# Install dependencies
pip install -r backend/requirements.txt

# Start the FastAPI server
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```
API Documentation will be live at: **`http://127.0.0.1:8000/docs`**

### 3. Frontend Setup
In a new terminal window:
```bash
cd frontend
npm install
npm run dev
```
Open your browser at: **`http://localhost:5173`**

---

## 🐳 Running with Docker & Docker Compose

Deploy the entire production stack (Nginx + React SPA + FastAPI + SQLite persistence) with one command:

```bash
docker compose up --build
```

* **Frontend Web Application**: [http://localhost:3000](http://localhost:3000)
* **Backend Swagger API**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **Health Check Probe**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## 🧪 Testing & Verification

### Run Backend Pytest Suite (with Statement Coverage)
```bash
pytest --cov=backend/app --cov-report=term-missing backend/tests/
```
* **Coverage**: **87% statement coverage** across all routes, models, and repositories (22/22 tests passing).

### Run Frontend Vitest Contract Suite
```bash
cd frontend
npm test
```

### Run Automated Production Smoke Tests
```bash
python backend/scripts/smoke_test.py --base-url http://127.0.0.1:8000
```

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Root service liveness check |
| `GET` | `/api/v1/health` | Comprehensive system health & model memory residency probe |
| `POST` | `/api/v1/predict` | Computes crop recommendations from 7 soil/weather parameters |
| `GET` | `/api/v1/history` | Retrieves paginated prediction and diagnosis audit records |
| `POST` | `/api/v1/diseases/diagnose` | Multipart upload for plant leaf image diagnosis |
| `GET` | `/docs` | Interactive Swagger UI API documentation |
| `GET` | `/redoc` | ReDoc API documentation specification |

---

## 📦 ML Model Governance & Cards

* [XGBoost Crop Recommendation Model Card](file:///C:/Users/TICKMARKS/OneDrive%20-%20tickmarks.net/Desktop/Cropfit/docs/models/crop_recommendation_card.md)
* [Computer Vision Disease Diagnosis Model Card](file:///C:/Users/TICKMARKS/OneDrive%20-%20tickmarks.net/Desktop/Cropfit/docs/models/plant_disease_vision_card.md)

---

## 👤 Author & License

* **Author**: Jayakaran ([@jayakaran20](https://github.com/jayakaran20)) — `jayakaran546@gmail.com`
* **Repository**: [https://github.com/jayakaran20/pros](https://github.com/jayakaran20/pros)
* **License**: MIT
