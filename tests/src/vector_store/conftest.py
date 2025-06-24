from typing import List
from unittest.mock import Mock

import pytest
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore

from src.vector_store.models import AvailableVectorStores, JobVectorStore
from src.vector_store.service import VectorStoreService
from src.vector_store.stores.memory_store import MemoryStore
from tests.factories.vector_store import JobVectorStoreFactory


@pytest.fixture
def sample_job_vector_store() -> JobVectorStore:
    """Sample JobVectorStore for testing"""
    return JobVectorStoreFactory.build()


@pytest.fixture
def sample_job_vector_stores() -> List[JobVectorStore]:
    """Multiple sample JobVectorStore objects for testing"""
    return JobVectorStoreFactory.batch(5)


@pytest.fixture
def mock_embedding() -> Mock:
    """Mock embedding for testing"""
    mock_embedding = Mock(spec=Embeddings)
    mock_embedding.embed_query.return_value = [0.1, 0.2, 0.3, 0.4, 0.5]
    mock_embedding.embed_documents.return_value = [[0.1, 0.2, 0.3, 0.4, 0.5]]
    return mock_embedding


@pytest.fixture
def mock_langchain_vector_store(sample_job_vector_store: JobVectorStore) -> Mock:
    """Mock LangChain InMemoryVectorStore for testing"""
    mock_store = Mock(spec=InMemoryVectorStore)
    mock_store.add_texts.return_value = ["doc_id_1"]
    mock_store.similarity_search.return_value = [
        Document(
            page_content=sample_job_vector_store.get_combined_text_document(),
            metadata=sample_job_vector_store.get_metadata(),
        )
    ]
    return mock_store


@pytest.fixture
def memory_store(mock_embedding) -> MemoryStore:
    """Create MemoryStore instance for testing"""
    return MemoryStore(embedding=mock_embedding)


@pytest.fixture
def vector_store_service(mock_embedding) -> VectorStoreService:
    """Create VectorStoreService instance for testing"""
    return VectorStoreService(vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding)


@pytest.fixture
def minimal_job_vector_store() -> JobVectorStore:
    """Minimal JobVectorStore with only required fields"""
    return JobVectorStoreFactory.build(
        employer_name=None,
        job_city=None,
        job_state=None,
        job_country=None,
        location_string=None,
    )
