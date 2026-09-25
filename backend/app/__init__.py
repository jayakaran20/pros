"""
Smart Crop Assistant — Backend Application Root Package.

Follows the Layered Monolith Architecture approved in Phase 0.
Each layer has a single responsibility and dependencies only point downward:
Transport (api) -> Application (services) -> Inference (ml) & Persistence (db, models)
"""

__version__ = "0.1.0"
