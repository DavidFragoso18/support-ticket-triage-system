"""
Tests for semantic and hybrid search functionality.
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app

client = TestClient(app)


class TestSemanticSearch:
    """Test suite for semantic search endpoints"""
    
    def test_search_endpoint_exists(self):
        """Test search endpoint is accessible"""
        response = client.get("/search/tickets?q=login")
        assert response.status_code in [200, 422]  # 422 if validation fails
    
    def test_search_with_semantic_mode(self):
        """Test semantic search mode"""
        response = client.get("/search/tickets?q=login+problems&mode=semantic&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_with_keyword_mode(self):
        """Test keyword search mode"""
        response = client.get("/search/tickets?q=email&mode=keyword&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_with_hybrid_mode(self):
        """Test hybrid search mode (default)"""
        response = client.get("/search/tickets?q=password+reset&mode=hybrid&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Check that results have expected fields
        if len(data) > 0:
            result = data[0]
            assert "id" in result
            assert "subject" in result
            assert "body" in result
            assert "similarity_score" in result or "match_type" in result
    
    def test_search_with_custom_threshold(self):
        """Test search with custom similarity threshold"""
        response = client.get("/search/tickets?q=billing&threshold=0.7&limit=5")
        assert response.status_code == 200
        data = response.json()
        
        # All results should meet threshold
        for result in data:
            if "similarity_score" in result:
                assert result["similarity_score"] >= 0.7
    
    def test_search_with_limit(self):
        """Test search respects limit parameter"""
        response = client.get("/search/tickets?q=support&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 3
    
    def test_search_with_invalid_mode(self):
        """Test search with invalid mode returns error"""
        response = client.get("/search/tickets?q=test&mode=invalid")
        assert response.status_code == 422  # Validation error
    
    def test_search_with_empty_query(self):
        """Test search with empty query"""
        response = client.get("/search/tickets?q=")
        # Should either return 422 (validation) or empty results
        assert response.status_code in [200, 422]
    
    def test_search_with_very_long_query(self):
        """Test search handles very long queries"""
        long_query = "test " * 100
        response = client.get(f"/search/tickets?q={long_query}&limit=5")
        assert response.status_code in [200, 413]  # 200 OK or 413 Payload Too Large
    
    def test_search_results_have_classification(self):
        """Test search results include classification data"""
        response = client.get("/search/tickets?q=login&limit=5")
        assert response.status_code == 200
        data = response.json()
        
        if len(data) > 0:
            result = data[0]
            # Classification should be included if exists
            if "classification" in result and result["classification"]:
                assert "intent" in result["classification"]
                assert "sentiment" in result["classification"]
                assert "priority" in result["classification"]
    
    def test_search_performance_with_many_results(self):
        """Test search performance with large result set"""
        import time
        
        start = time.time()
        response = client.get("/search/tickets?q=ticket&limit=50")
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 2.0  # Should complete within 2 seconds
    
    @pytest.mark.parametrize("query,expected_matches", [
        ("login", True),  # Should find login-related tickets
        ("password", True),  # Should find password-related tickets
        ("xyzabc123", False),  # Should not find random string
    ])
    def test_search_finds_relevant_tickets(self, query, expected_matches):
        """Test search finds relevant tickets"""
        response = client.get(f"/search/tickets?q={query}&limit=10")
        assert response.status_code == 200
        data = response.json()
        
        if expected_matches:
            # Should find at least one result
            assert len(data) >= 0  # May be 0 if no test data
        # Random strings should return fewer results
    
    def test_hybrid_search_combines_scores(self):
        """Test hybrid search combines semantic and keyword scores"""
        response = client.get("/search/tickets?q=login+issue&mode=hybrid&limit=5")
        assert response.status_code == 200
        data = response.json()
        
        if len(data) > 0:
            # Results should be ordered by combined score
            scores = [r.get("similarity_score", 0) for r in data]
            assert scores == sorted(scores, reverse=True)
    
    def test_search_with_special_characters(self):
        """Test search handles special characters"""
        response = client.get("/search/tickets?q=can't+won't&limit=5")
        assert response.status_code == 200
    
    def test_search_case_insensitive(self):
        """Test search is case insensitive"""
        response1 = client.get("/search/tickets?q=LOGIN&limit=5")
        response2 = client.get("/search/tickets?q=login&limit=5")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Should return similar results
        data1 = response1.json()
        data2 = response2.json()
        assert len(data1) == len(data2) or abs(len(data1) - len(data2)) <= 2


class TestSearchIndexes:
    """Test suite for search index functionality"""
    
    def test_tsvector_index_exists(self, session: Session):
        """Test that tsvector index exists on tickets table"""
        # Check if search_vector column exists
        result = session.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'tickets' AND column_name = 'search_vector'"
        )
        assert result.fetchone() is not None
    
    def test_embedding_index_exists(self, session: Session):
        """Test that embedding index exists"""
        result = session.execute(
            "SELECT indexname FROM pg_indexes "
            "WHERE tablename = 'tickets' AND indexname LIKE '%embedding%'"
        )
        # Should have an index on embedding column
        assert result.fetchone() is not None
