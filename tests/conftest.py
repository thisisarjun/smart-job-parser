import pytest
from unittest.mock import Mock, patch
from src.job_searcher.vendors.jsearch.vendor import JSearchVendor
from src.job_searcher.vendors.jsearch.models import Job as JSearchJob, SearchResponse


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
def sample_jsearch_job():
    """Sample JSearch job data for testing"""
    return JSearchJob(
        job_id="test_job_123",
        job_title="Software Engineer",
        job_description="Develop amazing software applications",
        job_apply_link="https://example.com/apply/123",
        employer_name="Tech Corp",
        job_city="San Francisco",
        job_state="CA",
        job_country="US"
    )


@pytest.fixture
def sample_search_response(sample_jsearch_job):
    """Sample search response for testing"""
    return SearchResponse(
        status="OK",
        request_id="test_request_123",
        parameters={"query": "software engineer"},
        data=[sample_jsearch_job]
    )


@pytest.fixture
def mock_httpx_response():
    """Mock httpx response"""
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    return mock_response
