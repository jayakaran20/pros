# Smart Crop Assistant — Architecture Decision Log

> This document records all significant architectural and technical decisions made during the project.  
> Decisions are numbered sequentially and immutable once recorded.  
> New decisions may supersede old ones but old entries are never deleted.

---

## ADR-001: Modular Layered Monolith Architecture

**Date**: 2026-09-24 (Phase 0)  
**Status**: Approved  

**Context**: The application needs a clear architecture pattern. Options considered:
1. Monolithic (single module, no internal boundaries)
2. Modular Layered Monolith (single deployment unit, strict internal layer boundaries)
3. Microservices (independent deployable services)

**Decision**: Use a Modular Layered Monolith with five clean layers:
- Transport/API Layer (FastAPI routers)
- Application/Service Layer (business orchestration)
- Inference Engine Layer (ML model wrappers)
- Data Repository Layer (SQLAlchemy ORM)
- Persistence Layer (PostgreSQL/SQLite)

**Reason**: A single developer cannot efficiently operate, debug, and deploy independent microservices. The monolith keeps operational complexity low while the layered boundaries ensure clean separation of concerns. If a component (e.g., the CV engine) needs independent scaling in the future, it can be extracted because its boundaries are already clean.

**Trade-offs**: 
- (+) Simple deployment, single Docker container for backend
- (+) Easy debugging with standard Python tools
- (+) Clean boundaries prevent spaghetti code
- (−) Cannot independently scale the vision inference from tabular inference
- (−) Single failure domain (one crash affects all features)

---

## ADR-002: FastAPI over Flask

**Date**: 2026-09-24 (Phase 0)  
**Status**: Approved  

**Context**: Need a Python web framework for serving ML predictions via REST API.

**Options Considered**:
1. Flask — Mature, large ecosystem, synchronous by default
2. FastAPI — Modern, async-native, built-in Pydantic validation, auto OpenAPI docs
3. Django REST Framework — Full-featured, heavy, opinionated

**Decision**: FastAPI

**Reason**: FastAPI provides native request validation via Pydantic (eliminating manual schema checking), automatic interactive API documentation (Swagger/ReDoc), and async support matching Node.js throughput. For an ML inference API where request/response contracts are critical, built-in validation is a significant advantage.

**Trade-offs**:
- (+) Type-safe request handling with Pydantic
- (+) Automatic OpenAPI documentation
- (+) Async performance for I/O-bound operations
- (−) Smaller ecosystem than Flask (fewer third-party extensions)
- (−) Steeper initial learning curve for async patterns

---

## ADR-003: PostgreSQL (Production) + SQLite (Development)

**Date**: 2026-09-24 (Phase 0)  
**Status**: Approved  

**Context**: Need a database for prediction history and user data.

**Options Considered**:
1. PostgreSQL only — Production-grade from day one
2. SQLite only — Zero configuration, file-based
3. PostgreSQL (production) + SQLite (early development) — Progressive complexity
4. MongoDB — Document store, flexible schema

**Decision**: SQLite for local development and testing; PostgreSQL for Docker Compose and production.

**Reason**: SQLite requires zero infrastructure setup, enabling immediate database integration without Docker dependency in early sessions. PostgreSQL provides ACID transactions, JSONB support, concurrent connections, and represents real production conditions. SQLAlchemy ORM abstracts the differences, so switching requires only changing the connection string.

**Trade-offs**:
- (+) Immediate productivity with SQLite (no server setup)
- (+) Production parity with PostgreSQL
- (+) SQLAlchemy abstracts dialect differences
- (−) Minor behavioral differences (e.g., SQLite type affinity is loose)
- (−) Some PostgreSQL-specific features (JSONB queries) not available in SQLite

---

## ADR-004: React + TypeScript over Streamlit

**Date**: 2026-09-24 (Phase 0)  
**Status**: Approved  

**Context**: Need a frontend for user interaction.

**Options Considered**:
1. Streamlit — Rapid Python-based data app prototyping
2. Gradio — ML-focused demo interface
3. React + TypeScript — Industry-standard component framework
4. Vue.js — Simpler learning curve, smaller ecosystem

**Decision**: React 18 with TypeScript, Tailwind CSS, and Vite.

**Reason**: Streamlit and Gradio are demo tools, not production frontend frameworks. They lack granular state management, cannot be independently deployed as static assets, do not demonstrate frontend engineering competency, and cannot cleanly integrate with a separate backend API. React with TypeScript teaches real frontend engineering with type safety matching backend Pydantic schemas.

**Trade-offs**:
- (+) Industry-standard skill set
- (+) Type safety with TypeScript
- (+) Full control over UI/UX
- (+) Independent deployment as static assets
- (−) Significantly more code than Streamlit
- (−) Requires learning JavaScript/TypeScript ecosystem
- (−) Longer time to first visible result

---

## ADR-005: PyTorch over TensorFlow for Computer Vision

**Date**: 2026-09-24 (Phase 0)  
**Status**: Approved  

**Context**: Need a deep learning framework for plant disease image classification.

**Options Considered**:
1. TensorFlow/Keras — Wide deployment, TFLite for mobile
2. PyTorch — Research standard, pythonic, easier debugging
3. JAX — Google research, functional programming

**Decision**: PyTorch with Torchvision

**Reason**: PyTorch dominates modern computer vision research and increasingly production deployment. Its imperative execution model allows standard Python debugging (breakpoints, print statements). Torchvision provides pre-trained backbones (MobileNetV3, EfficientNet) optimized for transfer learning.

**Trade-offs**:
- (+) Standard Python debugging works naturally
- (+) Dominant in research — easier to follow papers
- (+) Rich pre-trained model zoo via Torchvision
- (−) Slightly more verbose training loops than Keras
- (−) Less mature mobile deployment compared to TFLite

---

## ADR-006: MobileNetV3 as Primary Vision Backbone

**Date**: 2026-09-24 (Phase 0)  
**Status**: Approved  

**Context**: Need a CNN architecture for leaf disease classification.

**Options Considered**:
1. Custom CNN from scratch — Full control, poor accuracy
2. ResNet-50 — Proven, 25.6M parameters, heavier
3. EfficientNet-B0 — State-of-art accuracy/parameter ratio
4. MobileNetV3 — Designed for edge/mobile, ultra-low latency

**Decision**: MobileNetV3 (with EfficientNet-B0 as comparison candidate)

**Reason**: MobileNetV3 is specifically designed for resource-constrained environments. At ~2.5-5.4M parameters, it achieves >92% accuracy on transfer learning tasks while running at ~20ms on CPU. Since we deploy on cloud CPU instances (not GPUs), inference latency is critical.

**Trade-offs**:
- (+) Ultra-low latency on CPU
- (+) Small model artifact size
- (+) High accuracy via transfer learning
- (−) Slightly lower ceiling accuracy than ResNet-50/EfficientNet
- (−) Less interpretable intermediate features

---

## ADR-007: Unified prediction_records Parent Table

**Date**: 2026-09-24 (Phase 0)  
**Status**: Approved  

**Context**: Need to store prediction history for multiple task types (crop, disease, yield).

**Options Considered**:
1. Single wide table with nullable columns for all task types
2. Completely separate tables per task type
3. Parent table with 1:1 extension tables per task type

**Decision**: Option 3 — `prediction_records` parent table with `crop_predictions` and `disease_predictions` extension tables.

**Reason**: A single wide table wastes space and becomes unmaintainable as task types grow. Completely separate tables make cross-task queries ("show me all predictions") require UNION queries. The parent-extension pattern provides clean normalization while enabling simple history queries on the parent table with JOINs for task-specific details.

**Trade-offs**:
- (+) Clean normalization, no nullable columns
- (+) Easy cross-task history queries on parent table
- (+) Easy to add new task types without altering existing tables
- (−) Requires JOIN for full prediction details
- (−) Slightly more complex ORM relationships

---

*Further decisions will be recorded as the project progresses.*
