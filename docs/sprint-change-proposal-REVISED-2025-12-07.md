# Sprint Change Proposal: REVISED - Scope Reduction with Centroid RL Architecture

**Date:** 2025-12-07 (REVISED)
**Project:** Pookie (Circles of Care)
**Proposed By:** Scrum Master Agent (via Correct Course Workflow)
**Revision Reason:** Include centroid-based RL architecture from pookie-semantic-architecture.md
**Approved By:** _Pending user approval_
**Change Scope:** **MAJOR** - Affects sprint backlog, epic structure, and MVP definition

---

## Executive Summary (REVISED)

**Recommendation:** Remove Story 2.7 (voice capture) + Eliminate Epics 3 & 5 + Compress remaining work into **4-5 MVP stories** focused on **centroid-based personalized semantic architecture** (Circles with RL + Personalized RAG Chat).

**Impact:** Reduces total remaining work from **25+ stories → 4-5 stories** (5x reduction)
**Timeline:** Enables MVP completion in **1-2 weeks** instead of months
**Risk:** **LOW** - Architecture already designed, centroid implementation is ~11.5 hours effort
**Business Value:** **VERY HIGH** - Demonstrates advanced ML (reinforcement learning via centroids, personalized RAG, semantic evolution)

---

## Key Revision: Including Centroid RL Architecture

### What I Initially Missed

The user is correct - the architecture documents show **centroid-based reinforcement learning** is already fully designed and is NOT significantly more complicated:

**From `pookie-semantic-architecture.md`:**
- Circle centroids are **incremental** (simple math: `(N*old + new)/(N+1)`)
- Database impact: **ONE column** (`circles.centroid_embedding FLOAT[384]`)
- Implementation effort: **~11.5 hours** (per centroid-architecture-impact-analysis.md)
- RL learning loop: User feedback → centroid shift → improved predictions

**From `centroid-architecture-impact-analysis.md`:**
- Epic 2 Stories 2.1-2.3: **NO CHANGES NEEDED** ✅
- Story 2.4: Minor enhancement (add circle predictions in response)
- FAISS: **NO CHANGES NEEDED** (centroids stored in PostgreSQL)
- Total new code: **CentroidService** + 3 API endpoints

**This is simpler than Epic 3 (separation) or Epic 5 (discovery) and provides BETTER ML showcase!**

---

## Section 1: Issue Summary (UNCHANGED)

[Same as original proposal - user needs fast recruiting MVP, Story 2.7 causing issues, etc.]

---

## Section 2: Impact Analysis

### Epic Impact (REVISED)

**Epic 2: Something Capture & Storage**
- **Current:** Stories 2.1-2.7 (7 stories)
- **Proposed:** Stories 2.1-2.6 only (remove 2.7)
- **Minor Enhancement:** Story 2.4 - Add circle predictions to POST /somethings/ response (backward-compatible)
- **Impact:** Simpler capture system (text only), sets up centroid predictions
- **Status:** Can be marked DONE immediately after 2.7 removal + minor 2.4 enhancement

**Epic 3: AI-Powered Something Separation (Call Agents Mode)**
- **Status:** **REMOVE ENTIRE EPIC** - Defer to "Circles of Care v2"
- **Reason:** Separation adds complexity without core ML value
- **Comparison:** Centroid RL is simpler AND more impressive for recruiting

**Epic 4: Semantic Organization (Circles of Care)**
- **Status:** **STREAMLINE and ENHANCE with Centroid RL**
- **OLD Scope:** K-means clustering + LLM naming + junction table + UI
- **NEW Scope:** K-means + LLM naming + **CentroidService (RL)** + junction table + UI
- **Enhancement:** Add centroid learning (incremental updates, predictions, RL loop)
- **Effort:** +11.5 hours for centroid implementation (per architecture analysis)
- **Priority:** **VERY HIGH** - This is the core ML differentiator

**Epic 5: Personalized Discovery**
- **Status:** **REMOVE but KEEP core concept via Centroids**
- **OLD:** Taste profile as np.mean() of embeddings
- **NEW:** Vibe profile = Circle centroids (more sophisticated, personalized)
- **Impact:** Better ML showcase, less code, already architected
- **Note:** Taste-based recommendations deferred to v2, but vibe profiling built into centroids

**Epic 6: RAG-Powered Personal Chat**
- **Status:** **ENHANCE with Personalized Retrieval**
- **OLD:** Vanilla RAG (FAISS retrieval + LLM)
- **NEW:** Personalized RAG (FAISS + centroid re-ranking + LLM)
- **Hybrid Scoring:** 40% base similarity + 40% centroid similarity + 15% user assignment boost
- **Effort:** PersonalizedRetrievalService implementation (already designed)
- **Priority:** **VERY HIGH** - Shows ML learning in action

---

## Section 3: Recommended Approach (REVISED)

### Path Forward: **Rollback + Centroid-Enhanced MVP**

**Selected Strategy:** Rollback Story 2.7 + Compress to 4-5 stories **with centroid RL architecture**

**Why Centroids Make This Better:**

1. **Already Designed:** Architecture documents have full specs (pookie-semantic-architecture.md, centroid-architecture-impact-analysis.md)
2. **Low Effort:** ~11.5 hours implementation, ONE database column, NO FAISS changes
3. **High Impact:** Demonstrates reinforcement learning, personalized semantics, ML that evolves
4. **Simple Math:** Incremental centroid updates are just `(N*old + new)/(N+1)` - very clean
5. **Better Demo:** "Watch Pookie learn from your feedback" > "Pookie separates thoughts"

**Comparison:**

| Feature | Effort | ML Showcase | Demo Value |
|---------|--------|-------------|------------|
| **Centroids (RL)** | 11.5 hours | ⭐⭐⭐⭐⭐ (reinforcement learning, personalization) | VERY HIGH |
| Separation (Epic 3) | 4 stories | ⭐⭐ (LLM orchestration) | MEDIUM |
| Discovery (Epic 5) | 4 stories | ⭐⭐⭐ (recommendations) | MEDIUM |

**Conclusion:** Centroids give MORE ML value for LESS effort than the removed epics!

---

## Section 4: Detailed Change Proposals (REVISED)

### NEW COMPRESSED MVP STRUCTURE (4-5 Stories)

```
✅ Foundation Complete (Epic 1: 7 stories)
✅ Capture Complete (Epic 2: 6 stories, removed 2.7)

📋 MVP Remaining (Epic MVP: 4-5 stories):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Story MVP-1: Implement Centroid-Based Circle Organization with RL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Backend (~8 hours):
  ✅ Add centroid_embedding column to circles table (FLOAT[384])
  ✅ Implement CentroidService class:
     - initialize_centroid(circle_id, first_embedding)
     - update_centroid(circle_id, new_embedding) → incremental: (N*old + new)/(N+1)
     - remove_from_centroid(circle_id, removed_embedding)
     - predict_circles_for_something(something_id, threshold=0.7, top_k=3)
  ✅ K-means clustering for initial circle creation
  ✅ LLM naming via OpenRouter
  ✅ Learning signals: is_user_assigned=True when user assigns manually
  ✅ API endpoints:
     - POST /circles/{id}/somethings/{id} → assign + update centroid
     - DELETE /circles/{id}/somethings/{id} → remove + adjust centroid
     - GET /circles/{id}/predict-similar → suggestions based on centroid

iOS (~6 hours):
  ✅ Circle list view (shows auto-organized circles)
  ✅ Circle detail view (somethings in circle + suggestions)
  ✅ Assign/remove somethings to circles
  ✅ Visual confidence indicators for predictions (0.0-1.0)
  ✅ Quick-accept suggestions UI

Acceptance Criteria:
  ✅ Somethings auto-organized into circles via K-means
  ✅ When user assigns something to circle, centroid updates incrementally
  ✅ When user creates new something, backend predicts circles (top-3, >0.7 confidence)
  ✅ Future predictions improve based on user feedback (RL loop)
  ✅ Circle names generated by LLM
  ✅ User can manually assign/remove with centroid adjustments

Technical Showcase:
  - Reinforcement learning via user feedback
  - Incremental centroid updates (efficient)
  - Personalized semantic categories
  - Learning signals in junction table

Effort: ~14 hours (aligned with architecture analysis: 11.5 hours core + UI)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Story MVP-2: Implement Personalized RAG Chat with Centroid Re-ranking
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Backend (~6 hours):
  ✅ Implement PersonalizedRetrievalService:
     Step 1: FAISS retrieval (top-50 candidates)
     Step 2: Compute circle centroid similarities for query
     Step 3: Re-rank using hybrid scoring:
       final_score = 0.4 * base_similarity +
                     0.4 * max_centroid_similarity +
                     0.15 * user_assignment_boost
     Step 4: Return top-10 personalized results
  ✅ Integrate Claude Haiku via OpenRouter
  ✅ SSE streaming for real-time responses
  ✅ API endpoint: POST /chat/stream

iOS (~4 hours):
  ✅ Chat interface with text input + message list
  ✅ SSE event handling for streaming responses
  ✅ Show which circles influenced the response
  ✅ Visual indicator: "Personalized using: Music, Fitness, Desires"

Acceptance Criteria:
  ✅ Chat retrieves candidates using vanilla FAISS
  ✅ Results re-ranked using circle centroids for personalization
  ✅ Responses grounded in user's personal semantic universe
  ✅ Higher relevance than generic RAG (testable via user feedback)
  ✅ Streaming tokens appear in real-time
  ✅ User sees which circles contributed to response

Technical Showcase:
  - Hybrid RAG (vanilla + personalized layers)
  - Centroid-based semantic re-ranking
  - Multi-stage retrieval pipeline
  - Real-time streaming LLM

Effort: ~10 hours

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Story MVP-3: Implement Care → Intention → Action Hierarchy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Backend (~4 hours):
  ✅ Intention model (links to circles via intention_cares junction)
  ✅ Action model (links to intentions, tracks completion)
  ✅ API endpoints for intention/action CRUD
  ✅ Relationship: Circles → Intentions → Actions

iOS (~4 hours):
  ✅ Intention view (shows intentions linked to circles)
  ✅ Action tracking view (mark as done)
  ✅ Visual hierarchy navigation

Acceptance Criteria:
  ✅ Users can create intentions from circles
  ✅ Actions tracked under intentions
  ✅ Visual hierarchy: Somethings → Circles → Intentions → Actions
  ✅ Mark actions as complete

Effort: ~8 hours

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Story MVP-4: Polish, Testing & RL Validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Testing (~6 hours):
  ✅ Test centroid math (incremental add: verify (N*old + new)/(N+1))
  ✅ Test centroid removal (verify reverse operation)
  ✅ Test RL learning loop:
     1. Create something → get predictions
     2. User assigns to circle → centroid shifts
     3. Create similar something → improved prediction accuracy
  ✅ Test hybrid RAG scoring (verify personalization)
  ✅ End-to-end: capture → circles → chat with personalization

Polish (~4 hours):
  ✅ Error handling (graceful LLM failures, network errors)
  ✅ Loading states (clustering, predictions, chat streaming)
  ✅ Empty states (no circles, no somethings, no chat history)

Acceptance Criteria:
  ✅ RL loop validated (user feedback improves predictions)
  ✅ Centroid updates mathematically correct
  ✅ Personalized RAG more relevant than vanilla (subjective test)
  ✅ No critical bugs, stable demo
  ✅ All error cases handled gracefully

Effort: ~10 hours

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Story MVP-5: Deploy & ML Demo Documentation (OPTIONAL)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Deployment (~4 hours):
  ✅ Backend to Render with environment variables
  ✅ iOS TestFlight build
  ✅ Verify centroid persistence in PostgreSQL

Documentation (~2 hours):
  ✅ README with ML architecture explanation:
     - Centroid-based reinforcement learning
     - Personalized semantic retrieval
     - Hybrid RAG scoring formula
  ✅ Demo flow screenshots
  ✅ Recruiting pitch: "ML that learns from you"

Acceptance Criteria:
  ✅ Deployed MVP accessible
  ✅ Documentation explains centroid RL clearly
  ✅ Screenshots show learning in action

Effort: ~6 hours (can be done manually, not critical)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOTAL MVP EFFORT: 42-48 hours (5-6 days for solo dev)
TOTAL STORIES: 4-5 stories
TIMELINE: 1-2 weeks to recruiting-ready MVP
```

---

### Technical Depth: Why Centroids Are Not More Complicated

**Centroid Update Math (Incremental):**
```python
# Adding item to circle
centroid_new = (N * centroid_old + embedding_new) / (N + 1)

# Removing item from circle
centroid_new = ((N + 1) * centroid_old - embedding_removed) / N
```

**That's it.** No complex training, no gradient descent, no neural networks.

**Database Impact:**
- ONE column: `circles.centroid_embedding FLOAT[384]`
- ONE migration file
- Nullable (null until first item assigned)

**FAISS Impact:**
- ZERO changes needed
- Centroids stored in PostgreSQL, not FAISS
- FAISS continues to work exactly as before

**RL Learning Loop:**
```
1. User creates something → Backend predicts circles (compare to centroids)
2. User accepts/rejects → is_user_assigned flag set
3. Centroid shifts → Future predictions improve
```

**Effort Breakdown (from centroid-architecture-impact-analysis.md):**
- Database migration: 1 hour
- CentroidService implementation: 4 hours
- API endpoints (3 new): 3 hours
- Testing: 2 hours
- Epic 5 vibe profile update: 1.5 hours
- **Total: 11.5 hours**

**This is LESS effort than:**
- Epic 3 separation (4 stories)
- Epic 5 discovery (4 stories)
- Story 2.7 voice capture (threading nightmares)

---

## Section 5: Implementation Handoff (REVISED)

### Change Scope Classification: **MAJOR** (with centroid enhancement)

**Handoff Recipients:**

1. **Development Team (Dev Agent)**
   - Execute git revert (Story 2.7 removal)
   - Implement Story 2.4 enhancement (circle predictions)
   - Implement MVP-1 (Centroid RL + Circles)
   - Implement MVP-2 (Personalized RAG)
   - Implement MVP-3 (Care → Intention → Action)
   - Implement MVP-4 (Testing + Polish)
   - Optional: MVP-5 (Deployment)

2. **Scrum Master / Product Owner**
   - Update sprint status with new MVP structure
   - Update epics.md with centroid enhancements
   - Communicate centroid RL as key differentiator

3. **Product Manager / Solution Architect**
   - Approve centroid architecture integration
   - Define "Circles of Care v2" roadmap (voice, separation, discovery)
   - Update recruiting demo script to highlight RL learning

### Success Criteria (REVISED)

**MVP Complete When:**
1. ✅ Users can capture somethings via text (Story 2.6)
2. ✅ Somethings auto-organize into circles (K-means)
3. ✅ **Backend predicts circles for new somethings (centroid similarity)**
4. ✅ **User assigns something to circle → centroid shifts (RL learning)**
5. ✅ **Future predictions improve (testable: 2nd prediction > 1st prediction)**
6. ✅ Users see care → intention → action hierarchy
7. ✅ **Chat uses personalized RAG (hybrid: FAISS + centroids)**
8. ✅ Chat responses more relevant than vanilla RAG (subjective)
9. ✅ No critical bugs, stable demo
10. ✅ Optional: Deployed to Render + TestFlight

**ML Capabilities Demonstrated:**
- 🤖 **Reinforcement Learning:** User feedback → centroid shift → improved predictions
- 🤖 **Personalized Semantics:** Circle centroids = user's personal semantic categories
- 🤖 **Hybrid RAG:** Vanilla retrieval + custom re-ranking
- 🤖 **Evolution:** System learns and improves over time
- 🤖 **Vibe Profiling:** Circle centroids represent user's "vibe"

**Timeline Estimate (REVISED):**
- MVP-1: 2-3 days (centroids + circles + RL)
- MVP-2: 1.5-2 days (personalized RAG)
- MVP-3: 1 day (hierarchy)
- MVP-4: 1.5 days (testing + polish)
- MVP-5: 0.5-1 day (deployment - optional)

**Total:** 6.5-8.5 days → **Recruiting-ready in 1.5-2 weeks**

---

## Section 6: Why This Is Better Than Original Proposal

### Original Proposal (No Centroids)
- Circles with basic clustering
- Generic RAG chat
- 4-5 stories
- ML showcase: Medium (just clustering + LLM)

### REVISED Proposal (With Centroids)
- Circles with **centroid-based RL**
- **Personalized RAG** with hybrid scoring
- 4-5 stories (SAME count)
- **Effort:** +11.5 hours (one extra day)
- **ML showcase: VERY HIGH** (RL, personalization, evolution)

### Recruiting Demo Comparison

**Without Centroids:**
> "Pookie uses K-means to organize your thoughts into circles, then answers questions using RAG."

**With Centroids:**
> "Pookie builds a personalized semantic universe that evolves with you. Watch:
> 1. I create a thought → Pookie predicts which circle it belongs to
> 2. I correct Pookie → The circle's centroid shifts (reinforcement learning)
> 3. I create a similar thought → Pookie's prediction is now better
> 4. I ask a question → Pookie retrieves using MY personal semantics, not generic embeddings
>
> This is ML that learns from you in real-time."

**Impact:** Centroids turn Pookie from "smart organizer" → "learning AI companion"

---

## Appendix A: Centroid Architecture Quick Reference

### Database Schema
```sql
-- ONE column addition
ALTER TABLE circles ADD COLUMN centroid_embedding FLOAT[384];
```

### CentroidService Methods
```python
class CentroidService:
    async def initialize_centroid(circle_id, first_embedding)
    async def update_centroid(circle_id, new_embedding)  # (N*old + new)/(N+1)
    async def remove_from_centroid(circle_id, removed_embedding)
    async def predict_circles_for_something(something_id, threshold=0.7, top_k=3)
    async def compute_circle_similarities(query_embedding, user_id)
```

### PersonalizedRetrievalService
```python
class PersonalizedRetrievalService:
    async def retrieve_and_rerank(query, user_id, top_k=10):
        # Step 1: FAISS retrieval (top-50)
        raw_results = faiss_service.search(query_embedding, top_k=50)

        # Step 2: Get circle centroid similarities
        circle_sims = centroid_service.compute_circle_similarities(query_embedding, user_id)

        # Step 3: Hybrid scoring
        for result in raw_results:
            final_score = (
                0.4 * result.base_similarity +
                0.4 * max_centroid_similarity +
                0.15 * user_assignment_boost
            )

        # Step 4: Return top-10 personalized
        return sorted_by_final_score[:10]
```

### Hybrid Scoring Formula
```
final_similarity = (
    0.40 * cos(query_embedding, something_embedding) +  # Base semantic
    0.40 * cos(query_embedding, circle_centroid) +      # Personal semantic
    0.15 * is_user_assigned +                           # User feedback boost
    0.05 * confidence_penalty                           # LLM uncertainty
)
```

---

## Approval & Sign-off (REVISED)

**Proposed By:** Scrum Master Agent (Correct Course Workflow)
**Date:** 2025-12-07 (REVISED to include centroid RL architecture)
**Review Status:** ⏳ Pending user approval

**User Approval Required:**
- [ ] Approve git revert (Story 2.7 removal)
- [ ] Approve epic removals (Epic 3, Epic 5)
- [ ] Approve **centroid-enhanced MVP** (4-5 stories with RL)
- [ ] Approve "Circles of Care v2" roadmap for deferred features

**Key Decision:**
Do you want the **centroid-based personalized semantic architecture** in MVP?
- **YES (RECOMMENDED):** +11.5 hours, MUCH better ML showcase, RL learning demo
- **NO (simpler):** Basic circles, generic RAG, less impressive for recruiting

**Next Steps After Approval:**
1. Execute git revert to commit bce33b6
2. Implement Story 2.4 enhancement (circle predictions)
3. Update sprint-status.yaml
4. Update epics.md with centroid notes
5. Begin MVP-1 implementation (Centroid RL + Circles)

---

**End of REVISED Sprint Change Proposal**
