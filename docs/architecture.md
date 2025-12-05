---
stepsCompleted: [1, 2, 3, 4, 5, 6]
inputDocuments:
  - 'docs/analysis/product-brief-Pookie-2025-12-02.md'
  - 'docs/analysis/brainstorming-session-2025-12-02.md'
workflowType: 'architecture'
lastStep: 6
status: 'complete'
project_name: 'Pookie'
user_name: 'sudy'
date: '2025-12-02'
completed_date: '2025-12-03'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**

Pookie is an ML-powered personal knowledge management system with four core functional pillars:

1. **Capture & Thought Separation (Call Agents Mode)**
   - Text/voice input for brain dumps
   - AI-powered semantic boundary detection to separate distinct thoughts from rambling paragraphs
   - Interactive refinement chat ("split differently", "combine these")
   - Storage of individual separated thoughts as discrete entities

2. **Semantic Clustering (Abodes)**
   - Automatic grouping of related thoughts into thematic "abodes" using vector similarity
   - LLM-generated naming for discovered clusters
   - Dynamic reorganization as new thoughts are added
   - Knowledge graph structure tracking relationships between abodes

3. **Personalized Discovery (Discover Mode)**
   - Taste profile learning from saved content
   - Action recommendations (content + goal-oriented)
   - Embedding-based similarity matching to user preferences

4. **RAG-Powered Chat (Personal LLM)**
   - Natural language queries about saved thoughts ("what did I say about X?")
   - Context-aware responses using retrieved relevant thoughts
   - Conversational interface maintaining user's knowledge context

**Non-Functional Requirements:**

- **Cost Constraint:** ~$0-3/month (free-tier architecture)
- **Accuracy Targets:**
  - RAG retrieval: 80%+ accuracy for user queries
  - Thought separation: 75%+ acceptance rate
  - Discover Mode relevance: 70%+ suggestions user would act on
  - Clustering quality: Minimal manual reorganization needed
- **Performance:**
  - Chat response latency: <2 seconds end-to-end
  - Embedding generation: <500ms for typical thought (50-200 words)
  - Vector search: <100ms for top-k retrieval
  - Mobile app responsiveness: Native iOS performance standards
- **Usage Pattern:** Daily active use (3-5 sessions/day)
- **Scale:** Personal use (<100k thoughts initially)

### Technical Architecture Deep Dive

#### RAG Pipeline Architecture

**What RAG Does:**

Retrieval-Augmented Generation (RAG) solves the "AI with personal memory" problem. Standard LLMs don't know about your specific thoughts—RAG gives them access to your personal knowledge base.

**How It Works (Pookie's Implementation):**

```
User Query: "What did I say about productivity?"
    ↓
1. EMBEDDING GENERATION
   - Query converted to 384-dim vector using sentence-transformers
   - Same model used for stored thoughts (semantic consistency)
    ↓
2. VECTOR SIMILARITY SEARCH (FAISS)
   - Cosine similarity across all stored thought embeddings
   - Top-k retrieval (k=5-10 most relevant thoughts)
   - Sub-100ms search time for <100k vectors
    ↓
3. CONTEXT AUGMENTATION
   - Retrieved thoughts injected into LLM prompt
   - Format: "Based on these saved thoughts: [context], answer: [query]"
    ↓
4. LLM GENERATION (Claude Haiku)
   - Generates response grounded in user's actual saved content
   - Not generic ChatGPT—personalized to user's knowledge
    ↓
Response: "You mentioned productivity in 3 thoughts: [specific references]..."
```

**Embeddings Technical Details:**

- **Model:** `all-MiniLM-L6-v2` (sentence-transformers)
  - 384-dimensional dense vectors
  - 80MB model size (runs locally, no API cost)
  - Trained on semantic similarity tasks
- **How Embeddings Work:**
  - Text → neural network → fixed-length vector capturing semantic meaning
  - Similar concepts produce similar vectors (cosine similarity ~0.8-0.95)
  - "I want to get jacked" and "I care about fitness" → close in vector space
  - Enables semantic search (not just keyword matching)
- **Storage:** Raw embeddings stored in FAISS index (.faiss file on disk)
- **Generation:** On-demand when thoughts are saved (CPU-based, <500ms)

**Vector Search Mechanics (FAISS):**

- **Index Type:** Flat L2 or IndexFlatIP (exact search for <100k vectors)
- **Search Algorithm:** Brute-force cosine similarity (fast enough at this scale)
- **Performance:** O(n) search complexity, but n is small (<100k) and FAISS is highly optimized
- **Persistence:** Save index to disk, load into memory on FastAPI startup
- **No Cost:** Fully local, no API calls

#### Performance Expectations

**Current Architecture (Naive RAG):**

- **Strengths:**
  - Simple, fast, cheap (~$0/month for RAG pipeline)
  - Works well for personal scale (<100k thoughts)
  - Semantic search significantly better than keyword search
  - Low latency (<2s end-to-end including LLM)

- **Limitations:**
  - **No relationship awareness:** Doesn't understand connections between thoughts
  - **Context window limits:** Can only retrieve top-k thoughts (may miss relevant context)
  - **No reasoning chains:** Can't traverse "I care about X because Y" relationships
  - **Flat similarity:** All thoughts treated equally (no hierarchy or importance weighting)

**Expected Accuracy:**

- **RAG Retrieval:** 80%+ for straightforward queries ("what did I say about X?")
- **Semantic Clustering:** 75-85% quality (related thoughts group together)
- **Thought Separation:** 75%+ acceptance (AI correctly identifies thought boundaries)

#### Future Evolution: Naive RAG → Graph RAG

**Phase 1: Current (Naive RAG) - MVP**

```
Architecture: Simple vector similarity retrieval
Storage: FAISS (flat vectors) + Supabase (text)
Limitations: No relationship awareness, flat retrieval
```

**Phase 2: Enhanced RAG - Post-MVP**

```
Improvements:
- Hybrid search (vector + keyword BM25)
- Re-ranking with cross-encoder for better top-k selection
- Query expansion (reformulate user query for better retrieval)
- Chunk optimization (thought splitting for better embedding granularity)

Expected Gains:
- RAG accuracy: 80% → 85-90%
- Better handling of multi-faceted queries
```

**Phase 3: Graph-Augmented RAG - Future**

```
Architecture Addition: Knowledge graph layer
Storage: Graph structure in Supabase (nodes=thoughts, edges=relationships)

Graph Construction:
- Nodes: Individual thoughts + abodes
- Edges: Semantic similarity, temporal proximity, explicit user links
- Metadata: Importance scores, novelty rankings, timestamps

Retrieval Strategy:
1. Vector search for initial seed thoughts (top-k)
2. Graph traversal to find related thoughts (2-hop neighbors)
3. Re-rank by graph centrality + vector similarity
4. Include relationship context in LLM prompt

Example Query: "What do I care about?"
- Naive RAG: Returns top-5 thoughts with "care" keyword
- Graph RAG: Returns central nodes in knowledge graph (high-degree thoughts that connect many abodes)

Expected Gains:
- RAG accuracy: 85% → 90-95%
- Relationship-aware responses ("You care about X, which connects to Y and Z")
- Multi-hop reasoning ("You care about fitness → you mentioned getting jacked → you should hit the gym")
```

**Phase 4: Agentic RAG - Advanced Future**

```
Architecture: Multi-agent query planning + execution

Agents:
- Query Planner: Decomposes complex queries into sub-queries
- Retrieval Agent: Executes vector + graph searches
- Reasoning Agent: Synthesizes multi-source context
- Reflection Agent: Validates response quality

Example: "What should I focus on this week?"
- Query Planner: Break into "what do I care about?" + "what actions align?" + "what's urgent?"
- Retrieval Agent: Search abodes, recent thoughts, goal-related thoughts
- Reasoning Agent: Synthesize priorities
- Reflection Agent: Check if response is actionable

Expected Gains:
- Complex query handling
- Multi-turn reasoning
- Proactive insights ("I noticed you haven't worked on X in 2 weeks")
```

### Scale & Complexity

- **Primary domain:** iOS mobile app with ML backend (full-stack + AI/ML)
- **Complexity level:** Medium-High
  - ML pipeline orchestration
  - Multi-agent systems
  - Real-time chat interface
  - Mobile-backend synchronization
  - Graph data structure management
- **Estimated architectural components:** 8-10 major components
  1. iOS SwiftUI frontend
  2. FastAPI backend
  3. Supabase (auth + database)
  4. Embedding service (sentence-transformers)
  5. Vector search (FAISS)
  6. Multi-agent orchestration
  7. RAG chat pipeline
  8. Discover Mode recommendation engine
  9. Knowledge graph layer (future)
  10. Background sync service

### Technical Constraints & Dependencies

**Pre-Selected Technologies:**

- **Frontend:** SwiftUI (iOS 17+, MVVM with @Observable)
- **Backend:** FastAPI (Python)
- **Auth + DB:** Supabase (PostgreSQL + Storage)
- **Embeddings:** sentence-transformers (`all-MiniLM-L6-v2`)
- **Vector DB:** FAISS (local file persistence)
- **LLM Provider:** OpenRouter (free models) + Claude Haiku

**Cost Constraint:** Free-tier architecture (~$0-3/month total)

**Deployment:**

- Backend: Render free tier (750 hours/month)
- Mobile: iOS TestFlight → App Store
- Database: Supabase free tier (500MB PostgreSQL, 1GB storage)

**Scale Assumptions:**

- Single user (personal app)
- <100k thoughts initially
- <1000 abodes
- Local-first with cloud backup

### Cross-Cutting Concerns Identified

1. **Authentication & Authorization**
   - Supabase auth for mobile → backend
   - JWT token management
   - Secure API endpoints

2. **ML Pipeline Orchestration**
   - Embedding generation workflow
   - Vector index updates
   - Agent execution sequencing
   - Model loading/caching

3. **Data Consistency**
   - Mobile-backend sync strategy
   - Optimistic UI updates
   - Conflict resolution

4. **Performance Optimization**
   - FAISS index loading strategy (startup latency)
   - Embedding caching
   - LLM response streaming
   - Mobile app responsiveness

5. **Cost Management**
   - Free-tier monitoring
   - LLM token usage optimization
   - Background job efficiency

6. **Error Handling & Resilience**
   - LLM API failures
   - Network interruptions
   - Embedding generation errors
   - Vector search edge cases

## Starter Template Evaluation

### Primary Technology Domain

**iOS Mobile App + Python Backend** - This is a dual-platform architecture requiring separate starters for:
1. **Frontend:** SwiftUI iOS application
2. **Backend:** FastAPI Python ML service

### Starter Options Considered

#### iOS/SwiftUI Starters Evaluated

**1. Official Supabase Swift SDK + Manual MVVM Setup**
- **Source:** [Supabase iOS SwiftUI Quickstart](https://supabase.com/docs/guides/getting-started/quickstarts/ios-swiftui)
- **Approach:** Use Swift Package Manager to add Supabase SDK to a new Xcode project
- **Cost:** Free, official, well-maintained
- **Structure:** Manual MVVM setup with full control

**2. Supabase Bootstrap CLI**
- **Source:** [Supabase Bootstrap](https://dev.to/supabase/supabase-bootstrap-the-fastest-way-to-launch-a-new-project-56hf)
- **Approach:** `supabase bootstrap` CLI to generate iOS SwiftUI starter
- **Cost:** Free, official
- **Structure:** Pre-configured project structure with Supabase integration

**3. The Swift Kit (Commercial)**
- **Source:** [CodeCanyon](https://codecanyon.net/item/the-swift-kit/59904241)
- **Approach:** Production-ready starter with MVVM, Supabase auth, onboarding, paywalls
- **Cost:** Paid (~$79+), lifetime updates
- **Structure:** Full-featured with authentication, onboarding, and monetization

**4. StartBase Boilerplate**
- **Source:** [StartBase](https://startbase.dev/boilerplates/ios-supabase-auth)
- **Approach:** Robust authentication boilerplate with social logins
- **Cost:** Varies
- **Structure:** Authentication-focused with custom components

#### FastAPI Backend Starters Evaluated

**1. create-fastapi-project CLI**
- **Source:** [PyPI](https://pypi.org/project/create-fastapi-project/)
- **Approach:** Simple CLI to scaffold basic FastAPI structure
- **Cost:** Free, minimal setup
- **Structure:** Basic folders (api, models, schemas, core)

**2. cookiecutter-fastapi-ML**
- **Source:** [GitHub](https://github.com/xshapira/cookiecutter-fastapi-ML)
- **Approach:** Cookiecutter template for ML-focused FastAPI projects
- **Cost:** Free, ML-optimized
- **Structure:** Poetry, GitHub Actions, pytest, ML-ready architecture

**3. Full Stack FastAPI Template (Official)**
- **Source:** [FastAPI Docs](https://fastapi.tiangolo.com/project-generation/)
- **Approach:** Comprehensive full-stack template from FastAPI creator
- **Cost:** Free, official, production-ready
- **Structure:** PostgreSQL, Docker, testing, CI/CD, admin dashboard

**4. Manual Setup with Best Practices**
- **Approach:** Build from scratch following [2025 best practices](https://santiagoalvarez87.medium.com/fastapi-template-starter-a-boilerplate-for-your-next-backend-project-25e6338ed741)
- **Cost:** Free, maximum control
- **Structure:** Custom layered architecture (api, services, models, repositories)

### Selected Starters

#### iOS: Official Supabase Swift SDK + Manual MVVM Setup

**Rationale for Selection:**
- **Free and Official:** Maintained by Supabase team, guaranteed compatibility
- **Full Control:** MVVM architecture customized for Pookie's specific needs (not over-engineered)
- **Simplicity:** No unnecessary features (no paywalls, monetization, or extra boilerplate)
- **Well-Documented:** Comprehensive tutorials and API reference
- **Flexibility:** Add only what Pookie needs (embedding models, vector search, ML agents)

**Initialization Commands:**

```bash
# 1. Create new Xcode project
# File > New > Project > iOS > App
# - Product Name: Pookie
# - Interface: SwiftUI
# - Life Cycle: SwiftUI App
# - Language: Swift
# - Use @Observable: Yes (iOS 17+)

# 2. Add Supabase Swift SDK via Swift Package Manager
# In Xcode: File > Add Package Dependencies
# URL: https://github.com/supabase/supabase-swift
# Version: Latest release (2.x.x as of 2025)

# 3. Create Supabase.swift helper file
# See: https://supabase.com/docs/guides/getting-started/quickstarts/ios-swiftui
```

**Architectural Decisions Provided by Starter:**

**Language & Runtime:**
- Swift 5.9+ with SwiftUI (iOS 17+ for @Observable)
- Native iOS SDK integration
- Swift Package Manager for dependency management

**Authentication:**
- Supabase Auth SDK pre-integrated
- Magic link, email/password, OAuth support
- JWT token management handled by SDK

**Project Structure (Manual MVVM):**
```
Pookie/
├── App/
│   ├── PookieApp.swift (entry point)
│   └── Supabase.swift (client initialization)
├── Models/
│   ├── Thought.swift
│   ├── Abode.swift
│   └── User.swift
├── ViewModels/
│   ├── CaptureViewModel.swift
│   ├── AbodeViewModel.swift
│   ├── DiscoverViewModel.swift
│   └── ChatViewModel.swift
├── Views/
│   ├── Capture/
│   ├── Abodes/
│   ├── Discover/
│   └── Chat/
├── Services/
│   ├── APIService.swift (backend communication)
│   ├── EmbeddingService.swift (future local embeddings)
│   └── SyncService.swift
└── Resources/
```

**Development Experience:**
- Xcode previews for SwiftUI
- Native debugging tools
- iOS Simulator testing
- TestFlight deployment ready

---

#### Backend: cookiecutter-fastapi-ML

**Rationale for Selection:**
- **ML-Optimized:** Designed specifically for ML/AI projects (perfect for embeddings + FAISS)
- **Poetry Included:** Better dependency management than pip
- **Testing Setup:** pytest pre-configured
- **CI/CD Ready:** GitHub Actions workflows included
- **Production Patterns:** Follows FastAPI best practices with layered architecture
- **Free & Open Source:** Active community, well-documented

**Initialization Commands:**

```bash
# 1. Install cookiecutter (if not already installed)
pip install cookiecutter

# 2. Generate project from template
cookiecutter https://github.com/xshapira/cookiecutter-fastapi-ML

# You'll be prompted for:
# - project_name: Pookie Backend
# - project_slug: pookie-backend
# - author_name: sudy
# - python_version: 3.11 (recommended for sentence-transformers)
# - use_docker: yes
# - use_github_actions: yes

# 3. Navigate to project and install dependencies
cd pookie-backend
poetry install

# 4. Run development server
poetry run uvicorn app.main:app --reload
```

**Architectural Decisions Provided by Starter:**

**Language & Runtime:**
- Python 3.11+ (optimal for ML libraries)
- FastAPI framework (async-first, high performance)
- Poetry for dependency management
- Type hints enforced with Pydantic

**Project Structure:**
```
pookie-backend/
├── app/
│   ├── main.py (FastAPI app initialization)
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── thoughts.py
│   │   │   │   ├── abodes.py
│   │   │   │   ├── chat.py
│   │   │   │   └── discover.py
│   │   │   └── api.py (route aggregation)
│   ├── core/
│   │   ├── config.py (settings management)
│   │   └── security.py (auth utilities)
│   ├── models/
│   │   ├── thought.py (SQLAlchemy models)
│   │   └── abode.py
│   ├── schemas/
│   │   ├── thought.py (Pydantic schemas)
│   │   └── abode.py
│   ├── services/
│   │   ├── embedding_service.py (sentence-transformers)
│   │   ├── vector_service.py (FAISS operations)
│   │   ├── llm_service.py (OpenRouter/Claude integration)
│   │   └── agent_service.py (multi-agent orchestration)
│   └── ml/
│       ├── embedding_model.py (sentence-transformers loader)
│       ├── vector_index.py (FAISS index management)
│       └── agents/ (Tag, Reflection, Novelty agents)
├── tests/
│   ├── test_api/
│   └── test_services/
├── pyproject.toml (Poetry dependencies)
├── Dockerfile
└── .github/workflows/ (CI/CD)
```

**ML Pipeline Integration:**
- `services/embedding_service.py`: Load `all-MiniLM-L6-v2` on startup, generate embeddings
- `services/vector_service.py`: FAISS index persistence, search operations
- `services/llm_service.py`: OpenRouter/Claude API integration
- `services/agent_service.py`: Sequential agent orchestration

**Testing Framework:**
- pytest with async support
- Test fixtures for database and services
- Coverage reporting

**Development Experience:**
- Hot reload with `--reload` flag
- Interactive API docs at `/docs` (Swagger UI)
- Auto-generated OpenAPI spec
- Type checking with mypy
- Linting with ruff/flake8

**Deployment:**
- Docker containerization included
- Environment-based configuration (.env files)
- Render-ready (supports Dockerfile deployment)

---

**Cost Impact:**
- **iOS Starter:** $0 (official SDK, manual setup)
- **FastAPI Starter:** $0 (open source template)
- **Total Starter Cost:** $0 (aligns with free-tier architecture goal)

**Note:** Project initialization using these commands should be **Story 0: Project Setup** in the implementation phase.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
1. Database: SQLAlchemy Models + Alembic Migrations
2. Authentication: Supabase JWT validation with supabase-py
3. API Communication: REST + SSE for streaming LLM responses
4. ML Pipeline: Backend-only embeddings (centralized)
5. FAISS Persistence: Supabase Storage for index files

**Important Decisions (Shape Architecture):**
6. iOS State Management: ViewModels + Shared AppState
7. Mode Orchestration: Simple sequential functions (not framework-based)
8. Error Handling: Retry with exponential backoff + confidence-based RAG fallback
9. Environment Config: .env files + environment variables
10. Deployment: Automated backend CI/CD, manual iOS

**Deferred Decisions (Post-MVP):**
- Offline-first sync strategy
- Advanced caching layers
- Graph RAG implementation
- Performance optimizations

---

### Data Architecture

**Database Schema Management:**
- **Approach:** SQLAlchemy ORM models + Alembic migrations
- **Models:** `Thought`, `Abode`, `User` in `app/models/`
- **Migrations:** Version controlled via Alembic
- **Database:** Supabase PostgreSQL (free tier: 500MB)
- **Rationale:** Type-safe Python models, easy to version, works with FastAPI starter template

**Data Flow:**
```
iOS → FastAPI → Supabase PostgreSQL (structured data)
                → Supabase Storage (FAISS index)
```

---

### Authentication & Security

**Authentication Flow:**
- **Method:** Supabase JWT validation via `supabase-py`
- **Flow:**
  1. User logs in via Supabase Auth (iOS)
  2. iOS receives JWT token
  3. iOS sends token in `Authorization: Bearer <token>` header
  4. FastAPI validates JWT using Supabase public key
  5. User context available in all endpoints

**Security Middleware:**
- JWT validation middleware on all protected endpoints
- Supabase handles token refresh, expiry, key rotation
- User ID extracted from JWT for database queries

**API Security:**
- All endpoints require authentication (except health check)
- Row-level security policies in Supabase
- HTTPS only (enforced by Render + Supabase)

---

### API & Communication Patterns

**API Design:**
- **Standard Operations:** RESTful JSON APIs
  - `POST /api/v1/thoughts` - Create thought
  - `POST /api/v1/thoughts/separate` - Call Agents Mode (thought separation)
  - `GET /api/v1/abodes` - List abodes
  - `GET /api/v1/abodes/{id}/thoughts` - Get thoughts in abode
  - `POST /api/v1/discover` - Get action recommendations

- **Streaming Operations:** Server-Sent Events (SSE)
  - `POST /api/v1/chat/stream` - RAG chat with streaming response
  - Returns `StreamingResponse` with token-by-token LLM output

**iOS Implementation:**
- Standard REST: `URLSession` with `async/await`
- SSE Streaming: `URLSession` event stream handling
- JSON serialization via `Codable`

**Error Handling:**
- HTTP status codes: 200 (success), 401 (unauthorized), 422 (validation error), 500 (server error)
- Consistent error response format: `{"detail": "error message"}`
- LLM failures: Retry 2-3 times with exponential backoff before returning error

---

### Frontend Architecture (iOS)

**State Management Pattern:**
- **Architecture:** MVVM with `@Observable` (iOS 17+)
- **Shared State:** `@Observable class AppState`
  - User profile
  - Auth token
  - Sync status
  - Network connectivity
- **Screen ViewModels:**
  - `CaptureViewModel` - Text/voice input, thought separation
  - `AbodeViewModel` - Abode list, clustering
  - `DiscoverViewModel` - Action recommendations
  - `ChatViewModel` - RAG chat interface

**State Access:**
- ViewModels inject `AppState` via `@Environment` or initializer
- Views observe ViewModels via `@State` or `@Bindable`
- No third-party state management libraries

**Project Structure:**
```
Pookie/
├── App/
│   ├── PookieApp.swift
│   ├── Supabase.swift
│   └── AppState.swift (shared state)
├── Models/
├── ViewModels/
├── Views/
└── Services/
```

---

### ML Pipeline Architecture

**Embedding Generation:**
- **Location:** Backend-only (FastAPI)
- **Model:** `all-MiniLM-L6-v2` (sentence-transformers)
- **Loading:** Model loads once on FastAPI startup
- **Process:**
  1. iOS sends text to backend
  2. Backend generates 384-dim embedding (CPU, <500ms)
  3. Backend stores embedding in FAISS + text in Supabase
  4. Returns success to iOS

**Vector Search (FAISS):**
- **Index Type:** `IndexFlatIP` (exact cosine similarity for <100k vectors)
- **Persistence:** Save to Supabase Storage bucket
  - Download `.faiss` file on FastAPI startup
  - Cache in memory for fast search
  - Upload after updates (debounced)
- **Search:** `vector_service.search(query, top_k=5)` returns top-k thoughts

**Mode Orchestration:**
- **Implementation:** Simple sequential Python functions
- **Modes:**
  - `tag_mode(thought)` → generates tags via LLM
  - `reflection_mode(thought)` → generates insights via LLM
  - `novelty_mode(thought)` → scores importance (0-1)
- **Location:** `app/ml/modes/`
- **Execution:** Sequential function calls, no framework
- **LLM Provider:** OpenRouter free models for modes

**RAG Chat Pipeline:**
- **Hybrid Approach with Confidence-Based Fallback:**
  ```python
  def chat(query):
      # 1. Always search FAISS first
      results = vector_service.search(query, top_k=5)

      # 2. Check confidence (similarity score)
      if results[0].similarity > 0.7:
          # High confidence → RAG mode
          context = [r.text for r in results]
          return llm_service.rag_chat(query, context)
      else:
          # Low confidence → Direct LLM mode
          return llm_service.direct_chat(query)
  ```

- **RAG Mode (Personal Knowledge):**
  - Use retrieved thoughts as context
  - Prompt: "Based on these saved thoughts: [context], answer: [query]"
  - LLM: Claude Haiku via OpenRouter

- **Direct Mode (General Knowledge):**
  - No retrieval, pure LLM response
  - LLM uses its inherent training knowledge
  - Prompt: Just the query
  - User sees indication: "General knowledge response"

**Clustering (Abodes):**
- **Algorithm:** K-means or DBSCAN on embeddings
- **Execution:** Background job after N new thoughts
- **Naming:** LLM generates abode names based on cluster content
- **Storage:** Abode metadata in Supabase, relationships in graph structure

---

### Infrastructure & Deployment

**Backend Hosting:**
- **Platform:** Render free tier (750 hours/month)
- **Configuration:** Dockerfile deployment
- **Environment:** Production env vars in Render dashboard

**iOS Deployment:**
- **Development:** Xcode Simulator
- **Testing:** TestFlight (manual upload)
- **Production:** App Store (manual submission)

**CI/CD Pipeline:**
- **Backend (Automated):**
  ```yaml
  # GitHub Actions workflow
  on: push to main
  1. Run pytest (unit + integration tests)
  2. If tests pass → deploy to Render
  3. Notify on failure
  ```

- **iOS (Manual):**
  - Xcode → Archive → Upload to TestFlight
  - No automation (avoids GitHub macOS runner costs)

**Environment Configuration:**
- **Backend:**
  - Local: `.env` file (gitignored)
  - Production: Render environment variables
  - Secrets: Supabase keys, OpenRouter API key, Claude API key

- **iOS:**
  - Xcode build configurations (Debug/Release)
  - Supabase URL + anon key in Config.plist (gitignored)

**Monitoring & Logging:**
- FastAPI default logging to stdout
- Render aggregates logs
- Manual monitoring (no paid tools for MVP)

---

### Decision Impact Analysis

**Implementation Sequence:**
1. **Story 0:** Project setup (Xcode + cookiecutter-fastapi-ML)
2. **Foundation:** Supabase schema (Alembic migrations), Auth middleware
3. **ML Core:** sentence-transformers service, FAISS service, Supabase Storage persistence
4. **API Layer:** REST endpoints, SSE streaming for chat
5. **iOS Foundation:** AppState, Supabase client, Auth flow
6. **Features:** Capture → Abodes → Discover → Chat (in order)
7. **Modes:** Tag/Reflection/Novelty modes (sequential functions)
8. **CI/CD:** GitHub Actions for backend

**Cross-Component Dependencies:**
- Auth must be implemented before any API endpoints
- FAISS persistence must work before clustering
- Embedding service must be ready before thought separation
- AppState must exist before ViewModels
- SSE streaming enables real-time chat UX

## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

**Critical Conflict Points Identified:** 8 major areas where AI agents could make incompatible choices

These patterns ensure consistency across the dual-platform architecture (Swift + Python) and prevent implementation conflicts.

---

### Naming Patterns

#### Cross-Platform Naming (Python ↔ Swift)

**The Challenge:** Python uses `snake_case`, Swift uses `camelCase` - we need consistent JSON exchange.

**Solution: Hybrid with Pydantic Transformation**

- **Database:** `snake_case` (user_id, created_at, thought_text)
- **Python Models:** `snake_case` (native Python convention)
- **API JSON:** `camelCase` (userId, createdAt, thoughtText)
- **Swift Models:** `camelCase` (native Swift, no CodingKeys needed)
- **Transformation:** Pydantic schemas with `alias` parameter

**Example Implementation:**
```python
# Python Pydantic Schema
class ThoughtResponse(BaseModel):
    id: int
    user_id: int = Field(alias="userId")
    thought_text: str = Field(alias="thoughtText")
    created_at: datetime = Field(alias="createdAt")

    class Config:
        populate_by_name = True
```

```swift
// Swift Model (native camelCase, no custom CodingKeys)
struct Thought: Codable {
    let id: Int
    let userId: Int
    let thoughtText: String
    let createdAt: Date
}
```

---

#### Database Naming Conventions

**Tables:**
- **Pattern:** Plural nouns
- **Examples:** `users`, `thoughts`, `abodes`, `embeddings`

**Columns:**
- **Pattern:** `snake_case`
- **Examples:** `user_id`, `thought_text`, `created_at`, `embedding_vector`

**Foreign Keys:**
- **Pattern:** `{table_singular}_id`
- **Examples:** `user_id`, `abode_id`, `thought_id`

**Indexes:**
- **Pattern:** `idx_{table}_{column(s)}`
- **Examples:** `idx_thoughts_user_id`, `idx_thoughts_created_at`, `idx_abodes_user_id`

**Constraints:**
- **Pattern:** `{type}_{table}_{column}`
- **Examples:** `uq_users_email`, `fk_thoughts_user_id`, `chk_thoughts_text_length`

---

#### API Naming Conventions

**Endpoint Structure:**
- **Base:** `/api/v1/`
- **Resources:** Plural nouns (`/thoughts`, `/abodes`)
- **Parameters:** `{id}`, `{abode_id}`, `{thought_id}`

**Standard CRUD Endpoints:**
```
GET    /api/v1/thoughts          # List thoughts
POST   /api/v1/thoughts          # Create thought
GET    /api/v1/thoughts/{id}     # Get single thought
PUT    /api/v1/thoughts/{id}     # Update thought
DELETE /api/v1/thoughts/{id}     # Delete thought
```

**ML/Action Endpoints (Verb-based for non-CRUD):**

| Action | Purpose | API Endpoint | Method |
|--------|---------|--------------|--------|
| **Separate Thoughts** | AI-powered semantic boundary detection to split rambling paragraphs into distinct thoughts | `/api/v1/ml/separate-thoughts` | POST |
| **RAG Chat** | Ask questions and converse with your personal knowledge using vector search + LLM | `/api/v1/chat/stream` | POST |
| **Discover** | Explore new experiences using taste reasoning (RAG + LLM general knowledge) | `/api/v1/ml/discover` | POST |
| **Link** | Chain-of-thought reasoning from your abodes to new concepts (explicit reasoning path) | `/api/v1/ml/link` | POST |
| **Prioritize** | Rank existing thoughts/actions to decide what to do next | `/api/v1/ml/prioritize` | POST |
| **List Abodes** | Get all thought clusters/contexts | `/api/v1/abodes` | GET |
| **Add Thought to Abode** | Dynamically organize thoughts into clusters | `/api/v1/abodes/{abode_id}/thoughts` | POST |
| **Remove Thought** | Remove thought from cluster | `/api/v1/abodes/{abode_id}/thoughts/{thought_id}` | DELETE |

**Action Detailed Descriptions:**

1. **Separate Thoughts:**
   - User pastes messy brain dump → LLM identifies thought boundaries → returns separated thoughts
   - Example: "I care about fitness and also want to learn piano and maybe travel to Japan" → 3 separate thoughts

2. **RAG Chat (Streaming):**
   - Vector search retrieves relevant thoughts → LLM generates response using your context
   - Example: "What did I say about productivity?" → Returns personalized answer from your saved thoughts

3. **Discover:**
   - RAG reasoning (past preferences) + LLM general knowledge → recommendations for NEW experiences
   - Example: "What chocolate should I eat?" → Sees you liked Ghirardelli → recommends Lindt

4. **Link:**
   - Shows explicit reasoning chain connecting what you know to what you're learning
   - Example: "Help me understand calculus" → "You know algebra → connects to functions → leads to rates of change → therefore derivatives"

5. **Prioritize:**
   - Novelty mode scoring + user preferences → ranked list of existing items
   - Example: "Which of my saved thoughts should I act on first?"

---

#### Code Naming Conventions

**Swift (iOS):**
- **Files:** PascalCase (`CaptureView.swift`, `ThoughtModel.swift`, `AbodeViewModel.swift`)
- **Classes/Structs:** PascalCase (`CaptureViewModel`, `Thought`, `Abode`, `AppState`)
- **Functions/Variables:** camelCase (`fetchThoughts`, `userId`, `thoughtText`, `isLoading`)
- **Constants:** camelCase (`maxThoughtLength`, `defaultAbodeName`, `apiBaseURL`)
- **Enums:** PascalCase with camelCase cases (`enum LoadingState { case idle, loading, success, failure }`)

**Python (Backend):**
- **Files:** snake_case (`capture_view.py`, `thought_model.py`, `embedding_service.py`)
- **Classes:** PascalCase (`ThoughtModel`, `EmbeddingService`, `VectorService`, `ChatService`)
- **Functions/Variables:** snake_case (`fetch_thoughts`, `user_id`, `thought_text`, `is_loading`)
- **Constants:** UPPER_SNAKE_CASE (`MAX_THOUGHT_LENGTH`, `DEFAULT_ABODE_NAME`, `FAISS_INDEX_PATH`)
- **Private:** Leading underscore (`_internal_method`, `_cache`)

---

### Structure Patterns

#### Backend Project Structure

```
pookie-backend/
├── app/
│   ├── main.py                    # FastAPI app initialization
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── thoughts.py    # CRUD operations
│   │       │   ├── abodes.py      # Abode management
│   │       │   ├── chat.py        # RAG chat streaming
│   │       │   └── ml.py          # ML endpoints (separate, discover, link, prioritize)
│   │       └── api.py             # Route aggregation
│   ├── core/
│   │   ├── config.py              # Settings management
│   │   ├── security.py            # JWT validation
│   │   └── dependencies.py        # FastAPI dependencies
│   ├── models/
│   │   ├── thought.py             # SQLAlchemy ORM models
│   │   ├── abode.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── thought.py             # Pydantic request/response schemas
│   │   ├── abode.py
│   │   └── chat.py
│   ├── services/
│   │   ├── embedding_service.py   # sentence-transformers
│   │   ├── vector_service.py      # FAISS operations
│   │   ├── llm_service.py         # OpenRouter/Claude integration
│   │   ├── chat_service.py        # RAG chat orchestration
│   │   └── mode_service.py        # Mode orchestration
│   └── ml/
│       ├── embedding_model.py     # sentence-transformers loader
│       ├── vector_index.py        # FAISS index management
│       └── modes/
│           ├── tag_mode.py        # Tag generation
│           ├── reflection_mode.py # Insight generation
│           └── novelty_mode.py    # Importance scoring
├── tests/
│   ├── test_api/
│   └── test_services/
├── alembic/                       # Database migrations
├── .env                           # Local environment (gitignored)
├── pyproject.toml                 # Poetry dependencies
└── Dockerfile
```

#### iOS Project Structure

```
Pookie/
├── App/
│   ├── PookieApp.swift           # Entry point
│   ├── Supabase.swift            # Supabase client init
│   └── AppState.swift            # Shared observable state
├── Models/
│   ├── Thought.swift
│   ├── Abode.swift
│   └── User.swift
├── ViewModels/
│   ├── CaptureViewModel.swift
│   ├── AbodeViewModel.swift
│   ├── DiscoverViewModel.swift
│   └── ChatViewModel.swift
├── Views/
│   ├── Capture/
│   │   ├── CaptureView.swift
│   │   └── SeparateThoughtsView.swift
│   ├── Abodes/
│   │   ├── AbodeListView.swift
│   │   └── AbodeDetailView.swift
│   ├── Discover/
│   │   └── DiscoverView.swift
│   └── Chat/
│       └── ChatView.swift
├── Services/
│   ├── APIService.swift          # Backend API client
│   ├── AuthService.swift         # Supabase auth wrapper
│   └── SyncService.swift         # Data sync
└── Resources/
    ├── Assets.xcassets
    └── Config.plist              # Environment config (gitignored)
```

---

### Format Patterns

#### API Response Formats

**Success Responses (Direct Data, No Wrapper):**

```json
// GET /api/v1/thoughts/{id}
{
  "id": 1,
  "userId": 123,
  "thoughtText": "I want to get jacked",
  "createdAt": "2025-12-03T10:30:00Z",
  "abodeId": 5
}

// GET /api/v1/thoughts (list)
[
  {"id": 1, "userId": 123, ...},
  {"id": 2, "userId": 123, ...}
]
```

**Error Responses (Consistent Format):**

```json
{
  "detail": "Thought not found",
  "code": "THOUGHT_NOT_FOUND"
}
```

**HTTP Status Codes:**
- **200:** Success
- **201:** Created
- **202:** Accepted (async operations)
- **400:** Bad request (client error)
- **401:** Unauthorized (no/invalid JWT)
- **404:** Not found
- **422:** Unprocessable entity (Pydantic validation error)
- **500:** Internal server error

---

#### Date/Time Formats

**API (JSON):**
- **Format:** ISO 8601 with UTC timezone
- **Example:** `"2025-12-03T10:30:00Z"`
- **Pydantic:** Automatic serialization via `datetime` type

**Database:**
- **Type:** PostgreSQL `TIMESTAMP WITH TIME ZONE`
- **Storage:** Always UTC
- **Column Names:** `created_at`, `updated_at`

**iOS Display:**
- **Storage:** Native `Date` type (decoded from ISO 8601)
- **Display:** Convert to user's local timezone
- **Relative:** `RelativeDateTimeFormatter` for "2 hours ago"
- **Absolute:** `DateFormatter` for "Dec 3, 2025 at 10:30 AM"

---

### Communication Patterns

#### Authentication Flow

**JWT Token Management:**

1. **iOS Login:**
   ```swift
   // User logs in via Supabase Auth
   let session = try await supabase.auth.signIn(email: email, password: password)
   let token = session.accessToken // JWT token
   ```

2. **API Request:**
   ```swift
   // iOS sends token in Authorization header
   request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
   ```

3. **Backend Validation:**
   ```python
   # FastAPI middleware validates JWT
   from supabase import create_client
   user = supabase.auth.get_user(jwt_token)
   ```

4. **Token Refresh:**
   - Supabase SDK handles automatic refresh
   - iOS: Monitor session state, re-authenticate if expired

---

#### Streaming (SSE) Pattern

**Backend (FastAPI):**
```python
from fastapi.responses import StreamingResponse

@router.post("/chat/stream")
async def chat_stream(query: str):
    async def generate():
        # Vector search
        results = vector_service.search(query, top_k=5)

        # Stream LLM response token by token
        async for token in llm_service.stream_response(query, results):
            yield f"data: {token}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

**iOS (Swift):**
```swift
// URLSession with event stream
let request = URLRequest(url: chatURL)
let (bytes, _) = try await URLSession.shared.bytes(for: request)

for try await line in bytes.lines {
    if line.hasPrefix("data: ") {
        let token = String(line.dropFirst(6))
        // Update UI with streaming token
    }
}
```

---

### Process Patterns

#### Error Handling Patterns

**LLM API Failures (Graceful, Not Errors):**
- Retry 2-3 times with exponential backoff (100ms, 500ms, 2s)
- After retries exhausted → return graceful response: **"I, Pookie, don't know the answer to that"**
- **NOT shown as error UI** (feels natural, not broken)
- Backend logs failure for debugging

**Network Failures (iOS → Backend):**
- Show user-friendly error: "Connection issue, please try again"
- Don't retry automatically (user can retry manually)
- Log error for debugging
- Cache failed requests for offline mode (post-MVP)

**Validation Errors:**
- Backend returns 422 with specific field errors
- iOS displays field-level error messages
- Example: `{"detail": "Thought text cannot be empty"}`

**Example Error Handling in ViewModel:**
```swift
@Observable class CaptureViewModel {
    var error: String?

    func separateThoughts(_ text: String) async {
        do {
            let separated = try await apiService.separateThoughts(text)
            // Success
        } catch APIError.unauthorized {
            error = "Please log in again"
        } catch APIError.networkError {
            error = "Connection issue, please try again"
        } catch {
            error = "Something went wrong"
        }
    }
}
```

---

#### Loading State Patterns

**iOS ViewModels:**
```swift
@Observable class CaptureViewModel {
    var isLoading: Bool = false           // Generic loading
    var isSeparating: Bool = false        // Specific operation
    var isGeneratingEmbedding: Bool = false
    var error: String?
}
```

**Patterns:**
- Boolean flags for specific operations
- Generic `isLoading` for simple cases
- Specific flags (`isSeparating`, `isGeneratingEmbedding`) for distinct operations
- Views bind to these flags for loading indicators

**Backend:**
- ML operations: Synchronous with reasonable timeout (<30s)
- Long-running operations: Return 202 Accepted (if async processing needed)
- SSE streaming: Progress updates via event stream

---

#### RAG Chat Confidence-Based Fallback

**Hybrid Approach:**

```python
def chat(query: str, user_id: int):
    # 1. Always search FAISS first
    results = vector_service.search(query, top_k=5, user_id=user_id)

    # 2. Check confidence (similarity score)
    if len(results) > 0 and results[0].similarity > 0.7:
        # High confidence → RAG mode (use personal knowledge)
        context = [r.text for r in results]
        return llm_service.rag_chat(query, context)
    else:
        # Low confidence → Direct LLM mode (use general knowledge)
        return llm_service.direct_chat(query)
```

**Two Modes:**
1. **RAG Mode (similarity > 0.7):** Use retrieved thoughts as context
   - Prompt: "Based on these saved thoughts: [context], answer: [query]"
   - Response indicates: "From your thoughts: [answer]"

2. **Direct Mode (similarity < 0.7):** Pure LLM response
   - Prompt: Just the query
   - Response indicates: "General knowledge: [answer]"

---

### Enforcement Guidelines

**All AI Agents MUST:**

1. **Follow cross-platform naming:** Database = snake_case, API JSON = camelCase, code = native conventions
2. **Use established API endpoints:** No creating new endpoints without architectural approval
3. **Implement error handling:** Graceful LLM failures ("I, Pookie, don't know"), user-friendly network errors
4. **Apply loading states:** Boolean flags in ViewModels, reasonable timeouts (<30s)
5. **Use ISO 8601 UTC:** All datetime in API must be UTC strings
6. **Validate with Pydantic:** All request/response bodies use Pydantic schemas with Field aliases
7. **Structure follows patterns:** Files go in designated folders (services/, models/, views/, etc.)
8. **Test coverage:** Write tests for all services and API endpoints

**Pattern Enforcement:**

- **Linting:** ruff (Python), SwiftLint (iOS) - enforce naming conventions
- **Type Checking:** mypy (Python), Swift compiler - catch type mismatches
- **Code Review:** Check for pattern violations before merge
- **Documentation:** Update this document if patterns need to change

---

### Pattern Examples

**Good Examples:**

✅ **Pydantic Schema with Alias:**
```python
class ThoughtCreate(BaseModel):
    thought_text: str = Field(alias="thoughtText", min_length=1)
    abode_id: Optional[int] = Field(alias="abodeId", default=None)
```

✅ **Swift Model (Native camelCase):**
```swift
struct Thought: Codable, Identifiable {
    let id: Int
    let userId: Int
    let thoughtText: String
    let createdAt: Date
}
```

✅ **Graceful LLM Failure:**
```python
try:
    response = await llm_service.generate(prompt)
except LLMAPIError:
    return {"response": "I, Pookie, don't know the answer to that"}
```

✅ **Loading State in ViewModel:**
```swift
@Observable class ChatViewModel {
    var isStreaming: Bool = false

    func sendMessage(_ text: String) async {
        isStreaming = true
        defer { isStreaming = false }
        // ... stream chat
    }
}
```

---

**Anti-Patterns (Avoid These):**

❌ **Inconsistent JSON naming:**
```python
# Bad: mixing snake_case in API JSON
class ThoughtResponse(BaseModel):
    user_id: int  # Should use alias="userId"
```

❌ **Custom CodingKeys when not needed:**
```swift
// Bad: unnecessary CodingKeys (use Pydantic alias instead)
struct Thought: Codable {
    let userId: Int
    enum CodingKeys: String, CodingKey {
        case userId = "user_id"
    }
}
```

❌ **Showing LLM failures as errors:**
```swift
// Bad: treating LLM failure as error
catch {
    showError("API failed") // Should say "I don't know" instead
}
```

❌ **Hardcoded dates:**
```python
# Bad: non-ISO datetime
created_at = "12/03/2025"  # Should be ISO: "2025-12-03T10:30:00Z"
```

## Architecture Summary

### Executive Overview

Pookie is a **dual-platform ML-powered personal knowledge management system** consisting of:
- **iOS native app** (SwiftUI, MVVM with @Observable)
- **Python ML backend** (FastAPI, sentence-transformers, FAISS, LLM integration)
- **Free-tier architecture** optimized for ~$0-3/month operational cost

This architecture document provides comprehensive guidance for AI agents and developers to implement Pookie with consistent, production-ready code across both platforms.

---

### Technology Stack Summary

**Frontend (iOS):**
- Swift 5.9+ with SwiftUI (iOS 17+ for @Observable)
- MVVM architecture with shared AppState
- Supabase Swift SDK for auth
- Native URLSession for API + SSE streaming
- No third-party state management libraries

**Backend (Python):**
- FastAPI (async-first, Python 3.11+)
- SQLAlchemy ORM + Alembic migrations
- Supabase (PostgreSQL + Storage + Auth via JWT)
- sentence-transformers (`all-MiniLM-L6-v2`) for embeddings
- FAISS (local, file-persisted to Supabase Storage)
- OpenRouter (free models) + Claude Haiku for LLMs

**Infrastructure:**
- Backend: Render free tier (750 hours/month)
- Database: Supabase free tier (500MB PostgreSQL, 1GB storage)
- CI/CD: GitHub Actions (automated backend, manual iOS)
- Environment: .env files + environment variables

---

### Core Architectural Decisions Recap

**Critical Decisions:**
1. **Database:** SQLAlchemy Models + Alembic Migrations (type-safe, version-controlled schema)
2. **Authentication:** Supabase JWT validation with supabase-py (secure, automatic token refresh)
3. **API Communication:** REST + SSE for streaming LLM responses (real-time chat UX)
4. **ML Pipeline:** Backend-only embeddings (centralized, single source of truth)
5. **FAISS Persistence:** Supabase Storage for index files (survives restarts, free tier compatible)

**Important Decisions:**
6. **iOS State Management:** ViewModels + Shared AppState (balanced simplicity + scalability)
7. **Mode Orchestration:** Simple sequential Python functions (no framework overhead, FREE)
8. **Error Handling:** Retry with backoff + graceful LLM failures ("I, Pookie, don't know")
9. **Environment Config:** .env files + environment variables (standard, free, simple)
10. **Deployment:** Automated backend CI/CD, manual iOS (cost-effective, practical)

---

### API Endpoints Summary

**8 Total Actions (4 ML Operations + 1 Chat + 3 CRUD):**

| # | Action | Purpose | Endpoint | Method |
|---|--------|---------|----------|--------|
| 1 | **Separate Thoughts** | AI semantic boundary detection for rambling brain dumps | `/api/v1/ml/separate-thoughts` | POST |
| 2 | **RAG Chat** | Converse with personal knowledge (streaming) | `/api/v1/chat/stream` | POST |
| 3 | **Discover** | Explore new experiences using taste reasoning | `/api/v1/ml/discover` | POST |
| 4 | **Link** | Chain-of-thought reasoning from abodes to new concepts | `/api/v1/ml/link` | POST |
| 5 | **Prioritize** | Rank existing thoughts/actions for decision-making | `/api/v1/ml/prioritize` | POST |
| 6 | **List Abodes** | Get all thought clusters/contexts | `/api/v1/abodes` | GET |
| 7 | **Add Thought to Abode** | Organize thought into cluster | `/api/v1/abodes/{abode_id}/thoughts` | POST |
| 8 | **Remove Thought** | Remove thought from cluster | `/api/v1/abodes/{abode_id}/thoughts/{thought_id}` | DELETE |

---

### RAG Pipeline Architecture Summary

**How It Works:**
1. **Embedding Generation:** sentence-transformers converts text → 384-dim vectors (backend-only, <500ms)
2. **Vector Search:** FAISS IndexFlatIP performs cosine similarity (<100ms for <100k vectors)
3. **Confidence Check:** If similarity > 0.7 → RAG mode, else → Direct LLM mode
4. **RAG Mode:** Inject retrieved thoughts as context → Claude Haiku generates personalized response
5. **Direct Mode:** Pure LLM response using inherent training knowledge (no retrieval)

**Performance Expectations:**
- RAG retrieval accuracy: 80%+ for straightforward queries
- Semantic clustering quality: 75-85%
- Thought separation acceptance: 75%+
- Chat response latency: <2 seconds end-to-end

**Evolution Path:**
- **Phase 1 (MVP):** Naive RAG (simple vector retrieval)
- **Phase 2:** Enhanced RAG (hybrid search, re-ranking, query expansion)
- **Phase 3:** Graph-Augmented RAG (knowledge graph layer, 2-hop traversal, relationship-aware)
- **Phase 4:** Agentic RAG (multi-agent query planning, proactive insights)

---

### Implementation Patterns Summary

**Cross-Platform Naming (Critical):**
- **Database:** `snake_case` (user_id, created_at, thought_text)
- **API JSON:** `camelCase` (userId, createdAt, thoughtText)
- **Python Code:** `snake_case` functions/variables, PascalCase classes
- **Swift Code:** camelCase functions/variables, PascalCase classes/structs
- **Transformation:** Pydantic `Field(alias="camelCase")` handles conversion

**Error Handling:**
- **LLM Failures:** Graceful response ("I, Pookie, don't know") after 2-3 retries
- **Network Failures:** User-friendly error ("Connection issue, please try again")
- **Validation Errors:** Field-level errors from backend (422 status)

---

### Implementation Sequence

**Story 0: Project Setup**
1. Create Xcode project → Add Supabase SDK
2. Generate FastAPI backend → `cookiecutter-fastapi-ML`
3. Initialize Git, .gitignore, README

**Foundation (Story 1-3):**
4. Supabase schema (Alembic migrations for users, thoughts, abodes)
5. Auth middleware (JWT validation in FastAPI)
6. iOS AppState + Supabase client setup

**ML Core (Story 4-6):**
7. sentence-transformers service (model loading, embedding generation)
8. FAISS service (index management, search, Supabase Storage persistence)
9. LLM service (OpenRouter/Claude integration, retry logic)

**API Layer (Story 7-10):**
10. REST endpoints (thoughts CRUD, abodes CRUD)
11. SSE streaming endpoint (chat/stream)
12. ML endpoints (separate, discover, link, prioritize)

**iOS Features (Story 11-15):**
13. Capture view + separate thoughts
14. Abode list + detail views
15. Discover mode view
16. Chat view (SSE streaming)

**Modes (Story 16-18):**
17. Tag, reflection, novelty modes (sequential functions)

**CI/CD (Story 19):**
18. GitHub Actions (pytest → Render deploy)

---

### Cross-Component Dependencies

**Critical Path:**
- Auth MUST be implemented before any API endpoints
- FAISS persistence MUST work before clustering
- Embedding service MUST be ready before thought separation
- AppState MUST exist before ViewModels
- SSE streaming enables real-time chat UX

---

### Cost Estimate

**Monthly Operational Cost: ~$0-3**

| Service | Cost |
|---------|------|
| Supabase free tier | $0 |
| Render free tier | $0 |
| sentence-transformers (local) | $0 |
| FAISS (local) | $0 |
| OpenRouter free models | $0 |
| Claude Haiku (pay-per-use) | ~$0-3 |
| **TOTAL** | **~$0-3** |

---

### Readiness for Implementation

**✅ Architecture Complete:**
- All critical decisions made and documented
- Implementation patterns defined
- Project structures specified
- API endpoints designed
- Error handling strategies defined
- Cross-platform naming conventions established

**✅ Ready for Epic/Story Generation:**
- Requirements documented (Product Brief)
- Architecture decisions finalized
- Technical stack chosen
- Integration patterns defined
- Development sequence outlined

**Next Steps:**
1. Generate epics and user stories from Product Brief + Architecture
2. Begin Story 0: Project Setup (Xcode + cookiecutter-fastapi-ML)
3. Implement foundation (auth, schema, core services)
4. Build features iteratively (Capture → Abodes → Discover → Chat)
5. Deploy to TestFlight for testing

---

**Architecture Document Complete. Ready for epic and story generation.**
