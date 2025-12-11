# Sprint Change Proposal: Radical MVP Scope Reduction

**Date:** 2025-12-07
**Project:** Pookie (Circles of Care)
**Proposed By:** Scrum Master Agent (via Correct Course Workflow)
**Approved By:** _Pending user approval_
**Change Scope:** **MAJOR** - Affects sprint backlog, epic structure, and MVP definition

---

## Executive Summary

**Recommendation:** Remove Story 2.7 (voice capture) + Eliminate Epics 3 & 5 + Compress remaining work into 4-5 MVP stories focused on core ML capabilities (Circles + Chat).

**Impact:** Reduces total remaining work from **25+ stories → 4-5 stories** (5x reduction)
**Timeline:** Enables MVP completion in **1-2 weeks** instead of months
**Risk:** **LOW** - Simpler architecture, clearer focus, stable foundation
**Business Value:** **HIGH** - ML differentiation for recruiting demo (semantic organization + RAG chat)

---

## Section 1: Issue Summary

### Problem Statement

User needs to complete Pookie MVP **fast for recruiting purposes** (< 5 stories total remaining). Currently at Story 2.7 of Epic 2, with **4 more epics (20+ stories) in backlog**. Story 2.7 (voice capture) is "not working cleanly" and adds complexity without contributing to core ML value proposition.

### Context & Discovery

- **Trigger:** User request: "i need to finish project fast for recruiting purposes"
- **Current State:**
  - Epic 1: ✅ Done (Foundation)
  - Epic 2: ✅ Done (Stories 2.1-2.6), ⚠️ Story 2.7 problematic
  - Epics 3-6: 📋 Backlog (20+ stories remaining)
- **Pain Point:** Voice capture causing threading issues, permission complexity, speech recognition edge cases
- **Core Issue:** Scope is too large (30+ stories) for recruiting timeline; voice/separation are not ML differentiators

### Evidence

1. **Story 2.7 Complexity:** Code review found 13 issues (threading, memory leaks, permission handling, network errors)
2. **Git Status:** Uncommitted changes for 2.7, indicates work in progress/instability
3. **User Statement:** "get rid of any exogenous ux designs including 2.7 because its not working cleanly"
4. **Timeline Pressure:** "finish in < 5 stories everything"
5. **True Value:** "ml, chat with pookie, organization into circles, care into intention, and intention into action" - user identifies ML features as core

---

## Section 2: Impact Analysis

### Epic Impact

**Epic 2: Something Capture & Storage**
- **Current:** Stories 2.1-2.7 (7 stories)
- **Proposed:** Stories 2.1-2.6 only (remove 2.7)
- **Impact:** Simpler capture system (text only), stable baseline
- **Status:** Can be marked DONE immediately after 2.7 removal

**Epic 3: AI-Powered Something Separation (Call Agents Mode)**
- **Current:** 4 stories (LLM service, separation API, batch creation, iOS UI)
- **Proposed:** **REMOVE ENTIRE EPIC** - Defer to "Circles of Care v2"
- **Impact:** Saves 4 stories + reduces LLM orchestration complexity
- **Rationale:** Separation is convenience, not core ML value. Users can type individual thoughts.

**Epic 4: Semantic Organization (Circles of Care)**
- **Current:** 4-5 stories (models, clustering, naming, UI, graph)
- **Proposed:** **STREAMLINE to 1-2 stories** - Focus on core circle organization + care/intention/action hierarchy
- **Impact:** Keep ML differentiation (K-means, LLM naming, embeddings) but simplify implementation
- **Priority:** **HIGH** - This is the core product value

**Epic 5: Personalized Discovery**
- **Current:** 4 stories (taste learning, recommendations, API, iOS UI)
- **Proposed:** **REMOVE ENTIRE EPIC** - Defer to "Circles of Care v2"
- **Impact:** Saves 4 stories
- **Rationale:** Discovery is "nice to have". Core value is organization (circles) + retrieval (chat).

**Epic 6: RAG-Powered Personal Chat**
- **Current:** 4 stories (RAG service, streaming, confidence fallback, iOS chat UI)
- **Proposed:** **KEEP but STREAMLINE to 1 story** - Core RAG chat only
- **Impact:** Essential ML demo feature (vector search + LLM)
- **Priority:** **HIGH** - Shows ML capability for recruiting

### Story Impact Summary

| Epic | Original Stories | Proposed | Change |
|------|------------------|----------|--------|
| Epic 1 | 7 | 7 | ✅ Done |
| Epic 2 | 7 | 6 (remove 2.7) | -1 story |
| Epic 3 | 4 | 0 (remove all) | -4 stories |
| Epic 4 | 5 | 1-2 (streamline) | -3 stories |
| Epic 5 | 4 | 0 (remove all) | -4 stories |
| Epic 6 | 4 | 1 (streamline) | -3 stories |
| **TOTAL** | **31 stories** | **15-16 → 4-5 MVP** | **-15+ stories** |

### Artifact Conflicts

**PRD (Product Requirements Document):**
- ❌ **Remove:** FR3 (Voice Input), FR4 (Call Agents Separation), FR9-10 (Discover Mode)
- ✅ **Keep:** FR1 (Auth), FR2 (Text Capture), FR5-6 (Circles), FR7-8 (Chat), FR11-14 (ML modes)
- **MVP Redefined:** Text capture + Circles (semantic organization) + Chat (RAG) only

**Architecture Document:**
- **NO MAJOR CHANGES** - Architecture supports reduced scope
- **Remove Sections:** "iOS Speech Recognition", "Call Agents Mode API", "Discover Mode"
- **Keep:** All ML pipeline (embeddings, FAISS, LLM, clustering), backend structure, iOS MVVM

**UI/UX Specifications:**
- **Remove:** Voice capture UI (microphone button, recording indicator, permission flow)
- **Remove:** "Separate & Save" UI flow
- **Remove:** Discover Mode screens
- **Keep:** Text capture, Circles views, Chat interface
- **Simplified:** Navigation (3 tabs instead of 5: Capture, Circles, Chat)

**Technical Impact:**
- **Code Removal:** Speech recognition code, LLM separation service, discovery algorithms
- **Test Removal:** CaptureViewModelSpeechTests.swift, separation tests, discovery tests
- **API Changes:** Remove `/ml/separate-somethings`, `/ml/discover`, `/ml/link`, `/ml/prioritize` endpoints
- **Database:** Keep all tables (circles, intentions, actions) - no schema changes needed

---

## Section 3: Recommended Approach

### Path Forward: **Hybrid (Rollback + Scope Reduction)**

**Selected Strategy:** Rollback Story 2.7 + Radical MVP Scope Reduction

**Justification:**

1. **Timeline Impact:** Reduces 25+ stories → 4-5 stories **(5x faster to MVP)**
2. **Technical Risk:** **LOWER** - Simpler system, no voice complexity, no separation orchestration
3. **Team Momentum:** **POSITIVE** - Clear finish line, achievable in 1-2 weeks, recruiting-ready demo
4. **Long-term Sustainability:** **BETTER** - Stable text capture, proven ML features, clean codebase for v2
5. **Business Value:** **HIGHER for recruiting** - ML differentiation (circles, chat, predictions) > input methods (voice, separation)

**Trade-offs Considered:**

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| Keep Current Plan (25+ stories) | Complete feature set | Takes months, misses recruiting timeline | ❌ Rejected |
| Incremental Reduction (10-15 stories) | Some scope reduction | Still too many stories for < 5 target | ❌ Rejected |
| **Radical Reduction (4-5 stories)** | **Fast to MVP, clear focus, ML showcase** | **Defers voice, separation, discovery** | **✅ RECOMMENDED** |

---

## Section 4: Detailed Change Proposals

### 4.1 Git Revert Plan

**Target State:** Revert to commit **bce33b6** "Implement Story 2.4: Somethings CRUD API Endpoints (with Code Review Fixes)"

**Reason:** Last stable commit before Story 2.7 work. Story 2.4 completed successfully with comprehensive tests and code review.

**Steps:**

```bash
# 1. Confirm current state
git status
git log --oneline -5

# 2. Revert Story 2.7 changes (if not committed separately, use reset)
git reset --hard bce33b6

# 3. Remove untracked Story 2.7 files
git clean -fd

# 4. Manually remove test file
rm ios/Pookie/PookieTests/CaptureViewModelSpeechTests.swift

# 5. Commit revert
git add -A
git commit -m "Revert Story 2.7 (voice capture) - scope reduction for recruiting MVP

- Remove voice capture implementation
- Remove speech recognition tests
- Defer voice input to Circles of Care v2
- Focus MVP on core ML features (circles + chat)
"

# 6. Update sprint status
# (Will be done as part of this workflow)
```

**Files Affected:**
- ✅ Revert: `ios/Pookie/Pookie/ViewModels/CaptureViewModel.swift` (remove speech code)
- ✅ Revert: `ios/Pookie/Pookie/Views/Capture/CaptureView.swift` (remove microphone button)
- ❌ Delete: `ios/Pookie/PookieTests/CaptureViewModelSpeechTests.swift`
- ✅ Update: `docs/sprint-artifacts/2-7-*.md` (mark as deferred)

### 4.2 Epic Structure Changes

**OLD Epic Structure (31 stories):**
```
Epic 1: Foundation (7 stories) ✅ DONE
Epic 2: Capture (7 stories) ✅ DONE (after 2.7 removal)
Epic 3: Separation (4 stories) 📋 BACKLOG
Epic 4: Circles (5 stories) 📋 BACKLOG
Epic 5: Discovery (4 stories) 📋 BACKLOG
Epic 6: Chat (4 stories) 📋 BACKLOG
```

**NEW MVP Structure (4-5 stories):**
```
✅ Foundation Complete (Epic 1: 7 stories)
✅ Capture Complete (Epic 2: 6 stories, removed 2.7)

📋 MVP Remaining (Epic MVP: 4-5 stories):

Story MVP-1: Implement Circles Semantic Organization
  - Backend: Circle model, K-means clustering, LLM naming, care/intention/action models
  - iOS: Circle list view, basic hierarchy display (circles → intentions → actions)
  - AC: Users see somethings auto-organized into circles with intentions/actions

Story MVP-2: Implement RAG Chat with Pookie
  - Backend: FAISS search integration + Claude streaming via OpenRouter
  - iOS: Chat interface with SSE event handling
  - AC: Users can ask questions and get RAG-augmented answers from their somethings

Story MVP-3: Connect Circles to Chat (Context Integration)
  - Backend: Include circle context in RAG prompts
  - iOS: Show which circles were used in chat response
  - AC: Chat responses reference user's circle organization

Story MVP-4: Polish & Testing
  - Fix bugs from MVP-1, MVP-2, MVP-3
  - Add error handling and loading states
  - End-to-end testing (capture → circles → chat flow)
  - AC: Stable MVP demo ready for recruiting

Story MVP-5: Deploy & Documentation (OPTIONAL - can be manual)
  - Backend deployment to Render
  - iOS TestFlight build
  - README with screenshots and demo flow
  - AC: Deployed MVP accessible for recruiting demos

TOTAL: 4-5 stories

🚫 DEFERRED to "Circles of Care v2":
  - Story 2.7: Voice capture (with Speech Recognition)
  - Epic 3: Call Agents separation mode (all 4 stories)
  - Epic 5: Discover mode recommendations (all 4 stories)
  - Story page / timeline visualization
```

### 4.3 Specific Artifact Updates

**File:** `docs/epics.md`

**Change 1 - Epic 2 Summary:**
```diff
## Epic 2 Summary

Stories Created: 7 stories
+ Stories Remaining: 6 stories (2.7 removed)
FR Coverage:
- FR2 (Something Capture - Text Input) ✅
- FR3 (Something Capture - Voice Input) ❌ Deferred to v2
+ - Voice input removed from MVP scope
```

**Change 2 - Epic 3 Status:**
```diff
## Epic 3: AI-Powered Something Separation (Call Agents Mode)

+ **STATUS: REMOVED FROM MVP - Deferred to Circles of Care v2**
+
+ **Rationale:** Separation is a convenience feature that does not contribute to core ML
+ differentiation. Users can type individual thoughts directly. Removing this epic saves
+ 4 stories and reduces LLM orchestration complexity while maintaining focus on semantic
+ organization (circles) and retrieval (chat).

Epic Goal: Enable users to paste messy brain dumps...
```

**Change 3 - Epic 5 Status:**
```diff
## Epic 5: Personalized Discovery

+ **STATUS: REMOVED FROM MVP - Deferred to Circles of Care v2**
+
+ **Rationale:** Discovery mode is a "nice to have" feature. Core ML value is demonstrated
+ through circle organization and RAG chat. Removing this epic saves 4 stories.

Epic Goal: Enable users to get actionable recommendations...
```

**File:** `docs/architecture.md`

**Change 1 - Functional Requirements:**
```diff
1. **Capture & Thought Separation (Call Agents Mode)**
   - Text/voice input for brain dumps
   - AI-powered semantic boundary detection to separate distinct thoughts
+  **MVP: Text input only. Voice and separation deferred to Circles of Care v2.**

2. **Semantic Clustering (Circles)**
   - Automatic grouping of related thoughts into thematic "circles" using vector similarity
+  **MVP: Core feature - kept with streamlined implementation**
```

**Change 2 - API Endpoints:**
```diff
## API Endpoints Summary

- **8 Total Actions** (4 ML Operations + 1 Chat + 3 CRUD):
+ **5 MVP Actions** (2 ML Operations + 1 Chat + 2 CRUD):

| Action | Endpoint | MVP Status |
|--------|----------|------------|
- | Separate Thoughts | /ml/separate-thoughts | POST |
- | Discover | /ml/discover | POST |
- | Link | /ml/link | POST |
- | Prioritize | /ml/prioritize | POST |
+ | RAG Chat | /chat/stream | POST | ✅ MVP |
+ | List Circles | /circles | GET | ✅ MVP |
```

**File:** `docs/sprint-artifacts/sprint-status.yaml`

**Complete replacement of backlog section:**
```yaml
development_status:
  # ... Epic 1 & 2 (unchanged) ...

  # Story 2.7 - REMOVED
  2-7-implement-voice-capture-with-ios-speech-recognition: removed-deferred-to-v2

  # Epic 3 - REMOVED
  epic-3: removed-deferred-to-v2
  3-1-implement-llm-service-with-openrouter-integration: removed-deferred-to-v2
  3-2-create-something-separation-api-endpoint: removed-deferred-to-v2
  3-3-create-batch-something-creation-endpoint: removed-deferred-to-v2
  3-4-build-ios-separate-and-save-ui: removed-deferred-to-v2
  epic-3-retrospective: removed-deferred-to-v2

  # Epic MVP - NEW COMPRESSED BACKLOG
  epic-mvp: ready-for-dev
  mvp-1-implement-circles-semantic-organization: backlog
  mvp-2-implement-rag-chat-with-pookie: backlog
  mvp-3-connect-circles-to-chat-context: backlog
  mvp-4-polish-and-testing: backlog
  mvp-5-deploy-and-documentation: backlog
  epic-mvp-retrospective: optional

  # Epic 4 - MERGED INTO MVP
  epic-4: merged-into-mvp

  # Epic 5 - REMOVED
  epic-5: removed-deferred-to-v2
  5-1-implement-taste-profile-analysis-service: removed-deferred-to-v2
  5-2-implement-recommendation-generation-with-rag-llm: removed-deferred-to-v2
  5-3-create-discover-api-endpoint: removed-deferred-to-v2
  5-4-build-ios-discover-view-with-recommendation-ui: removed-deferred-to-v2
  epic-5-retrospective: removed-deferred-to-v2

  # Epic 6 - MERGED INTO MVP
  epic-6: merged-into-mvp
```

---

## Section 5: Implementation Handoff

### Change Scope Classification: **MAJOR**

**Requires:** Scrum Master + Product Manager approval and coordination

**Handoff Recipients:**

1. **Development Team (Dev Agent)**
   - Execute git revert (Story 2.7 removal)
   - Implement MVP-1 through MVP-4 stories
   - Follow new compressed epic structure

2. **Scrum Master / Product Owner**
   - Update sprint status (sprint-status.yaml)
   - Update epics.md with removals and deferrals
   - Communicate "Circles of Care v2" roadmap for deferred features

3. **Product Manager / Solution Architect**
   - Update PRD to reflect new MVP scope
   - Approve architecture simplifications
   - Define "Circles of Care v2" feature set (voice, separation, discovery, story page)

### Responsibilities

**Dev Agent:**
- ✅ Execute git revert to commit bce33b6
- ✅ Remove CaptureViewModelSpeechTests.swift
- ✅ Mark Story 2.7 as "removed-deferred-to-v2" in sprint status
- ✅ Implement MVP stories sequentially (MVP-1 → MVP-2 → MVP-3 → MVP-4)

**Scrum Master (current agent):**
- ✅ Update sprint-status.yaml with new MVP structure
- ✅ Update epics.md with removal/deferral notes
- ✅ Document this change in sprint change proposal

**Product Manager:**
- ⏳ Approve MVP scope reduction
- ⏳ Define "Circles of Care v2" feature priorities
- ⏳ Update recruiting demo script to focus on circles + chat

### Success Criteria

**MVP Complete When:**
1. ✅ Users can capture somethings via text (Story 2.6)
2. ✅ Somethings auto-organize into circles via K-means clustering (MVP-1)
3. ✅ Users see care → intention → action hierarchy (MVP-1)
4. ✅ Users can chat with Pookie using RAG over their somethings (MVP-2)
5. ✅ Chat responses include circle context (MVP-3)
6. ✅ No critical bugs, stable demo (MVP-4)
7. ✅ Deployed to Render + TestFlight (MVP-5 - optional)

**Timeline Estimate:**
- MVP-1: 2-3 days (circles + hierarchy implementation)
- MVP-2: 2-3 days (RAG chat)
- MVP-3: 1 day (context integration)
- MVP-4: 1-2 days (polish + testing)
- MVP-5: 1 day (deployment - can be manual)

**Total:** 7-10 days → **Recruiting-ready in 1.5-2 weeks**

---

## Section 6: Risk Assessment & Mitigation

### Risks

**Risk 1: Deferred features needed for recruiting demo**
- **Likelihood:** LOW
- **Impact:** MEDIUM
- **Mitigation:** Validate with user that circles + chat are sufficient for ML showcase. Voice/separation/discovery are "nice to have" not "must have".

**Risk 2: Circle organization complexity underestimated**
- **Likelihood:** MEDIUM
- **Impact:** MEDIUM
- **Mitigation:** K-means clustering is well-established. Architecture already has embedding service + FAISS. Can use simpler clustering first (DBSCAN fallback).

**Risk 3: Git revert causes merge conflicts**
- **Likelihood:** LOW
- **Impact:** LOW
- **Mitigation:** Story 2.7 is isolated (speech recognition code). Revert is clean. Test after revert to ensure 2.6 still works.

**Risk 4: User expectations mismatch (wants all features)**
- **Likelihood:** LOW
- **Impact:** HIGH
- **Mitigation:** User explicitly stated "finish in < 5 stories" and identified ML features as core. Clear communication about "Circles of Care v2" roadmap.

### Confidence Level

**Overall Confidence:** **HIGH** (85%)

**Reasoning:**
- Clear user directive for scope reduction
- Well-defined revert point (commit bce33b6)
- Compressed MVP aligns with stated core features (circles, chat, ML)
- Architecture supports reduced scope (no major changes needed)
- Simpler system = lower risk, faster delivery

---

## Appendices

### Appendix A: Change Summary Table

| Artifact | Section | Change Type | Details |
|----------|---------|-------------|---------|
| Git History | Story 2.7 | REVERT | Revert to commit bce33b6 |
| epics.md | Epic 2 | MODIFY | Remove Story 2.7, update summary |
| epics.md | Epic 3 | REMOVE | Mark entire epic as deferred to v2 |
| epics.md | Epic 4 | STREAMLINE | Merge into MVP-1 |
| epics.md | Epic 5 | REMOVE | Mark entire epic as deferred to v2 |
| epics.md | Epic 6 | STREAMLINE | Merge into MVP-2 |
| epics.md | NEW MVP | ADD | Create Epic MVP with 4-5 stories |
| architecture.md | Functional Reqs | MODIFY | Mark voice/separation/discovery as v2 |
| architecture.md | API Endpoints | MODIFY | Remove 3 endpoints from MVP |
| sprint-status.yaml | Backlog | REPLACE | New MVP structure, mark removals |
| Code | CaptureViewModel | REVERT | Remove speech recognition code |
| Code | CaptureView | REVERT | Remove microphone UI |
| Tests | SpeechTests | DELETE | Remove CaptureViewModelSpeechTests |

### Appendix B: "Circles of Care v2" Deferred Features

**Post-MVP Roadmap:**

**Version 2 Features:**
1. Voice Capture (Story 2.7)
   - iOS Speech Recognition
   - Real-time transcription
   - Permission handling

2. Call Agents Mode (Epic 3)
   - AI thought separation
   - Batch creation
   - Preview UI

3. Discover Mode (Epic 5)
   - Taste profile learning
   - Action recommendations
   - RAG + LLM synthesis

4. Story Page Timeline
   - Visual timeline of actions
   - Progress tracking
   - Reflection prompts

5. Advanced Features
   - Multi-circle assignment UI
   - Graph visualization
   - Offline sync

### Appendix C: Compressed MVP Feature Set

**What MVP Delivers:**

✅ **Foundation (Epic 1 - Complete)**
- User authentication (Supabase)
- Database schema (PostgreSQL)
- Backend API structure (FastAPI)
- iOS app structure (SwiftUI + MVVM)

✅ **Capture (Epic 2 - Complete after 2.7 removal)**
- Text input for somethings
- Embedding generation (sentence-transformers)
- FAISS vector index
- API endpoints for CRUD

✅ **Circles (MVP-1)**
- K-means clustering on embeddings
- LLM-generated circle names
- Care → Intention → Action hierarchy
- iOS circle list and detail views

✅ **Chat (MVP-2 + MVP-3)**
- RAG-powered chat with FAISS search
- Claude Haiku LLM integration
- SSE streaming for real-time responses
- Circle context in chat prompts
- iOS chat interface

✅ **Polish (MVP-4)**
- Bug fixes
- Error handling
- End-to-end testing

**Recruiting Demo Flow:**
1. Sign up / Log in
2. Capture 5-10 somethings via text
3. View circles (auto-organized by ML)
4. Chat with Pookie ("What do I care about?")
5. See RAG-augmented response using personal knowledge

**Demo Highlights:**
- 🤖 ML clustering (K-means on 384-dim embeddings)
- 🤖 LLM naming (OpenRouter for circle names)
- 🤖 Vector search (FAISS similarity)
- 🤖 RAG chat (retrieval-augmented generation)
- 🤖 Semantic understanding (sentence-transformers)

**Technical Showcase:**
- Dual-platform (iOS SwiftUI + Python FastAPI)
- Modern ML stack (sentence-transformers, FAISS, Claude)
- Free-tier architecture (~$0-3/month)
- Production patterns (JWT auth, SQLAlchemy, async/await)

---

## Approval & Sign-off

**Proposed By:** Scrum Master Agent (Correct Course Workflow)
**Date:** 2025-12-07
**Review Status:** ⏳ Pending user approval

**User Approval Required:**
- [ ] Approve git revert (Story 2.7 removal)
- [ ] Approve epic removals (Epic 3, Epic 5)
- [ ] Approve compressed MVP (4-5 stories)
- [ ] Approve "Circles of Care v2" roadmap for deferred features

**Next Steps After Approval:**
1. Execute git revert to commit bce33b6
2. Update sprint-status.yaml
3. Update epics.md with removal/deferral notes
4. Begin MVP-1 implementation (Circles)

---

**End of Sprint Change Proposal**
