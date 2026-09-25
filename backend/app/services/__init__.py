"""
Application / Domain Service Layer.

Responsibilities:
- Business logic orchestration.
- Mediating between the API controllers, ML inference engines, and database repositories.
- Generating agronomic advisory notes and formatting domain recommendations.

Rules:
- Services are pure Python; they DO NOT import FastAPI `Request` or `Response` objects.
- Can be invoked from CLI tools, background workers, or unit tests without an HTTP server.
"""
