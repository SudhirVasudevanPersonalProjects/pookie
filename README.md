# 🧠 Pookie

**Personal LLM with Centroid-Based Reinforcement Learning**

[![iOS](https://img.shields.io/badge/iOS-17%2B-blue.svg)](https://www.apple.com/ios/)
[![Swift](https://img.shields.io/badge/Swift-5.9-orange.svg)](https://swift.org)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 💡 Why I Built This

**The Problem:** ChatGPT doesn't know me. It's great for generic questions, but it has no memory of what I care about, my projects, or my personal knowledge. Every conversation starts from zero.

**What I Tried:**
- Note-taking apps: Manual organization, no intelligence
- Notion/Obsidian: Great for structured docs, terrible for quick thoughts
- Apple Notes: Easy capture, impossible to find anything later
- RAG tools: Generic retrieval, no personalization

**What I Actually Needed:** An AI that learns my personal semantics. Not just "what does 'running' mean in general?" but "why do I care for 'running'?" (Anime scenes, goals to lose weight, goals to increase ability to move).

**So I built Pookie** - a personal LLM powered by centroid-based reinforcement learning that learns from user feedback in real-time, over time.

---

## 🎯 What It Does

Pookie is a personalized knowledge companion with four core capabilities:

### 1. 📝 Capture Anything (Somethings)
- Quick text capture for thoughts, ideas, notes, quotes
- Automatic semantic embedding (sentence-transformers, local, fast)
- Voice capture coming in v2 (iOS Speech Recognition)

### 2. 🎯 ML-Powered Organization (Circles)
- **K-means clustering** automatically organizes somethings into semantic circles
- **LLM-generated names** for each circle (e.g., "Career Growth", "Creative Ideas")
- **Centroid-based predictions** suggest which circle new somethings belong to
- **Reinforcement learning loop**: When you correct predictions, centroids shift to match YOUR semantics (In-Progress)

### 3. 💬 Personalized Chat (RAG)
- Chat with YOUR knowledge base, not generic ChatGPT
- **Hybrid retrieval scoring**: 40% base FAISS + 40% circle centroids + 15% user feedback + 5% recency
- Streaming responses (Server-Sent Events with Claude Haiku)
- See which circles informed each answer

### 4. 🎯 Care Hierarchy (Intentions → Actions)
- **Intentions**: High-level goals linked to circles of care
- **Actions**: Concrete steps toward intentions
- Track what you're doing and why it matters
- Knowledge Graph Visualization (In-Progress)

---

## 🧪 The ML Innovation: Centroid-Based RL

**Why not fine-tuning?**
- Fine-tuning takes hours/days and requires GPUs
- Centroid updates take <50ms and run on a free-tier CPU
- Centroids are interpretable (you can visualize how they shift)
- Real-time learning: feedback → centroid update → better predictions immediately

**How it works:**

1. **Base Embeddings (sentence-transformers):**
   ```
   "I want to run a 5K" → [0.23, -0.15, 0.08, ..., 0.42]  # 384-dim vector
   ```

2. **Circle Centroids (incremental mean):**
   ```python
   # When you assign something to a circle:
   centroid_new = (N * centroid_old + embedding_new) / (N + 1)

   # When you remove something:
   centroid_new = ((N + 1) * centroid_old - embedding_removed) / N
   ```

3. **Hybrid Similarity Scoring:**
   ```python
   final_score = (
       0.40 * cosine_similarity(query, embedding_base) +      # Universal semantics
       0.40 * cosine_similarity(query, circle_centroid) +     # Personal semantics
       0.15 * (1.0 if is_user_assigned else 0.0) +            # User feedback boost
       0.05 * recency_score                                    # Time decay
   )
   ```

4. **Learning Loop:**
   ```
   User creates something → System predicts Circle A (0.75 confidence)
                          ↓
   User corrects: "Actually, Circle B" → Centroid B shifts toward new embedding
                          ↓
   Next similar something → System predicts Circle B (0.85 confidence) ✨
   ```

**Result:** Personalized semantic retrieval that learns YOUR meaning of concepts, not Wikipedia's.

---

## 🏗️ Architecture

### System Diagram

```mermaid
graph TD
    A[iOS App - SwiftUI] -->|HTTPS| B[FastAPI Backend]
    B -->|Auth| C[Supabase Auth]
    B -->|CRUD| D[PostgreSQL - Supabase]
    B -->|Embeddings| E[sentence-transformers - Local]
    B -->|Vector Search| F[FAISS Index - Local File]
    B -->|LLM Chat| G[OpenRouter - Claude Haiku]

    style A fill:#e1f5ff
    style B fill:#fff3e0
    style E fill:#f3e5f5
    style F fill:#f3e5f5
    style G fill:#f3e5f5
```

### ML Pipeline

```mermaid
graph LR
    A[User Input] --> B[sentence-transformers]
    B --> C[384-dim embedding]
    C --> D[FAISS Search - Top 50]
    D --> E[Centroid Re-ranking]
    E --> F[Top 10 Results]
    F --> G[Claude Haiku RAG]
    G --> H[Streaming Response]

    I[User Feedback] --> J[Centroid Update]
    J --> E

    style B fill:#f3e5f5
    style D fill:#f3e5f5
    style E fill:#fff9c4
    style G fill:#f3e5f5
    style J fill:#fff9c4
```

### Data Model

```mermaid
erDiagram
    USERS ||--o{ SOMETHINGS : owns
    SOMETHINGS ||--o{ SOMETHING_CIRCLES : belongs_to
    CIRCLES ||--o{ SOMETHING_CIRCLES : contains
    USERS ||--o{ CIRCLES : owns
    CIRCLES ||--o{ INTENTIONS : related_to
    INTENTIONS ||--o{ ACTIONS : has

    USERS {
        uuid id PK
        string email
        timestamp created_at
    }

    SOMETHINGS {
        uuid id PK
        uuid user_id FK
        text content
        float[] embedding
        timestamp created_at
    }

    CIRCLES {
        uuid id PK
        uuid user_id FK
        string name
        float[] centroid_embedding
        int member_count
        timestamp created_at
    }

    SOMETHING_CIRCLES {
        uuid something_id FK
        uuid circle_id FK
        float confidence_score
        bool is_user_assigned
        timestamp created_at
    }

    INTENTIONS {
        uuid id PK
        uuid user_id FK
        string title
        text description
        timestamp created_at
    }

    ACTIONS {
        uuid id PK
        uuid intention_id FK
        string title
        text description
        timestamp created_at
    }
```

---

## 🚀 Getting Started

### Prerequisites

- **Xcode 15+** (for iOS app)
- **Python 3.11+**
- **Poetry** (Python dependency management)
- **Supabase account** (free tier)
- **OpenRouter account** (optional, for chat features)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/pookie.git
cd pookie
```

### 2. Supabase Setup

**Create Project:**
1. Go to [supabase.com/dashboard](https://supabase.com/dashboard)
2. Click "New Project"
3. Choose: Name = "Pookie", Region = closest to you, Free tier
4. Wait 2-5 minutes for provisioning

**Collect Credentials:**
- Navigate to: Settings → API
- Copy:
  - **Project URL**: `https://YOUR_PROJECT_ID.supabase.co`
  - **anon public key**: `eyJxxx...` (safe for iOS)
  - **service_role key**: `eyJxxx...` (⚠️ SECRET - backend only!)

**Get Database URL:**
- Navigate to: Settings → Database → Connection string
- Select "Connection pooler" (for better IPv4 compatibility)
- Copy: `postgresql://postgres.PROJECT_ID:PASSWORD@aws-X-REGION.pooler.supabase.com:5432/postgres`

### 3. Backend Setup

```bash
cd backend/pookie-backend

# Install dependencies
poetry install

# Create environment file
cp .env.example .env
```

**Edit `.env`:**
```bash
# Supabase
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_ANON_KEY=your_anon_public_key
SUPABASE_SERVICE_KEY=your_service_role_key  # ⚠️ NEVER commit this

# Database (for migrations)
DATABASE_URL=postgresql://postgres.PROJECT_ID:PASSWORD@aws-1-us-east-2.pooler.supabase.com:5432/postgres

# OpenRouter (optional - chat will fail gracefully if not set)
OPENROUTER_API_KEY=your_openrouter_key

# FastAPI
SECRET_KEY=random-64-char-string-here
DEBUG=True
ENVIRONMENT=development
```

**Run Migrations:**
```bash
# DATABASE_URL must be set in .env
poetry run alembic upgrade head

# Verify in Supabase dashboard → Table Editor
# Should see: users, somethings, circles, something_circles, intentions, actions
```

**Start Server:**
```bash
poetry run uvicorn app.main:app --reload

# Server starts at: http://localhost:8000
# Swagger docs at: http://localhost:8000/docs
```

**Verify Health:**
```bash
curl http://localhost:8000/api/v1/health
# Should return: {"status":"healthy"}
```

### 4. iOS Setup

```bash
cd ios/Pookie/Pookie/Resources

# Create config from template
cp Config.plist.example Config.plist
```

**Edit `Config.plist`:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>SUPABASE_URL</key>
    <string>https://YOUR_PROJECT_ID.supabase.co</string>
    <key>SUPABASE_ANON_KEY</key>
    <string>your_anon_public_key_here</string>
</dict>
</plist>
```

**Verify Config is Gitignored:**
```bash
git check-ignore ios/Pookie/Pookie/Resources/Config.plist
# Should match .gitignore pattern
```

**Build and Run:**
```bash
cd ios/Pookie
open Pookie.xcodeproj

# In Xcode: Cmd+R to build and run on simulator
```

### 5. Verify Everything Works

1. **Sign up** with email/password in iOS app
2. **Create a something**: "I want to learn SwiftUI"
3. **Check backend logs**: Should see embedding generation
4. **Navigate to Circles**: After 5+ somethings, circles appear
5. **Try chat**: Ask "what have I been thinking about?"

---

## 📊 Performance Benchmarks

| Operation | Target | Actual (M1 MacBook) |
|-----------|--------|---------------------|
| Embedding generation | <200ms | ~150ms |
| Centroid calculation | <50ms | ~30ms |
| FAISS search (50 items) | <100ms | ~60ms |
| Hybrid re-ranking (50→10) | <100ms | ~70ms |
| Full RAG pipeline | <300ms | ~250ms |
| LLM first token | <500ms | ~400ms |
| Complete chat response | <2s | ~1.5s |

**Cost (Free Tier):**
- **Backend hosting (Render):** $0/month (750 hours free)
- **Database (Supabase):** $0/month (500MB limit)
- **Embeddings (local):** $0/month (no API)
- **Vector search (FAISS):** $0/month (local file)
- **LLM chat (Claude Haiku):** ~$0.50-3/month (depending on usage)

**Total:** ~$0-3/month for a personal AI system 🎉

---

## 📚 Project Structure

```
pookie/
├── backend/pookie-backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/routes/              # REST endpoints
│   │   ├── core/                    # Config, security, events
│   │   ├── models/                  # SQLAlchemy ORM models
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── services/                # Business logic
│   │   │   ├── centroid_service.py  # Centroid RL logic
│   │   │   ├── embedding_service.py # sentence-transformers
│   │   │   ├── faiss_service.py     # Vector search
│   │   │   ├── personalized_retrieval_service.py  # Hybrid scoring
│   │   │   ├── clustering_service.py  # K-means
│   │   │   └── llm_service.py       # OpenRouter integration
│   │   └── main.py                  # FastAPI app entry
│   ├── alembic/                     # Database migrations
│   ├── tests/                       # Pytest test suite
│   ├── pyproject.toml               # Poetry dependencies
│   ├── Dockerfile                   # Production deployment
│   └── .env.example                 # Environment template
│
├── ios/Pookie/                      # iOS SwiftUI app
│   ├── Pookie/
│   │   ├── App/                     # App entry point
│   │   ├── Models/                  # Data models
│   │   ├── ViewModels/              # MVVM view models
│   │   ├── Views/                   # SwiftUI views
│   │   │   ├── Capture/             # Something creation UI
│   │   │   └── Chat/                # RAG chat UI
│   │   ├── Services/                # API client, SSE client
│   │   └── Resources/
│   │       └── Config.plist.example # Supabase config template
│   └── PookieTests/                 # XCTest unit tests
│
└── docs/                            # Documentation
    ├── DEMO-SCRIPT.md               # 7-minute demo walkthrough
    ├── ML-ARCHITECTURE.md           # Detailed ML system design
    ├── pookie-semantic-architecture.md  # Centroid RL architecture
    └── sprint-artifacts/            # Development tracking
```

---

## 🧪 Testing

**Backend Tests:**
```bash
cd backend/pookie-backend

# Run all tests
DATABASE_URL="..." poetry run pytest

# Run specific test suites
poetry run pytest tests/test_centroid_service.py  # Centroid math validation
poetry run pytest tests/test_rl_learning_loop.py  # RL learning verification
poetry run pytest tests/test_hybrid_rag_scoring.py  # Hybrid scoring tests

# With coverage
poetry run pytest --cov=app --cov-report=html
```

**iOS Tests:**
```bash
cd ios/Pookie

# Run in Xcode: Cmd+U
# Or via command line:
xcodebuild test -scheme Pookie -destination 'platform=iOS Simulator,name=iPhone 15'
```

**Test Coverage:**
- Centroid Service: 95%+ (9 tests covering all formulas)
- RL Learning Loop: 100% (5 tests validating feedback cycle)
- Hybrid RAG Scoring: 90%+ (6 tests verifying personalization)
- API Endpoints: 85%+ (integration tests for all routes)

---

## 🚢 Deployment

### Backend (Render)

1. **Create Render Account**: [render.com](https://render.com)
2. **New Web Service**:
   - Connect GitHub repo: `yourusername/pookie`
   - Root Directory: `backend/pookie-backend`
   - Build Command: `poetry install`
   - Start Command: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. **Environment Variables** (in Render dashboard):
   ```
   SUPABASE_URL=https://xxx.supabase.co
   SUPABASE_ANON_KEY=eyJxxx...
   SUPABASE_SERVICE_KEY=eyJxxx...
   DATABASE_URL=postgresql://...
   OPENROUTER_API_KEY=sk-xxx...
   SECRET_KEY=random-64-chars
   ENVIRONMENT=production
   ```
4. **Auto-Deploy**: Enabled on push to `main` branch

**Verify Deployment:**
```bash
curl https://pookie-backend-xxx.onrender.com/api/v1/health
# {"status":"healthy"}
```

### iOS (TestFlight)

1. **Update Config**: Point to production Supabase
2. **Xcode Archive**: Product → Archive
3. **Upload to App Store Connect**: Organizer → Distribute App
4. **TestFlight**: Configure beta testing
5. **Invite Testers**: Internal testing group

---

## 🔒 Security

**DO NOT COMMIT:**
- ❌ `backend/pookie-backend/.env` (contains `SUPABASE_SERVICE_KEY`)
- ❌ `ios/Pookie/Pookie/Resources/Config.plist` (already gitignored)
- ❌ `alembic.ini` (may contain database credentials)

**Verify secrets are gitignored:**
```bash
git check-ignore .env
git check-ignore ios/Pookie/Pookie/Resources/Config.plist

# Check git history for leaks
git log --all -- '*.env' '*.plist'  # Should be empty
```

**If secrets leaked:**
1. Rotate keys immediately in Supabase dashboard
2. Update `.env` and Config.plist with new keys
3. Redeploy backend

---

## 🔮 Future Vision (v2)

**Advanced ML Features:**
- **Voice capture**: iOS Speech Recognition for real-time thought capture
- **Multi-circle assignments**: One something, multiple relevant circles
- **Confidence thresholds**: Auto-assign high confidence, suggest low confidence
- **Learning analytics**: Visualize how centroids evolve over time
- **Cross-user vibe matching**: Find people with similar circle patterns (privacy-preserving)

**Reality Integration:**
- **AR knowledge graph**: Visualize circles in 3D space
- **Location tagging**: Attach thoughts to physical places
- **Cross-device sync**: iOS + Web + Android
- **Offline-first**: Work without internet, sync later

**Discovery Mode:**
- **Recommendation engine**: Suggest articles/music based on YOUR circles
- **Pattern detection**: "You think about X when Y happens"
- **Reflection prompts**: Weekly summaries of circle activity

---

## 💡 Why This Matters (Recruiting Narrative)

This project demonstrates:

✅ **Reinforcement learning from human feedback**: Centroid-based RL that learns in real-time (<50ms updates)
✅ **Personalized semantic architectures**: Hybrid FAISS + centroid retrieval (not vanilla RAG)
✅ **End-to-end ML systems**: Embeddings → Vector search → Incremental learning → Multi-stage retrieval
✅ **Full-stack development**: iOS (SwiftUI + @Observable) + Backend (FastAPI + async/await)
✅ **Advanced ML techniques**: sentence-transformers, FAISS, hybrid scoring, learning signals
✅ **Cost-conscious engineering**: Free-tier architecture (~$0-3/month) proving technical efficiency
✅ **Product thinking**: Real problem, real solution - not just a tech demo
✅ **Modern patterns**: SwiftUI MVVM, SQLAlchemy async, SSE streaming, JWT auth

**The pitch:** "I built a cognitive architecture that learns personal semantics through feedback - using centroid-based RL, hybrid vector retrieval, and incremental learning. It's reinforcement learning without the GPU bills, running entirely on free tiers to prove I understand both ML theory and pragmatic engineering."

---

## 📖 Further Reading

- **[DEMO-SCRIPT.md](docs/DEMO-SCRIPT.md)**: 7-minute recruiting demo walkthrough
- **[ML-ARCHITECTURE.md](docs/ML-ARCHITECTURE.md)**: Deep dive into centroid RL system
- **[pookie-semantic-architecture.md](docs/pookie-semantic-architecture.md)**: Full system architecture document

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

This is a personal project built to demonstrate ML engineering skills.

---

## 🙏 Acknowledgments

**Technologies:**
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [sentence-transformers](https://www.sbert.net/) - Semantic embeddings
- [FAISS](https://github.com/facebookresearch/faiss) - Facebook AI Similarity Search
- [Supabase](https://supabase.com/) - Open-source Firebase alternative
- [OpenRouter](https://openrouter.ai/) - LLM API aggregation
- [SwiftUI](https://developer.apple.com/xcode/swiftui/) - Apple's declarative UI framework

**Inspiration:**
- Personal frustration with generic productivity tools
- Research in personalized learning systems
- Belief that AI should adapt to humans, not the other way around

---

## 📧 Contact

**Sudy** - Building AI tools that actually understand me

**Demo:** [Coming Soon - TestFlight Link]
**Project:** [github.com/yourusername/pookie](https://github.com/yourusername/pookie)

---

<div align="center">

**Pookie: Because my brain needed an AI that actually gets me.**

Built with ❤️ and late nights ☕

</div>
