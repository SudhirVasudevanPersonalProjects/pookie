---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments: ['docs/analysis/brainstorming-session-2025-12-02.md']
workflowType: 'product-brief'
lastStep: 5
project_name: 'Pookie'
user_name: 'sudy'
date: '2025-12-02'
---

# Product Brief: Circles of Care

**Date:** 2025-12-02 (Updated: 2025-12-05 - Evolved from "Pookie" to "Circles of Care")
**Author:** sudy

**Purpose:** Internal planning document for development. This is my personal project - built for me, by me - to solve my scattered thoughts problem and give me control over my attention. Not a business venture, just a portfolio piece that proves I can build production ML systems with agentic capabilities.

---

## Executive Summary

I built Circles of Care because I had a problem that no existing tool could solve: my brain dumps ideas everywhere, care can't find expression, and I lose control of my attention in the chaos.

**The Problem I Faced:**
Screenshots I never look at. Notes that make sense in the moment but are gibberish later. Long rambling paragraphs with 5 different thoughts mixed together. Bookmarks, links, half-formed ideas scattered across a dozen apps. I tried productivity tools - they made it worse. I tried journaling apps - they wanted perfect prose. I tried note-taking apps - they gave me folders and tags but no *understanding*. Most critically: I had no system to turn what I care about into what I actually do.

**What I Built:**
Circles of Care is the **attention controller for my phone** - an app that gives me systematic control over my attention guided by what I actually care about. Pookie lives inside as my AI companion, learning how MY mind works and helping me navigate from scattered captures to coherent action.

**How It Works - The Complete Action Loop:**
1. **Capture:** I dump raw thoughts (text/voice) without organization
2. **Circles (L1):** AI clusters related captures into thematic circles with semantic embeddings
3. **Intentions (L2):** I glance through circles, think "I want to do this" → up arrow → create intention
   - Link individual captures as "roots" feeding the intention (multi-care → one intention)
   - Visual: Arrow thickness = number of linked cares (stream of energy)
4. **Actions:** Outside Chamber, I toggle intentions, attach specific actions to them
5. **Story Timeline:** Completed actions get logged, building my narrative over time

**Core Features:**
- **Chamber:** 4-level hierarchy (L0 unorganized → L1 circles → L2 intentions → L3 story)
- **Pookie (AI Companion):** Suggests circles, separates thoughts, learns my vibe profile
- **Call Agents Mode:** Paste rambling paragraphs → AI automatically separates distinct thoughts
- **Discover Mode:** Intention-based recommendations powered by vibe profile
- **RAG Chat:** Personal knowledge assistant with full context (circles + intentions + vibe)

**Why It Matters (For My Career):**
This demonstrates end-to-end ML system design with agentic capabilities: RAG pipeline, multi-agent orchestration, vector search, embeddings, intention-driven architecture - all on free tiers (~$0-3/month) to prove technical efficiency. It's not a tech demo; it's solving my real problem (care → action) with production-grade architecture.

---

## Core Vision

### The Problem I'm Solving

I care about a lot of things. I have ideas constantly. But they scatter - across apps, screenshots, voice memos, random notes. When I try to capture them:

- **They're messy:** Long paragraphs mixing 5 different thoughts
- **They disappear:** Saved but never revisited, lost in the noise
- **They're disconnected:** Can't see patterns between related ideas
- **They're generic:** Productivity apps don't understand MY context

I tried existing solutions:
- **Notion, Obsidian:** Too complex, required manual organization I'd abandon
- **Things, Todoist:** Task-focused, didn't capture *why* I cared
- **Day One, Reflect:** Wanted polished writing, not brain dumps
- **ChatGPT:** Generic responses, no memory of my unique context

**What was missing:** An AI that actually learns ME. My patterns, my taste, my way of thinking.

### My Solution: Circles of Care

Circles of Care is my **attention controller** - an app that gives me systematic control over what I care about and turns it into action. Pookie lives inside as my AI companion, learning how my mind works.

**The Complete Action Loop:**

**1. Capture (Level 0: Raw Input)**
- I paste messy paragraphs, screenshots, voice memos - anything
- **Call Agents Mode:** AI agents identify semantic boundaries and separate thoughts automatically
- I chat with Pookie: "split that differently" or "combine these"
- Brain dump chaos → structured captures

**2. Circles (Level 1: Thematic Clustering)**
- Vector embeddings find patterns I don't see
- "Fitness" captures naturally cluster together
- "Career ideas" emerge as a theme
- Pookie suggests circle names, I can X them or add my own
- Machine learning does the organizing, not me

**3. Intentions (Level 2: Action-Oriented Goals)**
- I glance through circles and think "ooh, I want to do this"
- I "up arrow" the Chamber → type my intention → creates an Intention object
- **Critical:** I link **individual captures** (not just whole circles) as "roots" feeding the intention
  - Example: 5 fitness reels + 2 workout articles → "Hit the gym" intention
  - Multiple cares from different circles → one intention
  - Visual: Arrow thickness = number of linked cares (stream of energy)
- Intentions exist **outside the Chamber** as a separate actionable list

**4. Actions (Intention → Execution)**
- I toggle intentions on/off
- I attach specific actions to each intention
- I complete actions in the real world

**5. Story Timeline (Level 3: Completion Log)**
- Completed actions get logged automatically
- Builds my narrative over time
- Separate list showing what I've actually done

**The Chamber: 4-Level Hierarchy**
- **L0:** Unorganized captures (raw input)
- **L1:** Circles (semantic clusters of related cares)
- **L2:** Intentions (action-oriented goals with multi-care roots)
- **L3:** Story (completion log of actions)

**Core AI Features:**

**1. Pookie (AI Companion)**
- Suggests circle names and clustering
- Separates messy thoughts in Call Agents Mode
- Learns my vibe profile from what I care about
- Guides me through the Chamber

**2. Discover Mode (Intention-Based Recommendations)**
- AI learns MY taste from circles and intentions
- Recommends new content aligned with my active intentions
- Powered by vibe profile (aggregated preference vector)
- Not algorithmic engagement bait - genuinely personalized

**3. RAG-Powered Chat**
- Ask "what was that idea I had about...?" → it finds it
- Understands my full context (circles + intentions + vibe profile)
- Not generic ChatGPT - truly my external brain

**4. Multi-Agent System**
- Tag Agent: Categorizes automatically
- Reflection Agent: Generates insights
- Novelty Ranker: Identifies what's actually important

### Why This Approach Works

**It's built for ME:**
- Learns my patterns through embeddings and corrections
- Understands my context through RAG (circles + intentions + vibe profile)
- Adapts to my way of thinking, not forcing me into a system
- **Closes the action loop:** Care → Intention → Action → Story (not just capture)

**It's technically impressive:**
- Full RAG pipeline with vector search
- Multi-agent orchestration
- Interactive ML (learns from my feedback)
- Intention-driven architecture with many-to-many care linking
- Free-tier architecture proving efficiency

**It solves a real problem:**
- Not a tech demo - genuinely useful for my life (attention control)
- Proves product thinking alongside technical skill
- Demonstrates agentic capabilities (Pookie as AI companion)

### Key Differentiators

**What makes Circles of Care unique:**

1. **Attention controller, not task manager:** Systematic control over what I care about → what I do
2. **Complete action loop:** Capture → Circles → Intentions → Actions → Story (not just notes)
3. **Multi-care intention linking:** Link individual captures as "roots" feeding intentions (visual: arrow thickness)
4. **Personalized AI companion (Pookie):** Not generic productivity advice - learns my actual patterns and vibe
5. **Automatic thought separation:** Call Agents Mode solves the "messy brain dump" problem
6. **Intention-based discovery:** Recommendations aligned with my active intentions, not engagement metrics
7. **True RAG with context:** Knows my knowledge landscape (circles + intentions + vibe profile)
8. **Interactive ML:** Gets smarter from my corrections and feedback
9. **Free-tier proof:** Shows I can build production ML systems with agentic capabilities on a budget
10. **Built for myself:** Solving my real problem (scattered care → coherent action), not a generic use case

---

## Target Users

### Primary User: The Overthinking Young Adult (Me)

**Who I Am (And People Like Me):**
- **Age:** 18-28 (college through early career)
- **Context:** Lost, directionless, figuring out what I actually want in life
- **Core trait:** I care deeply about MANY things - diverse interests, wide-ranging taste
- **The paradox:** I overthink not because I'm anxious, but because I care so much about so many things

**The Problem I Experience:**
- **Overthinking → paralysis:** I care about too many things at once, can't decide what to focus on
- **Can't translate care → action:** I have motivation and energy, but it dissipates before I do anything
- **No clarity:** I struggle to answer "what do I actually care about?" and "why do I care about this?"
- **No meaning:** My cares feel scattered - they don't connect into a coherent sense of who I am

**My Current Reality:**
- I have ideas constantly, save links and screenshots, start projects and abandon them
- I unlock my phone looking for direction but end up doom-scrolling
- I know I care about things but can't articulate what or why
- I make lists, take notes, bookmark articles - then never look at them again
- The caring itself becomes a burden when it can't find expression through action

**What I Need from Circles of Care:**

**1. Understand What I Care About**
- Externalize the invisible act of caring
- See patterns in my scattered interests
- "Here's what you actually care about" (circles showing my real priorities)

**2. Understand WHY I Care**
- Make sense of my motivations
- Connect cares to deeper reasons
- Build self-knowledge through reflection

**3. Discover Actions Based on My Cares**
- **Content discovery actions:** "Watch this movie" "Listen to this song" (taste-based, immediate)
- **Goal-aligned actions:** "You care about getting jacked → Hit the gym" "You care about piano → Practice 30min"
- Turn caring into doing, not just consuming or overthinking

**4. Create Meaning Through Action**
- Cares → Actions → Story (building coherent identity)
- See how my actions connect to what I care about
- Feel like I'm building a meaningful life, not just reacting to algorithms

**What Success Looks Like for Me:**
- I can confidently answer "what do you care about?" when asked
- I make decisions faster because I understand my priorities
- **I ACT more** - caring leads to doing, not endless overthinking
- I feel coherent - my cares connect into a meaningful story of who I'm becoming
- My phone becomes a tool for focus and action, not a source of chaos

### Secondary Users

**N/A for MVP** - Circles of Care is built for me and people like me. I'm not trying to solve for multiple user types yet. If this works for overthinking young adults who care deeply, that's the validation I need.

### User Journey

**Discovery:**
I find Circles of Care because I built it. But others like me would find it through:
- Word of mouth from friends who struggle with the same overthinking
- Looking for "attention control" or "care-based productivity"
- Searching for solutions to "I have too many interests" or "can't focus"

**First Experience:**
- I dump a messy brain dump into Circles of Care
- Call Agents Mode separates my thoughts automatically - "whoa, it understood what I meant"
- I see my first circle form - "oh, THAT'S what I care about"
- I create my first intention by "up arrowing" from a circle - "wait, this feels like taking control"
- Aha moment: "This actually gets how my mind works AND helps me act"

**Core Usage (Daily):**
- Morning: Check Intentions list - "what am I working toward today?"
- Throughout day: Quick captures when ideas hit (voice note, screenshot, link)
- Evening: Review circles, see what emerged, create new intentions for things I want to act on
- Call Agents Mode when I have rambling thoughts that need separation
- Complete actions, watch Story timeline build my narrative

**Success Moment:**
- Week 2: Someone asks "what do you care about?" and I can actually answer
- Month 1: I notice I'm DOING more, not just thinking about doing - my Intentions list drives my day
- Month 3: I look at my Story timeline and see a coherent narrative emerging from completed actions

**Long-term:**
- Pookie (AI companion) becomes my external brain - I trust it to hold my thoughts
- Intentions list becomes my default for "what should I do next?"
- I stop overthinking because I have a system that turns care into action
- My cares feel meaningful because they lead to intention → action → story

---

## Success Metrics

### Personal Success (Subjective)

**The Core Question: "Am I living in flow?"**

**How I'll Know Circles of Care Is Working:**

**1. I Feel Like I'm Acting, Not Overthinking**
- Most days feel like flow days, not paralysis days
- When I unlock my phone, I check my Intentions list (not aimless scrolling)
- I'm DOING things that matter to me (actions flowing from intentions)

**2. I Can Answer "What Do You Care About?"**
- When someone asks, I have a real answer (not "idk, lots of things")
- My cares feel clear (organized in circles), not scattered
- I understand why I care about what I care about

**3. Overthinking Decreases**
- I notice myself overthinking less
- Cares don't rot into anxiety because they turn into intentions → actions → story
- Decision paralysis happens less often

**4. My Life Feels More Coherent**
- My actions connect to my cares through intentions
- I'm building a story (Story timeline shows my narrative), not just reacting
- There's meaning in what I do daily

**5. Circles of Care Becomes My Default**
- I check Intentions list for "what should I do?" instead of scrolling
- I trust Pookie (AI companion) to hold my thoughts
- The Chamber system actually gets how my mind works

### Technical Success (Measurable - Portfolio Proof)

**These metrics prove the tech works, not just that it's a concept:**

**1. RAG Pipeline Accuracy**
- I can ask "what was that idea I had about X?" → it finds it
- **Target:** 80%+ retrieval accuracy for my queries
- Proves the RAG pipeline actually works

**2. Call Agents Mode Performance**
- Thought separation quality: Does it correctly identify semantic boundaries?
- **Target:** 75%+ acceptance rate (I agree with AI's separation)
- Proves multi-agent orchestration works

**3. Discover Mode Relevance**
- Recommendations match my taste
- **Target:** 70%+ of suggestions are things I'd actually want to do
- Proves taste-learning via embeddings works

**4. Clustering Quality (Circles)**
- Circles make sense (related cares group together)
- **Target:** Rarely need to manually move cares between circles
- Proves vector similarity clustering works

**5. Daily Active Use (Engagement)**
- I open Circles of Care 3-5 times per day
- Morning check (Intentions list), throughout day captures, evening review (circles)
- Proves I actually use it (not abandoned after building)

**6. Feature Adoption**
- **Call Agents Mode:** Use it 2-3x per week for brain dumps
- **Intentions List:** Check it daily for action guidance
- **Discover Mode:** Check it for intention-aligned recommendations
- **RAG Chat:** Query it 3-5x per week with Pookie (AI companion)
- Proves all features get real usage

**7. System Cost Efficiency**
- Running cost: ~$0-3/month on free tiers
- Proves I can build production ML systems on a budget

### What Success Looks Like

**Personal:** I'm living in eternal flow - acting most of the day, not overthinking. My cares are clear (organized in circles), my actions flow from intentions, my life feels coherent (Story timeline shows my narrative).

**Technical:** All the ML features I built actually work and I use them daily. RAG finds what I need, agents separate my thoughts correctly, recommendations align with my intentions, the intention-care linking system works, and it costs basically nothing to run.

**Portfolio:** This proves I can build end-to-end ML systems with agentic capabilities (Pookie as AI companion) that solve real problems (attention control) with production-grade architecture and cost efficiency.

---

## MVP Scope

### Core Features (Build All, Keep Simple)

I'm building ALL the core features from my resume, implemented in the simplest way possible using free-tier architecture.

**1. Capture (with AI-Powered Thought Separation)**
- Text input box for brain dumps
- Mic button → speech-to-text (iOS native voice recognition)
- **Split button for save:**
  - "Save" → saves as-is
  - "Separate & Save" → AI splits distinct thoughts first, then saves each separately
- Backend: OpenRouter free models for thought separation logic
- Storage: Supabase PostgreSQL

**2. Circles (Semantic Clustering - Level 1)**
- **Embeddings:** sentence-transformers (local, free) running on FastAPI backend
- **Vector DB:** FAISS (local file storage, free)
- **Clustering:** Automatic grouping into 3-5 thematic circles based on semantic similarity
- **Naming:** Pookie (AI companion) suggests circle names, I can X them or add my own
- **UI:** Simple list view of circles with care counts
- **Care frequency:** Each circle tracks how often I interact with related cares

**3. Intentions (Action-Oriented Goals - Level 2)**
- **Creation:** "Up arrow" from Chamber (circles view) → type intention → creates Intention object
- **Intention-Care Linking:** Select individual captures (not just whole circles) as "roots"
  - Many-to-many relationship: multiple captures → one intention
  - Visual: Arrow thickness = number of linked cares (stream of energy)
- **UI:** Intentions list view (separate from Chamber) with toggle on/off
- **Database:** intentions table, intention_cares junction table
- **Actions:** Attach specific actions to each intention

**4. Story Timeline (Completion Log - Level 3)**
- **Automatic logging:** Completed actions from Intentions list
- **Narrative building:** Chronological view of what I've actually done
- **UI:** Separate timeline view showing completed actions linked to intentions
- **Database:** stories table linking completed actions to intentions

**5. Vibe Profile (Personalization Engine)**
- **Input:** Aggregated preference vector from circles + intentions + captures
- **Output:** Vibe profile (JSONB) representing my taste/care patterns
- **Purpose:** Powers Discover Mode recommendations and RAG context

**6. Chamber (4-Level Hierarchy Navigation)**
- **L0:** Unorganized captures (raw input)
- **L1:** Circles (thematic clustering)
- **L2:** Intentions (created by "up arrow" from circles)
- **L3:** Story timeline (completion log)
- **UI:** Level indicator showing current position in hierarchy

**7. Discover Mode (Intention-Based Recommendations)**
- **Learn taste profile** from vibe profile (circles + intentions)
- **AI recommends actions** aligned with active intentions:
  - Content actions: "Watch this movie" "Listen to this song"
  - Goal actions: "You care about getting jacked → Hit the gym"
- **UI:** Suggestions filtered by intention relevance
- **Backend:** Vibe profile + embedding similarity + LLM synthesis via Claude Haiku

**8. RAG Chat (My Personal LLM with Pookie)**
- Ask questions about my cares: "What did I say about X?"
- **RAG pipeline:**
  - FAISS vector search across all my cares
  - Retrieve top-k relevant cares, circles, intentions
  - LLM response with full context (circles + intentions + vibe profile) via Claude Haiku
- **Pookie personality:** Biased by vibe profile, acts as AI companion/guide
- **UI:** Simple chat interface
- Proves end-to-end RAG implementation with agentic capabilities

---

### What This Proves (Resume Coverage)

✅ **"End-to-end LLM-powered iOS app with RAG pipeline"**
- RAG Chat feature covers this completely
- FastAPI + SwiftUI + OpenRouter/Claude integration

✅ **"AI-driven semantic linking with embeddings + vector database"**
- sentence-transformers embeddings
- FAISS vector storage and similarity search
- Automatic grouping into circles
- Dynamic cross-referencing via semantic similarity
- Intention-care linking (many-to-many relationships)

✅ **"Lightweight knowledge-graph layer with agentic capabilities"**
- Data structure exists (circles + intentions + stories + relationships stored)
- Powers semantic clustering, intention linking, and narrative building
- Pookie acts as AI companion navigating the knowledge graph
- Visual Chamber UI with 4-level hierarchy (L0→L1→L2→L3)

✅ **"Structured capture → organize → act → reflect loops"**
- **Capture:** Text + voice + thought separation (L0)
- **Organize:** Circles clustering with ML (L1)
- **Act:** Intentions → Actions (L2)
- **Reflect:** Story timeline showing completed actions (L3)
- **ML-assisted:** Cluster naming, intention discovery, vibe profile generation

---

### Out of Scope for MVP

**Visual Polish:**
- No fancy animations or UI transitions
- No dark mode (yet)
- Basic SwiftUI components only
- Arrow thickness visual for intention-care linking is basic (not animated)

**Advanced Features (Post-MVP):**
- Interactive force-directed graph visualization of Chamber (data structure exists, advanced visual UI later)
- Advanced vibe-maps (Option C - paid tier with sophisticated AI)
- Photo/file capture (text + voice only for MVP)
- Offline-first sync (online-only for MVP)
- Social features (sharing, collaboration)

**Optimizations (Post-MVP):**
- Performance tuning
- Caching strategies
- Background processing
- Advanced error handling

---

### MVP Success Criteria

**It works if:**
1. ✅ I can capture text and voice notes
2. ✅ Thought separation accurately identifies distinct ideas (75%+ acceptance)
3. ✅ Circles cluster my cares correctly (rarely need manual moves)
4. ✅ I can create intentions by "up arrowing" from circles
5. ✅ I can link individual captures as "roots" to intentions (multi-care → one intention)
6. ✅ Intentions list drives my day (I check it for "what should I do?")
7. ✅ Completed actions appear in Story timeline
8. ✅ Discover Mode gives me intention-aligned suggestions (70%+ I'd actually do)
9. ✅ RAG Chat with Pookie finds what I'm looking for (80%+ retrieval accuracy)
10. ✅ I use it daily (3-5 times per day)
11. ✅ Total cost stays ~$0-3/month

**Then I iterate.**

---

### Future Vision (Post-MVP)

**If MVP works, next additions:**

**Phase 2: Advanced Visualization & Analytics**
- Interactive force-directed graph visualization of Chamber (advanced 3D layout)
- Advanced vibe-maps (Option C - paid tier with sophisticated AI)
- Trend detection in circles and intentions
- Pattern recognition: "You avoid this circle on weekends"

**Phase 3: Rich Capture**
- Photo capture with vision analysis
- Link/bookmark capture from Safari
- Audio note transcription

**Phase 4: Intelligence**
- Multi-turn chat refinement for thought separation
- Learning from my corrections (interactive ML)
- Advanced analytics: Intention completion rates, circle engagement patterns
- Weekly/monthly reflection summaries

**Phase 5: Scale**
- Offline-first with sync
- Performance optimization
- Advanced caching
- Consider paid tiers if others want to use it

---

### Development Timeline

**Fast execution approach:**

**Week 1-2: Backend Foundation**
- FastAPI scaffold
- Supabase setup (auth, database, schema)
- sentence-transformers + FAISS integration
- Basic embedding pipeline

**Week 3-4: iOS App Scaffold**
- SwiftUI project setup
- Auth flow (Supabase)
- Basic navigation structure
- Capture screen with voice

**Week 5-6: Core ML Features**
- Thought separation (OpenRouter integration)
- Circles clustering (FAISS + naming)
- Intentions + Story timeline
- RAG Chat (vector search + LLM)

**Week 7-8: Discover Mode + Polish**
- Action suggestion engine
- Basic UI refinement
- Testing with real usage
- Deploy to TestFlight

**Total: ~8 weeks to working MVP**

Then iterate based on daily use.

---
