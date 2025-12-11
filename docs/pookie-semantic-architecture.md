# Pookie Semantic Architecture: Personalized Semantic Universe

**Version:** 1.0
**Date:** 2025-12-06
**Status:** Architectural Decision Record

---

## Executive Summary

Pookie is not a search engine—it's a **cognitive architecture**. This document defines how Pookie builds a personalized semantic universe that evolves through user feedback, combining vanilla RAG with custom semantic layers to create an AI assistant that understands personal meaning, not just generic language patterns.

---

## The Core Philosophy

### What Traditional RAG Does
```
User Query → Embed → FAISS Retrieval → LLM Generation
```

Traditional RAG retrieves based on **pretrained semantic geometry**:
- "I'm hungry" → retrieves food-related content
- "I want to eat" → retrieves food-related content
- Fixed semantic space, no personalization

### What Pookie Does
```
User Query → Embed → FAISS (raw recall) → Centroid Re-ranking → LLM Generation
                                          ↑
                                    User Feedback → Centroid Shift (RL)
```

Pookie **layers custom semantics on top of base embeddings**:
- User marks items as "desire" not just "food"
- Centroid for "desire" shifts toward those items
- Future retrieval prioritizes personal semantic categories
- System evolves = **Reinforcement Learning**

---

## Architectural Layers

### Layer 1: Base Semantic Space (Vanilla RAG)
**Technology:** sentence-transformers (all-MiniLM-L6-v2)
**Purpose:** Generic human language understanding

- 384-dimensional dense vectors
- Pretrained on MS MARCO, natural questions
- Captures universal semantic relationships
- **Cannot be modified** (fixed geometry)

**Example:**
```
"I'm hungry" → [0.12, -0.45, 0.78, ...]  (384-dim)
"I want to eat" → [0.14, -0.43, 0.76, ...]  (similar vector)
```

### Layer 2: Semantic Lattice (Custom Centroids)
**Technology:** Dynamic centroid tracking per Circle of Care
**Purpose:** Personal semantic categories that learn from feedback

Each Circle has:
- `centroid_embedding` (384-dim vector) = mean of all Something embeddings in that circle
- Updated incrementally when user assigns items to circles

**Math:**
```python
# Initial centroid (first item in circle)
centroid = embedding_first_item

# Incremental update when user adds item to circle
centroid_new = (N * centroid_old + embedding_new) / (N + 1)

# Where N = number of items currently in circle
```

**Example:**
```
Circle: "Desires"
- User assigns "I'm hungry" → centroid shifts
- User assigns "I want to be famous" → centroid shifts
- User assigns "I need recognition" → centroid shifts
Result: "Desires" centroid now represents user's personal concept of desire
```

### Layer 3: Personalized Semantic Retrieval
**Technology:** Hybrid similarity scoring
**Purpose:** Retrieve based on personal meaning, not just generic similarity

**Similarity Formula:**
```python
final_similarity = (
    w1 * cos(base_embedding_query, base_embedding_item) +
    w2 * cos(circle_centroid, base_embedding_item) +
    w3 * user_assignment_boost +
    w4 * confidence_penalty
)
```

**Weights:**
- `w1 = 0.4` - Base semantic similarity (generic meaning)
- `w2 = 0.4` - Circle centroid similarity (personal meaning)
- `w3 = 0.15` - Boost if user manually assigned (high confidence)
- `w4 = 0.05` - Penalty for low-confidence auto-assignments

**Re-ranking Example:**

Query: "Why do I keep procrastinating eating?"

**Generic RAG retrieval:**
1. Food tips (0.82 similarity)
2. Recipes (0.78)
3. Hunger hormones (0.76)
4. Self-regulation (0.71)
5. Desire psychology (0.68)

**Pookie semantic retrieval** (user has marked items as "desire"):
1. Desire psychology (0.89 - boosted by centroid)
2. Self-regulation (0.85 - boosted by centroid)
3. Procrastination metaphysics (0.82 - boosted by centroid)
4. Hunger hormones (0.76)
5. Food tips (0.73)

---

## Reinforcement Learning Loop

### The Feedback Cycle

```
1. Pookie suggests → "This seems like 'Food'"
2. User corrects → "No, this is 'Desire'"
3. Backend updates:
   - Remove from "Food" centroid (if was assigned)
   - Add to "Desire" centroid
   - Store correction signal (is_user_assigned = True)
4. Future predictions improve → Next similar item more likely to be "Desire"
```

### Learning Signals in Database

**Table: `something_circles` (junction table)**
- `is_user_assigned` (Boolean) - TRUE if user manually assigned, FALSE if LLM-suggested
- `confidence_score` (Float 0-1) - LLM confidence in auto-assignment

**Table: `somethings`**
- `is_meaning_user_edited` (Boolean) - TRUE if user corrected LLM-generated meaning

These flags enable:
- Tracking prediction accuracy
- Weighting user corrections higher in retrieval
- Training future LLM prompts with examples of correct assignments

---

## Implementation Architecture

### Database Schema

**Circles Table:**
```sql
CREATE TABLE circles (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    circle_name TEXT NOT NULL,
    description TEXT,
    centroid_embedding FLOAT[384],  -- NEW: stores circle centroid
    care_frequency INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Junction Table with Learning Signals:**
```sql
CREATE TABLE something_circles (
    id SERIAL PRIMARY KEY,
    something_id INTEGER NOT NULL,
    circle_id INTEGER NOT NULL,
    is_user_assigned BOOLEAN DEFAULT FALSE,  -- Learning signal
    confidence_score FLOAT,  -- LLM confidence (0-1)
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(something_id, circle_id)
);
```

### Centroid Service

**Location:** `app/services/centroid_service.py`

```python
class CentroidService:
    """Manages circle centroids for personalized semantic retrieval"""

    async def initialize_centroid(
        self,
        circle_id: int,
        first_embedding: List[float],
        db: Session
    ) -> None:
        """Initialize centroid when first item added to circle"""
        circle = db.query(Circle).filter(Circle.id == circle_id).first()
        circle.centroid_embedding = first_embedding
        db.commit()

    async def update_centroid(
        self,
        circle_id: int,
        new_embedding: List[float],
        db: Session
    ) -> None:
        """Incrementally update centroid when item added to circle"""
        circle = db.query(Circle).filter(Circle.id == circle_id).first()

        # Count items in circle
        n_items = db.query(SomethingCircle).filter(
            SomethingCircle.circle_id == circle_id
        ).count()

        if circle.centroid_embedding is None:
            # First item
            circle.centroid_embedding = new_embedding
        else:
            # Incremental update
            old_centroid = np.array(circle.centroid_embedding)
            new_emb = np.array(new_embedding)
            updated_centroid = (
                (n_items - 1) * old_centroid + new_emb
            ) / n_items
            circle.centroid_embedding = updated_centroid.tolist()

        db.commit()

    async def remove_from_centroid(
        self,
        circle_id: int,
        removed_embedding: List[float],
        db: Session
    ) -> None:
        """Update centroid when item removed from circle"""
        circle = db.query(Circle).filter(Circle.id == circle_id).first()
        n_items = db.query(SomethingCircle).filter(
            SomethingCircle.circle_id == circle_id
        ).count()

        if n_items == 0:
            circle.centroid_embedding = None
        else:
            old_centroid = np.array(circle.centroid_embedding)
            removed = np.array(removed_embedding)
            updated_centroid = (
                (n_items + 1) * old_centroid - removed
            ) / n_items
            circle.centroid_embedding = updated_centroid.tolist()

        db.commit()

    async def compute_circle_similarities(
        self,
        query_embedding: List[float],
        user_id: str,
        db: Session
    ) -> List[Tuple[int, float]]:
        """Compute similarity between query and all user's circle centroids"""
        circles = db.query(Circle).filter(Circle.user_id == user_id).all()

        similarities = []
        query_vec = np.array(query_embedding)

        for circle in circles:
            if circle.centroid_embedding:
                centroid = np.array(circle.centroid_embedding)
                similarity = np.dot(query_vec, centroid) / (
                    np.linalg.norm(query_vec) * np.linalg.norm(centroid)
                )
                similarities.append((circle.id, float(similarity)))

        # Sort by similarity descending
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities
```

### Personalized Retrieval Service

**Location:** `app/services/personalized_retrieval_service.py`

```python
class PersonalizedRetrievalService:
    """Combines RAG + custom semantics for personalized retrieval"""

    async def retrieve_and_rerank(
        self,
        query: str,
        user_id: str,
        db: Session,
        top_k: int = 10
    ) -> List[Dict]:
        """
        Step 1: RAG retrieval (candidate set)
        Step 2: Re-rank using circle centroids
        """
        # Generate query embedding
        query_embedding = embedding_service.generate_embedding(query)

        # Step 1: RAG - Get candidate set from FAISS
        raw_results = await faiss_service.search(
            query_embedding,
            user_id,
            top_k=50  # Over-retrieve for re-ranking
        )

        # Step 2: Get circle centroid similarities
        circle_sims = await centroid_service.compute_circle_similarities(
            query_embedding, user_id, db
        )
        circle_sim_map = {cid: sim for cid, sim in circle_sims}

        # Step 3: Re-rank using hybrid scoring
        reranked = []
        for result in raw_results:
            something_id = result['id']
            base_similarity = result['similarity']

            # Get something's circles
            something_circles = db.query(SomethingCircle).filter(
                SomethingCircle.something_id == something_id
            ).all()

            # Calculate centroid boost
            max_centroid_sim = 0.0
            user_assignment_boost = 0.0

            for sc in something_circles:
                if sc.circle_id in circle_sim_map:
                    max_centroid_sim = max(
                        max_centroid_sim,
                        circle_sim_map[sc.circle_id]
                    )
                if sc.is_user_assigned:
                    user_assignment_boost = 0.15

            # Hybrid scoring
            final_score = (
                0.4 * base_similarity +
                0.4 * max_centroid_sim +
                user_assignment_boost
            )

            reranked.append({
                'id': something_id,
                'base_similarity': base_similarity,
                'centroid_similarity': max_centroid_sim,
                'final_score': final_score,
                'content': result['content']
            })

        # Sort by final score
        reranked.sort(key=lambda x: x['final_score'], reverse=True)
        return reranked[:top_k]
```

---

## Vibe Profile = Circle Centroids

### The Connection

The user's **vibe profile** is simply the collection of all their circle centroids:

```python
vibe_profile = {
    "music": centroid_music,      # 384-dim vector
    "food": centroid_food,         # 384-dim vector
    "desires": centroid_desires,   # 384-dim vector
    "fitness": centroid_fitness,   # 384-dim vector
    ...
}
```

### Applications

**1. Discover New Content**
```python
# User sees new content (e.g., YouTube video)
new_content_embedding = embedding_service.generate_embedding(video_description)

# Compare to circle centroids
similarities = []
for circle_name, centroid in vibe_profile.items():
    sim = cosine_similarity(new_content_embedding, centroid)
    similarities.append((circle_name, sim))

# Suggest: "This matches your 'Fitness' circle (0.89 similarity)"
```

**2. Personalized Recommendations**
```python
# Find external content similar to user's "Music" centroid
recommended_songs = search_spotify_api(
    query_embedding=vibe_profile["music"],
    top_k=10
)
```

**3. Semantic Search Enhancement**
```python
# User searches: "Why do I care about this?"
query_embedding = embedding_service.generate_embedding("Why do I care about this?")

# Find closest circle
closest_circle = max(
    vibe_profile.items(),
    key=lambda x: cosine_similarity(query_embedding, x[1])
)

# Answer: "Because it relates to your 'Desires' circle"
```

**4. Evolution Tracking**
```python
# Track how centroids shift over time
circle_history = [
    {"date": "2025-01-01", "centroid": [0.1, 0.2, ...]},
    {"date": "2025-02-01", "centroid": [0.15, 0.22, ...]},
    {"date": "2025-03-01", "centroid": [0.18, 0.25, ...]},
]

# Visualization: "Your 'Fitness' interests have shifted toward strength training"
```

---

## Scaling Considerations

### Memory Efficiency
- **Raw embeddings:** Store all in FAISS (millions possible)
- **Centroids:** Store only N centroids (N = number of circles)
- **Typical user:** 5-20 circles → 5-20 centroids (negligible storage)

### Computation Efficiency
- **Query to centroids:** O(N) where N = number of circles (~10-20)
- **Query to FAISS:** O(log M) where M = number of items (millions)
- **Total:** Dominated by FAISS, centroid layer adds minimal overhead

### Hierarchical Scaling (Future)
If a circle becomes very diverse (e.g., "Music" with 10,000 items covering jazz, rock, classical):
```
Circle: Music
  ├── Subcentroid: Jazz
  ├── Subcentroid: Rock
  └── Subcentroid: Classical
```

Update strategy:
1. K-means clustering within circle
2. Create subcentroids
3. Compare query to subcentroids first, then to parent centroid

### Dynamic Pruning (Future)
- Merge small, similar circles automatically
- Split large, diverse circles into subcategories
- Keep total centroid count manageable (<100 per user)

---

## Integration Points

### Epic 2: Something Capture & Storage
- **Story 2.2:** Embedding generation (no changes needed)
- **Story 2.3:** FAISS vector storage (no changes needed)
- **Story 2.4:** Somethings API → Add centroid update on circle assignment

### Epic 4: Circles of Care
- **Story 4.1:** Add `centroid_embedding` column to Circles table
- **Story 4.X (NEW):** Implement CentroidService for learning
- **Story 4.4:** Update Circles API to handle feedback and centroid updates

### Epic 5: Discover/Vibe Profile
- **Story 5.1:** Replace static `np.mean()` with circle centroids
- **Story 5.2:** Use PersonalizedRetrievalService for recommendations

### Epic 6: RAG Chat
- **Story 6.1:** Use PersonalizedRetrievalService instead of vanilla FAISS

---

## Success Metrics

### User Experience
- **Prediction accuracy:** % of LLM circle suggestions accepted by user
- **Correction rate:** % of meanings user edits (should decrease over time)
- **Circle stability:** How often users reorganize items (should decrease as learning improves)

### Technical Performance
- **Centroid update latency:** <50ms per update
- **Retrieval latency:** <200ms for top-10 results (RAG + re-ranking)
- **Storage overhead:** <1KB per circle centroid

### Learning Effectiveness
- **Cold start:** First 5 items → low accuracy (no centroid yet)
- **Warm up:** 20+ items → accuracy should exceed 70%
- **Mature:** 100+ items → accuracy should exceed 85%

---

## The Final Picture

**RAG = Body of Memory**
FAISS stores all embeddings, provides raw recall

**Centroids = Mind**
Circle centroids represent personal semantic categories

**User Feedback = Learning Mechanism**
Every correction shifts centroids, improves predictions

**Pookie = Unified Consciousness**
Combines generic language understanding with personal meaning

---

## Conclusion

Pookie isn't building a better search engine—it's building a **personalized semantic universe** that evolves with the user. By layering custom semantics (centroids) on top of base embeddings (sentence-transformers), Pookie learns what matters to each individual user, not just what words mean in general.

This architecture enables:
- **Personalized retrieval** beyond generic similarity
- **Reinforcement learning** through user feedback
- **Vibe profiling** via circle centroids
- **Scalable growth** from dozens to millions of items

The system is **simple enough to implement in MVP** (just add centroid column + update logic) but **powerful enough to evolve** into a full cognitive architecture.

---

**Next Steps:**
1. Implement Story 4.X: Circle centroid learning
2. Update Epic 5 to use centroids for vibe profile
3. Add personalized retrieval to Epic 6 RAG chat
