# 🧠 Pookie

**My personalized LLM for my mind and heart - transforming scattered thoughts into an intelligent knowledge companion that actually understands me.**

[![iOS](https://img.shields.io/badge/iOS-17%2B-blue.svg)](https://www.apple.com/ios/)
[![Swift](https://img.shields.io/badge/Swift-5.9-orange.svg)](https://swift.org)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 💭 Why I Built This

I had a problem: my brain dumps ideas everywhere. Screenshots I never look at. Notes that make sense in the moment but are gibberish later. Long rambling paragraphs with 5 different thoughts mixed together. Bookmarks, links, half-formed ideas scattered across apps.

I tried productivity tools - they made it worse. More apps, more complexity, more "systems" I'd abandon after a week. I tried journaling apps - they wanted perfect prose, not messy brain dumps. I tried note-taking apps - they gave me folders and tags but no understanding.

**What I actually needed:** An AI that learns how MY mind works. That understands what I care about. That can take my chaotic thoughts and find the patterns I can't see. A personalized LLM trained on my life, not generic productivity advice.

**So I built Pookie.**

---

## 🎯 What It Does (For Me)

Pookie is my external brain. I dump thoughts into it - messy, unstructured, raw - and it:

### 🤖 **Understands My Chaos**
- I paste rambling paragraphs → **Call Agents Mode** automatically separates distinct thoughts
- I can chat with Pookie to refine: "actually, combine these two" or "split this differently"
- No more manual cleanup - the AI figures out what I actually meant

### 🎯 **Organizes Into "Circles of Care"**
- Vector embeddings automatically cluster related thoughts into semantic groups
- "Career stuff" lives together, "creative ideas" cluster naturally, "personal growth" emerges as a theme
- I don't organize manually - machine learning finds the patterns

### 🔍 **Discovers What I Didn't Know I Cared About**
- **Discover Mode** learns my taste profile from what I save
- Recommends new articles, music, ideas based on MY actual preferences (not algorithmic engagement bait)
- Shows me connections between seemingly unrelated notes

### 💬 **Becomes My Personal LLM**
- RAG pipeline that actually knows my context
- I can ask "what was that idea I had about...?" and it finds it
- Chat interface that understands my knowledge landscape, not generic ChatGPT responses

### 🌐 **Visualizes How I Think**
- **Pookie-verse:** Knowledge graph showing how my thoughts connect
- See abodes as nodes, semantic relationships as edges
- Interactive exploration of my mental landscape

### 🏷️ **Multi-Agent Processing**
- **Tag Agent:** Categorizes my thoughts automatically
- **Reflection Agent:** Generates summaries and insights
- **Novelty Ranker:** Identifies what's actually important vs. noise

---

## 🏗️ How I Built It

I wanted this to be **fast and free** - proving I can build production ML systems on a budget.

### Tech Stack (All Free Tier)

**Frontend (iOS)**
- SwiftUI with MVVM - clean, native, zero dependencies
- `@Observable` state management (iOS 17+)
- Built for my iPhone, the tool I already use constantly

**Backend (Python)**
- **FastAPI** for REST API (simple, fast)
- **sentence-transformers** for local embeddings (no API costs)
- **FAISS** for vector search (local file, 100% free)
- **OpenRouter** with free models for agents (Mistral/Llama)
- **Claude Haiku** for premium chat ($0.25/1M tokens - pennies/month)

**Infrastructure**
- **Supabase** free tier (Auth, PostgreSQL, Storage)
- **Render.com** free tier (750 hours/month hosting)
- **Total cost:** ~$0-3/month

### Architecture

```
┌─────────────────────────────────────┐
│      My iPhone (SwiftUI App)        │
│  Where I dump all my thoughts       │
└─────────────┬───────────────────────┘
              │
         ┌────▼──────────────────────────────┐
         │   FastAPI Backend (Render)        │
         ├───────────────────────────────────┤
         │  RAG Pipeline                     │
         │  • sentence-transformers (local)  │
         │  • FAISS vector search (local)    │
         │                                   │
         │  Multi-Agent System (OpenRouter)  │
         │  • Tag Agent (free models)        │
         │  • Reflection Agent (free)        │
         │  • Novelty Ranker (free)          │
         │  • Chat (Claude Haiku - cheap)    │
         └─────────┬─────────────────────────┘
                   │
         ┌─────────▼──────────────┐
         │      Supabase          │
         │  • PostgreSQL (my DB)  │
         │  • Auth                │
         │  • File Storage        │
         └────────────────────────┘
```

**Why This Stack:**
- Proves I can build full-stack ML systems
- Demonstrates cost-conscious architecture decisions
- Shows I understand modern AI/ML tooling
- Résumé-worthy: RAG, vector search, multi-agent systems, embeddings

---

## 🚀 Getting Started

Want to run this yourself? Here's how:

### Prerequisites

- Xcode 15+ (for iOS app)
- Python 3.11+
- Supabase account (free)
- OpenRouter account (free tier available)

### Installation

#### 1. Clone the repo

```bash
git clone https://github.com/yourusername/pookie.git
cd pookie
```

#### 2. Supabase Setup

**Create Supabase Project:**

1. Go to [https://supabase.com/dashboard](https://supabase.com/dashboard)
2. Click "New Project"
3. Configure:
   - **Project Name:** Pookie
   - **Database Password:** Generate a strong password (save in password manager!)
   - **Region:** Closest to your location
   - **Pricing Plan:** Free tier
4. Wait 2-5 minutes for provisioning

**Collect Credentials:**

1. In Supabase dashboard → Settings → API
2. Copy and save these values:
   - **Project URL** (e.g., `https://xxx.supabase.co`)
   - **anon public key** (safe to expose in iOS app)
   - **service_role key** (⚠️ SECRET - backend only!)
3. Database host: In Settings → Database → Connection string → Connection pooler URL
   - Format: `aws-X-REGION.pooler.supabase.com`

**⚠️ CRITICAL SECURITY:**
- ✅ iOS gets: `SUPABASE_URL` + `SUPABASE_ANON_KEY`
- ✅ Backend gets: All 3 keys (URL, anon, service_role)
- ❌ NEVER put `service_role` key in iOS (full database access!)
- ❌ NEVER commit `.env` or `Config.plist` to git

**Free Tier Limits:**
- Database: 500MB (~50k-100k thoughts at 1KB avg)
- Storage: 1GB (for FAISS index files)
- Bandwidth: 2GB egress/month
- Auto-pauses after 1 week inactivity (wakes on first request)

#### 3. Backend Setup

```bash
cd backend/pookie-backend
poetry install

# Configure environment variables
cp .env.example .env
```

**Edit `.env` and add:**
```bash
# Supabase credentials
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_ANON_KEY=your_anon_public_key_here
SUPABASE_SERVICE_KEY=your_service_role_key_here

# Database URL for Alembic migrations
# Format: postgresql://postgres.PROJECT_ID:PASSWORD@HOST:5432/postgres
# Use connection pooler for IPv4 compatibility
DATABASE_URL=postgresql://postgres.YOUR_PROJECT_ID:YOUR_DB_PASSWORD@aws-1-us-east-2.pooler.supabase.com:5432/postgres

# OpenRouter (for LLM agents)
OPENROUTER_API_KEY=your_openrouter_key_here
```

**Run database migrations:**
```bash
# DATABASE_URL must be set in .env or environment
poetry run alembic upgrade head

# Verify tables created
# Check Supabase dashboard → Table Editor
# Should see: users, thoughts, circles, intentions, intention_cares, stories
```

**Run development server:**
```bash
poetry run uvicorn app.main:app --reload
```

#### 4. iOS Setup

```bash
cd ios/Pookie/Pookie/Resources
cp Config.plist.example Config.plist  # If template exists
```

**Edit `Config.plist` and add:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>SUPABASE_URL</key>
    <string>https://YOUR_PROJECT_ID.supabase.co</string>
    <key>SUPABASE_ANON_KEY</key>
    <string>your_anon_public_key_here</string>
</dict>
</plist>
```

**Verify Config.plist is gitignored:**
```bash
git status  # Should NOT show Config.plist
git check-ignore -v ios/Pookie/Pookie/Resources/Config.plist  # Should match .gitignore
```

**Build and run:**
```bash
cd ios/Pookie
open Pookie.xcodeproj
# In Xcode: Cmd+R to build and run
```

---

## 📚 Core Concepts

### Cares
Anything I save - notes, photos, random thoughts, links I screenshot from TikTok. Each one gets:
- Embedded using sentence-transformers
- Auto-tagged by the Tag Agent
- Assigned to an Abode (semantic cluster)
- Ranked by novelty (is this actually new/important?)

### Abodes
Semantic clusters that emerge from my cares:
- Not folders I manually create - patterns the AI discovers
- Named automatically by LLM based on content
- Connected through vector similarity
- Visualized in the Pookie-verse graph

### Call Agents Mode
My favorite feature:
1. I paste a long rambling paragraph
2. Agents identify semantic boundaries and separate thoughts
3. I chat with Pookie to refine: "split that differently" or "merge these"
4. Get organized notes from brain dump chaos

### Discover Mode
AI learns MY taste from what I save:
- Recommends articles I'd actually want to read
- Suggests music based on my actual preferences
- Finds patterns in what I care about
- Not generic algorithms - personalized to me

### Pookie-Verse
Interactive knowledge graph showing:
- How my thoughts cluster into abodes
- Connections between seemingly unrelated ideas
- Visual map of my mental landscape

---

## 🧪 MVP: Training a Pet for the Mind

The first goal is simple but ambitious: **see to what extent I can train an LLM using user feedback.** I'm building Pookie as a "pet for the mind" - an AI that learns what I care about through interaction, not just pattern matching.

### Why Centroid-Based Reinforcement Learning?

I chose a hybrid architecture combining **FAISS vector search** with **dynamic centroid tracking** because:

- **Base Embeddings (sentence-transformers):** Give me generic semantic understanding - "hunger" and "eating" are similar in anyone's language
- **Circle Centroids:** Let me build **personalized semantic categories** - when I mark items as "desires" (not "food"), the centroid shifts to represent MY concept of desire
- **Incremental Learning:** Every time I assign something to a circle, the centroid updates: `centroid_new = (N * centroid_old + embedding_new) / (N + 1)` - simple math, powerful results
- **Hybrid Retrieval:** When I search or chat, Pookie uses **40% base similarity + 40% centroid similarity + 15% user feedback boost** - balancing universal understanding with personal meaning

This isn't just RAG. It's **personalized semantic retrieval** where the system evolves with my feedback. The learning signals (`is_user_assigned`, `confidence_score`) create a reinforcement loop:
1. Pookie predicts → I correct → Centroid shifts → Next prediction improves

It's reinforcement learning without neural network complexity - just vector geometry and user feedback. Efficient, interpretable, and it actually learns.

### ML Architecture: The Technical Stack

**Why FAISS + Centroids (Not Fine-tuning)?**
- FAISS gives me fast similarity search over 384-dim embeddings (millions of items, milliseconds)
- Centroids add a custom semantic layer on top of base embeddings - no retraining needed
- I can update centroids incrementally in real-time (no batching, no GPU, no training runs)
- One database column (`circles.centroid_embedding FLOAT[384]`) - that's it

**Why sentence-transformers (all-MiniLM-L6-v2)?**
- Runs locally (no API costs, no rate limits, no privacy concerns)
- 384-dim embeddings are perfect for centroid averaging (compact but rich)
- Pre-trained on semantic search tasks (MS MARCO, natural questions)
- Fast enough for real-time embedding generation

**Why Personalized RAG?**
- Vanilla RAG retrieves based on universal semantics - "I'm hungry" finds food
- My personalized RAG layers circle centroids on top - "I'm hungry" finds MY concept of desire (if that's my pattern)
- The system learns: generic similarity gets me candidates, centroids re-rank for personal relevance

It's a cognitive architecture, not a search engine.

---

## 🚀 Future: Circles of Care (Full Vision)

Once the core RL loop works, I'm building the complete experience:

### 🌍 Reality Integration: Space, Time, and Shared Meaning
- **Attach meaning to physical reality:** Tag locations, moments, real-world objects
- **Collect cares in the real world:** AR experience where your circles exist in space
- **Sharable semantic anchors:** Friends can see what locations mean to YOU (not generic POI data)
- **Pookie learns from your physical patterns:** Where you go, when, what you think about there
- **Think: Pokémon GO meets personal knowledge** - discover your cares in the real world

### 🎭 User Vibe Profiles
- **Your vibe = your circle centroids:** Each circle represents a facet of your personality
- **Vibe evolution tracking:** See how your interests shift over time (centroid drift visualization)
- **Cross-user vibe matching:** Find people with similar circles (semantic compatibility)
- **Privacy-preserving:** Share vibes without exposing raw content

### 🧠 Advanced ML Capabilities
- **Voice capture:** Speak your thoughts, get real-time transcription + circle predictions
- **Call Agents Mode:** Paste rambling paragraphs → AI separates distinct thoughts → you refine via chat
- **Discover Mode:** Recommendations based on YOUR circle centroids (not algorithmic engagement)
- **Story Page:** Timeline visualization of how your thoughts connect over time
- **Graph exploration:** Interactive Pookie-verse showing semantic relationships

### 💎 The Full Experience
- Multi-circle assignments (one thought, multiple circles)
- Confidence-based predictions (high confidence = auto-assign, low = suggest)
- Learning from corrections (every edit makes Pookie smarter)
- Cross-device sync (iOS + web, eventually Android)
- Offline-first architecture (work without internet, sync later)
- Export your knowledge (own your data, always)

**The Goal:** Turn reality into something you can model, share, and experience through circles of care. Your mind's landscape, augmented onto the physical world.

---

## 💡 Why This Matters (For My Résumé)

This project demonstrates:

✅ **Reinforcement learning from human feedback:** Centroid-based RL loop that improves predictions through user corrections
✅ **Personalized semantic architectures:** Hybrid FAISS + centroid retrieval (not just vanilla RAG)
✅ **End-to-end ML systems:** Embeddings, vector search, incremental learning, multi-stage retrieval
✅ **Full-stack development:** iOS (SwiftUI + @Observable) + Backend (FastAPI + async/await)
✅ **Advanced ML techniques:** sentence-transformers, FAISS indexing, hybrid similarity scoring, learning signals
✅ **Cost-conscious engineering:** Free-tier architecture (~$0-3/month) proving technical efficiency
✅ **Product thinking:** Real problem, real solution - not just a tech demo
✅ **Modern patterns:** SwiftUI MVVM, SQLAlchemy async, SSE streaming, JWT auth

**The pitch:** "I built a cognitive architecture that learns MY personal semantics through feedback - using centroid-based RL, hybrid vector retrieval, and incremental learning. It's reinforcement learning without the GPU bills, running entirely on free tiers to prove I understand both ML theory and pragmatic engineering."

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

This is a personal project, but I'm sharing the code to show my work.

---

## 🙏 Built With

- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [sentence-transformers](https://www.sbert.net/) - Local embeddings
- [FAISS](https://github.com/facebookresearch/faiss) - Vector search
- [Supabase](https://supabase.com/) - Database and auth
- [OpenRouter](https://openrouter.ai/) - LLM API aggregation
- SwiftUI - iOS frontend
- A lot of late nights and coffee ☕

---

## 📧 Contact

**Sudy** - Building AI tools for myself, sharing what I learn

**Project Link:** [https://github.com/yourusername/pookie](https://github.com/yourusername/pookie)

---

<div align="center">

**Pookie: Because my brain needed an AI that actually gets me.**

Built with ❤️ for me, by me

</div>
