# Smart Crop Assistant — Implementation Plan

> **Document Type**: Technical Implementation Plan  
> **Version**: 1.0  
> **Last Updated**: 2026-09-24  
> **Architecture Reference**: Phase 0 Approved Architecture

---

## 1. Implementation Overview

This document defines WHAT will be implemented, WHY each component exists, which FILES are affected, and what RISKS and TESTING strategies apply. It serves as the engineering companion to the master roadmap.

---

## 2. Implementation Phases

### 2.1 Development Environment (Sessions 001–004)

**What**: Python 3.11+ virtual environment, VS Code tooling (Ruff, Mypy, Pylance), Git repository with .gitignore, GitHub remote, branching workflow practice.

**Why**: A professional development environment eliminates "works on my machine" issues, enforces consistent code formatting, catches type errors early, and provides version control safety. Without this foundation, all subsequent work is fragile.

**Files Affected**:
- `.venv/` (local, gitignored)
- `.vscode/settings.json`
- `.gitignore`
- `pyproject.toml`
- `README.md` (stub)

**Risks**:
- Python version mismatch on Windows (ensure 3.11+, not system Python 3.9)
- PATH issues with virtual environment activation on PowerShell
- Git line ending issues (CRLF vs LF on Windows)

**Testing**: `python --version` inside venv, `ruff check .` runs without errors, `git status` shows clean working tree.

**Learning Objectives**: Virtual environment isolation, dependency management, code quality tooling, version control fundamentals.

---

### 2.2 Project Structure (Sessions 005–008)

**What**: Scaffold the complete layered monolith architecture — `backend/app/` with api/, core/, db/, models/, schemas/, services/, ml/ subdirectories; `ml_experiments/` with data/, notebooks/, src/; `frontend/` React project; `docs/` documentation tree.

**Why**: Software architecture is NOT just about code — it's about organizing code so that future changes are isolated, testable, and maintainable. The layered structure prevents business logic from leaking into route handlers, ML code from coupling to database code, and training experiments from polluting production images.

**Files Affected**:
- `backend/app/**/__init__.py` (package markers with docstrings)
- `backend/pyproject.toml`
- `ml_experiments/` directory tree
- `frontend/` (Vite initialization)
- `docs/` structure
- `.env.example`
- `docker-compose.yml` (placeholder)

**Risks**:
- Over-engineering directory depth early (keep flat where sensible)
- Forgetting __init__.py files causing ModuleNotFoundError
- npm/node version issues during frontend initialization

**Testing**: Python imports between directories resolve correctly, frontend dev server starts.

**Learning Objectives**: Separation of concerns, Python package system, monorepo organization, npm/Node.js basics.

---

### 2.3 Data Science & ML Pipeline (Sessions 009–029)

**What**: Complete ML lifecycle — dataset acquisition, EDA, preprocessing, baseline modeling, model comparison (Logistic Regression, Decision Tree, Random Forest, XGBoost), hyperparameter tuning, evaluation, model selection, serialization, and standalone inference engine.

**Why**: This is the core AI/ML engineering competency. The pipeline must be reproducible, leak-free, and well-documented. Starting with baselines and progressively adding complexity teaches scientific rigor. The inference engine must be decoupled from the training environment so it can be loaded by FastAPI at startup.

**Files Affected**:
- `ml_experiments/data/raw/*.csv`
- `ml_experiments/notebooks/01_crop_eda.ipynb` through `04_tuning.ipynb`
- `ml_experiments/src/dataset.py`
- `ml_experiments/src/features.py`
- `ml_experiments/src/train_crop.py`
- `ml_experiments/src/evaluate.py`
- `ml_experiments/saved_models/*.joblib`
- `backend/app/ml/wrappers/tabular_engine.py`
- `backend/app/ml/artifacts/` (model files, gitignored)

**Risks**:
- Data leakage (fitting scaler on full dataset instead of train-only)
- Overfitting (high train accuracy, low test accuracy)
- Class imbalance masking poor minority-class performance
- Large model artifacts accidentally committed to Git

**Testing**: 
- Assertions: no null values, correct split proportions, no sample overlap
- Baseline metrics recorded as lower bounds
- Deterministic inference tests with fixed inputs
- Latency benchmarks (P95 < 50ms)

**Learning Objectives**: EDA methodology, data leakage, stratified splitting, feature scaling, algorithm comparison, cross-validation, hyperparameter search, confusion matrix analysis, model cards, artifact management.

---

### 2.4 Backend API (Sessions 030–044)

**What**: FastAPI application with health endpoint, Pydantic request/response schemas, crop recommendation endpoint, database integration (SQLAlchemy + Alembic), prediction persistence, and history query endpoint.

**Why**: The backend transforms a serialized ML model from a static file into a living, queryable service. FastAPI provides type-safe request validation, automatic API documentation, and async performance. The database stores prediction audit trails for the dashboard.

**Files Affected**:
- `backend/app/main.py`
- `backend/app/core/config.py`
- `backend/app/api/v1/endpoints/*.py`
- `backend/app/api/v1/router.py`
- `backend/app/api/deps.py`
- `backend/app/schemas/*.py`
- `backend/app/services/*.py`
- `backend/app/db/session.py`
- `backend/app/db/base.py`
- `backend/app/models/prediction.py`
- `backend/alembic.ini`
- `backend/app/db/migrations/`
- `backend/tests/`

**Risks**:
- Circular imports between modules (strict layer discipline prevents this)
- Database connection pool exhaustion under load
- Model loading failure at startup (must fail gracefully, not crash silently)

**Testing**:
- httpx TestClient integration tests
- Valid input → 200, invalid → 422, model error → 503
- Database persistence verified via test transactions

**Learning Objectives**: HTTP/REST fundamentals, request validation, dependency injection, ORM concepts, database migrations, repository pattern, API testing.

---

### 2.5 Frontend Client (Sessions 045–054)

**What**: React + TypeScript + Tailwind CSS application with routing, crop recommendation form, result display, prediction history dashboard, and full backend integration.

**Why**: Users cannot interact with JSON API responses. The frontend provides the user experience layer — form inputs with validation, loading states, error handling, and data visualization. Building it with TypeScript ensures type safety matching backend schemas.

**Files Affected**:
- `frontend/src/App.tsx`
- `frontend/src/components/**`
- `frontend/src/features/**`
- `frontend/src/hooks/**`
- `frontend/src/services/**`
- `frontend/src/types/**`
- `frontend/vite.config.ts`

**Risks**:
- CORS misconfiguration blocking API requests
- TypeScript type drift from backend Pydantic schemas
- Unhandled promise rejections on API errors

**Testing**: Component render tests, form validation tests, API mock tests.

**Learning Objectives**: React component model, TypeScript interfaces, state management, async API consumption, responsive design, loading/error states.

---

### 2.6 Computer Vision Pipeline (Sessions 058–074)

**What**: PlantVillage leaf disease dataset, image preprocessing and augmentation, MobileNetV3 transfer learning, training with cross-entropy loss, evaluation, confidence thresholding, FastAPI multipart upload endpoint, and frontend drag-and-drop UI.

**Why**: Image classification cannot be solved with tabular ML. Transfer learning leverages pre-trained ImageNet features, dramatically reducing training data requirements and training time. The multipart upload endpoint introduces file handling security.

**Files Affected**:
- `ml_experiments/data/raw/plant_disease/` (gitignored)
- `ml_experiments/notebooks/05_disease_*.ipynb`
- `ml_experiments/src/train_disease.py`
- `ml_experiments/saved_models/*.pth` (gitignored)
- `backend/app/ml/wrappers/vision_engine.py`
- `backend/app/api/v1/endpoints/diseases.py`
- `backend/app/schemas/disease.py`
- `backend/app/services/disease_service.py`
- `frontend/src/features/disease_detection/`

**Risks**:
- GPU not available (must work on CPU, will be slower)
- Large dataset download time and storage
- Overfitting on small class subsets
- Malicious file uploads disguised as images

**Testing**: Image validation tests, magic byte checks, confidence threshold tests, inference latency on CPU.

**Learning Objectives**: Convolutional neural networks, transfer learning, image augmentation, PyTorch training loops, file upload security, multipart HTTP.

---

### 2.7 Quality Assurance (Sessions 078–092)

**What**: Security hardening, comprehensive test suites (unit, integration, API, frontend, ML), structured logging, and production error handling.

**Why**: Untested software is broken software that hasn't been caught yet. Security vulnerabilities can expose user data and server resources. Structured logging enables debugging in production where you cannot attach a debugger.

**Files Affected**:
- `backend/tests/**`
- `frontend/src/**/*.test.tsx`
- `backend/app/core/logging.py`
- `backend/app/core/security.py`

**Risks**:
- Test coverage gaps in edge cases
- Flaky tests due to timing or external dependencies
- Over-mocking hiding real bugs

**Testing**: Coverage reports (≥80%), all suites green, pre-commit hooks enforce quality.

**Learning Objectives**: Testing pyramid, mocking, fixtures, code coverage, security mindset, structured logging.

---

### 2.8 DevOps & Deployment (Sessions 093–103)

**What**: Multi-stage Dockerfiles, Docker Compose orchestration, GitHub Actions CI pipeline, cloud deployment (Render/Railway/Fly.io), managed PostgreSQL, production configuration.

**Why**: Software that cannot be deployed is a science experiment, not a product. Docker guarantees environmental parity. CI/CD automates quality gates. Cloud deployment makes the application accessible.

**Files Affected**:
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `docker-compose.yml`
- `.github/workflows/ci.yml`
- `.github/workflows/cd.yml`
- Environment configuration files

**Risks**:
- Docker build failures from native dependencies (OpenCV, NumPy)
- Container networking issues between services
- Cloud platform free tier limitations
- Secret exposure in CI logs

**Testing**: Docker build verification, container health checks, CI pipeline passes, production smoke tests.

**Learning Objectives**: Containerization, multi-stage builds, container orchestration, CI/CD pipelines, cloud deployment, infrastructure management.

---

### 2.9 Documentation & Portfolio (Sessions 104–109)

**What**: Professional README, API documentation (OpenAPI), ML Model Cards, architecture documentation, deployment guide, CONTRIBUTING.md, demo recording, GitHub release.

**Why**: Code is read far more often than it is written. Documentation is what transforms a personal project into a professional portfolio piece. Model Cards document the ethical boundaries and performance characteristics of ML systems.

**Files Affected**:
- `README.md`
- `CONTRIBUTING.md`
- `docs/architecture/system_design.md`
- `docs/model_cards/*.md`
- `docs/api/openapi.json`
- `DEPLOYMENT.md`

**Risks**:
- Documentation rot (docs not matching current implementation)
- Incomplete setup instructions (test by cloning fresh and following the guide)

**Testing**: Fresh clone + docker compose up should work. Peer review of documentation clarity.

**Learning Objectives**: Technical writing, Model Card standards, API documentation, portfolio presentation.

---

## 3. Dependency Graph (Critical Path)

```
Environment (S001-S004)
    │
    ▼
Project Structure (S005-S008)
    │
    ├──────────────────────────┐
    ▼                          ▼
ML Pipeline (S009-S029)    Frontend Init (S007)
    │                          │
    ▼                          │
Backend API (S030-S044)        │
    │                          │
    ├──────────────────────────┤
    ▼                          ▼
Frontend Features (S045-S051)
    │
    ▼
█ MVP COMPLETE (S054) █
    │
    ├───────────────┐
    ▼               ▼
CV Pipeline      Auth (Optional)
(S058-S074)     (S075-S077)
    │               │
    ├───────────────┤
    ▼
Quality Assurance (S078-S092)
    │
    ▼
DevOps & Deployment (S093-S103)
    │
    ▼
Documentation & Portfolio (S104-S109)
    │
    ▼
█ PORTFOLIO COMPLETE (S109) █
```

---

## 4. Git Strategy

| Phase | Branch Pattern | Merge Target | Tag |
|-------|---------------|-------------|-----|
| Environment | `chore/initial-setup` | `main` | — |
| Structure | `chore/scaffold-*` | `main` | — |
| ML Pipeline | `feat/crop-*` | `main` | — |
| Backend | `feat/fastapi-*`, `feat/crop-api`, `feat/database` | `main` | — |
| Frontend | `feat/frontend-*`, `feat/crop-ui` | `main` | — |
| MVP | `feat/integration` | `main` | `v0.1.0-mvp` |
| CV Pipeline | `feat/disease-*` | `main` | — |
| Testing | `test/*` | `main` | — |
| DevOps | `chore/docker*`, `chore/ci-cd`, `chore/deployment` | `main` | — |
| Release | — | `main` | `v1.0.0` |

---

## 5. Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Data leakage in ML pipeline | Medium | High | Fit transformers on train split only; code review |
| Model overfitting | Medium | Medium | Cross-validation, hold-out test set, learning curves |
| CORS blocking frontend-backend | High | Low | Configure early in S052, test immediately |
| Large files in Git | Medium | High | Strict .gitignore, pre-commit hooks, code review |
| Docker build failures | Medium | Medium | Multi-stage builds, pin base images, CI verification |
| Scope creep | High | High | Strict MVP boundary, defer V2/V3 features |
| Dependency conflicts | Low | Medium | Pin versions in requirements.txt, use venv isolation |

---

## 6. Quality Gates

Before any merge to `main`:

1. ✅ `ruff check .` — Zero lint errors
2. ✅ `ruff format --check .` — Code formatted
3. ✅ `mypy app` — Zero type errors
4. ✅ `pytest --cov=app --cov-fail-under=80` — Tests pass, ≥80% coverage
5. ✅ Manual review of git diff
6. ✅ Session Definition of Done satisfied
7. ✅ Mentor/self review approved
