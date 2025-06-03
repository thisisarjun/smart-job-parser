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


# Text processing fixtures
@pytest.fixture
def sample_text():
    """Sample text for testing text processing functions"""
    return "This is a sample text. " * 100  # Creates a longer text for splitting


@pytest.fixture
def short_text():
    """Short text that shouldn't be split"""
    return "This is a short text that fits in one chunk."


@pytest.fixture
def empty_text():
    """Empty text for edge case testing"""
    return ""


@pytest.fixture
def mock_ollama_embeddings():
    """Mock OllamaEmbeddings for testing embed_text function"""
    mock_embeddings = Mock()
    mock_embeddings.embed_query.return_value = [0.1, 0.2, 0.3, 0.4, 0.5]  # Sample embedding vector
    return mock_embeddings
