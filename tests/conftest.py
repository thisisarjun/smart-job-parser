import pytest
from unittest.mock import Mock, patch
from src.job_searcher.vendors.jsearch.vendor import JSearchVendor
from src.job_searcher.vendors.jsearch.models import Job as JSearchJob, SearchResponse
from tests.fixtures.jsearch_result import jsearch_result


@pytest.fixture
def mock_api_key():
    """Mock API key for testing"""
    return "test_api_key_123"


@pytest.fixture
def jsearch_vendor(mock_api_key):
    """Create JSearchVendor instance with mock API key"""
    with patch.dict('os.environ', {'RAPIDAPI_KEY': mock_api_key}):
        return JSearchVendor()


@pytest.fixture
def sample_jsearch_response():
    """Real JSearch API response data for testing"""
    return jsearch_result


@pytest.fixture
def sample_jsearch_job():
    """Sample JSearch job data from real API response"""
    job_data = jsearch_result["data"][0]  # First job from the sample
    return JSearchJob(**job_data)


@pytest.fixture
def sample_search_response():
    """Sample search response using real data"""
    return SearchResponse(**jsearch_result)


@pytest.fixture
def mock_httpx_response():
    """Mock httpx response"""
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    return mock_response
