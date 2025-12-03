# 🧠 Pookie

**An ML-powered personal knowledge system that transforms your thoughts, notes, and memories into an intelligent, interconnected semantic universe.**

[![iOS](https://img.shields.io/badge/iOS-17%2B-blue.svg)](https://www.apple.com/ios/)
[![Swift](https://img.shields.io/badge/Swift-5.9-orange.svg)](https://swift.org)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Overview

Pookie is a personal knowledge companion that uses machine learning to help you capture, organize, and reflect on your life's moments. Every note, photo, or task becomes a "care" that's semantically understood, automatically organized into thematic "abodes," and interconnected in your personal "Pookie-verse."

### Key Features

- 🤖 **AI-Powered Chat Interface** - Conversational RAG pipeline provides personalized insights and contextual suggestions
- 🎯 **Semantic Clustering (Abodes)** - Automatic grouping of related content using vector embeddings and ML
- 🌐 **Knowledge Graph Visualization** - Interactive "Pookie-verse" showing semantic connections
- 🔄 **Capture → Organize → Reflect** - ML-assisted lifecycle with automated tagging and ranking
- 📊 **Multi-Agent System** - Specialized agents for tagging, reflection, and novelty detection

---

## 🏗️ Architecture

### Tech Stack

**Frontend (iOS)**
- SwiftUI with MVVM architecture
- Native `@Observable` state management (iOS 17+)
- Zero dependencies, pure Swift

**Backend (Python)**
- FastAPI for REST API
- sentence-transformers for local embeddings
- FAISS for vector search
- OpenRouter integration for LLM agents

**Infrastructure**
- Supabase (Auth, PostgreSQL, Storage)
- Render.com (FastAPI hosting)
- Free-tier architecture (~$0-3/month)

### System Components

```
┌─────────────────┐
│   SwiftUI App   │  ← iOS Frontend (MVVM)
└────────┬────────┘
         │
    ┌────▼────────────────────────────────────┐
    │       FastAPI Backend (Render)          │
    ├─────────────────────────────────────────┤
    │  • RAG Pipeline (sentence-transformers) │
    │  • FAISS Vector Search (local)          │
    │  • Multi-Agent System (OpenRouter)      │
    │    - Tag Agent                          │
    │    - Reflection Agent                   │
    │    - Novelty Ranker                     │
    └────┬────────────────────────────────────┘
         │
    ┌────▼──────────────┐
    │     Supabase      │
    │  • PostgreSQL     │
    │  • Auth           │
    │  • Storage        │
    └───────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- **iOS Development:**
  - Xcode 15+
  - iOS 17+ device or simulator

- **Backend Development:**
  - Python 3.11+
  - pip or poetry for dependency management

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/yourusername/pookie.git
cd pookie
```

#### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Supabase and OpenRouter credentials

# Run the server
uvicorn main:app --reload
```

#### 3. iOS Setup

```bash
cd ios/Pookie
open Pookie.xcodeproj

# Configure your Supabase credentials in Config.swift
# Build and run (Cmd+R)
```

---

## 📚 Core Concepts

### Cares
Individual pieces of content - notes, photos, tasks, or thoughts. Each care is:
- Embedded using sentence-transformers
- Automatically tagged by the Tag Agent
- Assigned to an Abode based on semantic similarity
- Ranked by novelty and relevance

### Abodes
Semantic clusters of related cares, automatically discovered through:
- Vector similarity (FAISS nearest-neighbor search)
- KMeans or HDBSCAN clustering
- LLM-generated names and descriptions

### Pookie-Verse
A knowledge graph visualization showing:
- Abodes as nodes
- Semantic relationships as edges
- Interactive exploration of your knowledge landscape

### Multi-Agent System
Specialized AI agents that process your content:
- **Tag Agent** - Categorizes and labels cares
- **Reflection Agent** - Generates summaries and insights
- **Novelty Ranker** - Identifies unique or important content

---

## 🎯 Roadmap

### Phase 1: MVP (Current)
- [x] Architecture decisions finalized
- [ ] Product Brief
- [ ] PRD (Product Requirements Document)
- [ ] Technical Architecture Document
- [ ] Core backend API
- [ ] Basic iOS app with auth
- [ ] Simple care creation and viewing

### Phase 2: Intelligence
- [ ] RAG pipeline with vector search
- [ ] Multi-agent system implementation
- [ ] Automatic abode creation
- [ ] Semantic linking

### Phase 3: Visualization
- [ ] Pookie-verse graph rendering
- [ ] Interactive exploration
- [ ] Advanced filtering and search

### Phase 4: Reflection & Insights
- [ ] Weekly/monthly summaries
- [ ] Trend detection
- [ ] Personalized recommendations

---

## 🤝 Contributing

This is currently a personal project, but suggestions and feedback are welcome! Feel free to:
- Open an issue for bugs or feature requests
- Submit PRs for documentation improvements
- Share your thoughts on architecture decisions

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [sentence-transformers](https://www.sbert.net/) - Semantic embeddings
- [FAISS](https://github.com/facebookresearch/faiss) - Efficient vector search
- [Supabase](https://supabase.com/) - Backend-as-a-Service
- [OpenRouter](https://openrouter.ai/) - LLM API aggregator

---

## 📧 Contact

**Sudy** - [Your Email or Social Links]

**Project Link:** [https://github.com/yourusername/pookie](https://github.com/yourusername/pookie)

---

<div align="center">
Made with ❤️ and a lot of ☕
</div>
