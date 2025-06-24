from unittest.mock import Mock

import pytest

from src.vector_store.models import JobVectorStore
from src.vector_store.service import VectorStoreService
from src.vector_store.stores.memory_store import MemoryStore


class TestVectorStoreService:
    """Test cases for VectorStoreService"""

    def test_init_with_vector_store(self):
        """Test initialization with vector store instance"""
        mock_store = Mock(spec=MemoryStore)
        service = VectorStoreService(vector_store=mock_store)

        assert service.vector_store is mock_store  # Test exact instance reference

    def test_init_requires_vector_store(self):
        """Test that initialization requires a vector store"""
        with pytest.raises(TypeError):
            VectorStoreService()  # No vector_store provided

    def test_add_job_details_delegates_to_vector_store(self, sample_job_vector_store):
        """Test that add_job_details delegates to the underlying vector store"""
        mock_store = Mock(spec=MemoryStore)
        service = VectorStoreService(vector_store=mock_store)

        service.add_job_details(sample_job_vector_store)

        mock_store.add_job_details.assert_called_once_with(sample_job_vector_store)

    def test_similarity_search_delegates_to_vector_store(self):
        """Test that similarity_search delegates to the underlying vector store"""
        mock_results = [Mock(spec=JobVectorStore)]
        mock_store = Mock(spec=MemoryStore)
        mock_store.similarity_search.return_value = mock_results
        service = VectorStoreService(vector_store=mock_store)

        query = "python developer"
        result = service.similarity_search(query)

        mock_store.similarity_search.assert_called_once_with(query)
        assert result == mock_results

    def test_add_job_details_with_multiple_jobs(self, sample_job_vector_stores):
        """Test adding multiple job details"""
        mock_store = Mock(spec=MemoryStore)
        service = VectorStoreService(vector_store=mock_store)

        # Add multiple jobs
        for job in sample_job_vector_stores:
            service.add_job_details(job)

        # Verify each job was added
        assert mock_store.add_job_details.call_count == len(sample_job_vector_stores)

        # Verify each call was made with correct job
        for i, job in enumerate(sample_job_vector_stores):
            call_args = mock_store.add_job_details.call_args_list[i]
            assert call_args[0][0] == job

    @pytest.mark.parametrize(
        "query",
        [
            "python developer",
            "react frontend",
            "data scientist",
            "machine learning engineer",
            "devops specialist",
            "",
            "very long query with many words to test edge cases",
        ],
    )
    def test_similarity_search_with_various_queries(self, query):
        """Test similarity_search with various query strings"""
        mock_store = Mock(spec=MemoryStore)
        mock_store.similarity_search.return_value = []
        service = VectorStoreService(vector_store=mock_store)

        result = service.similarity_search(query)

        mock_store.similarity_search.assert_called_once_with(query)
        assert result == []

    def test_similarity_search_returns_job_vector_stores(self, sample_job_vector_stores):
        """Test that similarity_search returns list of JobVectorStore objects"""
        mock_store = Mock(spec=MemoryStore)
        mock_store.similarity_search.return_value = sample_job_vector_stores
        service = VectorStoreService(vector_store=mock_store)

        result = service.similarity_search("test query")

        assert result == sample_job_vector_stores
        assert isinstance(result, list)
        assert len(result) == len(sample_job_vector_stores)

    def test_similarity_search_with_empty_results(self):
        """Test similarity_search when no results are found"""
        mock_store = Mock(spec=MemoryStore)
        mock_store.similarity_search.return_value = []
        service = VectorStoreService(vector_store=mock_store)

        result = service.similarity_search("nonexistent query")

        assert result == []
        assert isinstance(result, list)

    def test_add_job_details_preserves_exceptions(self, sample_job_vector_store):
        """Test that add_job_details preserves exceptions from vector store"""
        mock_store = Mock(spec=MemoryStore)
        mock_store.add_job_details.side_effect = ValueError("Storage error")
        service = VectorStoreService(vector_store=mock_store)

        with pytest.raises(ValueError, match="Storage error"):
            service.add_job_details(sample_job_vector_store)

    def test_similarity_search_preserves_exceptions(self):
        """Test that similarity_search preserves exceptions from vector store"""
        mock_store = Mock(spec=MemoryStore)
        mock_store.similarity_search.side_effect = RuntimeError("Search error")
        service = VectorStoreService(vector_store=mock_store)

        with pytest.raises(RuntimeError, match="Search error"):
            service.similarity_search("test query")

    def test_service_vector_store_attribute_access(self):
        """Test that vector_store attribute is accessible"""
        mock_store = Mock(spec=MemoryStore)
        service = VectorStoreService(vector_store=mock_store)

        assert hasattr(service, "vector_store")
        assert service.vector_store is mock_store  # Test exact instance reference

    def test_add_job_details_then_search_integration(self, sample_job_vector_store):
        """Test integration of adding job details then searching"""
        mock_store = Mock(spec=MemoryStore)
        mock_store.similarity_search.return_value = [sample_job_vector_store]
        service = VectorStoreService(vector_store=mock_store)

        # Add job
        service.add_job_details(sample_job_vector_store)

        # Search for job
        results = service.similarity_search("python developer")

        # Verify both operations were called
        mock_store.add_job_details.assert_called_once_with(sample_job_vector_store)
        mock_store.similarity_search.assert_called_once_with("python developer")
        assert results == [sample_job_vector_store]

    def test_multiple_sequential_operations(self, sample_job_vector_stores):
        """Test multiple sequential add and search operations"""
        mock_store = Mock(spec=MemoryStore)
        mock_store.similarity_search.return_value = sample_job_vector_stores
        service = VectorStoreService(vector_store=mock_store)

        # Add multiple jobs
        for job in sample_job_vector_stores:
            service.add_job_details(job)

        # Perform multiple searches
        queries = ["python", "react", "data science"]
        for query in queries:
            results = service.similarity_search(query)
            assert results == sample_job_vector_stores

        # Verify call counts
        assert mock_store.add_job_details.call_count == len(sample_job_vector_stores)
        assert mock_store.similarity_search.call_count == len(queries)

    def test_service_methods_return_types(self, sample_job_vector_store):
        """Test that service methods return correct types"""
        mock_store = Mock(spec=MemoryStore)
        mock_store.add_job_details.return_value = None
        mock_store.similarity_search.return_value = [sample_job_vector_store]
        service = VectorStoreService(vector_store=mock_store)

        # Test add_job_details returns None
        service.add_job_details(sample_job_vector_store)
        # No assertion needed since add_job_details returns None

        # Test similarity_search returns list
        result = service.similarity_search("test")
        assert isinstance(result, list)


class TestVectorStoreServiceIntegration:
    """Integration tests for VectorStoreService"""

    def test_service_with_real_memory_store(self, mock_embedding, sample_job_vector_store):
        """Test service with actual MemoryStore instance (not mocked)"""
        memory_store = MemoryStore(embedding=mock_embedding)
        service = VectorStoreService(vector_store=memory_store)

        # This should not raise an exception
        service.add_job_details([sample_job_vector_store])

        # This should return a list (even if empty due to mocked embedding)
        results = service.similarity_search("python developer")
        assert isinstance(results, list)

    def test_service_initialization_with_different_stores(self):
        """Test service initialization with different store types"""
        mock_stores = [
            Mock(spec=MemoryStore, name="store1"),
            Mock(spec=MemoryStore, name="store2"),
            Mock(spec=MemoryStore, name="store3"),
        ]

        for store in mock_stores:
            service = VectorStoreService(vector_store=store)
            assert service.vector_store is store  # Test exact instance reference
