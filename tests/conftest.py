from unittest.mock import Mock, patch

import pytest
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

from src.job_searcher.vendors.jsearch.vendor import JSearchVendor
from src.text_processor.text_processor_service import TextProcessor


@pytest.fixture
def mock_api_key():
    """Mock API key for testing"""
    return "test_api_key_123"


@pytest.fixture
def jsearch_vendor(mock_api_key):
    """Create JSearchVendor instance with mock API key"""
    with patch.dict("os.environ", {"JSEARCH_API_KEY": mock_api_key}):
        return JSearchVendor()


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
def mock_ollama_class():
    """Mock OllamaEmbeddings class for testing embed_text function"""
    mock_class = Mock(spec=OllamaEmbeddings)
    mock_class.embed_query.return_value = [0.1, 0.2, 0.3, 0.4, 0.5]
    return mock_class


@pytest.fixture
def mock_vector_store():
    """Mock vector store for testing process_text function"""
    mock_instance = Mock(spec=InMemoryVectorStore)
    mock_instance.similarity_search.return_value = [{"page_content": "test", "metadata": {"source": "test"}}]
    return mock_instance


@pytest.fixture(autouse=True)
def mock_pinecone():
    with patch("src.vector_store.stores.pinecone_store.Pinecone") as MockPinecone:
        yield MockPinecone


@pytest.fixture
def mock_text_processor(mock_ollama_class, mock_vector_store):
    """Mock text processor for testing process_text function"""
    text_processor = TextProcessor(mock_ollama_class, mock_vector_store)
    return text_processor
