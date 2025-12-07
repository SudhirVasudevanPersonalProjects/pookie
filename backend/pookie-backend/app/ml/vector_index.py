import faiss
import numpy as np
from typing import List, Tuple
import pickle
import os
from loguru import logger


class VectorIndex:
    def __init__(self, dimension: int = 384):
        """Initialize FAISS index with IndexFlatIP (exact cosine similarity)"""
        if dimension <= 0:
            raise ValueError(f"Dimension must be positive, got {dimension}")
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        self.something_ids: List[int] = []  # Maps index position to something ID
        logger.debug(f"Initialized VectorIndex with dimension={dimension}")

    def add(self, something_id: int, embedding: np.ndarray):
        """Add single embedding to index

        Args:
            something_id: Unique identifier for this embedding (must be >= 0)
            embedding: Numpy array of shape (dimension,)

        Raises:
            ValueError: If embedding is None, wrong dimension, or has zero norm
        """
        # Validate inputs
        if embedding is None:
            raise ValueError("Embedding cannot be None")
        if not isinstance(embedding, np.ndarray):
            raise ValueError(f"Embedding must be numpy array, got {type(embedding)}")
        if embedding.shape[0] != self.dimension:
            raise ValueError(f"Embedding dimension mismatch: expected {self.dimension}, got {embedding.shape[0]}")
        if something_id < 0:
            raise ValueError(f"something_id must be non-negative, got {something_id}")

        # Check for zero-norm vector (would cause division by zero)
        norm = np.linalg.norm(embedding)
        if norm < 1e-10:  # epsilon threshold
            raise ValueError(f"Embedding has zero or near-zero norm ({norm}), cannot normalize")

        # Normalize for cosine similarity
        embedding_normalized = embedding / norm
        self.index.add(np.array([embedding_normalized], dtype=np.float32))
        self.something_ids.append(something_id)
        logger.debug(f"Added something_id={something_id} to index (total: {self.total_vectors})")

    def add_batch(self, something_ids: List[int], embeddings: np.ndarray):
        """Add multiple embeddings to index (more efficient)

        Args:
            something_ids: List of unique identifiers (all must be >= 0)
            embeddings: Numpy array of shape (n, dimension)

        Raises:
            ValueError: If inputs are invalid or any embedding has zero norm
        """
        # Validate inputs
        if embeddings is None or something_ids is None:
            raise ValueError("Embeddings and IDs cannot be None")
        if not isinstance(embeddings, np.ndarray):
            raise ValueError(f"Embeddings must be numpy array, got {type(embeddings)}")
        if len(embeddings.shape) != 2:
            raise ValueError(f"Embeddings must be 2D array, got shape {embeddings.shape}")
        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Embedding dimension mismatch: expected {self.dimension}, got {embeddings.shape[1]}")
        if len(something_ids) != embeddings.shape[0]:
            raise ValueError(f"ID count ({len(something_ids)}) must match embedding count ({embeddings.shape[0]})")
        if any(sid < 0 for sid in something_ids):
            raise ValueError("All something_ids must be non-negative")

        # Normalize all embeddings
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)

        # Check for zero-norm vectors
        if np.any(norms < 1e-10):
            zero_indices = np.where(norms.flatten() < 1e-10)[0]
            raise ValueError(f"Embeddings at indices {zero_indices.tolist()} have zero or near-zero norm")

        embeddings_normalized = embeddings / norms

        self.index.add(embeddings_normalized.astype(np.float32))
        self.something_ids.extend(something_ids)
        logger.debug(f"Added batch of {len(something_ids)} embeddings to index (total: {self.total_vectors})")

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[int, float]]:
        """
        Search for most similar embeddings

        Args:
            query_embedding: Query vector of shape (dimension,)
            top_k: Number of results to return

        Returns:
            List of (something_id, similarity_score) tuples, sorted by similarity desc

        Raises:
            ValueError: If query is invalid or has zero norm
        """
        # Validate inputs
        if query_embedding is None:
            raise ValueError("Query embedding cannot be None")
        if not isinstance(query_embedding, np.ndarray):
            raise ValueError(f"Query must be numpy array, got {type(query_embedding)}")
        if query_embedding.shape[0] != self.dimension:
            raise ValueError(f"Query dimension mismatch: expected {self.dimension}, got {query_embedding.shape[0]}")
        if top_k <= 0:
            raise ValueError(f"top_k must be positive, got {top_k}")

        # Warn if index is empty
        if self.total_vectors == 0:
            logger.warning("Searching empty index, returning empty results")
            return []

        # Check for zero-norm vector
        norm = np.linalg.norm(query_embedding)
        if norm < 1e-10:
            raise ValueError(f"Query embedding has zero or near-zero norm ({norm}), cannot normalize")

        # Normalize query
        query_normalized = query_embedding / norm
        query_normalized = np.array([query_normalized], dtype=np.float32)

        # Search
        similarities, indices = self.index.search(query_normalized, top_k)

        # Map to something IDs
        results = []
        for idx, sim in zip(indices[0], similarities[0]):
            if idx < len(self.something_ids):
                something_id = self.something_ids[idx]
                results.append((something_id, float(sim)))

        logger.debug(f"Search returned {len(results)} results (top_k={top_k})")
        return results

    def save(self, filepath: str):
        """Save index to disk

        Args:
            filepath: Path to save .faiss file (will also create .ids file)
        """
        faiss.write_index(self.index, filepath)
        # Save something_ids mapping separately
        with open(filepath + ".ids", "wb") as f:
            pickle.dump(self.something_ids, f)
        logger.info(f"Saved index with {self.total_vectors} vectors to {filepath}")

    def load(self, filepath: str) -> bool:
        """Load index from disk

        Args:
            filepath: Path to .faiss file (will also load .ids file)

        Returns:
            True if loaded successfully, False if file doesn't exist
        """
        if os.path.exists(filepath):
            self.index = faiss.read_index(filepath)
            with open(filepath + ".ids", "rb") as f:
                self.something_ids = pickle.load(f)
            logger.info(f"Loaded index with {self.total_vectors} vectors from {filepath}")
            return True
        logger.warning(f"Index file not found at {filepath}")
        return False

    @property
    def total_vectors(self) -> int:
        """Get total number of vectors in index"""
        return self.index.ntotal
