import pytest
import numpy as np
import tempfile
import os
from app.ml.vector_index import VectorIndex


def test_vector_index_initialization():
    """Test VectorIndex initializes with correct dimension and empty state"""
    index = VectorIndex(dimension=384)
    assert index.dimension == 384
    assert index.total_vectors == 0
    assert len(index.something_ids) == 0


def test_add_single_embedding():
    """Test adding a single embedding to the index"""
    index = VectorIndex(dimension=384)

    # Generate random 384-dim embedding
    embedding = np.random.randn(384).astype(np.float32)

    # Add with something_id=1
    index.add(something_id=1, embedding=embedding)

    # Verify state
    assert index.total_vectors == 1
    assert index.something_ids == [1]


def test_add_batch_embeddings():
    """Test adding multiple embeddings in batch"""
    index = VectorIndex(dimension=384)

    # Generate batch of 5 random embeddings
    embeddings = np.random.randn(5, 384).astype(np.float32)
    something_ids = [1, 2, 3, 4, 5]

    # Add batch
    index.add_batch(something_ids=something_ids, embeddings=embeddings)

    # Verify state
    assert index.total_vectors == 5
    assert index.something_ids == [1, 2, 3, 4, 5]


def test_search_exact_match():
    """Test search returns exact match with similarity ~1.0"""
    index = VectorIndex(dimension=384)

    # Add 3 distinct embeddings
    emb1 = np.random.randn(384).astype(np.float32)
    emb2 = np.random.randn(384).astype(np.float32)
    emb3 = np.random.randn(384).astype(np.float32)

    index.add(1, emb1)
    index.add(2, emb2)
    index.add(3, emb3)

    # Search with exact embedding
    results = index.search(emb2, top_k=3)

    # Top result should be ID=2 with similarity ~1.0
    assert results[0][0] == 2  # something_id
    assert results[0][1] > 0.99  # similarity close to 1.0


def test_search_top_k():
    """Test search respects top_k parameter"""
    index = VectorIndex(dimension=384)

    # Add 10 embeddings
    for i in range(10):
        emb = np.random.randn(384).astype(np.float32)
        index.add(i + 1, emb)

    # Search with top_k=3
    query = np.random.randn(384).astype(np.float32)
    results = index.search(query, top_k=3)

    # Should return exactly 3 results
    assert len(results) == 3

    # Results should be sorted by similarity (descending)
    similarities = [score for _, score in results]
    assert similarities == sorted(similarities, reverse=True)


def test_save_and_load():
    """Test index persistence via save and load"""
    # Create index with 5 embeddings
    index1 = VectorIndex(dimension=384)
    embeddings = np.random.randn(5, 384).astype(np.float32)
    something_ids = [10, 20, 30, 40, 50]
    index1.add_batch(something_ids, embeddings)

    # Save to temp file
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_index.faiss")
        index1.save(filepath)

        # Create new index and load
        index2 = VectorIndex(dimension=384)
        success = index2.load(filepath)

        assert success is True
        assert index2.total_vectors == 5
        assert index2.something_ids == [10, 20, 30, 40, 50]

        # Verify search results match original
        query = embeddings[2]  # Use third embedding as query
        results1 = index1.search(query, top_k=1)
        results2 = index2.search(query, top_k=1)

        assert results1[0][0] == results2[0][0]  # Same ID
        assert abs(results1[0][1] - results2[0][1]) < 0.01  # Similar score


def test_normalization():
    """Test that embeddings are normalized for cosine similarity"""
    index = VectorIndex(dimension=384)

    # Create embedding with known norm (not 1.0)
    embedding = np.ones(384, dtype=np.float32) * 2.0  # Norm = 2.0 * sqrt(384)
    assert np.linalg.norm(embedding) > 1.0  # Verify not normalized

    # Add to index (should normalize internally)
    index.add(1, embedding)

    # Search with same embedding
    results = index.search(embedding, top_k=1)

    # Similarity should be ~1.0 (proves normalization)
    assert results[0][0] == 1
    assert results[0][1] > 0.99


def test_zero_norm_vector_rejected():
    """Test that zero-norm vectors raise ValueError"""
    index = VectorIndex(dimension=384)

    # Try to add zero vector
    zero_vector = np.zeros(384, dtype=np.float32)

    with pytest.raises(ValueError, match="zero or near-zero norm"):
        index.add(1, zero_vector)


def test_wrong_dimension_rejected():
    """Test that wrong dimension vectors raise ValueError"""
    index = VectorIndex(dimension=384)

    # Try to add 512-dim vector to 384-dim index
    wrong_dim = np.random.randn(512).astype(np.float32)

    with pytest.raises(ValueError, match="dimension mismatch"):
        index.add(1, wrong_dim)


def test_negative_id_rejected():
    """Test that negative IDs raise ValueError"""
    index = VectorIndex(dimension=384)
    embedding = np.random.randn(384).astype(np.float32)

    with pytest.raises(ValueError, match="non-negative"):
        index.add(-1, embedding)


def test_none_embedding_rejected():
    """Test that None embedding raises ValueError"""
    index = VectorIndex(dimension=384)

    with pytest.raises(ValueError, match="cannot be None"):
        index.add(1, None)


def test_search_empty_index():
    """Test that searching empty index returns empty list with warning"""
    index = VectorIndex(dimension=384)
    query = np.random.randn(384).astype(np.float32)

    results = index.search(query, top_k=5)
    assert results == []


def test_invalid_top_k():
    """Test that invalid top_k raises ValueError"""
    index = VectorIndex(dimension=384)
    query = np.random.randn(384).astype(np.float32)

    with pytest.raises(ValueError, match="must be positive"):
        index.search(query, top_k=0)

    with pytest.raises(ValueError, match="must be positive"):
        index.search(query, top_k=-5)
