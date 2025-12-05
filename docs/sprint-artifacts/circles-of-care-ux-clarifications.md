# Circles of Care - UX Clarifications (2025-12-05)

## Critical UX Design Decisions

These clarifications refine the Circles of Care implementation details based on user vision.

---

## 1. Interactive ML - Circle Name Learning

**Requirement:** FAISS clustering should learn from user feedback on circle names.

**User Flow:**
- Pookie suggests circle name via LLM
- User can:
  - Accept suggestion
  - **X (reject) suggestion** → System learns this was wrong
  - **Add own name** → System learns user's preferred naming

**Implementation Impact:**
- Epic 4 (Circles) needs feedback loop
- Store user corrections/preferences
- Retrain or adjust clustering based on feedback
- Improve circle naming accuracy over time

**Technical Approach:**
- Track accepted vs rejected suggestions
- Use user-provided names as training signal for future LLM naming prompts
- Potentially adjust FAISS clustering parameters based on user reorganization patterns

---

## 2. Voice Memo = Voice-to-Text

**Requirement:** Voice input automatically transcribes to text, not stored as audio.

**User Flow:**
- User taps 🎤 button
- Records voice memo
- **iOS native voice recognition** converts to text
- Stored as text in `thoughts` table (same as typed capture)

**Implementation Impact:**
- Epic 2 (Capture) - Story 2.1
- Use iOS native `SFSpeechRecognizer` (free, no API cost)
- No audio file storage needed
- No transcription API calls (Whisper, etc.)

**Benefits:**
- Zero cost (free-tier compatible)
- Immediate text for embedding generation
- Searchable/queryable like any other capture
- Smaller storage footprint

---

## 3. Intentions Visual UX - Circle Overview

**Requirement:** When creating intention, show visual overview of the source circle.

**User Flow:**
1. User browses Circles view (L1)
2. Sees "Beauty" circle with 8 cares
3. Thinks: "I want to work on skincare routine"
4. Taps [↑] "Up arrow" button
5. **Chamber zooms out** → Shows visual circle representation:
   ```
   ┌─────────────────────────────────┐
   │   CREATE INTENTION              │
   ├─────────────────────────────────┤
   │                                 │
   │   ⭕ Beauty                      │
   │   • • • • • • • •               │
   │   (8 cares)                     │
   │                                 │
   │   Type intention:               │
   │   "Build skincare routine"      │
   │                                 │
   │   [Create]                      │
   └─────────────────────────────────┘
   ```
6. User writes intention text
7. Adds cares as roots (starting with Beauty circle, but can add from any)

**Visual Design:**
- **Circle labeled with name** (e.g., "Beauty")
- **Dots representing individual cares** (visual scatter)
- **Zoomed-out aesthetic** - gives context of where intention originated
- Starting point for linking cares, but not restrictive

**Implementation Impact:**
- Epic 4 - New Story: "Intention Creation UI with Circle Visualization"
- SwiftUI canvas for circle visualization
- Simple scatter plot of dots representing cares
- Animation: zoom out from circles list → intention creation view

**Intentional Simplicity:**
- Intentions have **no complex metadata**
- Just: `intention_text`, `status`, `created_at`
- Visual focuses on the **circle of origin** for context

---

## 4. Search Captures for Intentions

**Requirement:** LLM-assisted search at Intentions level to remember why you want to do something.

**User Flow:**
- User in Intentions view
- Looking at intention: "Hit the gym regularly"
- Wants to remember: "Why did I create this?"
- **Search bar:** "Why gym?"
- **LLM search** queries linked captures (roots) + all captures
- Returns: "You saved 5 fitness reels about muscle building and 2 articles about health benefits"

**Purpose:**
- **Connect the dots** - understand motivation behind intentions
- Surface the cares that led to the intention
- Jog memory of scattered inputs

**Implementation:**
- Epic 4 - New Story: "LLM-Assisted Capture Search for Intentions"
- Simple DB query (small dataset, <100k captures)
- LLM semantic understanding of search query
- Return relevant captures with context

**Technical Approach:**
```python
# Pseudocode
def search_captures_for_intention(intention_id, query):
    # Get linked cares (roots)
    linked_cares = get_intention_cares(intention_id)

    # Get all user captures
    all_captures = get_user_captures(user_id)

    # LLM semantic search
    relevant = llm_search(query, all_captures + linked_cares)

    return relevant
```

**Why Easy:**
- Small DB (personal use, <100k thoughts)
- No need for complex vector search (can use LLM directly)
- Just query DB + LLM understanding

---

## 5. Complete Capture → Circles → Intentions → Actions → Story Flow

**Confirmed Flow:**

```
CAPTURE (L0)
📝 Voice memo → Voice-to-text → Stored as text

CIRCLES (L1)
🔵 FAISS clusters captures
   Pookie suggests name → User accepts/rejects/modifies
   System learns from feedback

INTENTIONS (L2)
[↑] Up arrow from circle
   → Show circle visualization (zoomed out, dots, label)
   → Write intention text
   → Link individual captures as roots
   → Search captures to remember "why"

ACTIONS
Toggle intentions ON/OFF
Attach specific actions

STORY (L3)
Completed actions logged
Build narrative over time
```

---

## Implementation Priorities

### Story 1.3 (Immediate - Ready to Execute)
- Database schema with intentions, intention_cares, stories tables ✅
- No changes needed from these clarifications

### Epic 2 (Capture)
- **Update Story 2.1:** Voice-to-text using iOS SFSpeechRecognizer
- No audio storage needed

### Epic 4 (Circles → Intentions)
- **New Story 4.X:** Interactive ML - Learn from circle name feedback
- **New Story 4.Y:** Intention creation UI with circle visualization
- **New Story 4.Z:** LLM-assisted capture search for intentions view

### Epic 5 (Discover Mode)
- Vibe profile generation (unchanged)

### Epic 6 (RAG Chat)
- Chat with Pookie (unchanged)

---

## Success Criteria Updates

**User can:**
- ✅ Record voice memo → automatically transcribed to text
- ✅ X Pookie's circle name suggestions → system learns
- ✅ See visual circle overview when creating intention
- ✅ Search captures from intentions view to remember "why I care"
- ✅ Connect the dots between scattered inputs and action goals

---

## Notes for Future Implementation

**FAISS Learning:**
- Track user corrections (accepted/rejected/modified circle names)
- Use as training signal for future clustering
- Store user preferences in DB

**Voice-to-Text:**
- iOS SFSpeechRecognizer (free, no API cost)
- Real-time transcription during recording
- Error handling for recognition failures

**Circle Visualization:**
- SwiftUI scatter plot of dots
- Animation: zoom out transition
- Label with circle name
- Simple aesthetic (not complex graph)

**LLM Search:**
- Simple implementation (small DB)
- Query all captures + linked cares
- Return relevant context for intention

---

**Status:** Ready for implementation
**Next Step:** Execute Story 1.3 → Database schema creation
