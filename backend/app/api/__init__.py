"""
API / Transport Layer.

Responsibilities:
- Route registration and URL prefixes.
- HTTP Request deserialization and Response serialization.
- Status code mapping and HTTP exception handling.

Rules:
- NEVER perform direct database queries here (delegate to services or repositories).
- NEVER execute machine learning math directly here (delegate to ML inference wrappers).
"""
