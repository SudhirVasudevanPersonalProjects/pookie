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

### 🎯 **Organizes Into "Abodes"**
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

#### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your Supabase and OpenRouter credentials

# Run the server
uvicorn main:app --reload
```

#### 3. iOS Setup

```bash
cd ios/Pookie
open Pookie.xcodeproj

# Configure Supabase credentials in Config.swift
# Build and run (Cmd+R)
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

## 🎯 What I'm Building

### Phase 1: MVP (Current)
- [x] Architecture decisions (free-tier everything)
- [ ] Product Brief (defining the vision)
- [ ] PRD (detailed requirements)
- [ ] Core backend API
- [ ] iOS app with auth
- [ ] Basic care creation and viewing

### Phase 2: Intelligence
- [ ] RAG pipeline with vector search
- [ ] Multi-agent system (Tag, Reflection, Novelty)
- [ ] Automatic abode creation
- [ ] Call Agents Mode (thought separation)

### Phase 3: Discovery
- [ ] Discover Mode (taste-based recommendations)
- [ ] Pookie-verse graph visualization
- [ ] Interactive knowledge exploration

### Phase 4: Personalization
- [ ] Learn from my corrections (interactive ML)
- [ ] Weekly/monthly reflection summaries
- [ ] Pattern detection in my thinking
- [ ] Truly personalized LLM for my mind

---

## 💡 Why This Matters (For My Résumé)

This project demonstrates:

✅ **End-to-end LLM application:** RAG pipeline, embeddings, vector search
✅ **Multi-agent AI systems:** Orchestrating specialized agents
✅ **Full-stack development:** iOS (SwiftUI) + Backend (Python/FastAPI)
✅ **ML/AI integration:** sentence-transformers, FAISS, OpenRouter
✅ **Cost-conscious architecture:** Free-tier everything (~$0-3/month)
✅ **Product thinking:** Built to solve my real problem, not just tech demo
✅ **Modern tooling:** Supabase, Render, latest iOS patterns

**The pitch:** "I built my own personalized LLM that understands my thoughts, separates my brain dumps automatically, and discovers patterns in how I think - all running on free tiers to prove technical efficiency."

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
