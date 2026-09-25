"""
Smart Crop Assistant — ASGI Application Entrypoint.

Initializes FastAPI application, mounts middleware, and registers versioned API routes.
"""

from typing import Any


def get_application_info() -> dict[str, Any]:
    """Return basic application metadata for startup verification."""
    return {
        "title": "Smart Crop Assistant API",
        "version": "0.1.0",
        "status": "scaffolded",
    }


if __name__ == "__main__":
    print(f"Application Initialized: {get_application_info()}")
