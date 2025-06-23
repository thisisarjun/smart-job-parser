from unittest.mock import Mock, patch

import pytest
from langchain_core.documents import Document

from src.vector_store.models import JobVectorStore
from src.vector_store.stores.memory_store import MemoryStore
from tests.factories.vector_store import JobVectorStoreFactory


class TestMemoryStore:
    """Test cases for MemoryStore"""

    def test_init_with_embedding(self, mock_embedding):
        """Test initialization with embedding"""
        store = MemoryStore(embedding=mock_embedding)
        assert store.vector_store is not None
        assert hasattr(store, "vector_store")

    @patch("src.vector_store.stores.memory_store.InMemoryVectorStore")
    def test_init_creates_langchain_vector_store(
        self, mock_vector_store_class, mock_embedding
    ):
        """Test that initialization creates LangChain InMemoryVectorStore"""
        mock_instance = Mock()
        mock_vector_store_class.return_value = mock_instance

        store = MemoryStore(embedding=mock_embedding)

        mock_vector_store_class.assert_called_once_with(embedding=mock_embedding)
        assert store.vector_store == mock_instance

    def test_add_job_details_calls_add_texts(
        self, mock_embedding, sample_job_vector_store
    ):
        """Test that add_job_details calls add_texts with correct parameters"""
        with patch(
            "src.vector_store.stores.memory_store.InMemoryVectorStore"
        ) as mock_vector_store_class:
            mock_instance = Mock()
            mock_vector_store_class.return_value = mock_instance

            store = MemoryStore(embedding=mock_embedding)
            store.add_job_details([sample_job_vector_store])

            # Verify add_texts was called
            mock_instance.add_texts.assert_called_once()

            # Get the call arguments
            call_args = mock_instance.add_texts.call_args
            texts = call_args[1]["texts"]  # keyword argument
            metadatas = call_args[1]["metadatas"]  # keyword argument

            # Verify texts parameter
            assert len(texts) == 1
            assert texts[0] == sample_job_vector_store.get_combined_text_document()

            # Verify metadatas parameter
            assert len(metadatas) == 1
            expected_metadata = sample_job_vector_store.get_metadata()
            expected_metadata["job_description"] = (
                sample_job_vector_store.job_description
            )
            expected_metadata["location_string"] = (
                sample_job_vector_store.location_string
            )
            assert metadatas[0] == expected_metadata

    def test_add_job_details_with_minimal_job(self, mock_embedding):
        """Test add_job_details with minimal job data"""
        with patch(
            "src.vector_store.stores.memory_store.InMemoryVectorStore"
        ) as mock_vector_store_class:
            mock_instance = Mock()
            mock_vector_store_class.return_value = mock_instance

            store = MemoryStore(embedding=mock_embedding)
            minimal_job_vector_store = JobVectorStoreFactory.build(
                job_id="minimal_job",
                job_description="Test description",
                employer_name=None,
                job_city=None,
                job_state=None,
                job_country=None,
                location_string=None,
            )
            store.add_job_details([minimal_job_vector_store])

            mock_instance.add_texts.assert_called_once()

            call_args = mock_instance.add_texts.call_args
            texts = call_args[1]["texts"]
            metadatas = call_args[1]["metadatas"]

            assert len(texts) == 1
            assert len(metadatas) == 1
            assert metadatas[0]["job_id"] == "minimal_job"
            assert metadatas[0]["job_description"] == "Test description"

    def test_add_job_details_metadata_includes_extra_fields(
        self, mock_embedding, sample_job_vector_store
    ):
        """Test that metadata includes job_description and location_string"""
        with patch(
            "src.vector_store.stores.memory_store.InMemoryVectorStore"
        ) as mock_vector_store_class:
            mock_instance = Mock()
            mock_vector_store_class.return_value = mock_instance

            store = MemoryStore(embedding=mock_embedding)
            store.add_job_details([sample_job_vector_store])

            call_args = mock_instance.add_texts.call_args
            metadata = call_args[1]["metadatas"][0]

            # Check that extra fields are added to metadata
            assert "job_description" in metadata
            assert "location_string" in metadata
            assert (
                metadata["job_description"] == sample_job_vector_store.job_description
            )
            assert (
                metadata["location_string"] == sample_job_vector_store.location_string
            )

    @pytest.mark.parametrize(
        "job_data",
        [
            {
                "job_id": "test_1",
                "job_title": "Python Developer",
                "job_description": "Build Python apps",
                "job_apply_link": "https://example.com/1",
                "employer_name": "Tech Co",
            },
            {
                "job_id": "test_2",
                "job_title": "React Developer",
                "job_description": "Build React apps",
                "job_apply_link": "https://example.com/2",
                "job_city": "Austin",
                "job_state": "TX",
            },
            {
                "job_id": "test_3",
                "job_title": "Full Stack Developer",
                "job_description": "Build full stack apps",
                "job_apply_link": "https://example.com/3",
            },
        ],
    )
    def test_add_job_details_with_various_job_data(self, mock_embedding, job_data):
        """Test add_job_details with various job configurations"""
        with patch(
            "src.vector_store.stores.memory_store.InMemoryVectorStore"
        ) as mock_vector_store_class:
            mock_instance = Mock()
            mock_vector_store_class.return_value = mock_instance

            job = JobVectorStore(**job_data)
            store = MemoryStore(embedding=mock_embedding)
            store.add_job_details([job])

            mock_instance.add_texts.assert_called_once()

            call_args = mock_instance.add_texts.call_args
            metadata = call_args[1]["metadatas"][0]

            assert metadata["job_id"] == job_data["job_id"]
            assert metadata["job_title"] == job_data["job_title"]
            assert metadata["job_description"] == job_data["job_description"]

    def test_similarity_search_calls_vector_store(self, mock_embedding):
        """Test that similarity_search calls the underlying vector store"""
        with patch(
            "src.vector_store.stores.memory_store.InMemoryVectorStore"
        ) as mock_vector_store_class:
            mock_instance = Mock()
            mock_vector_store_class.return_value = mock_instance
            mock_instance.similarity_search.return_value = []

            store = MemoryStore(embedding=mock_embedding)
            query = "python developer"

            result = store.similarity_search(query)

            mock_instance.similarity_search.assert_called_once_with(query)
            assert result == []

    def test_similarity_search_with_different_queries(self, mock_embedding):
        """Test similarity_search with different query strings"""
        with patch(
            "src.vector_store.stores.memory_store.InMemoryVectorStore"
        ) as mock_vector_store_class:
            mock_instance = Mock()
            mock_vector_store_class.return_value = mock_instance
            mock_instance.similarity_search.return_value = []

            store = MemoryStore(embedding=mock_embedding)

            queries = ["python", "react developer", "data scientist", ""]

            for query in queries:
                result = store.similarity_search(query)
                assert result == []

            # Verify all calls were made
            assert mock_instance.similarity_search.call_count == len(queries)

    def test_similarity_search_returns_langchain_results(self, mock_embedding):
        """Test that similarity_search returns results from LangChain"""
        mock_docs = [
            Document(
                page_content="Test content 1",
                metadata={
                    "job_id": "1",
                    "job_title": "Developer 1",
                    "job_apply_link": "https://example.com/1",
                },
            ),
            Document(
                page_content="Test content 2",
                metadata={
                    "job_id": "2",
                    "job_title": "Developer 2",
                    "job_apply_link": "https://example.com/2",
                },
            ),
        ]

        with patch(
            "src.vector_store.stores.memory_store.InMemoryVectorStore"
        ) as mock_vector_store_class:
            mock_instance = Mock()
            mock_vector_store_class.return_value = mock_instance
            mock_instance.similarity_search.return_value = mock_docs

            store = MemoryStore(embedding=mock_embedding)
            result = store.similarity_search("test query")
            expected_result = [
                JobVectorStore(
                    job_id="1",
                    job_title="Developer 1",
                    job_apply_link="https://example.com/1",
                    job_description="",
                ),
                JobVectorStore(
                    job_id="2",
                    job_title="Developer 2",
                    job_apply_link="https://example.com/2",
                    job_description="",
                ),
            ]
            assert result == expected_result
            assert len(result) == 2

    def test_similarity_search_with_empty_results(self, mock_embedding):
        """Test similarity_search when no results are found"""
        with patch(
            "src.vector_store.stores.memory_store.InMemoryVectorStore"
        ) as mock_vector_store_class:
            mock_instance = Mock()
            mock_vector_store_class.return_value = mock_instance
            mock_instance.similarity_search.return_value = []

            store = MemoryStore(embedding=mock_embedding)
            result = store.similarity_search("nonexistent query")

            assert result == []
            assert isinstance(result, list)

    def test_similarity_search_preserves_exceptions(self, mock_embedding):
        """Test that similarity_search preserves exceptions from vector store"""
        with patch(
            "src.vector_store.stores.memory_store.InMemoryVectorStore"
        ) as mock_vector_store_class:
            mock_instance = Mock()
            mock_vector_store_class.return_value = mock_instance
            mock_instance.similarity_search.side_effect = ValueError("Search error")

            store = MemoryStore(embedding=mock_embedding)

            with pytest.raises(ValueError, match="Search error"):
                store.similarity_search("test query")

    def test_multiple_add_job_details_calls(
        self, mock_embedding, sample_job_vector_stores
    ):
        """Test multiple calls to add_job_details"""
        with patch(
            "src.vector_store.stores.memory_store.InMemoryVectorStore"
        ) as mock_vector_store_class:
            mock_instance = Mock()
            mock_vector_store_class.return_value = mock_instance

            store = MemoryStore(embedding=mock_embedding)

            # Add multiple jobs
            for job in sample_job_vector_stores:
                store.add_job_details([job])

            # Verify add_texts was called for each job
            assert mock_instance.add_texts.call_count == len(sample_job_vector_stores)

    def test_add_job_details_then_search_integration(
        self, mock_embedding, sample_job_vector_store
    ):
        """Test integration of adding job details then searching"""
        with patch(
            "src.vector_store.stores.memory_store.InMemoryVectorStore"
        ) as mock_vector_store_class:
            mock_instance = Mock()
            mock_vector_store_class.return_value = mock_instance
            mock_instance.similarity_search.return_value = [
                Document(
                    page_content=sample_job_vector_store.get_combined_text_document(),
                    metadata=sample_job_vector_store.get_metadata(),
                )
            ]

            store = MemoryStore(embedding=mock_embedding)

            # Add job
            store.add_job_details([sample_job_vector_store])

            # Search for job
            results = store.similarity_search("python developer")

            # Verify both operations were called
            mock_instance.add_texts.assert_called_once()
            mock_instance.similarity_search.assert_called_once_with("python developer")
            assert len(results) == 1

    def test_store_inherits_from_vector_store_interface(self, mock_embedding):
        """Test that MemoryStore properly inherits from VectorStore interface"""
        store = MemoryStore(embedding=mock_embedding)

        # Check that it has the required methods
        assert hasattr(store, "add_job_details")
        assert hasattr(store, "similarity_search")
        assert callable(store.add_job_details)
        assert callable(store.similarity_search)
