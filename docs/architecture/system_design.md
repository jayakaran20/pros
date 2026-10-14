# System Design & Architecture — Cropfit

## 1. Architectural Philosophy: The Layered Monolith

Cropfit is deliberately designed as a **Layered Modular Monolith**. For early-to-mid-stage AI systems, a layered monolith drastically outperforms microservices by eliminating:
* Distributed network latency across model services.
* Complex inter-service gRPC / Kafka orchestration overhead.
* Multi-repo synchronization drift.

The application enforces strict separation of concerns across 4 discrete tiers:

```
[ Tier 1: Client Layer ]
   └─ React 18 + Vite + TypeScript (Single-Page App)
        │ (HTTP / JSON over Nginx Reverse Proxy)
        ▼
[ Tier 2: Presentation & API Layer ]
   └─ FastAPI Router (Endpoints: /predict, /history, /diseases, /health)
   └─ Pydantic v2 (Schema Validation, Type Contracts, Custom Bounds)
        │
        ▼
[ Tier 3: Business Logic & Orchestration Layer ]
   └─ CropService, DiseaseService, HistoryService
   └─ Preprocessing Pipeline & Feature Encoders
        │
        ├──> [ ML Inference Engines ] (XGBoost Booster, MobileNetV3 ONNX)
        │
        ▼
[ Tier 4: Data Persistence Layer ]
   └─ SQLAlchemy 2.0 ORM & SQLite Storage (/app/data/cropfit.db)
```

---

## 2. Database Schema Design

The persistence tier tracks all agronomic interactions via a single unified audit model (`PredictionRecord`):

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `Integer` | Primary Key, Auto-increment | Unique identifier |
| `task_type` | `String(50)` | Indexed, Not Null | `"crop_recommendation"` or `"disease_detection"` |
| `input_features` | `JSON` | Not Null | Serialized input dictionary (soil params or image metadata) |
| `recommended_crop` | `String(100)` | Nullable | Crop recommended by XGBoost |
| `confidence` | `Float` | Nullable | Confidence percentage ($0.0$ to $100.0$) |
| `disease_name` | `String(150)` | Nullable | Diagnosed foliar disease condition |
| `remedy` | `Text` | Nullable | Recommended agronomic treatment plan |
| `created_at` | `DateTime` | Indexed, Default UTC | ISO timestamp of prediction |

---

## 3. High-Throughput Model Inference Strategy

1. **In-Memory Residency (Lifespan Context)**:
   * Both the XGBoost Booster and ONNX Runtime session are initialized once during the FastAPI `lifespan` startup event and held in singleton memory wrappers.
   * Model files are NEVER re-read from disk on incoming requests, avoiding I/O bottlenecks.
2. **Native C++ Execution**:
   * Scikit-learn wrapper layers are discarded in favor of `xgboost.Booster` and NumPy array manipulation.
   * Eliminates Python Cython C-extension dependency conflicts and yields an inference latency of $\approx 1.8\text{ ms}$.

---

## 4. Security & Hardening Best Practices

* **Container Least Privilege**: All Docker containers execute under a dedicated non-root user (`appuser`, UID 10001).
* **MIME & Magic Byte Validation**: Image uploads are validated via binary headers (magic numbers) and size-restricted to prevent memory exhaustion.
* **CORS & Environment Separation**: Production CORS headers are tightly bounded to authorized domains.
* **Persistent Volumes**: SQLite files reside on dedicated storage volumes to ensure zero data loss during automated redeployments.
