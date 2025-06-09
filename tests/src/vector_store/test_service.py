from unittest.mock import Mock, patch

import pytest

from src.vector_store.models import AvailableVectorStores, JobVectorStore
from src.vector_store.service import VectorStoreService
from src.vector_store.stores.memory_store import MemoryStore


class TestVectorStoreService:
    """Test cases for VectorStoreService"""

    def test_init_with_memory_store_type(self, mock_embedding):
        """Test initialization with MEMORY vector store type"""
        service = VectorStoreService(
            vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding
        )

        assert service.vector_store is not None
        assert isinstance(service.vector_store, MemoryStore)

    @patch("src.vector_store.service.MemoryStore")
    def test_init_creates_memory_store_with_embedding(
        self, mock_memory_store_class, mock_embedding
    ):
        """Test that initialization creates MemoryStore with correct embedding"""
        mock_instance = Mock()
        mock_memory_store_class.return_value = mock_instance

        service = VectorStoreService(
            vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding
        )

        mock_memory_store_class.assert_called_once_with(embedding=mock_embedding)
        assert service.vector_store == mock_instance

    def test_add_job_details_delegates_to_vector_store(
        self, mock_embedding, sample_job_vector_store
    ):
        """Test that add_job_details delegates to the underlying vector store"""
        with patch("src.vector_store.service.MemoryStore") as mock_memory_store_class:
            mock_instance = Mock()
            mock_memory_store_class.return_value = mock_instance

            service = VectorStoreService(
                vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding
            )

            service.add_job_details(sample_job_vector_store)

            mock_instance.add_job_details.assert_called_once_with(
                sample_job_vector_store
            )

    def test_similarity_search_delegates_to_vector_store(self, mock_embedding):
        """Test that similarity_search delegates to the underlying vector store"""
        mock_results = [Mock(spec=JobVectorStore)]

        with patch("src.vector_store.service.MemoryStore") as mock_memory_store_class:
            mock_instance = Mock()
            mock_instance.similarity_search.return_value = mock_results
            mock_memory_store_class.return_value = mock_instance

            service = VectorStoreService(
                vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding
            )

            query = "python developer"
            result = service.similarity_search(query)

            mock_instance.similarity_search.assert_called_once_with(query)
            assert result == mock_results

    def test_add_job_details_with_multiple_jobs(
        self, mock_embedding, sample_job_vector_stores
    ):
        """Test adding multiple job details"""
        with patch("src.vector_store.service.MemoryStore") as mock_memory_store_class:
            mock_instance = Mock()
            mock_memory_store_class.return_value = mock_instance

            service = VectorStoreService(
                vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding
            )

            # Add multiple jobs
            for job in sample_job_vector_stores:
                service.add_job_details(job)

            # Verify each job was added
            assert mock_instance.add_job_details.call_count == len(
                sample_job_vector_stores
            )

            # Verify each call was made with correct job
            for i, job in enumerate(sample_job_vector_stores):
                call_args = mock_instance.add_job_details.call_args_list[i]
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
    def test_similarity_search_with_various_queries(self, mock_embedding, query):
        """Test similarity_search with various query strings"""
        with patch("src.vector_store.service.MemoryStore") as mock_memory_store_class:
            mock_instance = Mock()
            mock_instance.similarity_search.return_value = []
            mock_memory_store_class.return_value = mock_instance

            service = VectorStoreService(
                vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding
            )

            result = service.similarity_search(query)

            mock_instance.similarity_search.assert_called_once_with(query)
            assert result == []

    def test_similarity_search_returns_job_vector_stores(
        self, mock_embedding, sample_job_vector_stores
    ):
        """Test that similarity_search returns list of JobVectorStore objects"""
        with patch("src.vector_store.service.MemoryStore") as mock_memory_store_class:
            mock_instance = Mock()
            mock_instance.similarity_search.return_value = sample_job_vector_stores
            mock_memory_store_class.return_value = mock_instance

            service = VectorStoreService(
                vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding
            )

            result = service.similarity_search("test query")

            assert result == sample_job_vector_stores
            assert isinstance(result, list)
            assert len(result) == len(sample_job_vector_stores)

    def test_similarity_search_with_empty_results(self, mock_embedding):
        """Test similarity_search when no results are found"""
        with patch("src.vector_store.service.MemoryStore") as mock_memory_store_class:
            mock_instance = Mock()
            mock_instance.similarity_search.return_value = []
            mock_memory_store_class.return_value = mock_instance

            service = VectorStoreService(
                vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding
            )

            result = service.similarity_search("nonexistent query")

            assert result == []
            assert isinstance(result, list)

    def test_add_job_details_preserves_exceptions(
        self, mock_embedding, sample_job_vector_store
    ):
        """Test that add_job_details preserves exceptions from vector store"""
        with patch("src.vector_store.service.MemoryStore") as mock_memory_store_class:
            mock_instance = Mock()
            mock_instance.add_job_details.side_effect = ValueError("Storage error")
            mock_memory_store_class.return_value = mock_instance

            service = VectorStoreService(
                vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding
            )

            with pytest.raises(ValueError, match="Storage error"):
                service.add_job_details(sample_job_vector_store)

    def test_similarity_search_preserves_exceptions(self, mock_embedding):
        """Test that similarity_search preserves exceptions from vector store"""
        with patch("src.vector_store.service.MemoryStore") as mock_memory_store_class:
            mock_instance = Mock()
            mock_instance.similarity_search.side_effect = RuntimeError("Search error")
            mock_memory_store_class.return_value = mock_instance

            service = VectorStoreService(
                vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding
            )

            with pytest.raises(RuntimeError, match="Search error"):
                service.similarity_search("test query")

    def test_service_vector_store_attribute_access(self, mock_embedding):
        """Test that vector_store attribute is accessible"""
        service = VectorStoreService(
            vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding
        )

        assert hasattr(service, "vector_store")
        assert service.vector_store is not None
        assert isinstance(service.vector_store, MemoryStore)

    def test_add_job_details_then_search_integration(
        self, mock_embedding, sample_job_vector_store
    ):
        """Test integration of adding job details then searching"""
        with patch("src.vector_store.service.MemoryStore") as mock_memory_store_class:
            mock_instance = Mock()
            mock_instance.similarity_search.return_value = [sample_job_vector_store]
            mock_memory_store_class.return_value = mock_instance

            service = VectorStoreService(
                vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding
            )

            # Add job
            service.add_job_details(sample_job_vector_store)

            # Search for job
            results = service.similarity_search("python developer")

            # Verify both operations were called
            mock_instance.add_job_details.assert_called_once_with(
                sample_job_vector_store
            )
            mock_instance.similarity_search.assert_called_once_with("python developer")
            assert results == [sample_job_vector_store]

    def test_multiple_sequential_operations(
        self, mock_embedding, sample_job_vector_stores
    ):
        """Test multiple sequential add and search operations"""
        with patch("src.vector_store.service.MemoryStore") as mock_memory_store_class:
            mock_instance = Mock()
            mock_instance.similarity_search.return_value = sample_job_vector_stores
            mock_memory_store_class.return_value = mock_instance

            service = VectorStoreService(
                vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding
            )

            # Add multiple jobs
            for job in sample_job_vector_stores:
                service.add_job_details(job)

            # Perform multiple searches
            queries = ["python", "react", "data science"]
            for query in queries:
                results = service.similarity_search(query)
                assert results == sample_job_vector_stores

            # Verify call counts
            assert mock_instance.add_job_details.call_count == len(
                sample_job_vector_stores
            )
            assert mock_instance.similarity_search.call_count == len(queries)

    def test_service_methods_return_types(
        self, mock_embedding, sample_job_vector_store
    ):
        """Test that service methods return correct types"""
        with patch("src.vector_store.service.MemoryStore") as mock_memory_store_class:
            mock_instance = Mock()
            mock_instance.add_job_details.return_value = None
            mock_instance.similarity_search.return_value = [sample_job_vector_store]
            mock_memory_store_class.return_value = mock_instance

            service = VectorStoreService(
                vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding
            )

            # Test add_job_details returns None
            result = service.add_job_details(sample_job_vector_store)
            assert result is None

            # Test similarity_search returns list
            result = service.similarity_search("test")
            assert isinstance(result, list)


class TestVectorStoreServiceIntegration:
    """Integration tests for VectorStoreService"""

    def test_service_with_real_memory_store(
        self, mock_embedding, sample_job_vector_store
    ):
        """Test service with actual MemoryStore instance (not mocked)"""
        service = VectorStoreService(
            vector_store_type=AvailableVectorStores.MEMORY, embedding=mock_embedding
        )

        # This should not raise an exception
        service.add_job_details(sample_job_vector_store)

        # This should return a list (even if empty due to mocked embedding)
        results = service.similarity_search("python developer")
        assert isinstance(results, list)

    def test_service_initialization_with_different_embeddings(self):
        """Test service initialization with different embedding types"""
        mock_embeddings = [
            Mock(name="embedding1"),
            Mock(name="embedding2"),
            Mock(name="embedding3"),
        ]

        for embedding in mock_embeddings:
            service = VectorStoreService(
                vector_store_type=AvailableVectorStores.MEMORY, embedding=embedding
            )

            assert service.vector_store is not None
            assert isinstance(service.vector_store, MemoryStore)
