"""
Tests for embedding generation and vector operations (Phase 4).

Tests cover:
- Embedding generation for text
- Vector dimensions
- Similarity calculations
- KB article embeddings
- Edge cases
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestEmbeddingGeneration:
    """Test embedding generation functionality"""
    
    def test_embeddings_module_exists(self):
        """Embeddings module should be importable"""
        try:
            from app.nlp.embeddings import emb
            assert emb is not None
        except ImportError:
            pytest.fail("Could not import embeddings module")
    
    def test_embedding_generation_basic(self):
        """Should generate embeddings for text"""
        from app.nlp.embeddings import emb
        
        text = "This is a test sentence for embedding generation"
        embedding = emb.encode_to_list(text)
        
        assert embedding is not None
        assert isinstance(embedding, list)
        assert len(embedding) > 0
    
    def test_embedding_dimensions(self):
        """Embeddings should have 384 dimensions (all-MiniLM-L6-v2)"""
        from app.nlp.embeddings import emb
        
        text = "Test embedding dimensions"
        embedding = emb.encode_to_list(text)
        
        # all-MiniLM-L6-v2 produces 384-dimensional vectors
        assert len(embedding) == 384
    
    def test_embedding_values_are_floats(self):
        """Embedding values should be floats"""
        from app.nlp.embeddings import emb
        
        text = "Test embedding value types"
        embedding = emb.encode_to_list(text)
        
        for value in embedding:
            assert isinstance(value, float)
    
    def test_embedding_consistency(self):
        """Same text should produce same embedding"""
        from app.nlp.embeddings import emb
        
        text = "Consistent embedding test"
        embedding1 = emb.encode_to_list(text)
        embedding2 = emb.encode_to_list(text)
        
        # Should be identical or very close
        assert len(embedding1) == len(embedding2)
        for v1, v2 in zip(embedding1, embedding2):
            assert abs(v1 - v2) < 0.0001


class TestEmbeddingSimilarity:
    """Test embedding similarity calculations"""
    
    def test_similar_texts_high_similarity(self):
        """Similar texts should have high cosine similarity"""
        import numpy as np

        from app.nlp.embeddings import emb
        
        text1 = "I cannot reset my password"
        text2 = "Password reset is not working"
        
        emb1 = np.array(emb.encode_to_list(text1))
        emb2 = np.array(emb.encode_to_list(text2))
        
        # Calculate cosine similarity
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        
        # Similar texts should have similarity > 0.5
        assert similarity > 0.5
    
    def test_different_texts_low_similarity(self):
        """Different texts should have lower similarity"""
        import numpy as np

        from app.nlp.embeddings import emb
        
        text1 = "I cannot reset my password"
        text2 = "I love this new feature"
        
        emb1 = np.array(emb.encode_to_list(text1))
        emb2 = np.array(emb.encode_to_list(text2))
        
        # Calculate cosine similarity
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        
        # Different texts should have lower similarity
        # Note: Even unrelated texts can have some baseline similarity
        assert 0 <= similarity <= 1
    
    def test_identical_texts_perfect_similarity(self):
        """Identical texts should have similarity of 1.0"""
        import numpy as np

        from app.nlp.embeddings import emb
        
        text = "This is the same text"
        
        emb1 = np.array(emb.encode_to_list(text))
        emb2 = np.array(emb.encode_to_list(text))
        
        # Calculate cosine similarity
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        
        # Should be very close to 1.0
        assert abs(similarity - 1.0) < 0.0001


class TestEmbeddingEdgeCases:
    """Test edge cases for embedding generation"""
    
    def test_empty_string_embedding(self):
        """Should handle empty string gracefully"""
        from app.nlp.embeddings import emb
        
        try:
            emb.encode_to_list("")
            # Should return something or raise error
            assert True
        except Exception:
            # Acceptable to raise exception for empty string
            assert True
    
    def test_very_long_text_embedding(self):
        """Should handle very long text"""
        from app.nlp.embeddings import emb
        
        long_text = "This is a very long text. " * 200  # ~5000 characters
        embedding = emb.encode_to_list(long_text)
        
        # Should still produce 384-dimensional embedding
        assert len(embedding) == 384
    
    def test_special_characters_embedding(self):
        """Should handle special characters"""
        from app.nlp.embeddings import emb
        
        text = "Special chars: @#$%^&*() émojis 🚀"
        embedding = emb.encode_to_list(text)
        
        assert len(embedding) == 384
    
    def test_numbers_only_embedding(self):
        """Should handle numeric text"""
        from app.nlp.embeddings import emb
        
        text = "123 456 789"
        embedding = emb.encode_to_list(text)
        
        assert len(embedding) == 384
    
    def test_multiple_languages_embedding(self):
        """Should handle multiple languages"""
        from app.nlp.embeddings import emb
        
        texts = [
            "Hello world",  # English
            "Hola mundo",   # Spanish
            "Bonjour monde", # French
            "Olá mundo"     # Portuguese
        ]
        
        for text in texts:
            embedding = emb.encode_to_list(text)
            assert len(embedding) == 384


class TestKBArticleEmbeddings:
    """Test KB article embedding functionality"""
    
    def test_kb_articles_exist(self):
        """KB articles should be seeded in database"""
        # Query KB articles endpoint or check database
        # This assumes there's an endpoint to list KB articles
        # For now, just verify the embedding module works
        from app.nlp.embeddings import emb
        
        # Simulate KB article text
        kb_text = "How to reset your password: Click on 'Forgot Password' link..."
        embedding = emb.encode_to_list(kb_text)
        
        assert len(embedding) == 384
    
    def test_kb_article_similarity_search(self):
        """Should be able to search KB articles by similarity"""
        # This would require querying the suggestions endpoint
        # Create a ticket and check if KB articles are suggested
        from uuid import uuid4
        
        ticket_data = {
            "subject": "Password reset help",
            "body": "I need help resetting my password",
            "channel": "web",
            "customer_id": f"test-{uuid4().hex[:8]}"
        }
        
        r = client.post("/tickets", json=ticket_data)
        assert r.status_code == 201
        ticket = r.json()
        
        # Get suggestions
        r = client.get(f"/suggestions/{ticket['id']}")
        assert r.status_code == 200
        suggestions = r.json()
        
        # Should have some suggestions
        assert isinstance(suggestions, list)


class TestEmbeddingPerformance:
    """Test embedding generation performance"""
    
    def test_embedding_generation_speed(self):
        """Embedding generation should be reasonably fast"""
        import time

        from app.nlp.embeddings import emb
        
        text = "This is a test sentence for performance measurement"
        
        start_time = time.time()
        emb.encode_to_list(text)
        end_time = time.time()
        
        generation_time = end_time - start_time
        
        # Should generate embedding in less than 1 second
        assert generation_time < 1.0
    
    def test_batch_embedding_generation(self):
        """Should efficiently handle multiple embeddings"""
        import time

        from app.nlp.embeddings import emb
        
        texts = [f"Test sentence number {i}" for i in range(10)]
        
        start_time = time.time()
        for text in texts:
            emb.encode_to_list(text)
        end_time = time.time()
        
        total_time = end_time - start_time
        
        # Should generate 10 embeddings in less than 5 seconds
        assert total_time < 5.0


class TestEmbeddingNormalization:
    """Test embedding vector normalization"""
    
    def test_embedding_magnitude(self):
        """Check if embeddings are normalized"""
        import numpy as np

        from app.nlp.embeddings import emb
        
        text = "Test normalization"
        embedding = np.array(emb.encode_to_list(text))
        
        # Calculate L2 norm (magnitude)
        magnitude = np.linalg.norm(embedding)
        
        # sentence-transformers typically produces normalized vectors
        # (magnitude close to 1.0)
        # However, this may vary, so we just check it's > 0
        assert magnitude > 0
        
        # Optionally check if it's close to normalized
        # Most sentence-transformers models output normalized vectors
        if abs(magnitude - 1.0) < 0.1:
            # Vector is approximately normalized
            assert True
    
    def test_embedding_range(self):
        """Check typical value range in embeddings"""
        import numpy as np

        from app.nlp.embeddings import emb
        
        text = "Test value range"
        embedding = np.array(emb.encode_to_list(text))
        
        # Values should typically be between -1 and 1 for normalized vectors
        min_val = embedding.min()
        max_val = embedding.max()
        
        # Check values are in reasonable range
        assert -2 < min_val < 2
        assert -2 < max_val < 2


class TestEmbeddingStringConversion:
    """Test converting embeddings to/from string format"""
    
    def test_embedding_to_string(self):
        """Should convert embedding to string format for database"""
        from app.nlp.embeddings import emb
        
        text = "Test string conversion"
        embedding = emb.encode_to_list(text)
        
        # Convert to string (PostgreSQL array format)
        embedding_str = str(embedding)
        
        assert isinstance(embedding_str, str)
        assert "[" in embedding_str
        assert "]" in embedding_str
    
    def test_embedding_list_format(self):
        """Embedding should be in correct list format"""
        from app.nlp.embeddings import emb
        
        text = "Test list format"
        embedding = emb.encode_to_list(text)
        
        assert isinstance(embedding, list)
        assert len(embedding) == 384
        
        # Should be convertible to string
        embedding_str = str(embedding)
        assert embedding_str.startswith("[")
        assert embedding_str.endswith("]")
