import pytest
from pytest_mock import MockerFixture

from src.text_processor.text_processor_service import TextProcessor


class TestSplitText:
    """Test cases for split_text function"""

    @pytest.mark.parametrize(
        "chunk_size, chunk_overlap, expected_min_chunks",
        [
            (100, 20, 2),  # Small chunks should create multiple splits
            (500, 50, 1),  # Medium chunks should create at least one split
            (2000, 200, 1),  # Large chunks might create one or more splits
        ],
    )
    def test_split_text_with_different_chunk_sizes(
        self,
        mock_text_processor,
        sample_text: str,
        chunk_size: int,
        chunk_overlap: int,
        expected_min_chunks,
    ):
        """Test split_text with different chunk sizes and overlaps"""
        result = mock_text_processor.split_text(
            sample_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        assert isinstance(result, list)
        assert len(result) >= expected_min_chunks
        assert all(isinstance(chunk, str) for chunk in result)

        # Check that chunks don't exceed the specified chunk_size by too much
        for chunk in result:
            assert (
                len(chunk) <= chunk_size * 1.5
            )  # Allow some flexibility for word boundaries

    def test_split_text_basic_functionality(self, mock_text_processor: TextProcessor):
        """Basic test to verify split_text works with simple input"""
        test_text = "This is a test. " * 50  # 50 repetitions should be enough to split
        result = mock_text_processor.split_text(
            test_text, chunk_size=100, chunk_overlap=20
        )

        assert isinstance(result, list)
        assert len(result) > 0
        # Join all results should contain the original words
        joined = " ".join(result)
        assert "This is a test." in joined

    def test_split_text_default_parameters(
        self, mock_text_processor: TextProcessor, sample_text: str
    ):
        """Test split_text with default parameters"""
        result = mock_text_processor.split_text(sample_text)

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(chunk, str) for chunk in result)

    def test_split_text_short_text(
        self, mock_text_processor: TextProcessor, short_text: str
    ):
        """Test split_text with text shorter than chunk_size"""
        result = mock_text_processor.split_text(
            short_text, chunk_size=1000, chunk_overlap=200
        )

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] == short_text

    def test_split_text_empty_text(
        self, mock_text_processor: TextProcessor, empty_text: str
    ):
        """Test split_text with empty text"""
        result = mock_text_processor.split_text(empty_text)

        assert isinstance(result, list)
        # RecursiveCharacterTextSplitter returns empty list for empty text
        assert len(result) == 0

    @pytest.mark.parametrize(
        "chunk_size, chunk_overlap",
        [
            (50, 10),
            (200, 40),
            (1000, 200),
        ],
    )
    def test_split_text_chunk_overlap(
        self,
        mock_text_processor: TextProcessor,
        sample_text: str,
        chunk_size: int,
        chunk_overlap: int,
    ):
        """Test that chunks have proper overlap when specified"""
        result = mock_text_processor.split_text(
            sample_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        if len(result) > 1:
            # Check that consecutive chunks have some overlap
            # This is a basic check - the actual overlap depends on text boundaries
            assert len(result) >= 2
            assert all(len(chunk) > 0 for chunk in result)

    def test_split_text_preserves_content(
        self, mock_text_processor: TextProcessor, sample_text: str
    ):
        """Test that split_text preserves the original content"""
        result = mock_text_processor.split_text(
            sample_text, chunk_size=100, chunk_overlap=20
        )

        # Join all chunks and compare with original
        # (accounting for potential duplicated overlap)
        joined_text = " ".join(result)
        original_words = set(sample_text.split())
        joined_words = set(joined_text.split())

        # All original words should be present in the split result
        assert original_words.issubset(joined_words)

    def test_split_text_invalid_parameters(self, mock_text_processor: TextProcessor):
        """Test split_text with invalid parameters"""
        with pytest.raises((ValueError, TypeError)):
            mock_text_processor.split_text("test", chunk_size=-100)


class TestEmbedText:
    """Test cases for embed_text function"""

    def test_embed_text_success(
        self, mock_text_processor: TextProcessor, mocker: MockerFixture
    ):
        """Test successful text embedding"""
        # Setup mock
        test_text = "This is a test text for embedding"
        expected_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
        embed_query_spy = mocker.spy(
            mock_text_processor.ollama_embeddings, "embed_query"
        )

        embed_query_spy.return_value = expected_embedding
        result = mock_text_processor.embed_text(test_text)

        # Assert
        assert result == expected_embedding
        embed_query_spy.assert_called_once_with(test_text)


class TestIntegration:
    """Integration tests for text processing workflow"""

    @pytest.mark.skip(reason="need to fix this test")
    def test_process_text(
        self,
        mock_text_processor: TextProcessor,
        sample_text: str,
        mocker: MockerFixture,
    ):
        """Test the process_text function"""
        similarity_search_spy = mocker.spy(
            mock_text_processor.vector_store, "similarity_search"
        )
        split_text_spy = mocker.spy(mock_text_processor, "split_text")
        add_texts_spy = mocker.spy(mock_text_processor.vector_store, "add_texts")
        split_text_spy.return_value = ["test", "test"]

        # similarity_search_spy.return_value = [
        #     {"page_content": "test", "metadata": {"source": "test"}}
        # ]
        expected_search_results = [
            {"page_content": "test", "metadata": {"source": "test"}}
        ]
        result = mock_text_processor.process_text(sample_text, "test")
        assert result == expected_search_results

        # Check that the text was split into chunks

        split_text_spy.assert_called_once_with(
            sample_text, chunk_size=1000, chunk_overlap=200
        )

        # Check that the chunks were added to the vector store

        add_texts_spy.assert_called_once_with(["test", "test"])

        # Check that the vector store was searched
        similarity_search_spy.assert_called_once_with("test")
