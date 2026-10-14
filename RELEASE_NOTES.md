# 🚀 Cropfit v1.0.0 Release Notes

**Release Date**: October 2026  
**Tag**: `v1.0.0`  
**Git Commit**: [`91f249f`](https://github.com/jayakaran20/pros/commit/91f249f)  
**Author**: Jayakaran (`jayakaran546@gmail.com`)  
**Repository**: [https://github.com/jayakaran20/pros](https://github.com/jayakaran20/pros)

---

## 🌟 Overview

We are proud to announce the **v1.0.0 release of Cropfit**, a full-stack, cloud-ready AI agriculture platform engineered to bring precision machine learning and computer vision to agronomy.

---

## ✨ Features Included in v1.0.0

### 1. Tabular Machine Learning Recommendation
* **Model**: Native C++ XGBoost Classifier (`xgboost_crop_model.json`).
* **Accuracy**: **88.18% test accuracy** across 22 crop species.
* **Latency**: **$1.8\text{ ms}$ P95 inference latency**.
* **Features**: Evaluates Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Soil pH, and Rainfall.

### 2. Foliar Disease Computer Vision Engine
* **Model**: MobileNetV3-Small ONNX Runtime (`mobilenet_disease.onnx`).
* **Classes**: 11 botanical categories (Tomato, Potato, and Pepper Bell diseases + healthy classes).
* **Capabilities**: Multipart smartphone image upload, severity assessment, organic/chemical treatment plans, and prevention advice.

### 3. Layered Monolith Architecture & Database
* **API Framework**: FastAPI with strict Pydantic v2 schemas and validation bounds.
* **Database**: SQLite with SQLAlchemy 2.0 ORM and paginated `/api/v1/history` audit queries.
* **Observability**: Structured stream logging and `/api/v1/health` readiness probe.

### 4. Interactive Modern Frontend
* **Stack**: React 18, Vite, TypeScript, Lucide Icons, and Tailwind CSS.
* **Components**: Soil chemistry input forms, 1-click test presets, drag-and-drop leaf photo uploader, and history dashboard.

### 5. Production DevOps & Quality Gates
* **Containers**: Multi-stage `backend/Dockerfile` and `frontend/Dockerfile` with Nginx reverse proxying.
* **Orchestration**: `docker-compose.yml` with health check dependencies and volume persistence.
* **CI/CD**: GitHub Actions workflow (`.github/workflows/ci.yml`) enforcing 87% Pytest coverage and Vitest contract checks.
* **Cloud Blueprint**: `render.yaml` for zero-configuration PaaS deployment.
* **Smoke Testing**: Built-in CLI verification suite (`backend/scripts/smoke_test.py`) running 4 end-to-end checks in $<500\text{ ms}$.

---

## 📦 Documentation & AI Governance
* Flagship [`README.md`](README.md) with system architecture diagram and quickstart guides.
* [Crop Recommendation Model Card](docs/models/crop_recommendation_card.md)
* [Plant Disease Vision Model Card](docs/models/plant_disease_vision_card.md)
* [System Design Specification](docs/architecture/system_design.md)
* [Deployment Guide](DEPLOYMENT.md)
* [Contributing Guidelines](CONTRIBUTING.md)
