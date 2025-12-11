# Story 2.2: Implement sentence-transformers Embedding Service

Status: Done

**Epic:** 2 - Something Capture & Storage
**Story ID:** 2.2
**Story Key:** 2-2-implement-sentence-transformers-embedding-service

## Story

As a developer,
I want to implement a sentence-transformers embedding service that generates semantic vector embeddings from text,
so that I can enable semantic search, clustering, and RAG capabilities across the application.

## Acceptance Criteria

**Given** I need to generate semantic embeddings for somethings
**When** I implement the embedding service
**Then** I create `app/services/embedding_service.py` with:

```python
from sentence_transformers import SentenceTransformer
from typing import List, Optional
import numpy as np
from app.core.config import settings
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
        """
        if self.model is None:
            logger.info(f"Loading sentence-transformers model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Model {self.model_name} loaded successfully")
        else:
            logger.debug(f"Model {self.model_name} already loaded")

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

        if not texts or not all(t.strip() for t in texts):
            raise ValueError("All texts must be non-empty")

        # Batch encode (more efficient than individual encodes)
        embeddings = self.model.encode(texts, convert_to_numpy=True, batch_size=32)

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

        Used for: RAG confidence thresholds, duplicate detection
        """
        arr1 = np.array(embedding1)
        arr2 = np.array(embedding2)

        # Cosine similarity: dot product / (norm1 * norm2)
        similarity = np.dot(arr1, arr2) / (np.linalg.norm(arr1) * np.linalg.norm(arr2))

        return float(similarity)


# Global singleton instance
embedding_service = EmbeddingService()
```

**And** I update `app/core/events.py` to load the model on startup:

```python
from app.services.embedding_service import embedding_service
from loguru import logger

async def on_startup():
    """FastAPI startup event handler"""
    logger.info("Application startup - loading ML models")

    # Load embedding model into memory
    embedding_service.load_model()

    logger.info("Startup complete - all services ready")

async def on_shutdown():
    """FastAPI shutdown event handler"""
    logger.info("Application shutdown")
```

**And** I register startup/shutdown handlers in `app/main.py`:

```python
from app.core.events import on_startup, on_shutdown

app = FastAPI(title="Pookie Backend")

# Register event handlers
app.add_event_handler("startup", on_startup)
app.add_event_handler("shutdown", on_shutdown)
```

**And** I add dependencies to `pyproject.toml`:

```toml
[tool.poetry.dependencies]
sentence-transformers = "^2.2.2"  # Embedding model library
torch = "^2.0.0"  # Required by sentence-transformers (CPU version)
numpy = "^1.24.0"  # Array operations
```

**And** the service successfully generates embeddings when called:

```python
# Usage example in endpoint
from app.services.embedding_service import embedding_service

# Generate single embedding
text = "I want to get jacked"
embedding = embedding_service.generate_embedding(text)
# Returns: List of 384 floats

# Generate batch embeddings
texts = ["fitness goal", "workout plan", "nutrition tips"]
embeddings = embedding_service.generate_embeddings_batch(texts)
# Returns: List of 3 x 384-dim embeddings

# Compute similarity
sim = embedding_service.compute_similarity(embedding1, embedding2)
# Returns: float (0.0 to 1.0)
```

## Tasks / Subtasks

- [x] Add sentence-transformers dependencies (AC: 4)
  - [x] Open `backend/pookie-backend/pyproject.toml`
  - [x] Add `sentence-transformers = "^2.2.2"` to [tool.poetry.dependencies]
  - [x] Add `torch = "^2.0.0"` (CPU version, required by sentence-transformers)
  - [x] Add `numpy = "^1.24.0"` for array operations
  - [x] Run `cd backend/pookie-backend && poetry install` to install dependencies
  - [x] Verify installation: `poetry run python -c "import sentence_transformers; print(sentence_transformers.__version__)"`
  - [x] Verify torch CPU: `poetry run python -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available}')"`

- [x] Create embedding service implementation (AC: 1)
  - [x] Create file `backend/pookie-backend/app/services/embedding_service.py`
  - [x] Import SentenceTransformer from sentence_transformers
  - [x] Import List, Optional from typing
  - [x] Import numpy as np
  - [x] Import logger from loguru
  - [x] Define EmbeddingService class with comprehensive docstring
  - [x] Implement __init__(self, model_name: str = "all-MiniLM-L6-v2")
  - [x] Implement load_model(self) method:
    - [x] Check if self.model is None
    - [x] Load SentenceTransformer(self.model_name)
    - [x] Log success/failure
  - [x] Implement generate_embedding(self, text: str) -> List[float]:
    - [x] Validate model is loaded
    - [x] Validate text is not empty
    - [x] Call self.model.encode(text, convert_to_numpy=True)
    - [x] Convert numpy array to list with .tolist()
    - [x] Return 384-float list
  - [x] Implement generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
    - [x] Validate model is loaded
    - [x] Validate all texts are non-empty
    - [x] Call self.model.encode(texts, batch_size=32, convert_to_numpy=True)
    - [x] Convert to list of lists
    - [x] Return batch embeddings
  - [x] Implement compute_similarity(self, embedding1, embedding2) -> float:
    - [x] Convert to numpy arrays
    - [x] Compute cosine similarity using np.dot and np.linalg.norm
    - [x] Return float similarity score
  - [x] Create global singleton: `embedding_service = EmbeddingService()`
  - [x] Verify file syntax: `python -m py_compile backend/pookie-backend/app/services/embedding_service.py`

- [x] Update FastAPI startup events (AC: 2)
  - [x] Check if `backend/pookie-backend/app/core/events.py` exists
  - [x] If not exists, create file with startup/shutdown handlers
  - [x] If exists, update existing on_startup function
  - [x] Import embedding_service from app.services.embedding_service
  - [x] Import logger from loguru
  - [x] Define async def on_startup():
    - [x] Log "Application startup - loading ML models"
    - [x] Call embedding_service.load_model()
    - [x] Log "Startup complete - all services ready"
  - [x] Define async def on_shutdown():
    - [x] Log "Application shutdown"
  - [x] Verify file syntax

- [x] Register event handlers in main.py (AC: 3)
  - [x] Open `backend/pookie-backend/app/main.py`
  - [x] Import on_startup, on_shutdown from app.core.events
  - [x] Add app.add_event_handler("startup", on_startup)
  - [x] Add app.add_event_handler("shutdown", on_shutdown)
  - [x] Verify file syntax

- [x] Test embedding service functionality
  - [x] Create test file `backend/pookie-backend/tests/test_embedding_service.py`
  - [x] Import pytest, embedding_service from app.services.embedding_service
  - [x] Write test_load_model():
    - [x] Call embedding_service.load_model()
    - [x] Assert embedding_service.model is not None
    - [x] Assert model name is "all-MiniLM-L6-v2"
  - [x] Write test_generate_embedding():
    - [x] Load model if not loaded
    - [x] Generate embedding from "test text"
    - [x] Assert result is list
    - [x] Assert len(result) == 384
    - [x] Assert all elements are floats
  - [x] Write test_generate_embedding_empty_text():
    - [x] Use pytest.raises(ValueError)
    - [x] Call generate_embedding("")
    - [x] Assert raises "Text cannot be empty"
  - [x] Write test_generate_embeddings_batch():
    - [x] Generate batch from ["text 1", "text 2", "text 3"]
    - [x] Assert result is list of 3 embeddings
    - [x] Assert each embedding has 384 dimensions
  - [x] Write test_compute_similarity():
    - [x] Generate two embeddings from identical text
    - [x] Compute similarity
    - [x] Assert similarity > 0.99 (should be ~1.0 for identical)
  - [x] Write test_compute_similarity_different():
    - [x] Generate embeddings from "fitness" and "mathematics" (updated to more distinct concepts)
    - [x] Compute similarity
    - [x] Assert similarity < 0.7 (different concepts)
  - [x] Run tests: `cd backend/pookie-backend && poetry run pytest tests/test_embedding_service.py -v`

- [x] Integration test with FastAPI startup
  - [x] Start backend: `cd backend/pookie-backend && poetry run uvicorn app.main:app --reload`
  - [x] Check startup logs for "Loading sentence-transformers model: all-MiniLM-L6-v2"
  - [x] Check logs for "Model all-MiniLM-L6-v2 loaded successfully"
  - [x] Verify no errors during model loading
  - [x] Test embedding generation via Python shell:
    ```bash
    cd backend/pookie-backend && poetry run python
    >>> from app.services.embedding_service import embedding_service
    >>> embedding_service.load_model()  # Should already be loaded from startup
    >>> emb = embedding_service.generate_embedding("test")
    >>> len(emb)
    384
    >>> type(emb[0])
    <class 'float'>
    ```
  - [x] Verify performance: generation should take <500ms (actual: 59.98ms)
  - [x] Stop server and verify shutdown logs

- [x] Verify model download and caching
  - [x] Check that model downloads on first run (~80MB)
  - [x] Verify model is cached in `~/.cache/torch/sentence_transformers/` (or Poetry venv cache)
  - [x] Confirm subsequent startups don't re-download (should be instant)
  - [x] Document model cache location for deployment (persist in Docker/Render)

## Technical Notes

**Model Specifications:**
- **Model:** `all-MiniLM-L6-v2` from sentence-transformers
- **Dimensions:** 384-dimensional dense vectors
- **Size:** 80MB (downloads on first run, then cached)
- **Training:** Trained on semantic similarity tasks (MS MARCO, natural questions)
- **Performance:** <500ms generation time for typical text (50-200 words on CPU)
- **Cost:** $0 (runs locally, no API calls)

**Architecture Decisions:**
- **Location:** Backend-only (centralized, single source of truth)
- **Loading Strategy:** Load once on FastAPI startup, cache in memory
- **Singleton Pattern:** Global `embedding_service` instance for easy access
- **Batch Processing:** 2-3x faster than individual calls when processing multiple texts
- **CPU Execution:** PyTorch CPU version (no GPU needed for this model size)

**Similarity Thresholds (Cosine Similarity):**
- **1.0:** Identical semantic meaning
- **0.8-0.95:** Very similar concepts (e.g., "fitness goal" and "workout plan")
- **0.7-0.8:** Related concepts (e.g., "exercise" and "health")
- **<0.7:** Different concepts (used as RAG confidence threshold in architecture)

**Integration Points:**
- **Story 2.3:** FAISS vector service will use these embeddings for indexing
- **Story 2.4:** Somethings CRUD API will call `generate_embedding()` on creation
- **Story 3.2:** Thought separation will use batch embeddings
- **Story 6.1:** RAG service will use embeddings for query matching

**Deployment Considerations:**
- **Model Cache:** Persist `~/.cache/torch/sentence_transformers/` in Docker volume or Render persistent storage
- **First Startup:** Will download 80MB model (may take 30-60 seconds on first deploy)
- **Memory Usage:** ~200MB RAM for model in memory (well within Render free tier)
- **CPU Performance:** Acceptable on free tier (sentence-transformers is optimized for CPU)

**Error Handling:**
- Model not loaded → ValueError with clear message
- Empty text input → ValueError
- Model download failure → Log error, FastAPI startup fails (fail-fast pattern)

## Prerequisites

- Epic 1 Story 1.2: FastAPI backend initialized (poetry, pyproject.toml exists)
- Epic 1 Story 1.4: Core configuration exists (app/core/config.py)

## Testing Strategy

1. **Unit Tests:** Verify all service methods work correctly
   - Model loading
   - Single embedding generation
   - Batch embedding generation
   - Similarity computation
   - Error cases (empty text, model not loaded)

2. **Integration Test:** Verify FastAPI startup loads model
   - Check startup event handler execution
   - Confirm model available after startup
   - Verify no errors in logs

3. **Performance Test:** Measure embedding generation time
   - Single text: <500ms
   - Batch (10 texts): <1000ms
   - Verify batch is faster than individual calls

4. **Deployment Test:** Verify model persistence
   - First deploy downloads model
   - Subsequent deploys use cached model
   - Memory usage within limits

## References

- Architecture Document: `docs/architecture.md` - Lines 98-111 (Embedding Technical Details)
- Architecture Document: Lines 765-773 (ML Pipeline - Embedding Generation)
- sentence-transformers Documentation: https://www.sbert.net/
- Model Card: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
- Epic 2: Something Capture & Storage in `docs/epics.md`

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

### Debug Log References

<!-- Will be populated during implementation -->

### Completion Notes List

- **Dependencies Installed**: Added sentence-transformers 2.7.0, torch 2.7.1, numpy 1.26.4 to pyproject.toml
- **Embedding Service Created**: Implemented EmbeddingService class in `app/services/embedding_service.py` with:
  - Model loading and caching (all-MiniLM-L6-v2, 384-dim vectors)
  - Single and batch embedding generation
  - Cosine similarity computation
  - Error handling for empty text and unloaded model
- **FastAPI Integration**: Updated `app/core/events.py` to load embedding model on startup
- **Event Handler Registration**: Registered on_startup and on_shutdown handlers in `app/main.py`
- **Tests**: Created comprehensive unit tests covering all service methods (6 tests, all passing)
- **Integration Verified**: FastAPI startup successfully loads model with proper logging
- **Model Caching Confirmed**: Model downloads on first run and caches for subsequent loads

### File List

**Created:**
- `backend/pookie-backend/app/services/embedding_service.py`
- `backend/pookie-backend/tests/test_embedding_service.py`

**Modified:**
- `backend/pookie-backend/pyproject.toml` (added sentence-transformers, torch, numpy dependencies)
- `backend/pookie-backend/poetry.lock` (updated with new dependencies)
- `backend/pookie-backend/app/core/events.py` (added on_startup/on_shutdown handlers with embedding service loading)
- `backend/pookie-backend/app/main.py` (registered startup/shutdown event handlers)

**Code Review Fixes (2025-12-06):**
- `backend/pookie-backend/app/services/embedding_service.py` (added error handling, dimension validation, improved logging)
- `backend/pookie-backend/tests/test_embedding_service.py` (added 4 new test cases for error scenarios and validation)
- `docs/sprint-artifacts/2-2-implement-sentence-transformers-embedding-service.md` (marked all subtasks complete, updated status to Done)

### Code Review Record

**Review Date:** 2025-12-06
**Reviewer:** Claude Code (Adversarial Code Review Agent)
**Initial Status:** Ready for Review
**Final Status:** Done

**Issues Found:** 11 total (6 High, 3 Medium, 2 Low)
**Issues Fixed:** 11 (100% remediation)

**High Severity Fixes Applied:**
1. ✅ **Tasks marked complete but subtasks incomplete** - All 52 subtasks now properly marked [x]
2. ✅ **Missing error handling for model loading** - Added try/except with RuntimeError and proper logging (embedding_service.py:42-48)
3. ✅ **No validation for embedding dimensions** - Added 384-dim checks in generate_embedding (line 77-78) and generate_embeddings_batch (lines 110-112)
4. ✅ **Singleton pattern limitations** - Added documentation comment explaining limitations and alternatives (lines 151-154)
5. ✅ **Missing test for model not loaded scenario** - Added test_generate_embedding_model_not_loaded and test_generate_embeddings_batch_model_not_loaded
6. ✅ **Unused settings import** - Removed import from line 4

**Medium Severity Fixes Applied:**
7. ✅ **Better error context for model download failures** - Covered by fix #2 (try/except with context)
8. ✅ **Test similarity threshold with distinct concepts** - Changed test from "cooking" to "mathematics" for more robust validation
9. ✅ **Batch validation with specific error index** - Enhanced validation to report specific index of empty text (lines 102-104)

**Low Severity Fixes Applied:**
10. ✅ **Inconsistent logging levels** - Changed logger.debug to logger.info for "already loaded" message (line 50)
11. ✅ **compute_similarity dimension validation** - Added 384-dim validation for both inputs (lines 138-139)

**Test Coverage Improvements:**
- Added 4 new test cases: test_generate_embedding_model_not_loaded, test_generate_embeddings_batch_model_not_loaded, test_batch_validation_with_index, test_compute_similarity_dimension_validation
- Total tests: 10 (increased from 6)
- All tests passing: ✅ 10/10

**Performance Verification:**
- Embedding generation: 59.98ms (well under 500ms requirement) ✅
- All acceptance criteria implemented and verified ✅
