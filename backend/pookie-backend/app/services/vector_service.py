from app.ml.vector_index import VectorIndex
from app.core.config import settings
from supabase import create_client
import numpy as np
from typing import List, Tuple
import tempfile
import os
import asyncio
from loguru import logger


class VectorService:
    def __init__(self):
        self.index = VectorIndex(dimension=384)
        self.supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
        self.bucket_name = "vector-indices"
        self.index_filename = "somethings_index.faiss"
        self._lock = asyncio.Lock()  # Thread safety for concurrent operations

    async def initialize(self):
        """Load index from Supabase Storage on startup"""
        try:
            # Download from Supabase Storage
            with tempfile.TemporaryDirectory() as tmpdir:
                index_path = os.path.join(tmpdir, self.index_filename)

                # Download .faiss file
                response = self.supabase.storage.from_(self.bucket_name).download(self.index_filename)
                with open(index_path, "wb") as f:
                    f.write(response)

                # Download .ids file
                response_ids = self.supabase.storage.from_(self.bucket_name).download(self.index_filename + ".ids")
                with open(index_path + ".ids", "wb") as f:
                    f.write(response_ids)

                # Load into memory
                self.index.load(index_path)
                logger.info(f"Loaded FAISS index with {self.index.total_vectors} vectors")
        except Exception as e:
            logger.info(f"No existing index found, starting fresh: {e}")

    async def save_to_storage(self):
        """Save index to Supabase Storage"""
        with tempfile.TemporaryDirectory() as tmpdir:
            index_path = os.path.join(tmpdir, self.index_filename)

            # Save to temp file
            self.index.save(index_path)

            # Upload .faiss file
            with open(index_path, "rb") as f:
                self.supabase.storage.from_(self.bucket_name).upload(
                    self.index_filename,
                    f,
                    {"upsert": "true"}
                )

            # Upload .ids file
            with open(index_path + ".ids", "rb") as f:
                self.supabase.storage.from_(self.bucket_name).upload(
                    self.index_filename + ".ids",
                    f,
                    {"upsert": "true"}
                )
            logger.info(f"Saved FAISS index to Supabase Storage ({self.index.total_vectors} vectors)")

    async def add_something_embedding(self, something_id: int, embedding: List[float]):
        """Add a something embedding to the index (thread-safe)

        Args:
            something_id: Unique identifier for the embedding
            embedding: List of floats representing the embedding vector

        Raises:
            ValueError: If embedding is invalid (propagated from VectorIndex)
        """
        async with self._lock:
            embedding_array = np.array(embedding, dtype=np.float32)
            self.index.add(something_id, embedding_array)

    async def search_similar(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[int, float]]:
        """Search for similar somethings (thread-safe)

        Args:
            query_embedding: Query vector as list of floats
            top_k: Number of results to return

        Returns:
            List of (something_id, similarity_score) tuples

        Raises:
            ValueError: If query is invalid (propagated from VectorIndex)
        """
        async with self._lock:
            query_array = np.array(query_embedding, dtype=np.float32)
            return self.index.search(query_array, top_k)


# Singleton instance
vector_service = VectorService()
