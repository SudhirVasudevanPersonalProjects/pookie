# 🧠 Pookie ML Architecture

**Centroid-Based Reinforcement Learning for Personalized Semantic Retrieval**

---

## tl;dr

Pookie combines **FAISS vector search** with **dynamic centroid tracking** to create a personalized RAG system that learns from user feedback in real-time. Instead of fine-tuning language models (hours, GPU costs), we update circle centroids (simple vector means, <50ms, free). User corrections shift centroids, improving future predictions—reinforcement learning through vector geometry.

---

## The Problem with Generic RAG

**Traditional RAG pipeline:**
```
User Query → sentence-transformers → FAISS → Top-K Results → LLM Context
```

**Problem:** Everyone gets the same semantic space.

"I want to run" retrieves fitness articles for everyone—whether you're a marathon runner or a startup founder talking about "running a company."

**What's missing:** Personal semantics. The word "run" means different things to different people.

---

## The Pookie Solution: Layered Semantics

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERACTION                         │
│  "I need to run a 5K" → Create Something                    │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              LAYER 1: Base Embeddings                        │
│  sentence-transformers (all-MiniLM-L6-v2)                    │
│  384-dim vector: [0.23, -0.15, 0.08, ..., 0.42]            │
│  Generic semantic understanding (everyone gets same result)  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│           LAYER 2: Circle Prediction (ML)                    │
│  Compare to ALL circle centroids:                           │
│  - Circle "Fitness": cosine_sim = 0.85                      │
│  - Circle "Career": cosine_sim = 0.42                       │
│  - Circle "Personal Growth": cosine_sim = 0.38              │
│  → Predict: Fitness (85% confidence)                        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│         LAYER 3: Reinforcement Learning Loop                 │
│  IF user corrects prediction:                               │
│    1. Assign to correct circle                               │
│    2. Update centroid: centroid_new =                       │
│         (N * centroid_old + embedding_new) / (N + 1)        │
│    3. Mark as "user_assigned" (learning signal)             │
│  Next similar item → Improved prediction ✨                 │
└─────────────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│      LAYER 4: Personalized RAG Retrieval                     │
│  Chat query: "What have I thought about fitness?"           │
│  → FAISS search (top 50 candidates)                         │
│  → Centroid re-ranking (hybrid scoring):                    │
│      final_score = 0.40 * base_similarity +                 │
│                    0.40 * centroid_similarity +              │
│                    0.15 * user_feedback_boost +              │
│                    0.05 * recency_score                      │
│  → Top 10 results → LLM context → Streaming response        │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Components

### 1. Circle Centroids (Personal Semantic Anchors)

**What it is:**
- Each Circle has a `centroid_embedding` column (384-dim float array)
- Centroid = mathematical mean of all Something embeddings in that circle
- Updated incrementally every time user assigns/removes items

**Why it matters:**
- Centroids represent **your personal concept** of that category
- "Fitness" circle centroid ≠ Wikipedia's concept of fitness
- Your "Fitness" might emphasize mental health, mine might emphasize competition

**Math (Incremental Mean Update):**
```python
# Adding item to circle
centroid_new = (N * centroid_old + embedding_new) / (N + 1)

# Removing item from circle
centroid_new = ((N + 1) * centroid_old - embedding_removed) / N

# Normalization (unit vector for consistent similarity)
centroid_normalized = centroid_new / ||centroid_new||
```

**Performance:**
- Time complexity: O(384) = ~30ms on CPU
- No batching required (update immediately)
- No GPU needed (simple vector arithmetic)

---

### 2. Hybrid Similarity Scoring (Personalized Retrieval)

**Vanilla FAISS:**
```python
results = faiss.search(query_embedding, k=50)
# Everyone with same query gets same results
```

**Pookie's Hybrid Scoring:**
```python
# Step 1: FAISS baseline (top 50 candidates)
candidates = faiss.search(query_embedding, k=50)

# Step 2: Re-rank with circle centroids
for item in candidates:
    # Get all circles this item belongs to
    circles = get_circles_for_item(item.id)

    # Compute hybrid score
    base_similarity = cosine_similarity(query_embedding, item.embedding)

    # Average centroid similarity across all relevant circles
    centroid_similarity = mean([
        cosine_similarity(query_embedding, circle.centroid)
        for circle in circles
    ])

    # User feedback boost (did user manually assign this?)
    user_boost = 1.0 if item.is_user_assigned else 0.0

    # Recency penalty (prefer recent items)
    recency = calculate_time_decay(item.created_at)

    # Final weighted score
    final_score = (
        0.40 * base_similarity +      # Universal semantics
        0.40 * centroid_similarity +  # Personal semantics
        0.15 * user_boost +            # Learning signal
        0.05 * recency                 # Time decay
    )

# Step 3: Sort by final_score, return top 10
top_10 = sorted(candidates, key=lambda x: x.final_score, reverse=True)[:10]
```

**Why this works:**
- **Base similarity (40%):** Ensures general relevance (don't retrieve nonsense)
- **Centroid similarity (40%):** Adds personal meaning (YOUR definition of concepts)
- **User boost (15%):** Reinforces learning signals (items you corrected get priority)
- **Recency (5%):** Recent thoughts matter more

---

### 3. Reinforcement Learning Loop (Learning from Feedback)

**Traditional fine-tuning:**
```
User feedback → Collect dataset → Train model (hours/days, GPU) → Deploy
```

**Pookie's centroid RL:**
```
User correction → Update centroid (30ms, CPU) → Immediately better predictions
```

**Example Learning Flow:**

**Initial State:**
```
Circle "Fitness": 8 items, centroid = mean([running, gym, protein, ...])\nCircle "Career": 6 items, centroid = mean([promotion, skills, networking, ...])
```

**User creates:** "I need to run this sprint faster"
**System predicts:** Fitness (75% confidence) ← "run" semantically close to running/gym

**User corrects:** "Actually, this is Career" ← talking about software sprints

**System updates:**
```python
career_centroid_new = (6 * career_centroid_old + embedding_sprint) / 7
# Career centroid now includes "sprint" context
```

**Next item:** "Our sprint planning needs work"
**System predicts:** Career (85% confidence) ✨ ← learned from feedback!

**Result:** System adapts to YOUR language patterns in real-time.

---

### 4. K-Means Clustering (Initial Circle Formation)

**When:** After user creates 5-10 somethings
**How:**
```python
from sklearn.cluster import KMeans

# Cluster somethings into semantic groups
embeddings = [something.embedding for something in somethings]
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(embeddings)

# Create circles with cluster centroids
for cluster_id in range(3):
    circle = Circle(
        name=generate_name_with_llm(cluster_items),
        centroid_embedding=kmeans.cluster_centers_[cluster_id],
        user_id=user.id
    )
```

**Why K-means:**
- Simple, fast, interpretable
- Centroids are mathematically meaningful (mean of cluster)
- Good initialization for RL learning loop
- Works well with sentence-transformer embeddings

---

## Performance & Cost Analysis

### Latency Benchmarks (M1 MacBook Pro)

| Operation | Target | Actual | Details |
|-----------|--------|--------|---------|
| Embedding generation | <200ms | ~150ms | sentence-transformers local |
| **Centroid update** | **<50ms** | **~30ms** | Simple vector mean (384-dim) |
| FAISS search (50 items) | <100ms | ~60ms | Local index file |
| Hybrid re-ranking (50→10) | <100ms | ~70ms | Cosine similarity + sorting |
| Full RAG pipeline | <300ms | ~250ms | Retrieval + re-ranking |
| LLM first token | <500ms | ~400ms | OpenRouter + Claude Haiku |
| Complete chat response | <2s | ~1.5s | Streaming SSE |

### Cost Breakdown (Monthly, Free-Tier Stack)

| Component | Service | Cost | Notes |
|-----------|---------|------|-------|
| Backend hosting | Render Free | $0 | 750 hours/month (always on) |
| Database | Supabase Free | $0 | 500MB limit (~50k somethings) |
| Auth | Supabase Free | $0 | Included |
| **Embeddings** | **sentence-transformers** | **$0** | **Local CPU, no API** |
| **Vector search** | **FAISS** | **$0** | **Local file, no API** |
| **Centroid updates** | **In-app** | **$0** | **Pure math, no service** |
| LLM chat | OpenRouter (Claude Haiku) | ~$0.50-3 | $0.25/1M tokens, ~10-100 queries/day |

**Total: ~$0-3/month** for personal AI with reinforcement learning 🎉

---

## Why This Approach?

### Compared to Fine-Tuning

| Aspect | Fine-Tuning | Centroid RL |
|--------|-------------|-------------|
| **Learning time** | Hours/days | <50ms |
| **Hardware** | GPU required | CPU sufficient |
| **Cost** | $$$ GPU bills | $0 (free tier) |
| **Interpretability** | Black box weights | Geometric centroids (visualizable) |
| **Update frequency** | Batch (accumulate data) | Real-time (immediate feedback) |
| **Rollback** | Hard (need checkpoints) | Easy (recalculate mean) |

### Compared to Vanilla RAG

| Aspect | Vanilla RAG | Pookie (Personalized RAG) |
|--------|-------------|---------------------------|
| **Retrieval** | Base embeddings only | Base + centroids (hybrid) |
| **Personalization** | None | Circle centroids = personal semantics |
| **Learning** | Fixed (pretrained) | Adaptive (RL from feedback) |
| **Cost** | Same | Same (centroids are free) |
| **Complexity** | Low | Medium (hybrid scoring) |

---

## Implementation Details

### Database Schema (Key Columns)

**`circles` table:**
```sql
CREATE TABLE circles (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    centroid_embedding FLOAT[384],  -- ← The magic happens here
    member_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**`something_circles` junction table:**
```sql
CREATE TABLE something_circles (
    something_id UUID REFERENCES somethings(id),
    circle_id UUID REFERENCES circles(id),
    confidence_score FLOAT,         -- ← Prediction confidence (0-1)
    is_user_assigned BOOLEAN,       -- ← Learning signal (user corrected?)
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (something_id, circle_id)
);
```

### Key Services

**`app/services/centroid_service.py`:**
- `calculate_centroid()`: Compute mean of embeddings
- `update_centroid_add()`: Incremental update when adding item
- `update_centroid_remove()`: Incremental update when removing item
- `normalize_centroid()`: Ensure unit vector (cosine similarity)

**`app/services/personalized_retrieval_service.py`:**
- `hybrid_search()`: FAISS + centroid re-ranking
- `calculate_hybrid_score()`: 4-factor weighted scoring
- `get_top_k_with_centroids()`: Final results for LLM

**`app/services/clustering_service.py`:**
- `cluster_somethings()`: K-means initialization
- `generate_circle_name()`: LLM-based naming

---

## Test Coverage & Validation

**Centroid Math Validation** (`tests/test_centroid_service.py` - 9 tests):
- ✅ Incremental add formula produces correct mean
- ✅ Incremental remove formula reverses addition
- ✅ Normalization maintains unit vectors
- ✅ Edge cases: first item, last item, empty circle
- ✅ Floating point precision over 100 operations

**RL Learning Loop** (`tests/test_rl_learning_loop.py` - 5 tests):
- ✅ User correction shifts centroids toward assigned items
- ✅ Multiple corrections compound learning effect
- ✅ Centroid shift improves predictions for similar items
- ✅ Learning signals stored in junction table (`is_user_assigned`)
- ✅ Final centroids reflect learned distribution

**Hybrid RAG Scoring** (`tests/test_hybrid_rag_scoring.py` - 6 tests):
- ✅ Formula weights sum to 1.0 (0.40 + 0.40 + 0.15 + 0.05)
- ✅ Centroid boost increases relevance scores vs. vanilla FAISS
- ✅ User assignment boost (+0.15) applied correctly
- ✅ Re-ranking changes order (personalization works)
- ✅ Graceful fallback to vanilla FAISS when no circles exist

**Total:** 20 passing tests validating math, learning, and personalization.

---

## Future Enhancements (v2)

### Multi-Circle Semantics
- Allow somethings to belong to multiple circles
- Weighted centroid influence per circle
- Example: "meditation retreat" → 80% Wellness + 20% Travel

### Confidence Thresholds
- High confidence (>0.80): Auto-assign to predicted circle
- Medium confidence (0.50-0.80): Suggest to user
- Low confidence (<0.50): Ask user to choose

### Centroid Drift Analytics
- Visualize how centroids evolve over time
- "Your 'Fitness' concept shifted toward mental health in Q3"
- Detect interest changes, life transitions

### Cross-User Vibe Profiles (Privacy-Preserving)
- Share circle centroids (not raw content)
- Find users with similar semantic patterns
- "You and User X both have similar 'Creative Projects' vibes"

---

## Related Documents

- **[README.md](../README.md)**: High-level overview, getting started, deployment
- **[pookie-semantic-architecture.md](pookie-semantic-architecture.md)**: Full architectural philosophy and design rationale
- **[DEMO-SCRIPT.md](DEMO-SCRIPT.md)**: 7-minute recruiting demo walkthrough
- **[Sprint Change Proposal](sprint-change-proposal-2025-12-07.md)**: MVP scope decisions and centroid RL adoption

---

## Technical References

**sentence-transformers (all-MiniLM-L6-v2):**
- Paper: [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084)
- Model: 22M parameters, 384-dim embeddings, trained on NLI + semantic similarity tasks
- Performance: ~90% of BERT performance at 5x speed

**FAISS (Facebook AI Similarity Search):**
- GitHub: [facebookresearch/faiss](https://github.com/facebookresearch/faiss)
- IndexFlatL2: Exact L2 distance search (no approximation)
- Performance: <100ms for 10k vectors on CPU

**K-means Clustering:**
- scikit-learn implementation: `sklearn.cluster.KMeans`
- Lloyd's algorithm with k-means++ initialization
- Converges in <10 iterations for sentence embeddings

---

## Conclusion

Pookie demonstrates that **reinforcement learning doesn't require neural networks**. By treating user feedback as centroid updates in embedding space, we achieve:

1. **Real-time learning** (<50ms updates, no GPU)
2. **Interpretable personalization** (centroids are just vector means)
3. **Cost-efficient architecture** (~$0-3/month on free tiers)
4. **Production-ready ML system** (20 passing tests, deployed backend)

This is reinforcement learning through **vector geometry**, not gradient descent. And it works.

---

**Author:** Sudy
**Date:** 2025-12-08
**Version:** 1.0
**License:** MIT
