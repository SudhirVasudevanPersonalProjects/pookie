import pytest
from app.services.embedding_service import embedding_service, EmbeddingService


def test_load_model():
    """Test that model loads successfully"""
    embedding_service.load_model()
    assert embedding_service.model is not None
    assert embedding_service.model_name == "all-MiniLM-L6-v2"


def test_generate_embedding():
    """Test single embedding generation"""
    # Ensure model is loaded
    if embedding_service.model is None:
        embedding_service.load_model()

    text = "test text"
    result = embedding_service.generate_embedding(text)

    assert isinstance(result, list)
    assert len(result) == 384
    assert all(isinstance(x, float) for x in result)


def test_generate_embedding_empty_text():
    """Test that empty text raises ValueError"""
    # Ensure model is loaded
    if embedding_service.model is None:
        embedding_service.load_model()

    with pytest.raises(ValueError, match="Text cannot be empty"):
        embedding_service.generate_embedding("")

    with pytest.raises(ValueError, match="Text cannot be empty"):
        embedding_service.generate_embedding("   ")


def test_generate_embeddings_batch():
    """Test batch embedding generation"""
    # Ensure model is loaded
    if embedding_service.model is None:
        embedding_service.load_model()

    texts = ["text 1", "text 2", "text 3"]
    result = embedding_service.generate_embeddings_batch(texts)

    assert isinstance(result, list)
    assert len(result) == 3
    for embedding in result:
        assert isinstance(embedding, list)
        assert len(embedding) == 384
        assert all(isinstance(x, float) for x in embedding)


def test_compute_similarity_identical():
    """Test similarity computation for identical text"""
    # Ensure model is loaded
    if embedding_service.model is None:
        embedding_service.load_model()

    text = "fitness goal"
    emb1 = embedding_service.generate_embedding(text)
    emb2 = embedding_service.generate_embedding(text)

    similarity = embedding_service.compute_similarity(emb1, emb2)

    assert isinstance(similarity, float)
    assert similarity > 0.99  # Should be ~1.0 for identical text


def test_compute_similarity_different():
    """Test similarity computation for different concepts"""
    # Ensure model is loaded
    if embedding_service.model is None:
        embedding_service.load_model()

    # Use more distinct concepts to ensure robust test
    emb1 = embedding_service.generate_embedding("fitness")
    emb2 = embedding_service.generate_embedding("mathematics")

    similarity = embedding_service.compute_similarity(emb1, emb2)

    assert isinstance(similarity, float)
    assert similarity < 0.7  # Different concepts should have low similarity


def test_generate_embedding_model_not_loaded():
    """Test that calling generate_embedding before load_model raises error"""
    # Create fresh instance to ensure model is None
    service = EmbeddingService()
    with pytest.raises(ValueError, match="Model not loaded"):
        service.generate_embedding("test")


def test_generate_embeddings_batch_model_not_loaded():
    """Test that calling batch generation before load_model raises error"""
    service = EmbeddingService()
    with pytest.raises(ValueError, match="Model not loaded"):
        service.generate_embeddings_batch(["test"])


def test_batch_validation_with_index():
    """Test that batch validation provides specific index for empty text"""
    if embedding_service.model is None:
        embedding_service.load_model()

    # Test with empty text at index 1
    with pytest.raises(ValueError, match="Text at index 1 cannot be empty"):
        embedding_service.generate_embeddings_batch(["valid text", "  ", "also valid"])


def test_compute_similarity_dimension_validation():
    """Test that compute_similarity validates embedding dimensions"""
    if embedding_service.model is None:
        embedding_service.load_model()

    # Create invalid embeddings (wrong dimensions)
    invalid_emb = [0.1] * 100  # Only 100 dims instead of 384
    valid_emb = embedding_service.generate_embedding("test")

    with pytest.raises(ValueError, match="Expected 384-dim embeddings"):
        embedding_service.compute_similarity(invalid_emb, valid_emb)
