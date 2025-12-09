# Pookie - Epic Breakdown

**Author:** sudy
**Date:** 2025-12-03
**Project Level:** Medium-High Complexity
**Target Scale:** Personal use (<100k thoughts, single user)

---

## Overview

This document provides the complete epic and story breakdown for Pookie, decomposing the requirements from the [Product Brief](./analysis/product-brief-Pookie-2025-12-02.md) into implementable stories.

**Context Documents:**
- Product Brief: Complete ✅
- Architecture: Complete ✅
- UX Design: Not applicable for MVP

---

## Context Analysis

### Product Requirements Overview

Pookie is a personalized LLM-powered iOS app solving the "scattered thoughts" problem through four core capabilities:

1. **Call Agents Mode** - AI-powered thought separation from rambling brain dumps
2. **Semantic Clustering (Abodes)** - Automatic grouping of related thoughts via vector embeddings
3. **Discover Mode** - Personalized action recommendations based on taste learning
4. **RAG Chat** - Personal knowledge assistant using vector search + LLM

**Technical Constraints:**
- Free-tier architecture (~$0-3/month)
- Dual platform: iOS (SwiftUI) + Python (FastAPI)
- ML pipeline: sentence-transformers, FAISS, Claude Haiku
- Accuracy targets: 75-80%+ for all ML operations

---

## Functional Requirements Inventory

### Core Functional Requirements (From Product Brief)

**FR1: User Authentication & Profile Management**
- User can create account with email/password
- User can log in and maintain session
- JWT token management and refresh
- User profile storage

**FR2: Thought Capture (Text Input)**
- User can input text thoughts via text field
- User can save thoughts as-is
- Thoughts stored with timestamp and user association

**FR3: Thought Capture (Voice Input)**
- User can input thoughts via voice (speech-to-text)
- iOS native voice recognition integration
- Voice converted to text and saved

**FR4: Call Agents Mode - Thought Separation**
- User can trigger "Separate & Save" on text input
- AI identifies semantic boundaries in rambling paragraphs
- AI splits distinct thoughts automatically
- User can refine separation via chat ("split differently", "combine these")
- Each separated thought saved as discrete entity

**FR5: Semantic Clustering (Abodes) - Automatic Grouping**
- System generates embeddings for all thoughts (384-dim vectors)
- System clusters related thoughts into thematic "abodes" using vector similarity
- Clustering algorithm: K-means or DBSCAN
- Abodes updated dynamically as new thoughts added
- Target: Minimal manual reorganization needed

**FR6: Abode Naming & Management**
- LLM generates descriptive names for discovered abodes
- User can view list of abodes with thought counts
- User can view thoughts within specific abode
- User can manually add/remove thoughts from abodes

**FR7: RAG-Powered Chat Interface**
- User can ask natural language queries about saved thoughts
- System performs vector search across all thoughts (FAISS)
- System retrieves top-k relevant thoughts (k=5-10)
- LLM generates personalized response using retrieved context
- Target: 80%+ retrieval accuracy

**FR8: Confidence-Based Chat Fallback**
- System checks similarity score of retrieved results
- If similarity > 0.7 → RAG mode (use personal knowledge)
- If similarity < 0.7 → Direct LLM mode (general knowledge)
- User sees indication of mode ("From your thoughts" vs "General knowledge")

**FR9: Discover Mode - Taste Learning**
- System learns user taste profile from saved content
- System analyzes embedding patterns to understand preferences
- Taste profile updated as new thoughts added

**FR10: Discover Mode - Action Recommendations**
- User requests action suggestions
- System recommends content actions ("Watch this movie", "Listen to this song")
- System recommends goal-oriented actions ("Hit the gym", "Practice piano")
- RAG reasoning + LLM general knowledge synthesis
- Target: 70%+ suggestions user would actually do

**FR11: ML Mode Orchestration - Tag Mode**
- System generates tags for thoughts via LLM
- Sequential execution via OpenRouter free models
- Tags stored with thought metadata

**FR12: ML Mode Orchestration - Reflection Mode**
- System generates insights for thoughts via LLM
- Reflection stored with thought metadata

**FR13: ML Mode Orchestration - Novelty Mode**
- System scores thought importance (0-1 scale)
- Novelty ranking enables prioritization

**FR14: Knowledge Graph Structure**
- System maintains graph structure (nodes = thoughts + abodes)
- System tracks relationships (semantic similarity, temporal proximity)
- Graph powers clustering and future visualization

**FR15: Streaming LLM Responses**
- Chat responses stream token-by-token (SSE)
- Real-time display updates in iOS UI
- Improves perceived responsiveness (<2s latency target)

### Non-Functional Requirements (From Product Brief + Architecture)

**NFR1: Cost Constraint**
- Total operational cost ~$0-3/month
- All services on free tiers
- LLM usage optimized

**NFR2: Accuracy Targets**
- RAG retrieval: 80%+ accuracy
- Thought separation: 75%+ acceptance rate
- Discover Mode: 70%+ relevant suggestions
- Clustering: Minimal manual reorganization

**NFR3: Performance Targets**
- Chat response latency: <2 seconds end-to-end
- Embedding generation: <500ms per thought
- Vector search: <100ms for top-k retrieval
- Native iOS responsiveness

**NFR4: Daily Usage Pattern**
- Support 3-5 sessions per day
- Morning check, throughout day captures, evening review
- App must be reliable for daily use

**NFR5: Scale Assumptions**
- Personal use (single user)
- <100k thoughts initially
- <1000 abodes
- Local-first with cloud backup

---

## FR Coverage Map

*This section will be populated after epics are created, showing which stories implement each FR.*

---

## Epic Structure Plan

### Epic Design Principles Applied

**User-Value First:** Each epic delivers something users can actually use or benefit from
**Leverage Architecture:** Built on cookiecutter-fastapi-ML + Supabase Swift SDK decisions
**Incremental Delivery:** Each epic independently valuable
**Logical Dependencies:** Natural flow from foundation → capture → organize → discover → chat

### Proposed Epic Structure (6 Epics)

#### **Epic 1: Foundation & Infrastructure Setup**
**User Value:** Enable all subsequent features - users can create accounts and access the app
**PRD Coverage:** FR1 (Authentication & Profile)
**Technical Context:**
- Xcode project initialization with Supabase Swift SDK
- FastAPI backend scaffold using cookiecutter-fastapi-ML
- Supabase PostgreSQL schema (users, thoughts, abodes tables via Alembic)
- JWT authentication middleware
- iOS AppState + MVVM architecture setup
- Basic navigation structure

**Dependencies:** None (foundation epic)

---

#### **Epic 2: Thought Capture & Storage**
**User Value:** Users can capture and save their thoughts using text and voice input
**PRD Coverage:** FR2 (Text Input), FR3 (Voice Input)
**Technical Context:**
- iOS Capture view with text input field
- iOS native speech-to-text integration
- FastAPI `/api/v1/thoughts` CRUD endpoints
- SQLAlchemy Thought model
- sentence-transformers embedding generation (backend)
- FAISS index initialization and persistence to Supabase Storage
- Basic thought list view in iOS

**Dependencies:** Epic 1 (auth, schema, basic infrastructure)

---

#### **Epic 3: AI-Powered Thought Separation (Call Agents Mode)**
**User Value:** Users can paste messy brain dumps and AI automatically separates distinct thoughts
**PRD Coverage:** FR4 (Call Agents Mode)
**Technical Context:**
- FastAPI `/api/v1/ml/separate-thoughts` endpoint
- LLM service integration (OpenRouter free models)
- Semantic boundary detection algorithm
- iOS "Separate & Save" button and refinement UI
- Error handling with graceful LLM failures
- Retry logic with exponential backoff

**Dependencies:** Epic 2 (thought storage, embedding service)

---

#### **Epic 4: Semantic Organization (Abodes)**
**User Value:** Users see their thoughts automatically organized into meaningful themes without manual work
**PRD Coverage:** FR5 (Semantic Clustering), FR6 (Abode Management), FR11-13 (ML Modes), FR14 (Knowledge Graph)
**Technical Context:**
- K-means or DBSCAN clustering algorithm on embeddings
- FastAPI `/api/v1/abodes` endpoints (list, get thoughts)
- LLM-generated abode naming
- iOS Abode list and detail views
- Tag Mode, Reflection Mode, Novelty Mode (sequential functions)
- Knowledge graph structure storage (nodes + edges)
- Background clustering job after N thoughts
- Manual add/remove thought from abode

**Dependencies:** Epic 2 (embeddings, vector search), Epic 3 (LLM service)

---

#### **Epic 5: Personalized Discovery**
**User Value:** Users get actionable recommendations based on what they care about
**PRD Coverage:** FR9 (Taste Learning), FR10 (Action Recommendations)
**Technical Context:**
- Taste profile analysis via embedding patterns
- FastAPI `/api/v1/ml/discover` endpoint
- RAG reasoning + LLM general knowledge synthesis
- Content recommendations ("Watch this movie")
- Goal-oriented recommendations ("Hit the gym")
- iOS Discover Mode view with single suggestion UI
- Relevance: 70%+ target

**Dependencies:** Epic 4 (abodes, taste profile data)

---

#### **Epic 6: RAG-Powered Personal Chat**
**User Value:** Users can ask questions and get answers based on their own saved thoughts
**PRD Coverage:** FR7 (RAG Chat), FR8 (Confidence-Based Fallback), FR15 (Streaming Responses)
**Technical Context:**
- FAISS vector search integration (top-k retrieval)
- Confidence-based mode switching (similarity > 0.7 threshold)
- FastAPI `/api/v1/chat/stream` SSE endpoint
- Claude Haiku LLM integration
- Token-by-token streaming response
- iOS Chat view with SSE event handling
- Mode indicators ("From your thoughts" vs "General knowledge")
- RAG accuracy: 80%+ target

**Dependencies:** Epic 2 (vector search), Epic 3 (LLM service), Epic 4 (knowledge graph context)

---

## Epic Technical Context Summary

### Architecture Decisions Leveraged

**From cookiecutter-fastapi-ML starter:**
- Poetry dependency management
- FastAPI async-first architecture
- SQLAlchemy ORM + Alembic migrations
- Pydantic schemas with Field aliases (camelCase API)
- pytest testing framework
- GitHub Actions CI/CD
- Docker containerization

**From Supabase Swift SDK:**
- Native iOS authentication flow
- JWT token management
- @Observable state management (iOS 17+)
- URLSession for API + SSE streaming

**ML Pipeline Integration:**
- sentence-transformers (all-MiniLM-L6-v2) - 384-dim embeddings
- FAISS IndexFlatIP - exact cosine similarity search
- Supabase Storage - FAISS index persistence
- OpenRouter free models - mode orchestration
- Claude Haiku - RAG chat and discovery

**Cross-Platform Patterns:**
- Database: snake_case (user_id, thought_text)
- API JSON: camelCase (userId, thoughtText)
- Pydantic Field aliases handle transformation
- No custom Swift CodingKeys needed

**Error Handling:**
- LLM failures: Graceful "I, Pookie, don't know" after retries
- Network failures: User-friendly "Connection issue, please try again"
- Validation errors: Field-level 422 responses

**Deployment:**
- Backend: Render free tier (automated via GitHub Actions)
- iOS: TestFlight (manual upload)
- Cost: ~$0-3/month total

---

## Epic 1: Foundation & Infrastructure Setup

**Epic Goal:** Enable all subsequent features by establishing the technical foundation - users can create accounts and access the authenticated app.

**FR Coverage:** FR1 (User Authentication & Profile Management)

**User Value Statement:** After this epic, users can register for an account, log in securely, and access the Pookie app with a working navigation structure.

---

### Story 1.1: Initialize iOS Project with Supabase Swift SDK

**User Story:**
As a developer, I want to set up the iOS Xcode project with Supabase Swift SDK integrated, so that I have the foundation for building the SwiftUI app with authentication capabilities.

**Acceptance Criteria:**

**Given** I need to start the iOS project
**When** I create a new Xcode project
**Then** the project is configured as follows:
- Product Name: "Pookie"
- Interface: SwiftUI
- Life Cycle: SwiftUI App
- Language: Swift
- Minimum iOS version: iOS 17.0 (for @Observable support)

**And** I add Supabase Swift SDK via Swift Package Manager:
- Package URL: `https://github.com/supabase/supabase-swift`
- Version: Latest stable (2.x.x)
- Package products added: Supabase, Auth, PostgREST, Storage

**And** I create `App/Supabase.swift` with client initialization:
```swift
import Supabase

let supabase = SupabaseClient(
    supabaseURL: URL(string: "YOUR_SUPABASE_URL")!,
    supabaseKey: "YOUR_SUPABASE_ANON_KEY"
)
```

**And** I create `Resources/Config.plist` (gitignored) to store:
- Supabase URL
- Supabase anon key

**And** I add `.gitignore` with Config.plist excluded

**And** the project builds successfully without errors

**Technical Notes:**
- Follow Architecture section "iOS: Official Supabase Swift SDK + Manual MVVM Setup"
- Config.plist pattern from Architecture deployment section
- Use @Observable for state management (iOS 17+)

**Prerequisites:** None (first story)

---

### Story 1.2: Initialize FastAPI Backend with ML Template

**User Story:**
As a developer, I want to scaffold the FastAPI backend using cookiecutter-fastapi-ML, so that I have an ML-optimized project structure ready for implementing the embedding and vector search services.

**Acceptance Criteria:**

**Given** I need to start the backend project
**When** I run the cookiecutter template
**Then** I execute the following commands:

```bash
pip install cookiecutter
cookiecutter https://github.com/xshapira/cookiecutter-fastapi-ML
```

**And** I provide the following configuration:
- project_name: "Pookie Backend"
- project_slug: "pookie-backend"
- author_name: "sudy"
- python_version: "3.11"
- use_docker: "yes"
- use_github_actions: "yes"

**And** the generated project structure includes:
- `app/main.py` (FastAPI app)
- `app/api/v1/endpoints/` (for route modules)
- `app/models/` (SQLAlchemy ORM models)
- `app/schemas/` (Pydantic request/response schemas)
- `app/services/` (business logic)
- `app/core/` (config, security)
- `app/ml/` (ML components)
- `tests/` (pytest setup)
- `pyproject.toml` (Poetry dependencies)
- `Dockerfile`
- `.github/workflows/` (CI/CD)

**And** I install dependencies:
```bash
cd pookie-backend
poetry install
```

**And** I can run the development server:
```bash
poetry run uvicorn app.main:app --reload
```

**And** the server starts successfully on http://localhost:8000

**And** I can access interactive API docs at http://localhost:8000/docs

**Technical Notes:**
- Follow Architecture section "Backend: cookiecutter-fastapi-ML"
- Python 3.11+ required for optimal ML library support
- Poetry handles dependency management (better than pip for ML projects)

**Prerequisites:** None (parallel with Story 1.1)

---

### Story 1.3: Set Up Supabase Project and Database Schema

**User Story:**
As a developer, I want to create the Supabase project and define the database schema for users, thoughts, and abodes, so that the app has a PostgreSQL database ready for storing data.

**Acceptance Criteria:**

**Given** I need a database for Pookie
**When** I create a new Supabase project
**Then** I navigate to https://supabase.com/dashboard
**And** I create a new project with:
- Project name: "Pookie"
- Database password: (secure password stored in password manager)
- Region: (closest to user location)
- Pricing plan: Free tier

**And** I save the following credentials:
- Supabase URL (saved to iOS Config.plist and backend .env)
- Supabase anon key (saved to iOS Config.plist and backend .env)
- Supabase service_role key (saved to backend .env only - NEVER in iOS)

**And** I create Alembic migration in backend:
```bash
cd pookie-backend
poetry run alembic init alembic
```

**And** I create initial migration `alembic/versions/001_initial_schema.py` with tables:

**users table:**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_users_email ON users(email);
```

**thoughts table:**
```sql
CREATE TABLE thoughts (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    thought_text TEXT NOT NULL,
    tags TEXT[],
    reflection TEXT,
    novelty_score FLOAT,
    abode_id INTEGER REFERENCES abodes(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_thoughts_user_id ON thoughts(user_id);
CREATE INDEX idx_thoughts_created_at ON thoughts(created_at);
CREATE INDEX idx_thoughts_abode_id ON thoughts(abode_id);
```

**abodes table:**
```sql
CREATE TABLE abodes (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_abodes_user_id ON abodes(user_id);
```

**And** I run the migration:
```bash
poetry run alembic upgrade head
```

**And** the schema is created successfully in Supabase PostgreSQL

**And** I can verify tables exist in Supabase Table Editor

**Technical Notes:**
- Follow Architecture "Database Schema Management: SQLAlchemy ORM + Alembic"
- Database naming: snake_case for tables/columns (users, user_id, thought_text)
- Foreign keys: {table_singular}_id pattern
- Indexes: idx_{table}_{column} pattern
- Timestamp columns: TIMESTAMP WITH TIME ZONE (always UTC)
- Users table integrates with Supabase Auth (UUID primary key matches auth.users)

**Prerequisites:** Story 1.2 (backend initialized)

---

### Story 1.4: Implement JWT Authentication Middleware

**User Story:**
As a developer, I want to implement JWT authentication middleware in FastAPI, so that all API endpoints are protected and can identify the authenticated user.

**Acceptance Criteria:**

**Given** the backend needs to validate JWT tokens from iOS
**When** I implement authentication middleware
**Then** I create `app/core/security.py` with:

```python
from supabase import create_client
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

security = HTTPBearer()
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """Validate JWT token and return user info"""
    token = credentials.credentials

    try:
        # Verify JWT token with Supabase
        user = supabase.auth.get_user(token)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
```

**And** I update `app/core/config.py` to load environment variables:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
```

**And** I create `.env` file (gitignored) with:
```
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJxxx...
SUPABASE_SERVICE_KEY=eyJxxx...
```

**And** I add `.env` to `.gitignore`

**And** I create a test protected endpoint in `app/api/v1/endpoints/health.py`:
```python
from fastapi import APIRouter, Depends
from app.core.security import get_current_user

router = APIRouter()

@router.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"message": "Authenticated", "user_id": user.id}
```

**And** when I call `/protected` without Authorization header → 401 Unauthorized

**And** when I call `/protected` with valid JWT → 200 success with user_id

**Technical Notes:**
- Follow Architecture "Authentication & Security: Supabase JWT validation via supabase-py"
- Service key used server-side only (NEVER exposed to iOS)
- JWT validation handled by Supabase SDK
- User ID extracted from JWT for database queries
- All endpoints (except health check) require authentication

**Prerequisites:** Story 1.3 (Supabase setup, schema created)

---

### Story 1.5: Create iOS AppState and Authentication Service

**User Story:**
As a developer, I want to create a shared AppState observable class and authentication service in iOS, so that the app can manage user session state across all views.

**Acceptance Criteria:**

**Given** the iOS app needs centralized state management
**When** I implement AppState and AuthService
**Then** I create `App/AppState.swift`:

```swift
import Foundation
import Supabase

@Observable
class AppState {
    var currentUser: User?
    var session: Session?
    var isAuthenticated: Bool { session != nil }
    var isLoading: Bool = false
    var error: String?

    init() {
        // Check for existing session on init
        Task {
            await checkSession()
        }
    }

    func checkSession() async {
        do {
            let session = try await supabase.auth.session
            self.session = session
            self.currentUser = session.user
        } catch {
            // No active session
            self.session = nil
            self.currentUser = nil
        }
    }
}
```

**And** I create `Services/AuthService.swift`:

```swift
import Foundation
import Supabase

class AuthService {
    static let shared = AuthService()

    func signUp(email: String, password: String) async throws -> Session {
        let response = try await supabase.auth.signUp(
            email: email,
            password: password
        )
        guard let session = response.session else {
            throw AuthError.noSession
        }
        return session
    }

    func signIn(email: String, password: String) async throws -> Session {
        let session = try await supabase.auth.signIn(
            email: email,
            password: password
        )
        return session
    }

    func signOut() async throws {
        try await supabase.auth.signOut()
    }
}

enum AuthError: LocalizedError {
    case noSession

    var errorDescription: String? {
        switch self {
        case .noSession: return "No session created after sign up"
        }
    }
}
```

**And** I update `App/PookieApp.swift` to provide AppState:

```swift
import SwiftUI

@main
struct PookieApp: App {
    @State private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(appState)
        }
    }
}
```

**And** AppState is accessible in all views via `@Environment(AppState.self)`

**And** AuthService methods work with Supabase Auth API

**Technical Notes:**
- Follow Architecture "iOS State Management: ViewModels + Shared AppState"
- @Observable (iOS 17+) eliminates need for ObservableObject
- AppState holds session, user, global loading/error states
- AuthService is stateless singleton for auth operations
- JWT token automatically managed by Supabase SDK

**Prerequisites:** Story 1.1 (iOS project with Supabase SDK)

---

### Story 1.6: Build Authentication UI (Sign Up, Sign In, Sign Out)

**User Story:**
As a user, I want to sign up for an account, log in, and log out, so that I can securely access my personal Pookie data.

**Acceptance Criteria:**

**Given** I am a new user
**When** I open the app
**Then** I see an authentication screen with tabs: "Sign In" and "Sign Up"

**And** on the "Sign Up" tab, I see:
- Email text field
- Password secure field (obscured text)
- "Sign Up" button

**And** when I enter valid email + password (8+ characters) and tap "Sign Up"
**Then** the app calls `AuthService.signUp(email:password:)`
**And** Supabase creates the user account
**And** I receive a session with JWT token
**And** AppState.session is updated
**And** I navigate to the main app view (placeholder home screen)

**And** on the "Sign In" tab, I see:
- Email text field
- Password secure field
- "Sign In" button

**And** when I enter valid credentials and tap "Sign In"
**Then** the app calls `AuthService.signIn(email:password:)`
**And** Supabase authenticates the user
**And** I receive a session with JWT token
**And** AppState.session is updated
**And** I navigate to the main app view

**And** when I'm signed in and tap "Sign Out" (in placeholder home screen)
**Then** the app calls `AuthService.signOut()`
**And** AppState.session is cleared
**And** I navigate back to authentication screen

**And** if authentication fails (wrong password, network error)
**Then** I see a user-friendly error message below the form
**And** I can retry the operation

**And** while authenticating, I see a loading indicator
**And** the sign in/sign up button is disabled

**Implementation:**

Create `Views/Auth/AuthView.swift`:
```swift
import SwiftUI

struct AuthView: View {
    @Environment(AppState.self) private var appState
    @State private var email = ""
    @State private var password = ""
    @State private var isLoading = false
    @State private var error: String?
    @State private var selectedTab = 0 // 0 = Sign In, 1 = Sign Up

    var body: some View {
        VStack {
            Picker("Auth Mode", selection: $selectedTab) {
                Text("Sign In").tag(0)
                Text("Sign Up").tag(1)
            }
            .pickerStyle(.segmented)
            .padding()

            TextField("Email", text: $email)
                .textInputAutocapitalization(.never)
                .keyboardType(.emailAddress)
                .textFieldStyle(.roundedBorder)
                .padding(.horizontal)

            SecureField("Password", text: $password)
                .textFieldStyle(.roundedBorder)
                .padding(.horizontal)

            if let error = error {
                Text(error)
                    .foregroundColor(.red)
                    .font(.caption)
                    .padding(.horizontal)
            }

            Button(selectedTab == 0 ? "Sign In" : "Sign Up") {
                Task {
                    await authenticate()
                }
            }
            .disabled(isLoading || email.isEmpty || password.isEmpty)
            .padding()

            if isLoading {
                ProgressView()
            }
        }
        .padding()
    }

    func authenticate() async {
        isLoading = true
        error = nil

        do {
            let session = selectedTab == 0
                ? try await AuthService.shared.signIn(email: email, password: password)
                : try await AuthService.shared.signUp(email: email, password: password)

            appState.session = session
            appState.currentUser = session.user
        } catch {
            self.error = "Authentication failed. Please try again."
        }

        isLoading = false
    }
}
```

Create `Views/Home/HomeView.swift` (placeholder):
```swift
import SwiftUI

struct HomeView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        NavigationStack {
            VStack {
                Text("Welcome to Pookie!")
                    .font(.largeTitle)

                if let user = appState.currentUser {
                    Text("Signed in as: \(user.email ?? "Unknown")")
                        .font(.caption)
                }

                Button("Sign Out") {
                    Task {
                        try? await AuthService.shared.signOut()
                        appState.session = nil
                        appState.currentUser = nil
                    }
                }
                .padding()
            }
            .navigationTitle("Home")
        }
    }
}
```

Update `ContentView.swift`:
```swift
import SwiftUI

struct ContentView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        if appState.isAuthenticated {
            HomeView()
        } else {
            AuthView()
        }
    }
}
```

**Technical Notes:**
- Follow Architecture "Authentication Flow: Supabase JWT validation"
- Email validation via keyboardType and autocapitalization settings
- Password minimum length: 8 characters (Supabase default)
- Error handling: User-friendly messages, not raw error text
- Loading states: Boolean flag + ProgressView
- Navigation: Conditional based on AppState.isAuthenticated

**Prerequisites:** Story 1.5 (AppState, AuthService)

---

### Story 1.7: Implement Basic Navigation Structure

**User Story:**
As a developer, I want to set up the main app navigation structure with tab bar, so that users can navigate between Capture, Abodes, Discover, and Chat sections.

**Acceptance Criteria:**

**Given** the user is authenticated
**When** I navigate to the main app
**Then** I see a TabView with 4 tabs:
1. **Capture** - Icon: pencil, Title: "Capture"
2. **Abodes** - Icon: folder, Title: "Abodes"
3. **Discover** - Icon: sparkles, Title: "Discover"
4. **Chat** - Icon: message, Title: "Chat"

**And** each tab navigates to a placeholder view with the tab name displayed

**And** the tab bar is visible at the bottom of the screen

**And** I can tap each tab to switch between views

**And** the selected tab is highlighted

**Implementation:**

Update `Views/Home/HomeView.swift`:
```swift
import SwiftUI

struct HomeView: View {
    @Environment(AppState.self) private var appState
    @State private var selectedTab = 0

    var body: some View {
        TabView(selection: $selectedTab) {
            CaptureView()
                .tabItem {
                    Label("Capture", systemImage: "pencil")
                }
                .tag(0)

            AbodeListView()
                .tabItem {
                    Label("Abodes", systemImage: "folder")
                }
                .tag(1)

            DiscoverView()
                .tabItem {
                    Label("Discover", systemImage: "sparkles")
                }
                .tag(2)

            ChatView()
                .tabItem {
                    Label("Chat", systemImage: "message")
                }
                .tag(3)
        }
    }
}
```

Create placeholder views:

`Views/Capture/CaptureView.swift`:
```swift
import SwiftUI

struct CaptureView: View {
    var body: some View {
        NavigationStack {
            VStack {
                Text("Capture your thoughts here")
                Text("(Coming in Epic 2)")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .navigationTitle("Capture")
        }
    }
}
```

`Views/Abodes/AbodeListView.swift`:
```swift
import SwiftUI

struct AbodeListView: View {
    var body: some View {
        NavigationStack {
            VStack {
                Text("Your abodes will appear here")
                Text("(Coming in Epic 4)")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .navigationTitle("Abodes")
        }
    }
}
```

`Views/Discover/DiscoverView.swift`:
```swift
import SwiftUI

struct DiscoverView: View {
    var body: some View {
        NavigationStack {
            VStack {
                Text("Discover new experiences")
                Text("(Coming in Epic 5)")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .navigationTitle("Discover")
        }
    }
}
```

`Views/Chat/ChatView.swift`:
```swift
import SwiftUI

struct ChatView: View {
    var body: some View {
        NavigationStack {
            VStack {
                Text("Chat with your personal LLM")
                Text("(Coming in Epic 6)")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .navigationTitle("Chat")
        }
    }
}
```

**And** the project structure follows Architecture patterns:
```
Pookie/
├── App/
│   ├── PookieApp.swift
│   ├── Supabase.swift
│   └── AppState.swift
├── Views/
│   ├── Auth/
│   │   └── AuthView.swift
│   ├── Home/
│   │   └── HomeView.swift
│   ├── Capture/
│   │   └── CaptureView.swift
│   ├── Abodes/
│   │   └── AbodeListView.swift
│   ├── Discover/
│   │   └── DiscoverView.swift
│   └── Chat/
│       └── ChatView.swift
├── Services/
│   └── AuthService.swift
└── Resources/
    └── Config.plist
```

**Technical Notes:**
- Follow Architecture "iOS Project Structure"
- TabView for bottom navigation (iOS standard pattern)
- NavigationStack in each tab (independent navigation hierarchies)
- Placeholder views indicate future epic implementation
- SF Symbols for tab icons (built-in, free)

**Prerequisites:** Story 1.6 (Authentication UI complete)

---

## Epic 1 Summary

**Stories Created:** 7 stories
**FR Coverage:** FR1 (User Authentication & Profile Management) ✅

**Technical Foundation Established:**
- ✅ iOS Xcode project with Supabase Swift SDK
- ✅ FastAPI backend with cookiecutter-fastapi-ML structure
- ✅ Supabase PostgreSQL schema (users, thoughts, abodes tables)
- ✅ JWT authentication middleware
- ✅ iOS AppState + AuthService
- ✅ Authentication UI (sign up, sign in, sign out)
- ✅ Basic tab navigation structure

**Architecture Sections Implemented:**
- Database Schema Management (Alembic migrations)
- Authentication & Security (JWT validation)
- iOS State Management (AppState with @Observable)
- Project Structure (both iOS and Backend)

**Ready for Epic 2:** Thought Capture & Storage (text + voice input, embedding generation, FAISS)

---

## Epic 2: Something Capture & Storage

**Epic Goal:** Enable users to capture and save their thoughts/ideas/media using text, voice, images, videos, or URLs, with automatic embedding generation and meaning extraction for semantic search.

**FR Coverage:** FR2 (Text Input), FR3 (Voice Input), plus multimodal capture

**User Value Statement:** After this epic, users can capture somethings via text, voice, images, videos, or URLs, see a list of saved somethings, and have AI automatically extract meaning from each capture for better organization.

---

## Story 2.1: Create SQLAlchemy Something Model and Pydantic Schemas

**User Story:**
As a developer, I want to create the SQLAlchemy ORM model and Pydantic schemas for somethings, so that I have type-safe data structures for database operations and API communication.

**Acceptance Criteria:**

**Given** I need to persist somethings in the database
**When** I create the Something model and schemas
**Then** I create `app/models/something.py` with SQLAlchemy model:

```python
from sqlalchemy import Column, Integer, Text, Float, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base

class Something(Base):
    """
    Somethings are user-captured items that can be text, images, videos, or URLs.

    Voice notes are converted to text via voice-to-text.
    Images/videos are stored in Supabase Storage with URLs saved here.

    The 'meaning' field contains LLM-generated reasoning/interpretation about
    why this something matters or what it represents. Users can edit this,
    and the LLM learns from user edits via the is_meaning_user_edited flag.
    """
    __tablename__ = "somethings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=True)  # Text content (nullable if only media)
    content_type = Column(
        Enum('text', 'image', 'video', 'url', name='content_type'),
        default='text',
        nullable=False
    )
    media_url = Column(Text, nullable=True)  # URL to Supabase Storage or external URL
    meaning = Column(Text, nullable=True)  # LLM-generated reasoning/interpretation
    is_meaning_user_edited = Column(Boolean, default=False, nullable=False)  # Learning signal
    novelty_score = Column(Float, nullable=True)  # Importance ranking 0-1
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="somethings")
    circles = relationship("SomethingCircle", back_populates="something", cascade="all, delete-orphan")
    intention_cares = relationship("IntentionCare", back_populates="something", cascade="all, delete-orphan")
```

**And** I create `app/schemas/something.py` with Pydantic schemas:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class ContentType(str, Enum):
    text = "text"
    image = "image"
    video = "video"
    url = "url"

class SomethingBase(BaseModel):
    content: Optional[str] = None
    content_type: ContentType = Field(alias="contentType", default=ContentType.text)
    media_url: Optional[str] = Field(alias="mediaUrl", default=None)

class SomethingCreate(SomethingBase):
    pass

class SomethingResponse(SomethingBase):
    id: int
    user_id: str = Field(alias="userId")
    meaning: Optional[str] = None
    is_meaning_user_edited: bool = Field(alias="isMeaningUserEdited", default=False)
    novelty_score: Optional[float] = Field(alias="noveltyScore", default=None)
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        populate_by_name = True
        from_attributes = True

class SomethingUpdateMeaning(BaseModel):
    meaning: str
```

**And** the Pydantic schemas use Field aliases to convert:
- Database/Python: `content_type`, `media_url`, `user_id`, `created_at` (snake_case)
- API JSON: `contentType`, `mediaUrl`, `userId`, `createdAt` (camelCase)

**Technical Notes:**
- Multimodal support: text, image, video, url
- Meaning field for LLM-generated interpretation
- Learning signal: is_meaning_user_edited
- Nullable content (if only media)
- Junction table relationships (circles, intention_cares)

**Prerequisites:** Epic 1 Story 1.3 (Database schema created)

---

## Story 2.2: Implement sentence-transformers Embedding Service

[UNCHANGED from original - embedding service works the same]

---

## Story 2.3: Implement FAISS Vector Index Service

[UNCHANGED from original - FAISS service works the same]

---

## Story 2.4: Create Somethings CRUD API Endpoints

**User Story:**
As a developer, I want to implement RESTful API endpoints for something CRUD operations, so that the iOS app can create, read, update, and delete somethings with automatic embedding and meaning generation.

**Acceptance Criteria:**

**Given** the iOS app needs to manage somethings via API
**When** I implement the somethings endpoints
**Then** I create `app/api/v1/endpoints/somethings.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.core.database import get_db
from app.schemas.something import SomethingCreate, SomethingResponse, SomethingUpdateMeaning
from app.models.something import Something
from app.services.embedding_service import embedding_service
from app.services.vector_service import vector_service
from app.services.llm_service import llm_service
from typing import List

router = APIRouter()

@router.post("", response_model=SomethingResponse, status_code=201)
async def create_something(
    something: SomethingCreate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new something with automatic embedding and meaning generation"""

    # Create something in database
    db_something = Something(
        user_id=user.id,
        content=something.content,
        content_type=something.content_type,
        media_url=something.media_url
    )
    db.add(db_something)
    db.commit()
    db.refresh(db_something)

    # Generate embedding from content (text or media description)
    embedding_text = something.content or f"[{something.content_type}]: {something.media_url}"
    embedding = embedding_service.generate_embedding(embedding_text)

    # Add to FAISS index
    vector_service.add_something_embedding(db_something.id, embedding)

    # Generate meaning (async background task in production)
    if something.content or something.content_type == 'text':
        meaning = await llm_service.generate_meaning(embedding_text)
        if meaning:
            db_something.meaning = meaning
            db.commit()
            db.refresh(db_something)

    # Save index every 10 somethings (debounced)
    if vector_service.index.total_vectors % 10 == 0:
        await vector_service.save_to_storage()

    return db_something

@router.get("", response_model=List[SomethingResponse])
async def list_somethings(
    skip: int = 0,
    limit: int = 100,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's somethings (paginated, sorted by created_at desc)"""
    somethings = db.query(Something).filter(
        Something.user_id == user.id
    ).order_by(
        Something.created_at.desc()
    ).offset(skip).limit(limit).all()

    return somethings

@router.get("/{something_id}", response_model=SomethingResponse)
async def get_something(
    something_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a single something by ID"""
    something = db.query(Something).filter(
        Something.id == something_id,
        Something.user_id == user.id
    ).first()

    if not something:
        raise HTTPException(status_code=404, detail="Something not found")

    return something

@router.patch("/{something_id}/meaning", response_model=SomethingResponse)
async def update_meaning(
    something_id: int,
    update: SomethingUpdateMeaning,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update meaning (user edit) - marks as user-edited for learning"""
    something = db.query(Something).filter(
        Something.id == something_id,
        Something.user_id == user.id
    ).first()

    if not something:
        raise HTTPException(status_code=404, detail="Something not found")

    something.meaning = update.meaning
    something.is_meaning_user_edited = True
    db.commit()
    db.refresh(something)

    return something

@router.delete("/{something_id}", status_code=204)
async def delete_something(
    something_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a something"""
    something = db.query(Something).filter(
        Something.id == something_id,
        Something.user_id == user.id
    ).first()

    if not something:
        raise HTTPException(status_code=404, detail="Something not found")

    db.delete(something)
    db.commit()

    return None
```

**And** I add meaning generation to `app/services/llm_service.py`:

```python
async def generate_meaning(self, content: str) -> Optional[str]:
    """
    Generate meaning/interpretation for a something

    Returns:
        Meaning text (1-2 sentences), or None if LLM fails
    """
    system_prompt = """You are an AI that helps users understand why things matter to them.
Your task is to briefly explain what this capture might mean or represent.

Rules:
- 1-2 sentences maximum
- Focus on deeper meaning, not just description
- Be encouraging and insightful
- Don't restate the obvious"""

    user_prompt = f"""What might this capture mean or represent?

"{content}"

Return 1-2 sentences explaining the deeper meaning:"""

    response = await self.generate(
        prompt=user_prompt,
        system_prompt=system_prompt,
        temperature=0.6,
        max_tokens=100
    )

    if response is None:
        return None

    return response.strip()
```

**Technical Notes:**
- Multimodal support (text, image, video, url)
- Automatic meaning generation via LLM
- User can edit meaning (learning signal)
- Embedding from content or media description
- PATCH endpoint for meaning updates

**Prerequisites:** Story 2.1 (Models), Story 2.2 (Embeddings), Story 2.3 (FAISS)

---

## Story 2.5: Create iOS APIService and Something Model

**User Story:**
As a developer, I want to create an iOS API service and Something model, so that the app can communicate with the backend API using type-safe Swift code.

**Acceptance Criteria:**

**Given** the iOS app needs to call backend APIs
**When** I implement APIService and models
**Then** I create `Models/Something.swift`:

```swift
import Foundation

enum ContentType: String, Codable {
    case text
    case image
    case video
    case url
}

struct Something: Codable, Identifiable {
    let id: Int
    let userId: String
    let content: String?
    let contentType: ContentType
    let mediaUrl: String?
    let meaning: String?
    let isMeaningUserEdited: Bool
    let noveltyScore: Double?
    let createdAt: Date
    let updatedAt: Date
}

struct SomethingCreate: Codable {
    let content: String?
    let contentType: ContentType
    let mediaUrl: String?
}

struct SomethingUpdateMeaning: Codable {
    let meaning: String
}
```

**And** I update `Services/APIService.swift` with something endpoints:

```swift
extension APIService {
    func createSomething(content: String?, contentType: ContentType, mediaUrl: String? = nil) async throws -> Something {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/somethings")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body = SomethingCreate(content: content, contentType: contentType, mediaUrl: mediaUrl)
        request.httpBody = try JSONEncoder().encode(body)

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 201:
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .iso8601
            return try decoder.decode(Something.self, from: data)
        case 401:
            throw APIError.unauthorized
        default:
            throw APIError.serverError("Failed to create something")
        }
    }

    func listSomethings(skip: Int = 0, limit: Int = 100) async throws -> [Something] {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/somethings?skip=\(skip)&limit=\(limit)")!
        var request = URLRequest(url: url)
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 200:
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .iso8601
            return try decoder.decode([Something].self, from: data)
        case 401:
            throw APIError.unauthorized
        default:
            throw APIError.serverError("Failed to list somethings")
        }
    }

    func updateMeaning(somethingId: Int, meaning: String) async throws -> Something {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/somethings/\(somethingId)/meaning")!
        var request = URLRequest(url: url)
        request.httpMethod = "PATCH"
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body = SomethingUpdateMeaning(meaning: meaning)
        request.httpBody = try JSONEncoder().encode(body)

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 200:
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .iso8601
            return try decoder.decode(Something.self, from: data)
        case 401:
            throw APIError.unauthorized
        default:
            throw APIError.serverError("Failed to update meaning")
        }
    }
}
```

**Technical Notes:**
- Swift enum for ContentType
- Multimodal support in API
- PATCH endpoint for meaning updates
- Native camelCase (no CodingKeys needed)

**Prerequisites:** Story 2.4 (Backend API ready), Epic 1 Story 1.5 (AuthService)

---

## Story 2.6: Build Text Capture UI with ViewModel

**User Story:**
As a user, I want to type a thought and save it, so that I can capture my ideas in text form with AI-generated meaning.

**Acceptance Criteria:**

[Similar to original, but updated to use "Something" terminology and show meaning field]

**Implementation:**

Create `ViewModels/CaptureViewModel.swift`:

```swift
import Foundation
import Observation

@Observable
class CaptureViewModel {
    var somethingText: String = ""
    var isSaving: Bool = false
    var error: String?
    var successMessage: String?
    var lastCreated: Something?

    var characterCount: Int {
        somethingText.count
    }

    var canSave: Bool {
        !somethingText.isEmpty && somethingText.count <= 10000 && !isSaving
    }

    func saveSomething() async {
        guard canSave else { return }

        isSaving = true
        error = nil
        successMessage = nil

        do {
            let something = try await APIService.shared.createSomething(
                content: somethingText,
                contentType: .text
            )

            // Success
            lastCreated = something
            successMessage = "Saved!"
            somethingText = ""

            // Clear success message after 2 seconds
            Task {
                try? await Task.sleep(nanoseconds: 2_000_000_000)
                successMessage = nil
            }
        } catch {
            self.error = error.localizedDescription
        }

        isSaving = false
    }
}
```

Update `Views/Capture/CaptureView.swift`:

```swift
import SwiftUI

struct CaptureView: View {
    @State private var viewModel = CaptureViewModel()

    var body: some View {
        NavigationStack {
            VStack(spacing: 16) {
                // Text editor
                TextEditor(text: $viewModel.somethingText)
                    .frame(minHeight: 200)
                    .padding(8)
                    .background(Color(.systemGray6))
                    .cornerRadius(8)
                    .overlay(
                        Group {
                            if viewModel.somethingText.isEmpty {
                                Text("What's on your mind?")
                                    .foregroundColor(.secondary)
                                    .padding(.top, 16)
                                    .padding(.leading, 12)
                                    .allowsHitTesting(false)
                            }
                        },
                        alignment: .topLeading
                    )

                // Character count
                HStack {
                    Spacer()
                    Text("\(viewModel.characterCount) characters")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }

                // Show last created meaning
                if let something = viewModel.lastCreated, let meaning = something.meaning {
                    VStack(alignment: .leading, spacing: 4) {
                        Text("AI Interpretation:")
                            .font(.caption)
                            .foregroundColor(.secondary)

                        Text(meaning)
                            .font(.subheadline)
                            .italic()
                            .padding(8)
                            .background(Color.blue.opacity(0.1))
                            .cornerRadius(8)
                    }
                }

                // Error message
                if let error = viewModel.error {
                    Text(error)
                        .foregroundColor(.red)
                        .font(.caption)
                }

                // Success message
                if let success = viewModel.successMessage {
                    Text(success)
                        .foregroundColor(.green)
                        .font(.caption)
                }

                // Save button
                Button(action: {
                    Task {
                        await viewModel.saveSomething()
                    }
                }) {
                    if viewModel.isSaving {
                        ProgressView()
                            .frame(maxWidth: .infinity)
                    } else {
                        Text("Save")
                            .frame(maxWidth: .infinity)
                    }
                }
                .buttonStyle(.borderedProminent)
                .disabled(!viewModel.canSave)

                Spacer()
            }
            .padding()
            .navigationTitle("Capture")
        }
    }
}
```

**Technical Notes:**
- Shows AI-generated meaning after save
- Uses "Something" terminology
- Multimodal foundation (text for now)

**Prerequisites:** Story 2.5 (APIService, Something model)

---

## Story 2.7: Implement Voice Capture with iOS Speech Recognition

[Similar to original, but saves as Something with contentType=.text]

---

## Epic 2 Summary

**Stories Created:** 7 stories
**FR Coverage:**
- FR2 (Something Capture - Text Input) ✅
- FR3 (Something Capture - Voice Input) ✅
- Multimodal foundation (image/video/url ready for future)

**Technical Capabilities Established:**
- ✅ SQLAlchemy Something model with multimodal support
- ✅ Meaning extraction via LLM
- ✅ Learning signals (is_meaning_user_edited)
- ✅ sentence-transformers embedding service
- ✅ FAISS vector index
- ✅ Somethings CRUD API endpoints
- ✅ iOS APIService for backend communication
- ✅ iOS Something model (native camelCase)
- ✅ Text capture UI with meaning display
- ✅ Voice capture with iOS Speech framework

**Ready for Epic 3:** AI-Powered Something Separation (Call Agents Mode)

---

## Epic 3: AI-Powered Something Separation (Call Agents Mode)

**Epic Goal:** Enable users to paste messy brain dumps and have AI automatically identify and separate distinct somethings with semantic boundary detection.

**FR Coverage:** FR4 (Call Agents Mode - Something Separation)

**User Value Statement:** After this epic, users can paste rambling paragraphs with multiple mixed ideas, and AI will intelligently separate them into individual somethings for storage and organization.

---

## Story 3.1: Implement LLM Service with OpenRouter Integration

[UNCHANGED from original - LLM service works the same]

---

## Story 3.2: Create Something Separation API Endpoint

**User Story:**
As a developer, I want to implement the `/api/v1/ml/separate-somethings` endpoint, so that the iOS app can send rambling text and receive separated somethings with embeddings.

**Acceptance Criteria:**

**Given** the iOS app needs something separation capabilities
**When** I implement the separation endpoint
**Then** I create `app/schemas/ml.py` for ML endpoint schemas:

```python
from pydantic import BaseModel, Field
from typing import List

class SeparateSomethingsRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)

class SeparatedSomething(BaseModel):
    content: str

    class Config:
        populate_by_name = True

class SeparateSomethingsResponse(BaseModel):
    separated_somethings: List[SeparatedSomething] = Field(alias="separatedSomethings")
    original_text: str = Field(alias="originalText")
    count: int

    class Config:
        populate_by_name = True
```

**And** I create `app/api/v1/endpoints/ml.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.schemas.ml import SeparateSomethingsRequest, SeparateSomethingsResponse, SeparatedSomething
from app.services.llm_service import llm_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/separate-somethings", response_model=SeparateSomethingsResponse)
async def separate_somethings(
    request: SeparateSomethingsRequest,
    user: dict = Depends(get_current_user)
):
    """
    Separate rambling text into distinct somethings using LLM

    Returns:
        List of separated somethings (not saved to database yet)
    """

    # Call LLM service (reuse separate_thoughts method - works the same)
    separated = await llm_service.separate_thoughts(request.text)

    # Handle graceful LLM failure
    if separated is None:
        # Return original text as single something (fallback)
        logger.warning(f"LLM separation failed for user {user.id}, returning original text")
        separated = [request.text]

    # Build response
    separated_somethings = [
        SeparatedSomething(content=text)
        for text in separated
    ]

    return SeparateSomethingsResponse(
        separated_somethings=separated_somethings,
        original_text=request.text,
        count=len(separated_somethings)
    )
```

**Technical Notes:**
- Endpoint renamed to /separate-somethings
- Returns list of text somethings
- Graceful fallback to original text
- No database writes (preview only)

**Prerequisites:** Story 3.1 (LLM service), Story 2.1 (Schemas)

---

## Story 3.3: Create Batch Something Creation Endpoint

**User Story:**
As a developer, I want to implement a batch endpoint for creating multiple somethings at once, so that separated somethings can be saved efficiently with embeddings and meanings.

**Acceptance Criteria:**

**Given** the iOS app needs to save multiple separated somethings efficiently
**When** I implement the batch creation endpoint
**Then** I add to `app/schemas/something.py`:

```python
class SomethingBatchCreate(BaseModel):
    somethings: List[SomethingCreate]

class SomethingBatchResponse(BaseModel):
    somethings: List[SomethingResponse]
    count: int
```

**And** I add to `app/api/v1/endpoints/somethings.py`:

```python
@router.post("/batch", response_model=SomethingBatchResponse, status_code=201)
async def create_somethings_batch(
    request: SomethingBatchCreate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create multiple somethings at once with batch embedding and meaning generation

    More efficient than calling create_something multiple times
    """

    if not request.somethings:
        raise HTTPException(status_code=400, detail="No somethings provided")

    if len(request.somethings) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 somethings per batch")

    # Create somethings in database
    db_somethings = []
    for something_data in request.somethings:
        db_something = Something(
            user_id=user.id,
            content=something_data.content,
            content_type=something_data.content_type,
            media_url=something_data.media_url
        )
        db.add(db_something)
        db_somethings.append(db_something)

    db.commit()

    # Refresh all to get IDs
    for db_something in db_somethings:
        db.refresh(db_something)

    # Generate embeddings in batch (more efficient)
    texts = [s.content or f"[{s.content_type}]: {s.media_url}" for s in db_somethings]
    embeddings = embedding_service.generate_embeddings_batch(texts)

    # Add all to FAISS index
    for db_something, embedding in zip(db_somethings, embeddings):
        vector_service.add_something_embedding(db_something.id, embedding)

    # Generate meanings in batch (optional, can be background task)
    for db_something, text in zip(db_somethings, texts):
        if db_something.content:
            meaning = await llm_service.generate_meaning(text)
            if meaning:
                db_something.meaning = meaning

    db.commit()

    # Save FAISS index after batch
    await vector_service.save_to_storage()

    return SomethingBatchResponse(
        somethings=db_somethings,
        count=len(db_somethings)
    )
```

**Technical Notes:**
- Batch embedding generation
- Batch meaning generation
- Single FAISS save after all additions
- Validation: 1-50 somethings per batch

**Prerequisites:** Story 2.4 (Somethings endpoint), Story 2.2 (Embedding service)

---

## Story 3.4: Build iOS Separate & Save UI

**User Story:**
As a user, I want to see a "Separate & Save" button that shows me AI-separated somethings before saving, so that I can review and confirm the separation.

**Acceptance Criteria:**

**Given** I am on the Capture tab
**When** I type or speak a rambling paragraph with multiple ideas
**Then** I see two buttons:
1. "Save" - saves as-is (existing functionality)
2. "Separate & Save" - AI separates first

**And** when I tap "Separate & Save"
**Then** the app calls `POST /api/v1/ml/separate-somethings`
**And** I see a loading indicator with text "Separating..."
**And** the button is disabled during processing

**And** when separation completes successfully
**Then** I navigate to a preview screen showing:
- Title: "Separated Somethings"
- List of separated somethings (numbered)
- Each something is editable
- "Save All" button
- "Cancel" button

**And** I can edit any separated something before saving

**And** when I tap "Save All"
**Then** the app calls `POST /api/v1/somethings/batch` with all somethings
**And** I see a success message "3 somethings saved!"
**And** I navigate back to Capture screen
**And** the text field is cleared

**Implementation:**

Update `Services/APIService.swift`:

```swift
struct SeparatedSomething: Codable {
    let content: String
}

struct SeparateSomethingsResponse: Codable {
    let separatedSomethings: [SeparatedSomething]
    let originalText: String
    let count: Int
}

extension APIService {
    func separateSomethings(text: String) async throws -> SeparateSomethingsResponse {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/ml/separate-somethings")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body = ["text": text]
        request.httpBody = try JSONEncoder().encode(body)

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 200:
            return try JSONDecoder().decode(SeparateSomethingsResponse.self, from: data)
        case 401:
            throw APIError.unauthorized
        default:
            throw APIError.serverError("Failed to separate somethings")
        }
    }

    func createSomethingsBatch(somethings: [SomethingCreate]) async throws -> [Something] {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/somethings/batch")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body = ["somethings": somethings]
        request.httpBody = try JSONEncoder().encode(body)

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 201:
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .iso8601
            let batchResponse = try decoder.decode(SomethingBatchResponse.self, from: data)
            return batchResponse.somethings
        case 401:
            throw APIError.unauthorized
        default:
            throw APIError.serverError("Failed to save somethings")
        }
    }
}

struct SomethingBatchResponse: Codable {
    let somethings: [Something]
    let count: Int
}
```

[Rest of iOS implementation similar to original Epic 3 Story 3.4, but using "Something" terminology]

**Technical Notes:**
- Updated terminology: "somethings" not "thoughts"
- Batch creation with multimodal support
- Preview UI before saving

**Prerequisites:** Story 3.2 (Separation API), Story 3.3 (Batch API)

---

## Epic 3 Summary

**Stories Created:** 4 stories
**FR Coverage:** FR4 (Call Agents Mode - Something Separation) ✅

**Technical Capabilities Established:**
- ✅ LLM service with OpenRouter (mistralai/mistral-7b-instruct:free)
- ✅ Something separation API endpoint
- ✅ Batch something creation
- ✅ iOS separation UI with preview

**Ready for Epic 4:** Semantic Organization (Circles of Care)

---

## Epic 4: Semantic Organization (Circles of Care)

**Epic Goal:** Enable users to see their somethings automatically organized into meaningful Circles of Care, with AI-generated names and flexible multi-circle assignment.

**FR Coverage:** FR5 (Semantic Clustering), FR6 (Circle Naming & Management)

**User Value Statement:** After this epic, users see their somethings auto-organized into thematic Circles of Care, can view somethings within each circle, and can manually adjust assignments as needed.

---

## Story 4.1: Create Circle Model, Schemas, and Junction Table

**User Story:**
As a developer, I want to create the Circle SQLAlchemy model with junction table support, so that I can store thematic clusters with many-to-many relationships to somethings.

**Acceptance Criteria:**

**Given** I need to store circles and their relationships to somethings
**When** I create the models and schemas
**Then** I create `app/models/circle.py`:

```python
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
from sqlalchemy.orm import relationship
from app.models.base import Base

class Circle(Base):
    __tablename__ = "circles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    circle_name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    care_frequency = Column(Integer, server_default=text('0'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="circles")
    somethings = relationship("SomethingCircle", back_populates="circle", cascade="all, delete-orphan")
```

**And** I create `app/models/something_circle.py`:

```python
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base

class SomethingCircle(Base):
    """
    Junction table linking somethings to circles (many-to-many).

    One something can belong to multiple circles.
    Tracks whether the user manually assigned the circle (high confidence)
    or if it was LLM-suggested (has confidence_score).

    The LLM learns from is_user_assigned=True entries to improve future predictions.
    """
    __tablename__ = "something_circles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    something_id = Column(Integer, ForeignKey("somethings.id", ondelete="CASCADE"), nullable=False, index=True)
    circle_id = Column(Integer, ForeignKey("circles.id", ondelete="CASCADE"), nullable=False, index=True)
    is_user_assigned = Column(Boolean, default=False, nullable=False)  # Learning signal
    confidence_score = Column(Float, nullable=True)  # LLM confidence (0-1) if auto-assigned
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    something = relationship("Something", back_populates="circles")
    circle = relationship("Circle", back_populates="somethings")

    # Constraint: Prevent duplicate something-circle links
    __table_args__ = (
        UniqueConstraint('something_id', 'circle_id', name='uq_something_circle'),
    )
```

**And** I update `app/models/something.py` to add relationship:

```python
# Add to Something model:
circles = relationship("SomethingCircle", back_populates="something", cascade="all, delete-orphan")
```

**And** I create `app/schemas/circle.py`:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CircleBase(BaseModel):
    circle_name: str = Field(alias="circleName", min_length=1, max_length=255)
    description: Optional[str] = None

class CircleCreate(CircleBase):
    pass

class CircleResponse(CircleBase):
    id: int
    user_id: str = Field(alias="userId")
    care_frequency: int = Field(alias="careFrequency", default=0)
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    something_count: int = Field(alias="somethingCount", default=0)

    class Config:
        populate_by_name = True
        from_attributes = True

class CircleWithSomethings(CircleResponse):
    somethings: list['SomethingResponse'] = []

    class Config:
        populate_by_name = True
        from_attributes = True
```

**Technical Notes:**
- Junction table pattern (many-to-many)
- Learning signals: is_user_assigned, confidence_score
- No direct foreign key in somethings table
- care_frequency field for future features

**Prerequisites:** Story 2.1 (Something model), Epic 1 Story 1.3 (Database schema)

---

## Story 4.2: Implement K-means Clustering Algorithm

[Similar to original, but updated to use "Something" and handle junction table assignments]

```python
# In clustering_service.py
async def cluster_user_somethings(self, user_id: str, db: Session) -> Dict[int, List[int]]:
    """
    Cluster all somethings for a user

    Returns:
        Dictionary mapping cluster_id to list of something_ids
    """
    # Get all somethings for user
    somethings = db.query(Something).filter(Something.user_id == user_id).all()

    if len(somethings) < 5:
        logger.info(f"User {user_id} has {len(somethings)} somethings, skipping clustering")
        return {}

    # Get embeddings from FAISS
    something_ids = [s.id for s in somethings]
    texts = [s.content or f"[{s.content_type}]" for s in somethings]

    # Generate fresh embeddings
    embeddings_list = embedding_service.generate_embeddings_batch(texts)
    embeddings = np.array(embeddings_list, dtype=np.float32)

    # Perform clustering
    clustered = self.clusterer.cluster_kmeans(embeddings, something_ids)

    # Group by cluster_id
    clusters: Dict[int, List[int]] = {}
    for something_id, cluster_id in clustered:
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append(something_id)

    logger.info(f"Created {len(clusters)} clusters for user {user_id}")
    return clusters
```

**Technical Notes:**
- Updated to use Something model
- Handles multimodal content (uses content or content_type)
- Returns cluster_id → something_ids mapping

**Prerequisites:** Story 2.2 (Embedding service), Story 2.3 (FAISS)

---

## Story 4.3: Implement LLM-Based Circle Naming

**User Story:**
As a developer, I want to use LLM to generate descriptive names for circles based on something content and meanings, so that users can understand what each cluster represents.

**Acceptance Criteria:**

**Given** I have a cluster of related somethings
**When** I request a circle name
**Then** I add to `app/services/llm_service.py`:

```python
async def generate_circle_name(self, something_texts: List[str], meanings: List[Optional[str]]) -> Optional[str]:
    """
    Generate a descriptive name for a circle based on something content and meanings

    Args:
        something_texts: List of something texts in the circle (sample of 5-10)
        meanings: List of corresponding meanings (can be None)

    Returns:
        Circle name (2-4 words), or None if LLM fails
    """
    # Sample somethings if too many (use first 10 for performance)
    sample_texts = something_texts[:10]
    sample_meanings = meanings[:10] if meanings else []

    system_prompt = """You are an expert at analyzing themes and creating descriptive labels.
Your task is to generate a short, descriptive name for a Circle of Care.

Rules:
- Name should be 2-4 words maximum
- Name should capture the central theme or topic
- Use title case (e.g., "Fitness Goals", "Creative Projects")
- Be specific, not generic (avoid "Various Ideas", "Random Thoughts")
- Return ONLY the name, no explanation or commentary"""

    # Build context from somethings and meanings
    context_lines = []
    for i, (text, meaning) in enumerate(zip(sample_texts, sample_meanings)):
        line = f"- {text}"
        if meaning:
            line += f" (meaning: {meaning})"
        context_lines.append(line)

    somethings_text = "\n".join(context_lines)

    user_prompt = f"""Generate a descriptive name for this Circle of Care:

{somethings_text}

Return only the name (2-4 words, title case)."""

    response = await self.generate(
        prompt=user_prompt,
        system_prompt=system_prompt,
        temperature=0.5,  # Moderate creativity
        max_tokens=20  # Short response
    )

    if response is None:
        return None

    # Clean up response
    name = response.strip().strip('"').strip("'").strip()

    # Validate length
    words = name.split()
    if len(words) > 4 or len(name) > 50:
        logger.warning(f"Generated name too long: {name}, using fallback")
        return "Untitled Circle"

    return name
```

**Technical Notes:**
- Uses both content and meaning for naming
- 2-4 word names
- Fallback to "Untitled Circle"

**Prerequisites:** Story 3.1 (LLM service)

---

## Story 4.4: Create Circles API Endpoints with Junction Table Support

**User Story:**
As a developer, I want to implement CRUD API endpoints for circles with junction table operations, so that iOS can list, view, and manage circles with flexible multi-circle assignments.

**Acceptance Criteria:**

**Given** iOS needs to interact with circles
**When** I implement circles endpoints
**Then** I create `app/api/v1/endpoints/circles.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.core.database import get_db
from app.schemas.circle import CircleResponse, CircleWithSomethings, CircleCreate
from app.models.circle import Circle
from app.models.something import Something
from app.models.something_circle import SomethingCircle
from typing import List

router = APIRouter()

@router.get("", response_model=List[CircleResponse])
async def list_circles(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all circles for authenticated user with something counts"""
    circles = db.query(Circle).filter(Circle.user_id == user.id).all()

    # Add something counts
    result = []
    for circle in circles:
        something_count = db.query(SomethingCircle).filter(
            SomethingCircle.circle_id == circle.id
        ).count()

        circle_dict = {
            **circle.__dict__,
            "something_count": something_count
        }
        result.append(CircleResponse(**circle_dict))

    return result

@router.get("/{circle_id}", response_model=CircleWithSomethings)
async def get_circle(
    circle_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get single circle with all somethings"""
    circle = db.query(Circle).filter(
        Circle.id == circle_id,
        Circle.user_id == user.id
    ).first()

    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")

    # Get somethings in this circle (via junction table)
    something_circles = db.query(SomethingCircle).filter(
        SomethingCircle.circle_id == circle_id
    ).all()

    something_ids = [sc.something_id for sc in something_circles]
    somethings = db.query(Something).filter(
        Something.id.in_(something_ids)
    ).order_by(Something.created_at.desc()).all()

    return CircleWithSomethings(
        **circle.__dict__,
        something_count=len(somethings),
        somethings=somethings
    )

@router.post("/{circle_id}/somethings/{something_id}", status_code=204)
async def add_something_to_circle(
    circle_id: int,
    something_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Manually add a something to a circle (creates junction record)"""
    # Verify circle exists and belongs to user
    circle = db.query(Circle).filter(
        Circle.id == circle_id,
        Circle.user_id == user.id
    ).first()

    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")

    # Verify something exists and belongs to user
    something = db.query(Something).filter(
        Something.id == something_id,
        Something.user_id == user.id
    ).first()

    if not something:
        raise HTTPException(status_code=404, detail="Something not found")

    # Check if relationship already exists
    existing = db.query(SomethingCircle).filter(
        SomethingCircle.something_id == something_id,
        SomethingCircle.circle_id == circle_id
    ).first()

    if existing:
        return None  # Already exists, idempotent

    # Create junction record (user-assigned)
    something_circle = SomethingCircle(
        something_id=something_id,
        circle_id=circle_id,
        is_user_assigned=True,
        confidence_score=None  # No confidence score for manual assignments
    )
    db.add(something_circle)
    db.commit()

    return None

@router.delete("/{circle_id}/somethings/{something_id}", status_code=204)
async def remove_something_from_circle(
    circle_id: int,
    something_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a something from a circle (deletes junction record)"""
    # Verify circle belongs to user
    circle = db.query(Circle).filter(
        Circle.id == circle_id,
        Circle.user_id == user.id
    ).first()

    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")

    # Find and delete junction record
    something_circle = db.query(SomethingCircle).filter(
        SomethingCircle.something_id == something_id,
        SomethingCircle.circle_id == circle_id
    ).first()

    if not something_circle:
        raise HTTPException(status_code=404, detail="Something not found in this circle")

    db.delete(something_circle)
    db.commit()

    return None

@router.post("/trigger-clustering", status_code=202)
async def trigger_clustering(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Manually trigger clustering for user's somethings
    Creates circles and assigns somethings via junction table
    """
    from app.services.clustering_service import clustering_service
    from app.services.llm_service import llm_service

    # Get clusters
    clusters = await clustering_service.cluster_user_somethings(user.id, db)

    if not clusters:
        return {"message": "Not enough somethings for clustering"}

    # Create/update circles for each cluster
    circles_created = 0
    for cluster_id, something_ids in clusters.items():
        # Get somethings in cluster
        somethings = db.query(Something).filter(
            Something.id.in_(something_ids)
        ).all()

        something_texts = [s.content or f"[{s.content_type}]" for s in somethings]
        meanings = [s.meaning for s in somethings]

        # Generate circle name
        circle_name = await llm_service.generate_circle_name(something_texts, meanings)
        if circle_name is None:
            circle_name = f"Untitled Circle {cluster_id + 1}"

        # Create circle
        circle = Circle(
            user_id=user.id,
            circle_name=circle_name,
            description=f"Auto-generated cluster with {len(something_ids)} somethings"
        )
        db.add(circle)
        db.flush()  # Get circle.id

        # Assign somethings to circle via junction table
        for something in somethings:
            # Check if already assigned
            existing = db.query(SomethingCircle).filter(
                SomethingCircle.something_id == something.id,
                SomethingCircle.circle_id == circle.id
            ).first()

            if not existing:
                something_circle = SomethingCircle(
                    something_id=something.id,
                    circle_id=circle.id,
                    is_user_assigned=False,  # Auto-assigned
                    confidence_score=0.8  # Default confidence for clustering
                )
                db.add(something_circle)

        circles_created += 1

    db.commit()

    return {
        "message": f"Created {circles_created} circles",
        "circle_count": circles_created
    }
```

**Technical Notes:**
- Junction table operations (add/remove)
- Many-to-many support
- Learning signals tracked
- Clustering creates junction records

**Prerequisites:** Story 4.1 (Circle model), Story 4.2 (Clustering), Story 4.3 (Naming)

---

## Story 4.5: Build iOS Circle List and Detail Views

**User Story:**
As a user, I want to see a list of my Circles of Care with something counts, and view all somethings within a circle, so that I can explore my organized knowledge.

**Acceptance Criteria:**

[Similar to original Epic 4 Story 4.6, but using Circle/Something terminology and junction table logic]

**Implementation:**

Update `Services/APIService.swift`:

```swift
struct Circle: Codable, Identifiable {
    let id: Int
    let userId: String
    let circleName: String
    let description: String?
    let somethingCount: Int
    let careFrequency: Int
    let createdAt: Date
    let updatedAt: Date
}

struct CircleWithSomethings: Codable {
    let id: Int
    let userId: String
    let circleName: String
    let description: String?
    let somethingCount: Int
    let somethings: [Something]
    let careFrequency: Int
    let createdAt: Date
    let updatedAt: Date
}

extension APIService {
    func listCircles() async throws -> [Circle] {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/circles")!
        var request = URLRequest(url: url)
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 200:
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .iso8601
            return try decoder.decode([Circle].self, from: data)
        case 401:
            throw APIError.unauthorized
        default:
            throw APIError.serverError("Failed to list circles")
        }
    }

    func getCircle(id: Int) async throws -> CircleWithSomethings {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/circles/\(id)")!
        var request = URLRequest(url: url)
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 200:
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .iso8601
            return try decoder.decode(CircleWithSomethings.self, from: data)
        case 401:
            throw APIError.unauthorized
        case 404:
            throw APIError.serverError("Circle not found")
        default:
            throw APIError.serverError("Failed to get circle")
        }
    }

    func triggerClustering() async throws {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/circles/trigger-clustering")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")

        let (_, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 202:
            return
        case 401:
            throw APIError.unauthorized
        default:
            throw APIError.serverError("Failed to trigger clustering")
        }
    }
}
```

[Views similar to original, but using Circle terminology]

**Technical Notes:**
- Updated to use "Circle" and "Something"
- Junction table relationships handled by backend
- Pull-to-refresh support

**Prerequisites:** Story 4.4 (Circles API), Story 2.5 (APIService)

---

## Story 4.6: Implement Circle Centroid Learning (RL Feedback Loop)

**User Story:**
As a developer, I want to implement circle centroid tracking and incremental updates based on user feedback, so that the system learns from user corrections and improves circle predictions over time.

**Acceptance Criteria:**

**Given** I need to build a personalized semantic system that learns from user feedback
**When** I implement centroid tracking and updates
**Then** I update the Circle model to include centroid storage:

**Step 1: Update Circle Model**

```python
# In app/models/circle.py
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, ARRAY, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
from sqlalchemy.orm import relationship
from app.models.base import Base

class Circle(Base):
    __tablename__ = "circles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    circle_name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    centroid_embedding = Column(ARRAY(Float, dimensions=1), nullable=True)  # NEW: 384-dim centroid
    care_frequency = Column(Integer, server_default=text('0'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="circles")
    somethings = relationship("SomethingCircle", back_populates="circle", cascade="all, delete-orphan")
```

**Step 2: Create Centroid Service**

Create `app/services/centroid_service.py`:

```python
from app.models.circle import Circle
from app.models.something_circle import SomethingCircle
from app.models.something import Something
from sqlalchemy.orm import Session
from typing import List, Tuple, Optional
import numpy as np
from loguru import logger

class CentroidService:
    """Manages circle centroids for personalized semantic learning"""

    async def initialize_centroid(
        self,
        circle_id: int,
        first_embedding: List[float],
        db: Session
    ) -> None:
        """Initialize centroid when first item added to circle"""
        circle = db.query(Circle).filter(Circle.id == circle_id).first()
        if not circle:
            raise ValueError(f"Circle {circle_id} not found")

        circle.centroid_embedding = first_embedding
        db.commit()
        logger.info(f"Initialized centroid for circle {circle_id}")

    async def update_centroid_add(
        self,
        circle_id: int,
        new_embedding: List[float],
        db: Session
    ) -> None:
        """
        Incrementally update centroid when item added to circle

        Formula: centroid_new = (N * centroid_old + embedding_new) / (N + 1)
        """
        circle = db.query(Circle).filter(Circle.id == circle_id).first()
        if not circle:
            raise ValueError(f"Circle {circle_id} not found")

        # Count items currently in circle
        n_items = db.query(SomethingCircle).filter(
            SomethingCircle.circle_id == circle_id
        ).count()

        if circle.centroid_embedding is None or n_items == 1:
            # First item - initialize centroid
            circle.centroid_embedding = new_embedding
        else:
            # Incremental update
            old_centroid = np.array(circle.centroid_embedding)
            new_emb = np.array(new_embedding)
            updated_centroid = ((n_items - 1) * old_centroid + new_emb) / n_items

            # Normalize to unit vector
            norm = np.linalg.norm(updated_centroid)
            if norm > 0:
                updated_centroid = updated_centroid / norm

            circle.centroid_embedding = updated_centroid.tolist()

        db.commit()
        logger.info(f"Updated centroid for circle {circle_id} (n_items={n_items})")

    async def update_centroid_remove(
        self,
        circle_id: int,
        removed_embedding: List[float],
        db: Session
    ) -> None:
        """
        Update centroid when item removed from circle

        Formula: centroid_new = (N * centroid_old - embedding_removed) / (N - 1)
        """
        circle = db.query(Circle).filter(Circle.id == circle_id).first()
        if not circle:
            raise ValueError(f"Circle {circle_id} not found")

        # Count items after removal
        n_items = db.query(SomethingCircle).filter(
            SomethingCircle.circle_id == circle_id
        ).count()

        if n_items == 0:
            # No items left - clear centroid
            circle.centroid_embedding = None
        elif circle.centroid_embedding:
            # Reverse the addition
            old_centroid = np.array(circle.centroid_embedding)
            removed = np.array(removed_embedding)
            updated_centroid = ((n_items + 1) * old_centroid - removed) / n_items

            # Normalize
            norm = np.linalg.norm(updated_centroid)
            if norm > 0:
                updated_centroid = updated_centroid / norm

            circle.centroid_embedding = updated_centroid.tolist()

        db.commit()
        logger.info(f"Removed item from centroid for circle {circle_id} (n_items={n_items})")

    async def compute_circle_similarities(
        self,
        query_embedding: List[float],
        user_id: str,
        db: Session,
        top_k: int = 5
    ) -> List[Tuple[int, str, float]]:
        """
        Compute similarity between query and all user's circle centroids

        Returns:
            List of (circle_id, circle_name, similarity_score) tuples, sorted by similarity
        """
        circles = db.query(Circle).filter(Circle.user_id == user_id).all()

        similarities = []
        query_vec = np.array(query_embedding)
        query_norm = np.linalg.norm(query_vec)

        for circle in circles:
            if circle.centroid_embedding:
                centroid = np.array(circle.centroid_embedding)

                # Cosine similarity
                similarity = np.dot(query_vec, centroid) / (
                    query_norm * np.linalg.norm(centroid)
                )

                similarities.append((circle.id, circle.circle_name, float(similarity)))

        # Sort by similarity descending
        similarities.sort(key=lambda x: x[2], reverse=True)

        return similarities[:top_k]

    async def predict_circles_for_something(
        self,
        something_id: int,
        user_id: str,
        db: Session,
        threshold: float = 0.7,
        top_k: int = 3
    ) -> List[Tuple[int, str, float]]:
        """
        Predict which circles a something should belong to

        Returns:
            List of (circle_id, circle_name, confidence_score) suggestions
        """
        # Get something's embedding (assuming it's stored or can be retrieved)
        something = db.query(Something).filter(Something.id == something_id).first()
        if not something:
            raise ValueError(f"Something {something_id} not found")

        # Generate embedding if not stored (this assumes embedding is stored or regenerated)
        from app.services.embedding_service import embedding_service
        content = something.content or f"[{something.content_type}]"
        embedding = embedding_service.generate_embedding(content)

        # Get similar circles
        similarities = await self.compute_circle_similarities(
            embedding, user_id, db, top_k=top_k
        )

        # Filter by threshold
        predictions = [
            (cid, name, score)
            for cid, name, score in similarities
            if score >= threshold
        ]

        return predictions

# Singleton instance
centroid_service = CentroidService()
```

**Step 3: Update Circles API to Trigger Centroid Updates**

Update `app/api/v1/endpoints/circles.py`:

```python
# Add centroid updates when somethings are assigned/removed

@router.post("/{circle_id}/somethings/{something_id}")
async def assign_something_to_circle(
    circle_id: int,
    something_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Assign a something to a circle and update centroid"""
    from app.services.centroid_service import centroid_service
    from app.services.embedding_service import embedding_service

    # Verify ownership
    circle = db.query(Circle).filter(
        Circle.id == circle_id,
        Circle.user_id == user.id
    ).first()
    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")

    something = db.query(Something).filter(
        Something.id == something_id,
        Something.user_id == user.id
    ).first()
    if not something:
        raise HTTPException(status_code=404, detail="Something not found")

    # Check if already assigned
    existing = db.query(SomethingCircle).filter(
        SomethingCircle.something_id == something_id,
        SomethingCircle.circle_id == circle_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already assigned")

    # Create assignment
    assignment = SomethingCircle(
        something_id=something_id,
        circle_id=circle_id,
        is_user_assigned=True,  # User explicitly assigned
        confidence_score=1.0
    )
    db.add(assignment)
    db.commit()

    # Update centroid
    content = something.content or f"[{something.content_type}]"
    embedding = embedding_service.generate_embedding(content)
    await centroid_service.update_centroid_add(circle_id, embedding, db)

    return {"message": "Something assigned and centroid updated"}

@router.delete("/{circle_id}/somethings/{something_id}")
async def remove_something_from_circle(
    circle_id: int,
    something_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a something from a circle and update centroid"""
    from app.services.centroid_service import centroid_service
    from app.services.embedding_service import embedding_service

    # Verify assignment exists and user owns it
    assignment = db.query(SomethingCircle).join(Circle).filter(
        SomethingCircle.something_id == something_id,
        SomethingCircle.circle_id == circle_id,
        Circle.user_id == user.id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Get embedding before deletion
    something = db.query(Something).filter(Something.id == something_id).first()
    content = something.content or f"[{something.content_type}]"
    embedding = embedding_service.generate_embedding(content)

    # Delete assignment
    db.delete(assignment)
    db.commit()

    # Update centroid
    await centroid_service.update_centroid_remove(circle_id, embedding, db)

    return {"message": "Something removed and centroid updated"}

@router.get("/{circle_id}/predict-similar")
async def get_similar_somethings_to_circle(
    circle_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    top_k: int = 10
):
    """Get somethings similar to this circle's centroid (for suggestions)"""
    from app.services.centroid_service import centroid_service

    circle = db.query(Circle).filter(
        Circle.id == circle_id,
        Circle.user_id == user.id
    ).first()
    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")

    if not circle.centroid_embedding:
        return {"predictions": []}

    # Get all user's somethings not in this circle
    somethings = db.query(Something).filter(
        Something.user_id == user.id
    ).outerjoin(
        SomethingCircle,
        (SomethingCircle.something_id == Something.id) &
        (SomethingCircle.circle_id == circle_id)
    ).filter(SomethingCircle.id.is_(None)).all()

    # Compute similarities
    from app.services.embedding_service import embedding_service
    predictions = []

    for something in somethings:
        content = something.content or f"[{something.content_type}]"
        embedding = embedding_service.generate_embedding(content)

        # Cosine similarity with centroid
        emb_arr = np.array(embedding)
        centroid_arr = np.array(circle.centroid_embedding)
        similarity = np.dot(emb_arr, centroid_arr) / (
            np.linalg.norm(emb_arr) * np.linalg.norm(centroid_arr)
        )

        if similarity >= 0.7:  # Threshold
            predictions.append({
                "somethingId": something.id,
                "content": something.content,
                "similarity": float(similarity)
            })

    # Sort by similarity
    predictions.sort(key=lambda x: x["similarity"], reverse=True)

    return {"predictions": predictions[:top_k]}
```

**Step 4: Create Database Migration**

```bash
cd backend/pookie-backend
poetry run alembic revision -m "add_centroid_embedding_to_circles"
```

Migration file:
```python
def upgrade():
    op.add_column('circles', sa.Column('centroid_embedding',
        postgresql.ARRAY(sa.Float()), nullable=True))

def downgrade():
    op.drop_column('circles', 'centroid_embedding')
```

**Technical Notes:**

**Centroid Math:**
- **Initialize:** `centroid = embedding_first_item`
- **Add item:** `centroid_new = (N * centroid_old + embedding_new) / (N + 1)`
- **Remove item:** `centroid_new = ((N+1) * centroid_old - embedding_removed) / N`
- **Normalize:** Convert to unit vector for consistent similarity comparisons

**Learning Loop:**
1. User uploads something → Backend predicts circles using centroids
2. User accepts/rejects → `is_user_assigned=True` stored
3. Centroid shifts toward accepted items
4. Future predictions improve (RL-style feedback)

**Storage:**
- Centroid stored as PostgreSQL `ARRAY(Float)` (384 dimensions)
- Updated incrementally in O(1) time (no need to recompute from scratch)
- Normalized to unit vector for consistent cosine similarity

**Similarity Threshold:**
- 0.7-1.0: High confidence (auto-assign)
- 0.5-0.7: Medium confidence (suggest to user)
- <0.5: Low confidence (don't suggest)

**Prerequisites:**
- Story 4.1 (Circle model)
- Story 2.2 (Embedding service)
- Story 4.4 (Circles API)

**References:**
- Architecture Document: `docs/pookie-semantic-architecture.md`
- Centroid learning section in architecture doc

---

## Epic 4 Summary

**Stories Created:** 6 stories (added Story 4.6: Circle Centroid Learning)
**FR Coverage:**
- FR5 (Semantic Clustering - Automatic Grouping) ✅
- FR6 (Circle Naming & Management) ✅

**Technical Capabilities Established:**
- ✅ SQLAlchemy Circle model with junction table
- ✅ K-means clustering algorithm
- ✅ LLM-based circle naming
- ✅ Circles CRUD API with many-to-many support
- ✅ Junction table operations (add/remove somethings)
- ✅ iOS Circle list, detail, and something detail views
- ✅ Manual clustering trigger
- ✅ Circle centroid tracking and incremental updates (NEW - Story 4.6)
- ✅ Reinforcement learning loop via user feedback (NEW - Story 4.6)
- ✅ Personalized circle prediction using centroids (NEW - Story 4.6)

**Ready for Epic 5:** Personalized Discovery (now using circle centroids instead of static averages)

---

## Epic 5: Personalized Discovery

**Epic Goal:** Enable users to receive personalized action recommendations based on their unique taste profile learned from saved somethings, helping them discover experiences and activities aligned with their interests.

**FR Coverage:** FR9 (Discover Mode - Taste Learning), FR10 (Discover Mode - Action Recommendations)

**User Value Statement:** After this epic, users can request recommendations and receive personalized suggestions (content to consume, goals to pursue) that align with their interests, learned from the patterns in their somethings.

---

## Story 5.1: Implement Taste Profile Analysis Service

**User Story:**
As a developer, I want to analyze embedding patterns and meanings to generate a user's taste profile, so that I can understand what topics and themes the user cares about.

**Acceptance Criteria:**

**Given** I need to understand user preferences
**When** I implement taste profile analysis
**Then** I create `app/services/taste_service.py`:

```python
from app.models.something import Something
from app.models.circle import Circle
from app.models.something_circle import SomethingCircle
from app.services.embedding_service import embedding_service
from sqlalchemy.orm import Session
from typing import Dict, List, Tuple
import numpy as np
from collections import Counter
import logging

logger = logging.getLogger(__name__)

class TasteService:
    async def generate_taste_profile(self, user_id: str, db: Session) -> Dict:
        """
        Analyze user's somethings to generate taste profile

        Returns:
            Dictionary with:
            - top_topics: List of (topic_name, relevance_score) tuples
            - top_meanings: Most common meaning themes
            - dominant_circles: Circles with most somethings (main interests)
            - embedding_centroid: Average embedding vector (taste center)
        """
        # Get all user somethings
        somethings = db.query(Something).filter(Something.user_id == user_id).all()

        if len(somethings) < 3:
            logger.info(f"User {user_id} has {len(somethings)} somethings, insufficient for taste profile")
            return {
                "top_topics": [],
                "top_meanings": [],
                "dominant_circles": [],
                "embedding_centroid": None
            }

        # Extract meanings
        all_meanings = []
        for something in somethings:
            if something.meaning:
                all_meanings.append(something.meaning)

        # Get dominant circles
        circles = db.query(Circle).filter(Circle.user_id == user.id).all()
        circle_something_counts = []
        for circle in circles:
            count = db.query(SomethingCircle).filter(
                SomethingCircle.circle_id == circle.id
            ).count()
            if count > 0:
                circle_something_counts.append((circle.circle_name, count))

        # Sort by something count descending
        dominant_circles = sorted(circle_something_counts, key=lambda x: x[1], reverse=True)[:5]

        # Use circle centroids for vibe profile (personalized semantic space)
        # This leverages the RL-learned centroids from Story 4.6
        circle_centroids = {}
        for circle in circles:
            if circle.centroid_embedding:
                circle_centroids[circle.circle_name] = circle.centroid_embedding

        # Calculate overall vibe centroid (weighted average of circle centroids)
        if circle_centroids:
            # Weight by number of somethings in each circle
            weighted_centroids = []
            total_items = 0
            for circle_name, count in circle_something_counts:
                if circle_name in circle_centroids:
                    weighted_centroids.append(
                        np.array(circle_centroids[circle_name]) * count
                    )
                    total_items += count

            if weighted_centroids:
                # Weighted average
                centroid = sum(weighted_centroids) / total_items
                centroid_normalized = centroid / np.linalg.norm(centroid)
            else:
                centroid_normalized = None
        else:
            centroid_normalized = None

        # Top topics from circle names
        top_topics = []
        for circle_name, count in dominant_circles:
            relevance = count / len(somethings)  # Proportion of somethings in this circle
            top_topics.append((circle_name, relevance))

        # Top meanings (sample first 10)
        top_meanings = all_meanings[:10]

        logger.info(f"Generated taste profile for user {user_id}: {len(top_topics)} topics, {len(all_meanings)} meanings")

        return {
            "top_topics": top_topics,  # [(topic, relevance), ...]
            "top_meanings": top_meanings,  # [meaning1, meaning2, ...]
            "dominant_circles": [name for name, count in dominant_circles],  # [circle1, circle2, ...]
            "embedding_centroid": centroid_normalized.tolist() if centroid_normalized is not None else None,  # Overall vibe (weighted avg of circle centroids)
            "circle_centroids": circle_centroids  # NEW: Individual circle centroids for personalized retrieval
        }

    async def get_taste_summary(self, user_id: str, db: Session) -> str:
        """
        Generate human-readable taste summary

        Returns:
            String like "You care about Fitness Goals, Creative Projects, and Learning"
        """
        profile = await self.generate_taste_profile(user_id, db)

        if not profile["top_topics"]:
            return "Not enough data to understand your interests yet. Capture more somethings!"

        # Format top topics
        topics = [topic for topic, _ in profile["top_topics"][:3]]

        if len(topics) == 0:
            return "Not enough data yet"
        elif len(topics) == 1:
            return f"You care about {topics[0]}"
        elif len(topics) == 2:
            return f"You care about {topics[0]} and {topics[1]}"
        else:
            return f"You care about {', '.join(topics[:-1])}, and {topics[-1]}"

# Singleton instance
taste_service = TasteService()
```

**Technical Notes:**
- Uses meanings instead of tags
- Circles instead of abodes
- Junction table relationships
- **UPDATED:** Uses circle centroids from Story 4.6 (RL-learned) instead of static np.mean()
- Vibe profile = weighted average of circle centroids (personalized semantic space)
- Each circle centroid represents learned user preferences in that category
- Overall centroid weighted by circle size (larger circles have more influence)

**Prerequisites:** Story 4.1 (Circle model), Story 2.2 (Embedding service), Story 4.6 (Circle centroids)

---

## Story 5.2: Implement Recommendation Generation with RAG + LLM

[Similar to original, but updated to use "somethings" and "meanings"]

```python
async def generate_recommendations(
    self,
    taste_summary: str,
    recommendation_type: str,
    recent_somethings_sample: List[str],
    recent_meanings_sample: List[str]
) -> Optional[Dict]:
    """
    Generate personalized recommendations using RAG + LLM

    Args:
        taste_summary: Human-readable taste profile
        recommendation_type: "content" or "goal"
        recent_somethings_sample: Sample of recent something texts (5-10)
        recent_meanings_sample: Sample of recent meanings (5-10)

    Returns:
        Dictionary with:
        - action: The recommended action
        - reason: Why this recommendation fits
        - category: Type of recommendation
    """
    # Build context from recent somethings and meanings
    context_lines = []
    for text, meaning in zip(recent_somethings_sample[:10], recent_meanings_sample[:10]):
        line = f"- {text}"
        if meaning:
            line += f" (meaning: {meaning})"
        context_lines.append(line)

    somethings_context = "\n".join(context_lines)

    # [Rest similar to original Epic 5 Story 5.2]
```

**Technical Notes:**
- Includes meanings in context
- Uses "somethings" terminology
- Otherwise similar flow

**Prerequisites:** Story 5.1 (Taste service), Story 3.1 (LLM service)

---

## Story 5.3: Create Discover API Endpoint

[Similar to original, updated to use Something/Circle terminology]

---

## Story 5.4: Build iOS Discover View with Recommendation UI

[Similar to original, updated UI text to reference "somethings" and "circles"]

---

## Epic 5 Summary

**Stories Created:** 4 stories
**FR Coverage:**
- FR9 (Discover Mode - Taste Learning) ✅
- FR10 (Discover Mode - Action Recommendations) ✅

**Technical Capabilities Established:**
- ✅ Taste profile analysis (circles, meanings, embedding centroid)
- ✅ Recommendation generation (RAG + LLM synthesis)
- ✅ Two recommendation types: content vs goal
- ✅ Discover API endpoint
- ✅ iOS Discover view with card-based UI

**Ready for Epic 6:** RAG-Powered Personal Chat

---

## Epic 6: RAG-Powered Personal Chat

**Epic Goal:** Enable users to ask natural language questions and receive personalized answers based on their saved somethings, with streaming responses and intelligent fallback to general knowledge when needed.

**FR Coverage:** FR7 (RAG-Powered Chat Interface), FR8 (Confidence-Based Chat Fallback), FR15 (Streaming LLM Responses)

**User Value Statement:** After this epic, users can chat with their personal knowledge base, asking questions and getting instant answers based on their own somethings, with real-time streaming responses for a responsive experience.

---

## Story 6.1: Implement RAG Service with Vector Search

**User Story:**
As a developer, I want to implement RAG (Retrieval-Augmented Generation) with FAISS vector search, so that I can retrieve relevant somethings for a user's question.

**Acceptance Criteria:**

[Similar to original, but updated to retrieve "Somethings" and include meanings in context]

```python
class RAGService:
    def format_context(self, somethings: List[Something]) -> str:
        """
        Format retrieved somethings into context string for LLM

        Returns:
            Formatted context with content and meanings
        """
        if not somethings:
            return "No relevant somethings found."

        context_lines = ["From your saved somethings:"]
        for i, something in enumerate(somethings, 1):
            line = f"{i}. {something.content or f'[{something.content_type}]'}"
            if something.meaning:
                line += f" (meaning: {something.meaning})"
            context_lines.append(line)

        return "\n".join(context_lines)
```

**Technical Notes:**
- Retrieves "Something" objects
- Includes meanings in context
- Handles multimodal content types

**Prerequisites:** Story 2.3 (FAISS), Story 2.2 (Embeddings)

---

## Story 6.2: Implement Streaming Chat Service with Claude Haiku

[Similar to original, but updated to use "somethings" terminology]

```python
# System prompt updated:
system_prompt = """You are Pookie, a personal AI assistant with access to the user's saved somethings.
Your task is to answer questions based on their personal knowledge.

Rules:
- Use ONLY information from the provided somethings
- If the somethings don't contain the answer, say "I don't have that information in your somethings"
- Be conversational and helpful
- Reference specific somethings when relevant
- Keep responses concise (2-3 paragraphs max)"""
```

**Technical Notes:**
- Updated terminology
- Otherwise similar flow

**Prerequisites:** Story 6.1 (RAG service)

---

## Story 6.3: Create Streaming Chat API Endpoint with SSE

[UNCHANGED from original - SSE endpoint works the same]

---

## Story 6.4: Implement iOS SSE Client and Chat UI

[UNCHANGED from original - iOS chat UI works the same]

---

## Epic 6 Summary

**Stories Created:** 4 stories
**FR Coverage:**
- FR7 (RAG-Powered Chat Interface) ✅
- FR8 (Confidence-Based Chat Fallback) ✅
- FR15 (Streaming LLM Responses) ✅

**Technical Capabilities Established:**
- ✅ RAG service with FAISS vector search
- ✅ Confidence-based mode switching (similarity ≥ 0.7)
- ✅ Streaming chat with Claude Haiku
- ✅ SSE API endpoint
- ✅ iOS SSE client
- ✅ Real-time chat UI with mode indicators

**MVP Complete!** All 6 epics finished, aligned with actual schema.

---
---

# Epic Summary & Story Count

## Epic 1: Foundation & Infrastructure Setup
- **Stories:** 7
- **User Value:** Users can create accounts, log in, and access the app
- **Key Deliverables:** iOS + FastAPI projects, Supabase database, JWT auth, tab navigation

## Epic 2: Thought Capture & Storage
- **Stories:** 7
- **User Value:** Users can capture thoughts via text or voice
- **Key Deliverables:** Embeddings, FAISS vector search, CRUD API, voice input

## Epic 3: AI-Powered Thought Separation
- **Stories:** 4
- **User Value:** Users can paste brain dumps and AI separates distinct thoughts
- **Key Deliverables:** LLM service (OpenRouter), separation API, batch creation, iOS preview UI

## Epic 4: Semantic Organization (Abodes)
- **Stories:** 6
- **User Value:** Users see thoughts auto-organized into themed clusters
- **Key Deliverables:** K-means clustering, LLM naming, ML modes (tag/reflection/novelty), iOS abode views

## Epic 5: Personalized Discovery
- **Stories:** 4
- **User Value:** Users get personalized recommendations based on interests
- **Key Deliverables:** Taste profile analysis, recommendation generation, discover API, iOS card UI

## Epic 6: RAG-Powered Personal Chat
- **Stories:** 4
- **User Value:** Users chat with their knowledge base in real-time
- **Key Deliverables:** RAG service, streaming chat (Claude Haiku), SSE endpoint, iOS chat UI

**Total Stories:** 32 implementation-ready user stories

---

# Technology Stack Summary

## Backend (Python)
- **Framework:** FastAPI (cookiecutter-fastapi-ML)
- **Database:** PostgreSQL (Supabase, Alembic migrations)
- **ML:** sentence-transformers (all-MiniLM-L6-v2), scikit-learn, FAISS-CPU
- **LLM:** OpenRouter (mistralai/mistral-7b-instruct:free), Anthropic Claude Haiku
- **Auth:** Supabase JWT validation
- **Deployment:** Render free tier

## iOS (Swift)
- **Framework:** SwiftUI + iOS 17+ (@Observable)
- **Architecture:** MVVM + Shared AppState
- **Auth:** Supabase Swift SDK
- **Networking:** URLSession (REST + SSE streaming)
- **Voice:** iOS Speech framework (native)
- **Deployment:** TestFlight

## Infrastructure
- **Database:** Supabase PostgreSQL (free tier)
- **Storage:** Supabase Storage (FAISS index persistence)
- **Vector Search:** FAISS IndexFlatIP (exact cosine similarity)
- **Cost:** ~$0-3/month total (all free tiers)

---

# Success Metrics & Acceptance Targets

| Metric | Target | Epic | Validation Method |
|--------|--------|------|-------------------|
| RAG Retrieval Accuracy | 80%+ | Epic 6 | Manual testing with diverse queries |
| Thought Separation Acceptance | 75%+ | Epic 3 | User review of separated thoughts |
| Discover Recommendations Relevance | 70%+ | Epic 5 | User satisfaction feedback |
| Chat Response Latency | <2s to first token | Epic 6 | Performance monitoring |
| Clustering Quality | Minimal manual reorganization | Epic 4 | Silhouette score + user feedback |
| Embedding Generation | <500ms per thought | Epic 2 | Backend performance logs |
| Vector Search | <100ms for top-k | Epic 2 | FAISS benchmarks |

---

# Implementation Notes

## Development Order
1. **Epic 1** → Foundation (required for all others)
2. **Epic 2** → Thought capture (required for Epics 3-6)
3. **Epic 3** → Thought separation (optional, enhances capture)
4. **Epic 4** → Abodes (required for Epic 5)
5. **Epic 5** → Discovery (independent, requires Epic 4)
6. **Epic 6** → Chat (independent, requires Epic 2)

## Critical Path
Epic 1 → Epic 2 → Epic 4 → Epic 6 (core RAG functionality)

## Optional/Deferrable
- Epic 3 (Thought separation): Nice-to-have, can be added later
- Epic 5 (Discovery): Standalone feature, can be post-MVP
- ML Modes (Story 4.5): Optional enrichment, can run async/batch

## Testing Strategy
- **Unit Tests:** Services (embedding, LLM, clustering, RAG)
- **Integration Tests:** API endpoints (thoughts, abodes, chat)
- **E2E Tests:** iOS UI flows (capture → cluster → chat)
- **Manual Tests:** ML quality (separation, naming, recommendations, RAG accuracy)

---

# Next Steps After Epic Completion

## Phase 1: Core Implementation (Epics 1-2, 4, 6)
1. Set up infrastructure (Epic 1: Stories 1.1-1.7)
2. Implement thought capture (Epic 2: Stories 2.1-2.7)
3. Build clustering (Epic 4: Stories 4.1-4.4, skip 4.5 initially)
4. Add RAG chat (Epic 6: Stories 6.1-6.4)
5. **Testing & validation**

## Phase 2: Enhancement (Epics 3, 5, ML Modes)
1. Add thought separation (Epic 3: Stories 3.1-3.4)
2. Build discovery (Epic 5: Stories 5.1-5.4)
3. Enable ML modes (Epic 4: Story 4.5)
4. **Polish & optimization**

## Phase 3: Production Readiness
1. Deployment automation (GitHub Actions CI/CD)
2. Monitoring & logging (Sentry, CloudWatch)
3. Performance optimization (caching, batch processing)
4. Security audit (penetration testing, OWASP)
5. Documentation (API docs, deployment guide, user guide)

---

# Document Metadata

- **Project:** Pookie - Personal ML-Powered Knowledge Management
- **Author:** sudy
- **Generated:** 2025-12-03
- **Document Type:** Epic & Story Breakdown
- **Total Epics:** 6
- **Total Stories:** 32
- **Total Lines:** 6300+
- **FR Coverage:** 15/15 (100%)

**Status:** ✅ **COMPLETE - Ready for Implementation**

