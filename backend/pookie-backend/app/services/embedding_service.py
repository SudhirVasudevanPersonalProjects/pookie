from sentence_transformers import SentenceTransformer
from typing import List, Optional
import numpy as np
from loguru import logger


class EmbeddingService:
    """
    Centralized embedding generation service using sentence-transformers.

    Model: all-MiniLM-L6-v2
    - 384-dimensional dense vectors
    - 80MB model size (runs locally, no API cost)
    - Trained on semantic similarity tasks
    - Generation time: <500ms for typical input (50-200 words)

    Architecture Decision: Backend-only embedding generation (centralized, single source of truth)
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding model.

        Model loads once on service instantiation (typically at FastAPI startup).
        Cached in memory for fast subsequent generations.
        """
        self.model_name = model_name
        self.model: Optional[SentenceTransformer] = None
        logger.info(f"Initializing EmbeddingService with model: {model_name}")

    def load_model(self):
        """
        Load sentence-transformers model into memory.

        Called during FastAPI startup (app/core/events.py startup handler).
        Downloads model on first run (~80MB), then caches locally.

        Raises:
            RuntimeError: If model loading fails (network issues, corrupted files, etc.)
        """
        if self.model is None:
            try:
                logger.info(f"Loading sentence-transformers model: {self.model_name}")
                self.model = SentenceTransformer(self.model_name)
                logger.info(f"Model {self.model_name} loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load model {self.model_name}: {e}")
                raise RuntimeError(f"Embedding model initialization failed: {e}") from e
        else:
            logger.info(f"Model {self.model_name} already loaded")

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate 384-dim embedding vector from text.

        Args:
            text: Input text (something content, query, etc.)

        Returns:
            List of 384 floats representing semantic embedding

        Raises:
            ValueError: If model not loaded or text is empty

        Performance: <500ms for typical text (50-200 words)
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")

        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # Generate embedding
        embedding = self.model.encode(text, convert_to_numpy=True)

        # Validate dimension (should always be 384 for all-MiniLM-L6-v2)
        if len(embedding) != 384:
            raise ValueError(f"Expected 384-dim embedding, got {len(embedding)}")

        # Convert numpy array to Python list for JSON serialization
        return embedding.tolist()

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch (more efficient).

        Args:
            texts: List of input texts

        Returns:
            List of 384-dim embeddings (one per input text)

        Performance: Batch processing is ~2-3x faster than individual calls
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")

        if not texts:
            raise ValueError("Texts list cannot be empty")

        # Validate each text and provide specific index for errors
        for i, text in enumerate(texts):
            if not text or not text.strip():
                raise ValueError(f"Text at index {i} cannot be empty")

        # Batch encode (more efficient than individual encodes)
        embeddings = self.model.encode(texts, convert_to_numpy=True, batch_size=32)

        # Validate dimensions for all embeddings
        for i, emb in enumerate(embeddings):
            if len(emb) != 384:
                raise ValueError(f"Expected 384-dim embedding at index {i}, got {len(emb)}")

        # Convert to list of lists
        return [emb.tolist() for emb in embeddings]

    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings.

        Args:
            embedding1: First 384-dim embedding
            embedding2: Second 384-dim embedding

        Returns:
            Cosine similarity score (0.0 to 1.0)
            - 1.0 = identical semantic meaning
            - 0.8-0.95 = very similar concepts
            - 0.7-0.8 = related concepts
            - <0.7 = different concepts

        Raises:
            ValueError: If embeddings don't have exactly 384 dimensions

        Used for: RAG confidence thresholds, duplicate detection
        """
        # Validate dimensions
        if len(embedding1) != 384 or len(embedding2) != 384:
            raise ValueError(f"Expected 384-dim embeddings, got {len(embedding1)} and {len(embedding2)}")

        arr1 = np.array(embedding1)
        arr2 = np.array(embedding2)

        # Cosine similarity: dot product / (norm1 * norm2)
        similarity = np.dot(arr1, arr2) / (np.linalg.norm(arr1) * np.linalg.norm(arr2))

        return float(similarity)


# Global singleton instance
# NOTE: This singleton pattern is simple but has limitations:
# - Cannot easily swap models at runtime
# - Testing with different models requires module reload
# - For multi-model scenarios, consider dependency injection pattern
embedding_service = EmbeddingService()
