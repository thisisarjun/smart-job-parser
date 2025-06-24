"""
Logging configuration for different environments.

This module provides pre-configured logging setups for development,
testing, and production environments.
"""

import os
from pathlib import Path

from src.logger import AppLogger


def setup_development_logging() -> None:
    """Setup logging for development environment."""
    AppLogger.setup_logging(
        level="DEBUG",
        log_file="logs/dev.log",
        console_output=True,
        log_format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
    )


def setup_testing_logging() -> None:
    """Setup logging for testing environment."""
    AppLogger.setup_logging(
        level="INFO",
        log_file="logs/test.log",
        console_output=False,
        log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def setup_production_logging() -> None:
    """Setup logging for production environment."""
    AppLogger.setup_logging(
        level="WARNING",
        log_file="logs/production.log",
        console_output=False,
        max_bytes=50 * 1024 * 1024,  # 50MB
        backup_count=10,
        log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def setup_logging_by_environment() -> None:
    """Setup logging based on the current environment."""
    env = os.getenv("ENVIRONMENT", "development").lower()

    if env == "production":
        setup_production_logging()
    elif env == "testing":
        setup_testing_logging()
    else:
        setup_development_logging()


def setup_logging_from_config(config_path: str = None) -> None:
    """
    Setup logging from a configuration file.

    Args:
        config_path: Path to logging configuration file
    """
    if config_path and Path(config_path).exists():
        # TODO: Implement configuration file parsing
        # For now, use environment-based setup
        setup_logging_by_environment()
    else:
        setup_logging_by_environment()


# Environment-specific convenience functions
def get_development_logger(name: str):
    """Get a logger configured for development."""
    setup_development_logging()
    return AppLogger.get_logger(name)


def get_testing_logger(name: str):
    """Get a logger configured for testing."""
    setup_testing_logging()
    return AppLogger.get_logger(name)


def get_production_logger(name: str):
    """Get a logger configured for production."""
    setup_production_logging()
    return AppLogger.get_logger(name)
