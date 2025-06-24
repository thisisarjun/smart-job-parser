import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Optional


class AppLogger:
    """Centralized logging configuration for the smart-job-parser application."""

    _initialized = False
    _loggers = {}

    @classmethod
    def setup_logging(
        cls,
        level: str = "INFO",
        log_file: Optional[str] = None,
        log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        date_format: str = "%Y-%m-%d %H:%M:%S",
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        console_output: bool = True,
    ) -> None:
        """
        Setup application-wide logging configuration.

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Path to log file (optional)
            log_format: Format string for log messages
            date_format: Format string for timestamps
            max_bytes: Maximum size of log file before rotation
            backup_count: Number of backup log files to keep
            console_output: Whether to output logs to console
        """
        if cls._initialized:
            return

        # Convert string level to logging constant
        numeric_level = getattr(logging, level.upper(), logging.INFO)

        # Create formatter
        formatter = logging.Formatter(log_format, date_format)

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(numeric_level)

        # Clear any existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Console handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(numeric_level)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)

        # File handler with rotation
        if log_file:
            # Ensure log directory exists
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
            )
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

        # Set propagate to False for all existing loggers to avoid duplicate messages
        for logger_name in logging.root.manager.loggerDict:
            logger = logging.getLogger(logger_name)
            logger.propagate = False

        cls._initialized = True

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get a logger instance for the specified module.

        Args:
            name: Logger name (typically __name__)

        Returns:
            Configured logger instance
        """
        if not cls._initialized:
            # Auto-setup with default configuration if not initialized
            cls.setup_logging()

        if name not in cls._loggers:
            logger = logging.getLogger(name)
            cls._loggers[name] = logger

        return cls._loggers[name]

    @classmethod
    def set_level(cls, level: str) -> None:
        """
        Set the logging level for all loggers.

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        logging.getLogger().setLevel(numeric_level)

    @classmethod
    def shutdown(cls) -> None:
        """Shutdown the logging system gracefully."""
        logging.shutdown()
        cls._initialized = False
        cls._loggers.clear()


def get_logger(name: str) -> logging.Logger:
    """
    Convenience function to get a logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    return AppLogger.get_logger(name)


def setup_logging_from_env() -> None:
    """Setup logging based on environment variables."""
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_file = os.getenv("LOG_FILE")
    console_output = os.getenv("LOG_CONSOLE", "true").lower() == "true"

    AppLogger.setup_logging(level=log_level, log_file=log_file, console_output=console_output)


# Example usage and configuration
if __name__ == "__main__":
    # Setup logging
    AppLogger.setup_logging(level="DEBUG", log_file="logs/app.log", console_output=True)

    # Get loggers for different modules
    logger = get_logger(__name__)
    logger.info("Logging system initialized")
    logger.debug("Debug message")
    logger.warning("Warning message")
    logger.error("Error message")
