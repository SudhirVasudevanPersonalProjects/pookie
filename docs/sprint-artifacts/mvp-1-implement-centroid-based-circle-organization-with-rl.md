# Story MVP-1: Implement Centroid-Based Circle Organization with RL

Status: review

## Story

As a personal knowledge system user,
I want my thoughts automatically organized into "Circles of Care" with intelligent centroid tracking,
so that the system learns my personal semantic categories and improves its predictions of where new items belong through reinforcement learning feedback.

## Acceptance Criteria

1. **Given** circles need to track personalized semantic meaning
   **When** the database is migrated
   **Then** the `circles` table has a new column:
   - `centroid_embedding` (type: ARRAY(Float), nullable: True)
   - Size: 384 floats (matches sentence-transformers embedding dimensions)
   - Purpose: Stores the mean vector of all somethings assigned to that circle
   - Initial value: NULL (populated on first something assignment)

2. **Given** circles need to learn from user feedback
   **When** CentroidService is implemented
   **Then** it provides these core methods:
   - `initialize_centroid(circle_id, first_embedding, db)` - Sets initial centroid
   - `update_centroid_add(circle_id, new_embedding, db)` - Incremental update: `(N * old + new) / (N + 1)`
   - `update_centroid_remove(circle_id, removed_embedding, db)` - Reverse update
   - `compute_circle_similarities(query_embedding, user_id, db, top_k=5)` - Find matching circles
   - `predict_circles_for_something(something_id, user_id, db, threshold=0.7, top_k=3)` - Auto-suggest circles

3. **Given** users need to assign somethings to circles with centroid updates
   **When** API endpoints are called
   **Then** three new endpoints exist:
   - `POST /api/v1/circles/{circle_id}/somethings/{something_id}` - Assign (sets is_user_assigned=True)
   - `DELETE /api/v1/circles/{circle_id}/somethings/{something_id}` - Remove (updates centroid)
   - `GET /api/v1/circles/{circle_id}/predict-similar?top_k=10` - Get suggestions

4. **Given** users need circle suggestions when creating somethings
   **When** POST `/api/v1/somethings` is called
   **Then** response includes `suggestedCircles` field:
   ```json
   {
     "id": 123,
     "content": "I want to get fit",
     "suggestedCircles": [
       {"circleId": 5, "circleName": "Fitness", "confidence": 0.89}
     ]
   }
   ```
   - Uses `predict_circles_for_something()` with threshold=0.7, top_k=3
   - Empty array if no strong matches

5. **Given** the system needs to learn from user feedback
   **When** assignments are made
   **Then** learning signals are tracked:
   - `SomethingCircle.is_user_assigned` = TRUE for manual assignments
   - `SomethingCircle.confidence_score` = 0-1 for auto-assignments
   - Used for RL weighting in future predictions

6. **Given** centroid calculations must be mathematically correct
   **When** tests validate centroid operations
   **Then** formulas are verified:
   - Add: `(N * old + new) / (N + 1)` produces correct mean
   - Remove: `((N + 1) * old - removed) / N` reverses correctly
   - Normalization: Unit vector has magnitude 1.0
   - Edge cases: First item, remove last item, empty circle

## Tasks / Subtasks

- [x] Create Alembic migration for centroid_embedding column (AC: 1)
  - [x] Generate migration: `alembic revision -m "add_centroid_embedding_to_circles"`
  - [x] Add column: `ARRAY(Float)` nullable
  - [x] Run migration: `alembic upgrade head`
  - [x] Verify in database

- [x] Update Circle model (AC: 1)
  - [x] Add `centroid_embedding = Column(ARRAY(Float), nullable=True)` to Circle class
  - [x] Verify relationships still work

- [x] Implement CentroidService (AC: 2)
  - [x] Create `app/services/centroid_service.py`
  - [x] Implement `initialize_centroid()` method
  - [x] Implement `update_centroid_add()` with incremental formula
  - [x] Implement `update_centroid_remove()` with reverse formula
  - [x] Implement `compute_circle_similarities()` with cosine similarity
  - [x] Implement `predict_circles_for_embedding()` with threshold filtering
  - [x] Implement `predict_circles_for_something()` wrapper method
  - [x] Add normalization to unit vectors
  - [x] Create singleton instance

- [x] Add circle assignment API endpoints (AC: 3)
  - [x] Create `app/api/routes/circles.py`
  - [x] Implement POST assign endpoint with centroid update
  - [x] Implement DELETE remove endpoint with centroid update
  - [x] Implement GET predict-similar endpoint
  - [x] Add JWT authentication to all endpoints
  - [x] Add user_id filtering for data isolation
  - [x] Register circles router in api.py

- [x] Enhance somethings creation response (AC: 4)
  - [x] Update POST `/api/v1/somethings` endpoint
  - [x] Call `predict_circles_for_something()` after creation
  - [x] Add `suggestedCircles` to response schema
  - [x] Add `CirclePrediction` schema
  - [x] Handle graceful degradation if prediction fails

- [x] Write comprehensive tests (AC: 6)
  - [x] Create `tests/test_centroid_service.py` with 8 unit tests
  - [x] Test initialize, add, remove, similarities, predict
  - [x] Test edge cases (empty, first, last)
  - [x] All 8 tests passing
  - [ ] Create `tests/test_circles_api_centroid.py` with integration tests
  - [ ] Test assign/remove with centroid updates
  - [ ] Test full RL learning loop
  - [ ] Test user isolation and auth

- [ ] iOS updates (AC: 4) - DEFERRED TO SEPARATE TASK
  - [ ] Add `CirclePrediction` model struct
  - [ ] Update `SomethingResponse` to include `suggestedCircles`
  - [ ] Add APIService methods: `assignToCircle()`, `removeFromCircle()`
  - [ ] Update CaptureView to show circle suggestions after creation
  - [ ] Add assign/remove UI in CircleDetailView
  - [ ] Add iOS unit tests

## Dev Notes

### Architecture Patterns and Constraints

**Centroid RL Architecture:**
This story implements the core of Pookie's personalized semantic architecture (see `docs/pookie-semantic-architecture.md`). The key innovation is layering custom semantics (centroids) on top of base embeddings:

- **Layer 1:** Base embeddings (sentence-transformers) = universal language understanding
- **Layer 2:** Circle centroids = personalized semantic categories that learn from feedback
- **Layer 3:** Hybrid retrieval = 40% base + 40% centroid + 15% user feedback + 5% temporal

**Why Centroids Over Fine-tuning:**
- Fine-tuning requires GPU, training runs, batching (~hours per iteration)
- Centroids update incrementally in real-time (<50ms per update)
- Interpretable: See exactly how circles shift with feedback
- Free tier compatible: No GPU needed, no API costs
- No catastrophic forgetting

**Database Schema:**
```sql
-- Migration adds this column to existing circles table
ALTER TABLE circles ADD COLUMN centroid_embedding FLOAT[384];
```

**Service Pattern:**
```python
# Singleton service at module level
class CentroidService:
    async def update_centroid_add(self, circle_id, new_embedding, db):
        circle = db.query(Circle).filter(Circle.id == circle_id).first()
        n_items = db.query(SomethingCircle).filter(
            SomethingCircle.circle_id == circle_id
        ).count()

        if circle.centroid_embedding is None:
            circle.centroid_embedding = new_embedding
        else:
            old = np.array(circle.centroid_embedding)
            new = np.array(new_embedding)
            updated = ((n_items - 1) * old + new) / n_items
            # Normalize to unit vector
            circle.centroid_embedding = (updated / np.linalg.norm(updated)).tolist()

        db.commit()

centroid_service = CentroidService()
```

**API Endpoints:**
- `POST /api/v1/circles/{circle_id}/somethings/{something_id}` - Returns 204
- `DELETE /api/v1/circles/{circle_id}/somethings/{something_id}` - Returns 204
- `GET /api/v1/circles/{circle_id}/predict-similar?top_k=10` - Returns JSON

**Learning Signals:**
Junction table `something_circles` tracks:
- `is_user_assigned` (Boolean) - TRUE = user manually assigned (high signal)
- `confidence_score` (Float 0-1) - LLM confidence in auto-assignment

### Source Tree Components to Touch

**Files to Create:**
```
backend/pookie-backend/
├── alembic/versions/[timestamp]_add_centroid_embedding_to_circles.py
├── app/services/centroid_service.py
├── tests/test_centroid_service.py
└── tests/test_circles_api_centroid.py

ios/Pookie/Pookie/
├── Models/CirclePrediction.swift (new)
└── PookieTests/CentroidPredictionTests.swift (new)
```

**Files to Modify:**
```
backend/pookie-backend/
├── app/models/circle.py (add centroid_embedding column)
├── app/api/routes/circles.py (add centroid endpoints)
├── app/api/routes/somethings.py (enhance response with suggestions)
└── app/schemas/something.py (add suggestedCircles field)

ios/Pookie/Pookie/
├── Services/APIService.swift (add assign/remove methods)
├── ViewModels/CircleViewModel.swift (add prediction handling)
└── Views/Capture/CaptureView.swift (show suggestions)
```

**Files to Reference:**
```
docs/pookie-semantic-architecture.md - Complete centroid architecture
docs/centroid-architecture-impact-analysis.md - Impact analysis
backend/pookie-backend/app/services/embedding_service.py - Embedding generation
backend/pookie-backend/app/services/vector_service.py - FAISS integration
backend/pookie-backend/app/models/something_circle.py - Junction table
```

### Testing Standards Summary

**Unit Tests (CentroidService):**
1. `test_initialize_centroid_first_item()` - Verify first item sets centroid
2. `test_update_centroid_add_formula()` - Math: `(N*old + new)/(N+1)`
3. `test_update_centroid_add_normalization()` - Unit vector magnitude = 1.0
4. `test_update_centroid_remove_formula()` - Reverse operation correct
5. `test_update_centroid_remove_last_item()` - Centroid becomes NULL
6. `test_compute_circle_similarities()` - Cosine similarity sorted
7. `test_predict_circles_for_something()` - Top-k with threshold
8. `test_predict_circles_no_centroids()` - Empty list when no centroids

**Integration Tests (API):**
1. `test_assign_something_to_circle()` - POST creates record, updates centroid
2. `test_assign_idempotent()` - Second assign returns 400 or 204
3. `test_remove_something_from_circle()` - DELETE removes, updates centroid
4. `test_get_predict_similar()` - Returns items similar to centroid
5. `test_full_rl_loop()` - User correction → centroid shift → next prediction improves
6. `test_unauthorized_access()` - 401 without JWT
7. `test_user_isolation()` - Can't access other users' data

**Test Coverage Target:** 80%+ on centroid service and API endpoints

### Project Structure Notes

**Alignment with Established Patterns:**
- Service layer: Singleton pattern (from `embedding_service`, `vector_service`)
- API endpoints: RESTful CRUD with JWT auth (from `somethings.py`)
- Database: SQLAlchemy ORM with user_id filtering (from all models)
- Testing: pytest with TestClient (from `test_somethings_api.py`)
- Naming: snake_case DB, camelCase API JSON (from architecture)

**Performance Targets:**
- Centroid calculation: <50ms per circle
- Circle prediction: <100ms (3-5 centroid comparisons)
- Assignment with update: <50ms
- Full RAG chat (includes centroid re-ranking): <2 seconds

### References

**Architecture Documents:**
- [Source: docs/pookie-semantic-architecture.md] - Complete centroid RL architecture
- [Source: docs/centroid-architecture-impact-analysis.md] - Impact on existing epics
- [Source: docs/architecture.md] - Overall system architecture
- [Source: docs/sprint-change-proposal-2025-12-07.md] - MVP scope reduction rationale

**Story Dependencies:**
- Story 2.2 (Embedding Service) ✅ - Provides 384-dim embeddings
- Story 2.3 (FAISS Vector Index) ✅ - Vector storage and search
- Story 2.4 (Somethings CRUD API) ✅ - Base API to enhance
- Epic 1 (Foundation) ✅ - Auth, database, models

**Code Patterns from Previous Stories:**
- Singleton service pattern: `embedding_service = EmbeddingService()` (Story 2.2)
- API response enhancement: Add optional field, backward compatible (Story 2.4)
- Junction table operations: Create/delete with cascade (Story 2.4)
- Error handling: Graceful degradation, log but don't fail (Story 2.2)

**Technical Specifications:**
- Vector dimensions: 384 (sentence-transformers all-MiniLM-L6-v2)
- Similarity metric: Cosine similarity (dot product after normalization)
- Storage: PostgreSQL ARRAY(Float) column (~1.5 KB per circle)
- Math library: NumPy for vector operations
- Learning rate: Incremental (no hyperparameter, mean calculation)

## Dev Agent Record

### Context Reference

<!-- Story context created by SM agent with comprehensive architecture analysis -->

### Agent Model Used

Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

### Debug Log References

N/A

### Completion Notes List

**2025-12-07 Code Review Completion:**
- Backend implementation completed for AC 1-5
- All core centroid RL functionality implemented and tested
- API endpoints created for circle assignment/removal with centroid updates
- Circle prediction integrated into somethings creation response
- 8/8 unit tests passing for centroid service
- Integration tests deferred (not critical for MVP backend completion)
- iOS implementation deferred to separate task (can be done in parallel with MVP-2)

**Implementation Decisions:**
1. Added `predict_circles_for_something()` wrapper method beyond spec for better API ergonomics
2. Implemented graceful degradation - circle prediction failures don't block something creation
3. Learning signals (is_user_assigned, confidence_score) set automatically in assignment endpoints
4. GET predict-similar endpoint uses simplified similarity calculation (production would use FAISS)

**Known Limitations:**
- Integration tests not yet written (test_circles_api_centroid.py)
- iOS updates not completed (deferred to allow parallel work)
- predict-similar endpoint does O(N) scan instead of FAISS (acceptable for MVP scale)

### File List

**Files Created:**
- `backend/pookie-backend/alembic/versions/80625ba7815f_add_centroid_embedding_to_circles.py` - Database migration
- `backend/pookie-backend/app/services/centroid_service.py` - Centroid RL service (289 lines)
- `backend/pookie-backend/app/api/routes/circles.py` - Circle assignment API endpoints (346 lines)
- `backend/pookie-backend/tests/test_centroid_service.py` - Unit tests (279 lines, 8 tests passing)

**Files Modified:**
- `backend/pookie-backend/app/models/circle.py` - Added centroid_embedding column (line 16)
- `backend/pookie-backend/app/schemas/something.py` - Added CirclePrediction schema and suggestedCircles field (lines 27-44)
- `backend/pookie-backend/app/api/routes/somethings.py` - Added circle prediction to POST endpoint (lines 100-128)
- `backend/pookie-backend/app/api/routes/api.py` - Registered circles router (line 9)

**Files Referenced:**
- `backend/pookie-backend/app/services/embedding_service.py` - Used for generating embeddings
- `backend/pookie-backend/app/models/something_circle.py` - Junction table with learning signals
- `backend/pookie-backend/app/core/security.py` - JWT authentication
- `backend/pookie-backend/app/core/database.py` - Database session management
