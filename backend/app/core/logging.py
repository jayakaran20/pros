import logging
import os
import sys
from typing import Any

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

class EndpointFilter(logging.Filter):
    """Filter out routine health-check polling from access logs to prevent log pollution."""
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        return not ("/health" in msg or "GET / HTTP" in msg)

def setup_logging() -> logging.Logger:
    """Configures structured, production-ready stream logging for Cropfit."""
    log_format = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format=log_format,
        datefmt=date_format,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    logger = logging.getLogger("cropfit")
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
    return logger

def get_logger(name: str) -> logging.Logger:
    """Returns a module-specific logger under the 'cropfit' namespace."""
    return logging.getLogger(f"cropfit.{name}")
