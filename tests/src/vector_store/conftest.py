from typing import List
from unittest.mock import Mock

import pytest
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore

from src.vector_store.models import AvailableVectorStores, JobVectorStore
from src.vector_store.service import VectorStoreService
from src.vector_store.stores.memory_store import MemoryStore


@pytest.fixture
def sample_job_vector_store() -> JobVectorStore:
    """Sample JobVectorStore for testing"""
    return JobVectorStore(
        job_id="job_123",
        job_title="Senior Python Developer",
        job_description=(
            "We are looking for an experienced Python developer to join our "
            "team. You will work on backend services, APIs, and data "
            "processing pipelines."
        ),
        job_apply_link="https://example.com/jobs/123",
        employer_name="Tech Solutions Inc",
        job_city="San Francisco",
        job_state="CA",
        job_country="USA",
        location_string="San Francisco, CA, USA",
    )


@pytest.fixture
def sample_job_vector_stores() -> List[JobVectorStore]:
    """Multiple sample JobVectorStore objects for testing"""
    return [
        JobVectorStore(
            job_id="job_123",
            job_title="Senior Python Developer",
            job_description=(
                "We are looking for an experienced Python developer to "
                "join our team."
            ),
            job_apply_link="https://example.com/jobs/123",
            employer_name="Tech Solutions Inc",
            job_city="San Francisco",
            job_state="CA",
            job_country="USA",
            location_string="San Francisco, CA, USA",
        ),
        JobVectorStore(
            job_id="job_456",
            job_title="Frontend React Developer",
            job_description=(
                "Join our frontend team to build amazing user interfaces " "with React."
            ),
            job_apply_link="https://example.com/jobs/456",
            employer_name="Web Innovations LLC",
            job_city="New York",
            job_state="NY",
            job_country="USA",
            location_string="New York, NY, USA",
        ),
        JobVectorStore(
            job_id="job_789",
            job_title="Data Scientist",
            job_description=(
                "Analyze data and build machine learning models for "
                "business insights."
            ),
            job_apply_link="https://example.com/jobs/789",
            employer_name="Data Corp",
            job_city="Austin",
            job_state="TX",
            job_country="USA",
            location_string="Austin, TX, USA",
        ),
    ]


@pytest.fixture
def mock_embedding() -> Mock:
    """Mock embedding for testing"""
    mock_embedding = Mock(spec=Embeddings)
    mock_embedding.embed_query.return_value = [0.1, 0.2, 0.3, 0.4, 0.5]
    mock_embedding.embed_documents.return_value = [[0.1, 0.2, 0.3, 0.4, 0.5]]
    return mock_embedding


@pytest.fixture
def mock_langchain_vector_store() -> Mock:
    """Mock LangChain InMemoryVectorStore for testing"""
    mock_store = Mock(spec=InMemoryVectorStore)
    mock_store.add_texts.return_value = ["doc_id_1"]
    mock_store.similarity_search.return_value = [
        Document(
            page_content=(
                "Job Title: Senior Python Developer\nCompany: Tech Solutions "
                "Inc\nLocation: San Francisco, CA, USA\n\nDescription: We are "
                "looking for an experienced Python developer to join our team."
            ),
            metadata={
                "job_id": "job_123",
                "job_title": "Senior Python Developer",
                "employer_name": "Tech Solutions Inc",
                "job_city": "San Francisco",
                "job_state": "CA",
                "job_country": "USA",
                "job_apply_link": "https://example.com/jobs/123",
                "job_description": (
                    "We are looking for an experienced Python developer to "
                    "join our team."
                ),
                "location_string": "San Francisco, CA, USA",
            },
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
    return VectorStoreService(
        vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding
    )


@pytest.fixture
def minimal_job_vector_store() -> JobVectorStore:
    """Minimal JobVectorStore with only required fields"""
    return JobVectorStore(
        job_id="minimal_job",
        job_title="Test Job",
        job_description="Test description",
        job_apply_link="https://example.com/test",
    )
