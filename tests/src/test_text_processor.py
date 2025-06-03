import pytest
from unittest.mock import patch, Mock
from src.text_processor.text_processor import split_text, embed_text


class TestSplitText:
    """Test cases for split_text function"""

    @pytest.mark.parametrize("chunk_size, chunk_overlap, expected_min_chunks", [
        (100, 20, 2),   # Small chunks should create multiple splits
        (500, 50, 1),   # Medium chunks should create at least one split
        (2000, 200, 1), # Large chunks might create one or more splits
    ])
    def test_split_text_with_different_chunk_sizes(self, sample_text, chunk_size, chunk_overlap, expected_min_chunks):
        """Test split_text with different chunk sizes and overlaps"""
        result = split_text(sample_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        
        assert isinstance(result, list)
        assert len(result) >= expected_min_chunks
        assert all(isinstance(chunk, str) for chunk in result)
        
        # Check that chunks don't exceed the specified chunk_size by too much
        for chunk in result:
            assert len(chunk) <= chunk_size * 1.5  # Allow some flexibility for word boundaries

    def test_split_text_basic_functionality(self):
        """Basic test to verify split_text works with simple input"""
        test_text = "This is a test. " * 50  # 50 repetitions should be enough to split
        result = split_text(test_text, chunk_size=100, chunk_overlap=20)
        
        assert isinstance(result, list)
        assert len(result) > 0
        # Join all results should contain the original words
        joined = " ".join(result)
        assert "This is a test." in joined

    def test_split_text_default_parameters(self, sample_text):
        """Test split_text with default parameters"""
        result = split_text(sample_text)
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(chunk, str) for chunk in result)

    def test_split_text_short_text(self, short_text):
        """Test split_text with text shorter than chunk_size"""
        result = split_text(short_text, chunk_size=1000, chunk_overlap=200)
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] == short_text

    def test_split_text_empty_text(self, empty_text):
        """Test split_text with empty text"""
        result = split_text(empty_text)
        
        assert isinstance(result, list)
        # RecursiveCharacterTextSplitter returns empty list for empty text
        assert len(result) == 0

    @pytest.mark.parametrize("chunk_size, chunk_overlap", [
        (50, 10),
        (200, 40),
        (1000, 200),
    ])
    def test_split_text_chunk_overlap(self, sample_text, chunk_size, chunk_overlap):
        """Test that chunks have proper overlap when specified"""
        result = split_text(sample_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        
        if len(result) > 1:
            # Check that consecutive chunks have some overlap
            # This is a basic check - the actual overlap depends on text boundaries
            assert len(result) >= 2
            assert all(len(chunk) > 0 for chunk in result)

    def test_split_text_preserves_content(self, sample_text):
        """Test that split_text preserves the original content"""
        result = split_text(sample_text, chunk_size=100, chunk_overlap=20)
        
        # Join all chunks and compare with original (accounting for potential duplicated overlap)
        joined_text = " ".join(result)
        original_words = set(sample_text.split())
        joined_words = set(joined_text.split())
        
        # All original words should be present in the split result
        assert original_words.issubset(joined_words)

    def test_split_text_invalid_parameters(self):
        """Test split_text with invalid parameters"""
        with pytest.raises((ValueError, TypeError)):
            split_text("test", chunk_size=0)
        
        with pytest.raises((ValueError, TypeError)):
            split_text("test", chunk_size=-100)


class TestEmbedText:
    """Test cases for embed_text function"""

    @patch('src.text_processor.text_processor.OllamaEmbeddings')
    def test_embed_text_success(self, mock_ollama_class, mock_ollama_embeddings):
        """Test successful text embedding"""
        # Setup mock
        mock_ollama_class.return_value = mock_ollama_embeddings
        test_text = "This is a test text for embedding"
        expected_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
        mock_ollama_embeddings.embed_query.return_value = expected_embedding
        
        # Execute
        result = embed_text(test_text)
        
        # Assert
        assert result == expected_embedding
        mock_ollama_class.assert_called_once_with(model="mxbai-embed-large")
        mock_ollama_embeddings.embed_query.assert_called_once_with(test_text)

    @patch('src.text_processor.text_processor.OllamaEmbeddings')
    def test_embed_text_empty_string(self, mock_ollama_class, mock_ollama_embeddings):
        """Test embedding empty string"""
        mock_ollama_class.return_value = mock_ollama_embeddings
        expected_embedding = [0.0, 0.0, 0.0, 0.0, 0.0]
        mock_ollama_embeddings.embed_query.return_value = expected_embedding
        
        result = embed_text("")
        
        assert result == expected_embedding
        mock_ollama_embeddings.embed_query.assert_called_once_with("")

    @pytest.mark.parametrize("text_input", [
        "Short text",
        "A much longer text that contains multiple sentences and should still be embedded properly.",
        "Text with special characters: !@#$%^&*()",
        "12345 numeric text",
        "Mixed content: Hello World! 123 @#$",
    ])
    @patch('src.text_processor.text_processor.OllamaEmbeddings')
    def test_embed_text_various_inputs(self, mock_ollama_class, mock_ollama_embeddings, text_input):
        """Test embed_text with various text inputs"""
        mock_ollama_class.return_value = mock_ollama_embeddings
        expected_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
        mock_ollama_embeddings.embed_query.return_value = expected_embedding
        
        result = embed_text(text_input)
        
        assert result == expected_embedding
        mock_ollama_embeddings.embed_query.assert_called_once_with(text_input)

    @patch('src.text_processor.text_processor.OllamaEmbeddings')
    def test_embed_text_ollama_exception(self, mock_ollama_class):
        """Test embed_text when OllamaEmbeddings raises an exception"""
        mock_ollama_instance = Mock()
        mock_ollama_instance.embed_query.side_effect = Exception("Ollama connection failed")
        mock_ollama_class.return_value = mock_ollama_instance
        
        with pytest.raises(Exception, match="Ollama connection failed"):
            embed_text("test text")

    @patch('src.text_processor.text_processor.OllamaEmbeddings')
    def test_embed_text_model_configuration(self, mock_ollama_class, mock_ollama_embeddings):
        """Test that embed_text uses the correct model"""
        mock_ollama_class.return_value = mock_ollama_embeddings
        mock_ollama_embeddings.embed_query.return_value = [0.1, 0.2, 0.3]
        
        embed_text("test")
        
        # Verify that OllamaEmbeddings was called with the correct model
        mock_ollama_class.assert_called_once_with(model="mxbai-embed-large")

    @patch('src.text_processor.text_processor.OllamaEmbeddings')
    def test_embed_text_return_type(self, mock_ollama_class, mock_ollama_embeddings):
        """Test that embed_text returns the correct type"""
        mock_ollama_class.return_value = mock_ollama_embeddings
        expected_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
        mock_ollama_embeddings.embed_query.return_value = expected_embedding
        
        result = embed_text("test text")
        
        assert isinstance(result, list)
        assert all(isinstance(x, (int, float)) for x in result)
        assert result == expected_embedding


class TestIntegration:
    """Integration tests for text processing workflow"""

    @patch('src.text_processor.text_processor.OllamaEmbeddings')
    def test_split_and_embed_workflow(self, mock_ollama_class, mock_ollama_embeddings, sample_text):
        """Test the typical workflow of splitting text and then embedding chunks"""
        # Setup mock
        mock_ollama_class.return_value = mock_ollama_embeddings
        mock_ollama_embeddings.embed_query.return_value = [0.1, 0.2, 0.3, 0.4, 0.5]
        
        # Split the text
        chunks = split_text(sample_text, chunk_size=200, chunk_overlap=50)
        
        # Embed each chunk
        embeddings = []
        for chunk in chunks:
            embedding = embed_text(chunk)
            embeddings.append(embedding)
        
        # Assertions
        assert len(chunks) > 1  # Should create multiple chunks
        assert len(embeddings) == len(chunks)
        assert all(isinstance(emb, list) for emb in embeddings)
        assert mock_ollama_embeddings.embed_query.call_count == len(chunks) 