import pytest

from config import settings


def test_with_session_fixture(setup_test_environment):
    """Test that uses the session-level fixture"""
    assert settings.JSEARCH_API_KEY == "test_api_key"  # pragma: allowlist secret
    assert settings.PINECONE_API_KEY == "test_pinecone_key"  # pragma: allowlist secret


def test_with_function_fixture(setup_each_test):
    """Test that uses the function-level fixture"""
    # This test will have its own setup and teardown
    assert True


class TestClass:
    """Test class that uses class-level fixture"""

    def test_with_class_fixture(self, setup_test_class):
        """Test that uses the class-level fixture"""
        assert True

    def test_another_with_class_fixture(self, setup_test_class):
        """Another test that uses the same class-level fixture"""
        assert True


@pytest.mark.usefixtures("setup_test_module")
def test_with_module_fixture():
    """Test that uses the module-level fixture"""
    assert True


# You can also use multiple fixtures
def test_with_multiple_fixtures(setup_test_environment, setup_each_test):
    """Test that uses multiple fixtures"""
    assert settings.DEBUG is True
