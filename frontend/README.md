# Frontend Client Architecture (`frontend/`)

React 18 + TypeScript + Vite + Tailwind CSS Single Page Application (SPA).

## Structure
- `src/components/`: Reusable UI design system primitives (Button, Modal, Input, Card).
- `src/features/`: Domain-driven feature slices:
  - `crop_recommendation/`: Form inputs, probability charts, advisory display.
  - `disease_detection/`: Drag-and-drop file upload, diagnosis result card.
  - `history_dashboard/`: Prediction history table and metrics.
- `src/services/`: HTTP client abstraction (Axios/Fetch) communicating with `/api/v1/`.
- `src/types/`: TypeScript interfaces mirroring backend Pydantic schemas.
