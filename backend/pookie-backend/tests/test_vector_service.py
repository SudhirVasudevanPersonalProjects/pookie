import pytest
import numpy as np
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from app.services.vector_service import VectorService
from app.ml.vector_index import VectorIndex


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset singleton between tests"""
    from app.services import vector_service
    # Re-import the module to reset singleton
    import importlib
    importlib.reload(vector_service)


def test_vector_service_initialization():
    """Test VectorService initializes with correct configuration"""
    service = VectorService()

    assert isinstance(service.index, VectorIndex)
    assert service.index.dimension == 384
    assert service.bucket_name == "vector-indices"
    assert service.index_filename == "somethings_index.faiss"


@pytest.mark.asyncio
async def test_add_something_embedding():
    """Test adding embedding converts list to numpy array"""
    service = VectorService()

    # Generate random embedding as list (not numpy array)
    embedding_list = [0.1] * 384

    # Add to service
    await service.add_something_embedding(1, embedding_list)

    # Verify it was added
    assert service.index.total_vectors == 1
    assert service.index.something_ids == [1]


@pytest.mark.asyncio
async def test_search_similar():
    """Test search_similar converts list to numpy and returns results"""
    service = VectorService()

    # Add 5 embeddings (use non-zero values to avoid zero-norm rejection)
    for i in range(5):
        # Generate distinct non-zero embeddings
        embedding = [float(i + 1) * 0.1] * 384  # Start from 1, not 0
        await service.add_something_embedding(i + 1, embedding)

    # Search with list embedding (not numpy)
    query_list = [0.2] * 384
    results = await service.search_similar(query_list, top_k=3)

    # Verify results
    assert len(results) == 3
    assert all(isinstance(r, tuple) for r in results)
    assert all(len(r) == 2 for r in results)
    assert all(isinstance(r[0], int) and isinstance(r[1], float) for r in results)


@pytest.mark.asyncio
@patch('app.services.vector_service.create_client')
async def test_initialize_with_existing_index(mock_create_client):
    """Test initialize() loads index from Supabase Storage"""
    import tempfile
    import os

    # Create a real index file to return
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a small index
        temp_index = VectorIndex(dimension=384)
        embeddings = np.random.randn(3, 384).astype(np.float32)
        temp_index.add_batch([10, 20, 30], embeddings)

        # Save it
        temp_path = os.path.join(tmpdir, "test.faiss")
        temp_index.save(temp_path)

        # Read the files
        with open(temp_path, "rb") as f:
            faiss_bytes = f.read()
        with open(temp_path + ".ids", "rb") as f:
            ids_bytes = f.read()

    # Setup mocks
    mock_bucket = MagicMock()
    mock_bucket.download.side_effect = [faiss_bytes, ids_bytes]
    mock_storage = MagicMock()
    mock_storage.from_.return_value = mock_bucket
    mock_client = MagicMock()
    mock_client.storage = mock_storage
    mock_create_client.return_value = mock_client

    # Create service (will use mocked client)
    service = VectorService()

    # Initialize
    await service.initialize()

    # Verify index loaded
    assert service.index.total_vectors == 3
    assert service.index.something_ids == [10, 20, 30]


@pytest.mark.asyncio
@patch('app.services.vector_service.create_client')
async def test_initialize_no_existing_index(mock_create_client):
    """Test initialize() handles missing index gracefully"""
    # Mock Supabase to raise exception (no index found)
    mock_bucket = MagicMock()
    mock_bucket.download.side_effect = Exception("File not found")
    mock_storage = MagicMock()
    mock_storage.from_.return_value = mock_bucket
    mock_client = MagicMock()
    mock_client.storage = mock_storage
    mock_create_client.return_value = mock_client

    # Create service
    service = VectorService()

    # Should not raise exception, just log
    await service.initialize()

    # Index should be empty
    assert service.index.total_vectors == 0


@pytest.mark.asyncio
@patch('app.services.vector_service.create_client')
async def test_save_to_storage(mock_create_client):
    """Test save_to_storage() uploads to Supabase"""
    # Mock Supabase client
    mock_bucket = MagicMock()
    mock_bucket.upload = MagicMock(return_value={"Key": "test"})
    mock_storage = MagicMock()
    mock_storage.from_.return_value = mock_bucket
    mock_client = MagicMock()
    mock_client.storage = mock_storage
    mock_create_client.return_value = mock_client

    # Create service
    service = VectorService()

    # Add some embeddings
    embeddings = np.random.randn(5, 384).astype(np.float32)
    service.index.add_batch([1, 2, 3, 4, 5], embeddings)

    # Save
    await service.save_to_storage()

    # Verify upload was called twice (.faiss and .ids)
    assert mock_bucket.upload.call_count == 2

    # Check upload arguments
    calls = mock_bucket.upload.call_args_list
    assert calls[0][0][0] == "somethings_index.faiss"
    assert calls[1][0][0] == "somethings_index.faiss.ids"
    assert calls[0][0][2] == {"upsert": "true"}
    assert calls[1][0][2] == {"upsert": "true"}
