# Logging System Documentation

## Overview

The smart-job-parser application uses a centralized logging system built on Python's standard `logging` module. This system provides consistent logging across all modules with configurable output destinations, log levels, and formatting.

## Architecture

### Core Components

1. **`src/logger.py`** - Main logging module containing:
   - `AppLogger` class - Centralized logging configuration
   - `get_logger()` convenience function
   - `setup_logging_from_env()` for environment-based configuration

2. **`logging_config.py`** - Environment-specific logging configurations:
   - Development logging setup
   - Testing logging setup
   - Production logging setup
   - Environment detection and auto-configuration

## Usage

### Basic Usage

```python
from src.logger import get_logger

# Get a logger for your module
logger = get_logger(__name__)

# Use the logger
logger.info("Application started")
logger.debug("Processing job search request")
logger.warning("API rate limit approaching")
logger.error("Failed to connect to database")
```

### Application Startup

In your main application file (`src/main.py`):

```python
from src.logger import setup_logging_from_env

# Setup logging based on environment variables
setup_logging_from_env()

# Or use environment-specific setup
from logging_config import setup_logging_by_environment
setup_logging_by_environment()
```

### Environment-Specific Configuration

```python
from logging_config import (
    setup_development_logging,
    setup_testing_logging,
    setup_production_logging
)

# For development
setup_development_logging()

# For testing
setup_testing_logging()

# For production
setup_production_logging()
```

## Configuration

### Environment Variables

The logging system can be configured using environment variables:

- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `LOG_FILE` - Path to log file (optional)
- `LOG_CONSOLE` - Whether to output to console (true/false)
- `ENVIRONMENT` - Environment name (development, testing, production)

### Default Configurations

#### Development
- Level: DEBUG
- Output: Console + File (`logs/dev.log`)
- Format: Includes function name and line number
- Console: Enabled

#### Testing
- Level: INFO
- Output: File only (`logs/test.log`)
- Format: Standard format
- Console: Disabled

#### Production
- Level: WARNING
- Output: File only (`logs/production.log`)
- Format: Standard format
- Console: Disabled
- Rotation: 50MB files, 10 backups

### Custom Configuration

```python
from src.logger import AppLogger

AppLogger.setup_logging(
    level="DEBUG",
    log_file="custom.log",
    console_output=True,
    log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    max_bytes=1024*1024,  # 1MB
    backup_count=3
)
```

## Features

### Log Rotation

Log files are automatically rotated when they reach the specified size limit:

```python
AppLogger.setup_logging(
    log_file="app.log",
    max_bytes=10*1024*1024,  # 10MB
    backup_count=5  # Keep 5 backup files
)
```

This creates files like:
- `app.log` (current)
- `app.log.1` (most recent backup)
- `app.log.2` (second most recent)
- etc.

### Logger Caching

Logger instances are cached to improve performance:

```python
logger1 = get_logger("my_module")
logger2 = get_logger("my_module")
assert logger1 is logger2  # Same instance
```

### Automatic Setup

If logging hasn't been configured when `get_logger()` is called, it automatically sets up default logging:

```python
# No setup required
logger = get_logger("my_module")  # Auto-initializes with defaults
```

## Best Practices

### 1. Use Module Names

Always use `__name__` when getting a logger:

```python
# Good
logger = get_logger(__name__)

# Bad
logger = get_logger("hardcoded_name")
```

### 2. Appropriate Log Levels

- `DEBUG` - Detailed information for debugging
- `INFO` - General information about program execution
- `WARNING` - Something unexpected happened, but the program can continue
- `ERROR` - A serious problem occurred
- `CRITICAL` - A critical error that may prevent the program from running

### 3. Structured Logging

Include relevant context in log messages:

```python
logger.info(f"Processing job search for query: '{query}', filters: {filters}")
logger.error(f"API request failed for endpoint: {endpoint}, status: {status_code}")
```

### 4. Exception Logging

Always log exceptions with context:

```python
try:
    result = api_call()
except Exception as e:
    logger.error(f"API call failed: {str(e)}", exc_info=True)
    raise
```

### 5. Performance Considerations

- Use lazy evaluation for expensive operations in debug logs
- Avoid logging in tight loops at INFO level or higher
- Use appropriate log levels to control verbosity

```python
# Good - lazy evaluation
logger.debug(f"Processing large dataset: {len(data)} items")

# Bad - expensive operation always executed
logger.debug(f"Processing large dataset: {expensive_operation(data)}")
```

## Testing

### Test Configuration

The logging system includes comprehensive tests in `tests/test_logger.py`:

```python
# Run logger tests
pytest tests/test_logger.py -v
```

### Mocking Loggers in Tests

```python
import pytest
from unittest.mock import patch

def test_my_function():
    with patch('src.my_module.logger') as mock_logger:
        # Your test code here
        my_function()

        # Assert logging calls
        mock_logger.info.assert_called_with("Expected message")
```

### Test Log Output

For testing log output, you can capture log messages:

```python
import logging
from io import StringIO

def test_log_output():
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)

    logger = get_logger("test")
    logger.addHandler(handler)

    logger.info("Test message")

    assert "Test message" in log_stream.getvalue()
```

## Troubleshooting

### Common Issues

1. **No logs appearing**
   - Check if logging is initialized
   - Verify log level is appropriate
   - Ensure handlers are configured

2. **Duplicate log messages**
   - Check for multiple logger instances
   - Verify `propagate` settings

3. **Log file not created**
   - Check file permissions
   - Verify directory exists
   - Ensure path is writable

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
import os
os.environ["LOG_LEVEL"] = "DEBUG"
from src.logger import setup_logging_from_env
setup_logging_from_env()
```

## Migration Guide

### From Basic Logging

If you're migrating from basic `logging` usage:

```python
# Old way
import logging
logger = logging.getLogger(__name__)

# New way
from src.logger import get_logger
logger = get_logger(__name__)
```

### From Custom Logging Setup

Replace custom logging configuration with the centralized system:

```python
# Old way
logging.basicConfig(level=logging.INFO)

# New way
from src.logger import setup_logging_from_env
setup_logging_from_env()
```

## API Reference

### AppLogger Class

#### Methods

- `setup_logging(**kwargs)` - Configure logging system
- `get_logger(name)` - Get logger instance
- `set_level(level)` - Set logging level
- `shutdown()` - Shutdown logging system

#### Parameters

- `level` - Logging level (str)
- `log_file` - Path to log file (str, optional)
- `log_format` - Log message format (str)
- `date_format` - Timestamp format (str)
- `max_bytes` - Max file size before rotation (int)
- `backup_count` - Number of backup files (int)
- `console_output` - Enable console output (bool)

### Convenience Functions

- `get_logger(name)` - Get logger instance
- `setup_logging_from_env()` - Setup from environment variables
