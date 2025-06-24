import logging
import os
import tempfile
from unittest.mock import patch

from src.logger import AppLogger, get_logger, setup_logging_from_env


class TestAppLogger:
    """Test cases for the AppLogger class."""

    def setup_method(self):
        """Reset logging state before each test."""
        AppLogger.shutdown()
        # Clear all existing loggers
        for logger_name in list(logging.root.manager.loggerDict.keys()):
            del logging.root.manager.loggerDict[logger_name]

    def teardown_method(self):
        """Clean up after each test."""
        AppLogger.shutdown()

    def test_setup_logging_defaults(self):
        """Test logging setup with default parameters."""
        AppLogger.setup_logging()

        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO
        assert len(root_logger.handlers) == 1  # Console handler only

        # Check console handler
        console_handler = root_logger.handlers[0]
        assert isinstance(console_handler, logging.StreamHandler)
        assert console_handler.level == logging.INFO

    def test_setup_logging_with_file(self):
        """Test logging setup with file output."""
        with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as tmp_file:
            log_file = tmp_file.name

        try:
            AppLogger.setup_logging(level="DEBUG", log_file=log_file, console_output=False)

            root_logger = logging.getLogger()
            assert root_logger.level == logging.DEBUG
            assert len(root_logger.handlers) == 1  # File handler only

            # Check file handler
            file_handler = root_logger.handlers[0]
            assert isinstance(file_handler, logging.handlers.RotatingFileHandler)
            assert file_handler.level == logging.DEBUG

            # Test logging to file
            logger = get_logger("test_module")
            test_message = "Test log message"
            logger.info(test_message)

            # Verify message was written to file
            with open(log_file, "r") as f:
                log_content = f.read()
                assert test_message in log_content

        finally:
            # Cleanup
            if os.path.exists(log_file):
                os.unlink(log_file)

    def test_setup_logging_with_both_handlers(self):
        """Test logging setup with both console and file handlers."""
        with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as tmp_file:
            log_file = tmp_file.name

        try:
            AppLogger.setup_logging(level="WARNING", log_file=log_file, console_output=True)

            root_logger = logging.getLogger()
            assert root_logger.level == logging.WARNING
            assert len(root_logger.handlers) == 2  # Console and file handlers

            # Check handlers
            handler_types = [type(handler) for handler in root_logger.handlers]
            assert logging.StreamHandler in handler_types
            assert logging.handlers.RotatingFileHandler in handler_types

        finally:
            if os.path.exists(log_file):
                os.unlink(log_file)

    def test_setup_logging_idempotent(self):
        """Test that setup_logging is idempotent."""
        AppLogger.setup_logging(level="DEBUG")
        initial_handlers = logging.getLogger().handlers.copy()

        # Call setup again
        AppLogger.setup_logging(level="INFO")
        final_handlers = logging.getLogger().handlers

        # Should have the same handlers (no duplicates)
        assert len(initial_handlers) == len(final_handlers)

    def test_get_logger_auto_setup(self):
        """Test that get_logger automatically sets up logging if not initialized."""
        # Ensure logging is not initialized
        AppLogger.shutdown()

        logger = AppLogger.get_logger("test_module")
        assert logger is not None
        assert logger.name == "test_module"

        # Verify logging was auto-initialized
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) > 0

    def test_get_logger_caching(self):
        """Test that get_logger caches logger instances."""
        AppLogger.setup_logging()

        logger1 = AppLogger.get_logger("test_module")
        logger2 = AppLogger.get_logger("test_module")

        assert logger1 is logger2

    def test_set_level(self):
        """Test setting logging level."""
        AppLogger.setup_logging(level="INFO")
        AppLogger.set_level("DEBUG")

        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG

    def test_shutdown(self):
        """Test logging shutdown."""
        AppLogger.setup_logging()
        assert AppLogger._initialized is True

        AppLogger.shutdown()
        assert AppLogger._initialized is False
        assert len(AppLogger._loggers) == 0


class TestGetLogger:
    """Test cases for the get_logger convenience function."""

    def setup_method(self):
        """Reset logging state before each test."""
        AppLogger.shutdown()

    def teardown_method(self):
        """Clean up after each test."""
        AppLogger.shutdown()

    def test_get_logger_convenience_function(self):
        """Test the get_logger convenience function."""
        logger = get_logger("test_module")
        assert logger is not None
        assert logger.name == "test_module"
        assert isinstance(logger, logging.Logger)


class TestSetupLoggingFromEnv:
    """Test cases for environment-based logging setup."""

    def setup_method(self):
        """Reset logging state before each test."""
        AppLogger.shutdown()

    def teardown_method(self):
        """Clean up after each test."""
        AppLogger.shutdown()

    @patch.dict(
        os.environ,
        {"LOG_LEVEL": "DEBUG", "LOG_FILE": "/tmp/test.log", "LOG_CONSOLE": "false"},
    )
    def test_setup_logging_from_env_with_all_vars(self):
        """Test setup_logging_from_env with all environment variables set."""
        setup_logging_from_env()

        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG
        assert len(root_logger.handlers) == 1  # File handler only

        file_handler = root_logger.handlers[0]
        assert isinstance(file_handler, logging.handlers.RotatingFileHandler)

    @patch.dict(os.environ, {}, clear=True)
    def test_setup_logging_from_env_defaults(self):
        """Test setup_logging_from_env with no environment variables."""
        setup_logging_from_env()

        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO
        assert len(root_logger.handlers) == 1  # Console handler only

        console_handler = root_logger.handlers[0]
        assert isinstance(console_handler, logging.StreamHandler)

    @patch.dict(os.environ, {"LOG_LEVEL": "INVALID"})
    def test_setup_logging_from_env_invalid_level(self):
        """Test setup_logging_from_env with invalid log level."""
        setup_logging_from_env()

        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO  # Default fallback
