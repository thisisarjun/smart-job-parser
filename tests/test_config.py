import os

from config import settings


def test_environment_is_testing():
    """Verify that we're running in testing environment"""
    assert os.getenv("ENV") == "testing"
    assert settings.current_env == "testing"


def test_settings_are_loaded():
    """Verify that settings are loaded correctly"""
    assert settings.project_name == "Smart Job Parser"
    assert settings.api_prefix == "/api/v1"
    assert settings.vector_store_type == "memory"
