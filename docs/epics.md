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

## Epic 2: Thought Capture & Storage

**Epic Goal:** Enable users to capture and save their thoughts using text and voice input, with automatic embedding generation and vector storage for semantic search.

**FR Coverage:** FR2 (Thought Capture - Text Input), FR3 (Thought Capture - Voice Input)

**User Value Statement:** After this epic, users can capture thoughts via text or voice, see a list of saved thoughts, and know that their thoughts are being processed for semantic organization (even if clustering isn't visible yet).

---

### Story 2.1: Create SQLAlchemy Thought Model and Pydantic Schemas

**User Story:**
As a developer, I want to create the SQLAlchemy ORM model and Pydantic schemas for thoughts, so that I have type-safe data structures for database operations and API communication.

**Acceptance Criteria:**

**Given** I need to persist thoughts in the database
**When** I create the Thought model and schemas
**Then** I create `app/models/thought.py` with SQLAlchemy model:

```python
from sqlalchemy import Column, Integer, String, Float, ARRAY, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.models.base import Base

class Thought(Base):
    __tablename__ = "thoughts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    thought_text = Column(Text, nullable=False)
    tags = Column(ARRAY(String), default=list)
    reflection = Column(Text, nullable=True)
    novelty_score = Column(Float, nullable=True)
    abode_id = Column(Integer, ForeignKey("abodes.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

**And** I create `app/schemas/thought.py` with Pydantic schemas:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class ThoughtBase(BaseModel):
    thought_text: str = Field(alias="thoughtText", min_length=1, max_length=10000)

class ThoughtCreate(ThoughtBase):
    pass

class ThoughtResponse(ThoughtBase):
    id: int
    user_id: str = Field(alias="userId")
    tags: List[str] = Field(default_factory=list)
    reflection: Optional[str] = None
    novelty_score: Optional[float] = Field(alias="noveltyScore", default=None)
    abode_id: Optional[int] = Field(alias="abodeId", default=None)
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        populate_by_name = True
        from_attributes = True
```

**And** the Pydantic schemas use Field aliases to convert:
- Database/Python: `thought_text`, `user_id`, `created_at` (snake_case)
- API JSON: `thoughtText`, `userId`, `createdAt` (camelCase)

**And** I can import and use these models in API endpoints

**Technical Notes:**
- Follow Architecture "Cross-Platform Naming: Hybrid with Pydantic Transformation"
- Database: snake_case columns (thought_text, user_id)
- API JSON: camelCase via Pydantic Field aliases
- No custom Swift CodingKeys needed (native camelCase)
- DateTime columns use TIMESTAMP WITH TIME ZONE (UTC)
- from_attributes enables ORM object serialization

**Prerequisites:** Epic 1 Story 1.3 (Database schema created)

---

### Story 2.2: Implement sentence-transformers Embedding Service

**User Story:**
As a developer, I want to set up the sentence-transformers embedding service in the backend, so that I can generate 384-dimensional vector embeddings for all saved thoughts.

**Acceptance Criteria:**

**Given** I need to generate embeddings for semantic search
**When** I implement the embedding service
**Then** I add dependencies to `pyproject.toml`:

```toml
[tool.poetry.dependencies]
sentence-transformers = "^2.2.2"
torch = "^2.1.0"
```

**And** I run `poetry install` to install the packages

**And** I create `app/ml/embedding_model.py`:

```python
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class EmbeddingModel:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Load sentence-transformers model on initialization"""
        self.model = SentenceTransformer(model_name)
        self.dimension = 384  # all-MiniLM-L6-v2 embedding dimension

    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts

        Args:
            texts: List of text strings to encode

        Returns:
            numpy array of shape (len(texts), 384)
        """
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings

    def encode_single(self, text: str) -> np.ndarray:
        """Generate embedding for a single text (convenience method)"""
        return self.encode([text])[0]
```

**And** I create `app/services/embedding_service.py`:

```python
from app.ml.embedding_model import EmbeddingModel
from typing import List
import numpy as np

class EmbeddingService:
    def __init__(self):
        # Model loads once on service initialization
        self.embedding_model = EmbeddingModel()

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single thought

        Args:
            text: Thought text to encode

        Returns:
            List of 384 float values (embedding vector)
        """
        embedding = self.embedding_model.encode_single(text)
        return embedding.tolist()

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts (more efficient)"""
        embeddings = self.embedding_model.encode(texts)
        return embeddings.tolist()

# Singleton instance (loaded once at startup)
embedding_service = EmbeddingService()
```

**And** I update `app/main.py` to load the model at startup:

```python
from fastapi import FastAPI
from app.services.embedding_service import embedding_service

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Warm up embedding model (loads into memory)
    _ = embedding_service.generate_embedding("test")
    print("Embedding model loaded successfully")
```

**And** when the server starts, I see "Embedding model loaded successfully" in logs

**And** I can generate an embedding in <500ms for typical thought (50-200 words)

**And** the embedding is a list of 384 float values

**And** I can verify by calling:
```python
embedding = embedding_service.generate_embedding("I want to get jacked")
assert len(embedding) == 384
assert all(isinstance(x, float) for x in embedding)
```

**Technical Notes:**
- Follow Architecture "ML Pipeline: Backend-only embeddings (centralized)"
- Model: all-MiniLM-L6-v2 (80MB, runs on CPU, free)
- Dimension: 384 (fixed for this model)
- Performance: <500ms on CPU for typical thought
- Loading: Once at startup (not per request)
- Singleton pattern prevents multiple model loads
- CPU-based (no GPU required for personal scale)

**Prerequisites:** Story 1.2 (Backend initialized)

---

### Story 2.3: Implement FAISS Vector Index Service

**User Story:**
As a developer, I want to set up FAISS vector index service with Supabase Storage persistence, so that I can perform fast similarity searches across all thought embeddings.

**Acceptance Criteria:**

**Given** I need vector similarity search capabilities
**When** I implement the FAISS service
**Then** I add dependencies to `pyproject.toml`:

```toml
[tool.poetry.dependencies]
faiss-cpu = "^1.7.4"
supabase = "^2.0.0"
```

**And** I create `app/ml/vector_index.py`:

```python
import faiss
import numpy as np
from typing import List, Tuple
import pickle
import os

class VectorIndex:
    def __init__(self, dimension: int = 384):
        """Initialize FAISS index with IndexFlatIP (exact cosine similarity)"""
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        self.thought_ids: List[int] = []  # Maps index position to thought ID

    def add(self, thought_id: int, embedding: np.ndarray):
        """Add single embedding to index"""
        # Normalize for cosine similarity
        embedding_normalized = embedding / np.linalg.norm(embedding)
        self.index.add(np.array([embedding_normalized], dtype=np.float32))
        self.thought_ids.append(thought_id)

    def add_batch(self, thought_ids: List[int], embeddings: np.ndarray):
        """Add multiple embeddings to index (more efficient)"""
        # Normalize all embeddings
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings_normalized = embeddings / norms

        self.index.add(embeddings_normalized.astype(np.float32))
        self.thought_ids.extend(thought_ids)

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[int, float]]:
        """
        Search for most similar embeddings

        Returns:
            List of (thought_id, similarity_score) tuples, sorted by similarity desc
        """
        # Normalize query
        query_normalized = query_embedding / np.linalg.norm(query_embedding)
        query_normalized = np.array([query_normalized], dtype=np.float32)

        # Search
        similarities, indices = self.index.search(query_normalized, top_k)

        # Map to thought IDs
        results = []
        for idx, sim in zip(indices[0], similarities[0]):
            if idx < len(self.thought_ids):
                thought_id = self.thought_ids[idx]
                results.append((thought_id, float(sim)))

        return results

    def save(self, filepath: str):
        """Save index to disk"""
        faiss.write_index(self.index, filepath)
        # Save thought_ids mapping separately
        with open(filepath + ".ids", "wb") as f:
            pickle.dump(self.thought_ids, f)

    def load(self, filepath: str):
        """Load index from disk"""
        if os.path.exists(filepath):
            self.index = faiss.read_index(filepath)
            with open(filepath + ".ids", "rb") as f:
                self.thought_ids = pickle.load(f)
            return True
        return False

    @property
    def total_vectors(self) -> int:
        """Get total number of vectors in index"""
        return self.index.ntotal
```

**And** I create `app/services/vector_service.py`:

```python
from app.ml.vector_index import VectorIndex
from app.core.config import settings
from supabase import create_client
import numpy as np
from typing import List, Tuple
import tempfile
import os

class VectorService:
    def __init__(self):
        self.index = VectorIndex(dimension=384)
        self.supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
        self.bucket_name = "vector-indices"
        self.index_filename = "thoughts_index.faiss"

    async def initialize(self):
        """Load index from Supabase Storage on startup"""
        try:
            # Download from Supabase Storage
            with tempfile.TemporaryDirectory() as tmpdir:
                index_path = os.path.join(tmpdir, self.index_filename)

                # Download .faiss file
                response = self.supabase.storage.from_(self.bucket_name).download(self.index_filename)
                with open(index_path, "wb") as f:
                    f.write(response)

                # Download .ids file
                response_ids = self.supabase.storage.from_(self.bucket_name).download(self.index_filename + ".ids")
                with open(index_path + ".ids", "wb") as f:
                    f.write(response_ids)

                # Load into memory
                self.index.load(index_path)
                print(f"Loaded FAISS index with {self.index.total_vectors} vectors")
        except Exception as e:
            print(f"No existing index found, starting fresh: {e}")

    async def save_to_storage(self):
        """Save index to Supabase Storage"""
        with tempfile.TemporaryDirectory() as tmpdir:
            index_path = os.path.join(tmpdir, self.index_filename)

            # Save to temp file
            self.index.save(index_path)

            # Upload .faiss file
            with open(index_path, "rb") as f:
                self.supabase.storage.from_(self.bucket_name).upload(
                    self.index_filename,
                    f,
                    {"upsert": "true"}
                )

            # Upload .ids file
            with open(index_path + ".ids", "rb") as f:
                self.supabase.storage.from_(self.bucket_name).upload(
                    self.index_filename + ".ids",
                    f,
                    {"upsert": "true"}
                )

    def add_thought_embedding(self, thought_id: int, embedding: List[float]):
        """Add a thought embedding to the index"""
        embedding_array = np.array(embedding, dtype=np.float32)
        self.index.add(thought_id, embedding_array)

    def search_similar(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[int, float]]:
        """Search for similar thoughts"""
        query_array = np.array(query_embedding, dtype=np.float32)
        return self.index.search(query_array, top_k)

# Singleton instance
vector_service = VectorService()
```

**And** I update `app/main.py` to initialize FAISS on startup:

```python
@app.on_event("startup")
async def startup_event():
    # Load embedding model
    _ = embedding_service.generate_embedding("test")
    print("Embedding model loaded successfully")

    # Load FAISS index from Supabase Storage
    await vector_service.initialize()
```

**And** I create the Supabase Storage bucket "vector-indices" (public read, authenticated write)

**And** when the server starts, FAISS index loads successfully (or starts fresh if none exists)

**And** I can add embeddings to the index

**And** I can search for similar embeddings in <100ms

**And** the index persists to Supabase Storage after updates

**Technical Notes:**
- Follow Architecture "FAISS Persistence: Supabase Storage for index files"
- Index type: IndexFlatIP (exact cosine similarity, optimal for <100k vectors)
- Normalization: Required for cosine similarity with inner product
- Persistence: .faiss + .ids files stored in Supabase Storage bucket
- Performance: <100ms search for <100k vectors
- Singleton pattern: One index in memory
- Debouncing: Save to storage after N additions (implement in next story)

**Prerequisites:** Story 2.2 (Embedding service ready)

---

### Story 2.4: Create Thoughts CRUD API Endpoints

**User Story:**
As a developer, I want to implement RESTful API endpoints for thought CRUD operations, so that the iOS app can create, read, update, and delete thoughts with automatic embedding generation.

**Acceptance Criteria:**

**Given** the iOS app needs to manage thoughts via API
**When** I implement the thoughts endpoints
**Then** I create `app/api/v1/endpoints/thoughts.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.core.database import get_db
from app.schemas.thought import ThoughtCreate, ThoughtResponse
from app.models.thought import Thought
from app.services.embedding_service import embedding_service
from app.services.vector_service import vector_service
from typing import List

router = APIRouter()

@router.post("", response_model=ThoughtResponse, status_code=201)
async def create_thought(
    thought: ThoughtCreate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new thought with automatic embedding generation"""

    # Create thought in database
    db_thought = Thought(
        user_id=user.id,
        thought_text=thought.thought_text
    )
    db.add(db_thought)
    db.commit()
    db.refresh(db_thought)

    # Generate embedding (async in background ideally, but sync for MVP)
    embedding = embedding_service.generate_embedding(thought.thought_text)

    # Add to FAISS index
    vector_service.add_thought_embedding(db_thought.id, embedding)

    # Save index every 10 thoughts (debounced)
    if vector_service.index.total_vectors % 10 == 0:
        await vector_service.save_to_storage()

    return db_thought

@router.get("", response_model=List[ThoughtResponse])
async def list_thoughts(
    skip: int = 0,
    limit: int = 100,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's thoughts (paginated, sorted by created_at desc)"""
    thoughts = db.query(Thought).filter(
        Thought.user_id == user.id
    ).order_by(
        Thought.created_at.desc()
    ).offset(skip).limit(limit).all()

    return thoughts

@router.get("/{thought_id}", response_model=ThoughtResponse)
async def get_thought(
    thought_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a single thought by ID"""
    thought = db.query(Thought).filter(
        Thought.id == thought_id,
        Thought.user_id == user.id
    ).first()

    if not thought:
        raise HTTPException(status_code=404, detail="Thought not found")

    return thought

@router.delete("/{thought_id}", status_code=204)
async def delete_thought(
    thought_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a thought"""
    thought = db.query(Thought).filter(
        Thought.id == thought_id,
        Thought.user_id == user.id
    ).first()

    if not thought:
        raise HTTPException(status_code=404, detail="Thought not found")

    db.delete(thought)
    db.commit()

    # Note: FAISS index not updated (rebuild needed, acceptable for MVP)
    return None
```

**And** I register the router in `app/api/v1/api.py`:

```python
from fastapi import APIRouter
from app.api.v1.endpoints import thoughts

api_router = APIRouter()
api_router.include_router(thoughts.router, prefix="/thoughts", tags=["thoughts"])
```

**And** I update `app/main.py` to include the API router:

```python
from app.api.v1.api import api_router

app.include_router(api_router, prefix="/api/v1")
```

**And** I can test the endpoints:

**POST /api/v1/thoughts**
- Request: `{"thoughtText": "I want to get jacked"}`
- Response: 201 with full thought object (camelCase JSON)
- Embedding generated automatically
- Added to FAISS index

**GET /api/v1/thoughts**
- Response: 200 with array of thoughts (sorted newest first)
- Pagination via `skip` and `limit` query params

**GET /api/v1/thoughts/{id}**
- Response: 200 with single thought, or 404 if not found/not owned by user

**DELETE /api/v1/thoughts/{id}**
- Response: 204 no content on success, or 404 if not found

**And** all endpoints require authentication (401 if no JWT)

**And** users can only access their own thoughts (user_id filter)

**And** response JSON uses camelCase (thoughtText, userId, createdAt)

**Technical Notes:**
- Follow Architecture "API Endpoints Summary" and "API Naming Conventions"
- Endpoint pattern: POST /api/v1/thoughts (no trailing slash)
- JSON format: camelCase via Pydantic aliases
- Authentication: get_current_user dependency on all routes
- Embedding generation: Synchronous for MVP (acceptable latency)
- FAISS persistence: Debounced (every 10 thoughts)
- Pagination: Standard skip/limit pattern
- Soft deletion not needed (hard delete acceptable for MVP)

**Prerequisites:** Story 2.1 (Models), Story 2.2 (Embeddings), Story 2.3 (FAISS)

---

### Story 2.5: Create iOS APIService and Thought Model

**User Story:**
As a developer, I want to create an iOS API service and Thought model, so that the app can communicate with the backend API using type-safe Swift code.

**Acceptance Criteria:**

**Given** the iOS app needs to call backend APIs
**When** I implement APIService and models
**Then** I create `Models/Thought.swift`:

```swift
import Foundation

struct Thought: Codable, Identifiable {
    let id: Int
    let userId: String
    let thoughtText: String
    let tags: [String]
    let reflection: String?
    let noveltyScore: Double?
    let abodeId: Int?
    let createdAt: Date
    let updatedAt: Date
}

struct ThoughtCreate: Codable {
    let thoughtText: String
}
```

**And** I create `Services/APIService.swift`:

```swift
import Foundation
import Supabase

enum APIError: LocalizedError {
    case unauthorized
    case networkError
    case decodingError
    case serverError(String)

    var errorDescription: String? {
        switch self {
        case .unauthorized: return "Please log in again"
        case .networkError: return "Connection issue, please try again"
        case .decodingError: return "Data format error"
        case .serverError(let message): return message
        }
    }
}

class APIService {
    static let shared = APIService()

    private let baseURL = "http://localhost:8000/api/v1"  // TODO: Use Config.plist

    private var session: Session? {
        // Get current session from AppState (injected or accessed)
        // For now, assume supabase.auth.session
        return try? await supabase.auth.session
    }

    // MARK: - Thoughts API

    func createThought(text: String) async throws -> Thought {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/thoughts")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body = ThoughtCreate(thoughtText: text)
        request.httpBody = try JSONEncoder().encode(body)

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 201:
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .iso8601
            return try decoder.decode(Thought.self, from: data)
        case 401:
            throw APIError.unauthorized
        default:
            throw APIError.serverError("Failed to create thought")
        }
    }

    func listThoughts(skip: Int = 0, limit: Int = 100) async throws -> [Thought] {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/thoughts?skip=\(skip)&limit=\(limit)")!
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
            return try decoder.decode([Thought].self, from: data)
        case 401:
            throw APIError.unauthorized
        default:
            throw APIError.serverError("Failed to list thoughts")
        }
    }

    func deleteThought(id: Int) async throws {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/thoughts/\(id)")!
        var request = URLRequest(url: url)
        request.httpMethod = "DELETE"
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")

        let (_, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 204:
            return
        case 401:
            throw APIError.unauthorized
        case 404:
            throw APIError.serverError("Thought not found")
        default:
            throw APIError.serverError("Failed to delete thought")
        }
    }
}
```

**And** the Swift models use native camelCase (no CodingKeys needed)

**And** JSON decoding works automatically with backend camelCase responses

**And** ISO 8601 date decoding strategy handles timestamps correctly

**And** all API calls include JWT token in Authorization header

**And** error handling follows Architecture patterns:
- 401 → unauthorized (prompt re-login)
- Network errors → user-friendly message
- Other errors → generic server error

**Technical Notes:**
- Follow Architecture "API Communication: REST + SSE"
- No custom CodingKeys (backend uses Pydantic aliases for camelCase)
- URLSession with async/await (native Swift concurrency)
- ISO 8601 date format (UTC timestamps from backend)
- JWT token from Supabase session
- Error enum with LocalizedError for user-friendly messages

**Prerequisites:** Story 2.4 (Backend API ready), Epic 1 Story 1.5 (AuthService)

---

### Story 2.6: Build Text Capture UI with ViewModel

**User Story:**
As a user, I want to type a thought and save it, so that I can capture my ideas in text form.

**Acceptance Criteria:**

**Given** I am on the Capture tab
**When** I type a thought
**Then** I see a multiline text editor with placeholder "What's on your mind?"

**And** I can type multiple lines of text

**And** I see a character count below the text field (e.g., "125 characters")

**And** I see a "Save" button

**And** when I tap "Save" with valid text
**Then** the app calls `APIService.createThought(text:)`
**And** the thought is saved to the backend
**And** an embedding is generated automatically
**And** the thought is added to FAISS index
**And** I see a success message or confirmation
**And** the text field is cleared
**And** I'm ready to capture another thought

**And** while saving, I see a loading indicator
**And** the Save button is disabled

**And** if the save fails (network error, server error)
**Then** I see an error message below the text field
**And** my text is preserved (not cleared)
**And** I can retry saving

**And** the Save button is disabled when:
- Text is empty
- Text exceeds 10,000 characters
- Save is in progress

**Implementation:**

Create `ViewModels/CaptureViewModel.swift`:

```swift
import Foundation
import Observation

@Observable
class CaptureViewModel {
    var thoughtText: String = ""
    var isSaving: Bool = false
    var error: String?
    var successMessage: String?

    var characterCount: Int {
        thoughtText.count
    }

    var canSave: Bool {
        !thoughtText.isEmpty && thoughtText.count <= 10000 && !isSaving
    }

    func saveThought() async {
        guard canSave else { return }

        isSaving = true
        error = nil
        successMessage = nil

        do {
            _ = try await APIService.shared.createThought(text: thoughtText)

            // Success
            successMessage = "Thought saved!"
            thoughtText = ""

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
                TextEditor(text: $viewModel.thoughtText)
                    .frame(minHeight: 200)
                    .padding(8)
                    .background(Color(.systemGray6))
                    .cornerRadius(8)
                    .overlay(
                        Group {
                            if viewModel.thoughtText.isEmpty {
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
                        await viewModel.saveThought()
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

**And** when I type text, the character count updates in real-time

**And** when I tap Save, the thought is persisted to the backend

**And** I can save multiple thoughts in succession

**Technical Notes:**
- Follow Architecture "iOS State Management: ViewModels + Shared AppState"
- @Observable ViewModel (iOS 17+)
- TextEditor for multiline input
- Disabled state management via computed property
- Loading state: Boolean flag + ProgressView
- Error handling: Display error message, preserve text
- Success feedback: Temporary message, auto-clear after 2s

**Prerequisites:** Story 2.5 (APIService, Thought model)

---

### Story 2.7: Implement Voice Capture with iOS Speech Recognition

**User Story:**
As a user, I want to capture thoughts using my voice, so that I can quickly save ideas without typing.

**Acceptance Criteria:**

**Given** I am on the Capture tab
**When** I tap the microphone button
**Then** iOS prompts me for microphone permission (first time only)

**And** when I grant permission, speech recognition starts

**And** I see a visual indicator that recording is active (pulsing red circle)

**And** as I speak, my words appear in real-time in the text field

**And** when I tap the microphone button again, recording stops

**And** my transcribed text remains in the text field

**And** I can edit the transcribed text before saving

**And** I can tap "Save" to save the thought (same flow as text input)

**And** if I deny microphone permission
**Then** I see an alert: "Microphone access is required for voice capture"
**And** I can open Settings to grant permission

**And** if speech recognition fails
**Then** I see an error: "Speech recognition unavailable, please try again"
**And** I can retry or type manually

**Implementation:**

Create `Services/SpeechService.swift`:

```swift
import Foundation
import Speech
import AVFoundation

class SpeechService: NSObject, ObservableObject {
    static let shared = SpeechService()

    private let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    private let audioEngine = AVAudioEngine()

    @Published var isRecording = false
    @Published var transcribedText = ""

    func requestAuthorization() async -> Bool {
        await withCheckedContinuation { continuation in
            SFSpeechRecognizer.requestAuthorization { status in
                continuation.resume(returning: status == .authorized)
            }
        }
    }

    func startRecording(onTranscription: @escaping (String) -> Void) throws {
        // Cancel previous task
        recognitionTask?.cancel()
        recognitionTask = nil

        // Audio session
        let audioSession = AVAudioSession.sharedInstance()
        try audioSession.setCategory(.record, mode: .measurement, options: .duckOthers)
        try audioSession.setActive(true, options: .notifyOthersOnDeactivation)

        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        guard let recognitionRequest = recognitionRequest else {
            throw SpeechError.recognitionRequestFailed
        }

        recognitionRequest.shouldReportPartialResults = true

        let inputNode = audioEngine.inputNode

        recognitionTask = speechRecognizer?.recognitionTask(with: recognitionRequest) { result, error in
            if let result = result {
                let transcription = result.bestTranscription.formattedString
                onTranscription(transcription)
            }

            if error != nil || result?.isFinal == true {
                self.stopRecording()
            }
        }

        let recordingFormat = inputNode.outputFormat(forBus: 0)
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { buffer, _ in
            recognitionRequest.append(buffer)
        }

        audioEngine.prepare()
        try audioEngine.start()

        isRecording = true
    }

    func stopRecording() {
        audioEngine.stop()
        recognitionRequest?.endAudio()
        audioEngine.inputNode.removeTap(onBus: 0)

        recognitionRequest = nil
        recognitionTask = nil
        isRecording = false
    }
}

enum SpeechError: LocalizedError {
    case recognitionRequestFailed
    case unauthorized

    var errorDescription: String? {
        switch self {
        case .recognitionRequestFailed: return "Speech recognition unavailable, please try again"
        case .unauthorized: return "Microphone access is required for voice capture"
        }
    }
}
```

Update `ViewModels/CaptureViewModel.swift`:

```swift
@Observable
class CaptureViewModel {
    // ... existing properties ...
    var isRecording: Bool = false
    var hasMicrophonePermission: Bool = false

    func requestMicrophonePermission() async {
        hasMicrophonePermission = await SpeechService.shared.requestAuthorization()
    }

    func toggleRecording() {
        if isRecording {
            SpeechService.shared.stopRecording()
            isRecording = false
        } else {
            do {
                try SpeechService.shared.startRecording { [weak self] transcription in
                    DispatchQueue.main.async {
                        self?.thoughtText = transcription
                    }
                }
                isRecording = true
            } catch {
                self.error = error.localizedDescription
            }
        }
    }
}
```

Update `Views/Capture/CaptureView.swift`:

```swift
struct CaptureView: View {
    @State private var viewModel = CaptureViewModel()
    @State private var showPermissionAlert = false

    var body: some View {
        NavigationStack {
            VStack(spacing: 16) {
                // ... existing TextEditor ...

                // Microphone button
                Button(action: {
                    if viewModel.hasMicrophonePermission {
                        viewModel.toggleRecording()
                    } else {
                        Task {
                            await viewModel.requestMicrophonePermission()
                            if !viewModel.hasMicrophonePermission {
                                showPermissionAlert = true
                            }
                        }
                    }
                }) {
                    Image(systemName: viewModel.isRecording ? "mic.fill" : "mic")
                        .font(.system(size: 24))
                        .foregroundColor(viewModel.isRecording ? .red : .blue)
                        .padding()
                        .background(Circle().fill(Color(.systemGray6)))
                }

                // ... rest of UI ...
            }
            .padding()
            .navigationTitle("Capture")
            .alert("Microphone Permission Required", isPresented: $showPermissionAlert) {
                Button("Open Settings") {
                    if let url = URL(string: UIApplication.openSettingsURLString) {
                        UIApplication.shared.open(url)
                    }
                }
                Button("Cancel", role: .cancel) { }
            } message: {
                Text("Microphone access is required for voice capture. Please enable it in Settings.")
            }
        }
    }
}
```

**And** I need to add to `Info.plist`:
```xml
<key>NSMicrophoneUsageDescription</key>
<string>Pookie needs microphone access to capture your thoughts via voice</string>
<key>NSSpeechRecognitionUsageDescription</key>
<string>Pookie needs speech recognition to transcribe your voice thoughts</string>
```

**And** when I speak "I want to get jacked", the text appears in the text field

**And** I can edit the transcription before saving

**And** the microphone icon changes to red and filled when recording

**Technical Notes:**
- iOS native Speech framework (free, on-device for short recordings)
- Real-time transcription with partial results
- Permission handling via SFSpeechRecognizer authorization
- Audio session management for recording
- Visual feedback: mic icon color change (blue → red)
- Error handling: Permission denied → alert with Settings link
- Text remains editable after transcription

**Prerequisites:** Story 2.6 (Text capture UI complete)

---

## Epic 2 Summary

**Stories Created:** 7 stories
**FR Coverage:**
- FR2 (Thought Capture - Text Input) ✅
- FR3 (Thought Capture - Voice Input) ✅

**Technical Capabilities Established:**
- ✅ SQLAlchemy Thought model with Pydantic schemas (cross-platform naming)
- ✅ sentence-transformers embedding service (384-dim vectors, <500ms)
- ✅ FAISS vector index with Supabase Storage persistence
- ✅ Thoughts CRUD API endpoints with automatic embedding generation
- ✅ iOS APIService for backend communication
- ✅ iOS Thought model (native camelCase, no custom CodingKeys)
- ✅ Text capture UI with ViewModel (multiline editor, character count)
- ✅ Voice capture with iOS Speech framework (real-time transcription)

**Architecture Sections Implemented:**
- Cross-Platform Naming (Pydantic Field aliases)
- ML Pipeline (sentence-transformers + FAISS)
- API Endpoints (REST with camelCase JSON)
- iOS MVVM (ViewModels with @Observable)
- Error Handling (graceful failures, user-friendly messages)

**Ready for Epic 3:** AI-Powered Thought Separation (Call Agents Mode)

---

## Epic 3: AI-Powered Thought Separation (Call Agents Mode)

**Epic Goal:** Enable users to paste messy brain dumps and have AI automatically identify and separate distinct thoughts with semantic boundary detection.

**FR Coverage:** FR4 (Call Agents Mode - Thought Separation)

**User Value Statement:** After this epic, users can paste rambling paragraphs with multiple mixed thoughts, and AI will intelligently separate them into individual thoughts for storage and organization.

---

### Story 3.1: Implement LLM Service with OpenRouter Integration

**User Story:**
As a developer, I want to integrate OpenRouter for LLM calls with retry logic and graceful failure handling, so that the backend can use free LLM models for thought separation.

**Acceptance Criteria:**

**Given** I need LLM capabilities for AI operations
**When** I implement the LLM service
**Then** I add dependencies to `pyproject.toml`:

```toml
[tool.poetry.dependencies]
openai = "^1.0.0"  # OpenRouter uses OpenAI-compatible API
httpx = "^0.25.0"  # For async HTTP requests
```

**And** I update `app/core/config.py` to add LLM settings:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    LLM_MODEL: str = "mistralai/mistral-7b-instruct:free"  # Free tier model

    class Config:
        env_file = ".env"

settings = Settings()
```

**And** I update `.env` with:
```
OPENROUTER_API_KEY=sk-or-v1-xxx
```

**And** I create `app/services/llm_service.py`:

```python
from openai import AsyncOpenAI
from app.core.config import settings
import asyncio
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=settings.OPENROUTER_BASE_URL,
            api_key=settings.OPENROUTER_API_KEY
        )
        self.model = settings.LLM_MODEL
        self.max_retries = 3
        self.retry_delays = [0.1, 0.5, 2.0]  # Exponential backoff (100ms, 500ms, 2s)

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Optional[str]:
        """
        Generate LLM response with retry logic and graceful failure

        Returns:
            Generated text, or None if all retries failed
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        for attempt in range(self.max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                return response.choices[0].message.content

            except Exception as e:
                logger.warning(f"LLM API attempt {attempt + 1} failed: {e}")

                if attempt < self.max_retries - 1:
                    # Wait before retry (exponential backoff)
                    await asyncio.sleep(self.retry_delays[attempt])
                else:
                    # All retries exhausted
                    logger.error(f"LLM API failed after {self.max_retries} attempts")
                    return None

    async def separate_thoughts(self, text: str) -> Optional[list[str]]:
        """
        Separate a rambling paragraph into distinct thoughts

        Returns:
            List of separated thought texts, or None if LLM fails
        """
        system_prompt = """You are an expert at identifying semantic boundaries in text.
Your task is to separate rambling paragraphs into distinct, independent thoughts.

Rules:
- Each thought should be a complete, self-contained idea
- Preserve the original wording exactly (don't rephrase)
- Return ONLY the separated thoughts, one per line
- If the text contains only one thought, return it as-is
- Don't add commentary or explanations"""

        user_prompt = f"""Separate this text into distinct thoughts:

{text}

Return only the separated thoughts, one per line."""

        response = await self.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3,  # Lower temperature for more consistent separation
            max_tokens=2000
        )

        if response is None:
            return None

        # Split response by newlines, filter empty lines
        thoughts = [line.strip() for line in response.split('\n') if line.strip()]

        # Validate: at least one thought returned
        if not thoughts:
            return None

        return thoughts

# Singleton instance
llm_service = LLMService()
```

**And** I can test the LLM service:

```python
# Test basic generation
response = await llm_service.generate("Say hello")
assert response is not None
assert "hello" in response.lower()

# Test thought separation
text = "I want to get jacked and also learn piano and maybe travel to Japan"
thoughts = await llm_service.separate_thoughts(text)
assert thoughts is not None
assert len(thoughts) >= 2  # Should separate into multiple thoughts
```

**And** when OpenRouter API fails after retries, the function returns `None` (not an exception)

**And** retry delays use exponential backoff: 100ms, 500ms, 2s

**And** all errors are logged for debugging

**Technical Notes:**
- Follow Architecture "Error Handling: Graceful LLM failures"
- OpenRouter uses OpenAI-compatible API (use openai library)
- Free tier model: mistralai/mistral-7b-instruct:free
- Retry logic: 3 attempts with exponential backoff
- Graceful failure: Return None (not exception) after retries
- Low temperature (0.3) for thought separation (more consistent)
- Logging: Warning on retry, error on final failure

**Prerequisites:** Story 1.2 (Backend initialized)

---

### Story 3.2: Create Thought Separation API Endpoint

**User Story:**
As a developer, I want to implement the `/api/v1/ml/separate-thoughts` endpoint, so that the iOS app can send rambling text and receive separated thoughts with embeddings.

**Acceptance Criteria:**

**Given** the iOS app needs thought separation capabilities
**When** I implement the separation endpoint
**Then** I create `app/schemas/ml.py` for ML endpoint schemas:

```python
from pydantic import BaseModel, Field
from typing import List

class SeparateThoughtsRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)

class SeparatedThought(BaseModel):
    thought_text: str = Field(alias="thoughtText")

    class Config:
        populate_by_name = True

class SeparateThoughtsResponse(BaseModel):
    separated_thoughts: List[SeparatedThought] = Field(alias="separatedThoughts")
    original_text: str = Field(alias="originalText")
    count: int

    class Config:
        populate_by_name = True
```

**And** I create `app/api/v1/endpoints/ml.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.schemas.ml import SeparateThoughtsRequest, SeparateThoughtsResponse, SeparatedThought
from app.services.llm_service import llm_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/separate-thoughts", response_model=SeparateThoughtsResponse)
async def separate_thoughts(
    request: SeparateThoughtsRequest,
    user: dict = Depends(get_current_user)
):
    """
    Separate rambling text into distinct thoughts using LLM

    Returns:
        List of separated thoughts (not saved to database yet)
    """

    # Call LLM service
    separated = await llm_service.separate_thoughts(request.text)

    # Handle graceful LLM failure
    if separated is None:
        # Return original text as single thought (fallback)
        logger.warning(f"LLM separation failed for user {user.id}, returning original text")
        separated = [request.text]

    # Build response
    separated_thoughts = [
        SeparatedThought(thought_text=text)
        for text in separated
    ]

    return SeparateThoughtsResponse(
        separated_thoughts=separated_thoughts,
        original_text=request.text,
        count=len(separated_thoughts)
    )
```

**And** I register the router in `app/api/v1/api.py`:

```python
from app.api.v1.endpoints import thoughts, ml

api_router = APIRouter()
api_router.include_router(thoughts.router, prefix="/thoughts", tags=["thoughts"])
api_router.include_router(ml.router, prefix="/ml", tags=["ml"])
```

**And** I can test the endpoint:

**POST /api/v1/ml/separate-thoughts**
- Request:
```json
{
  "text": "I want to get jacked and also learn piano and maybe travel to Japan"
}
```
- Response: 200
```json
{
  "separatedThoughts": [
    {"thoughtText": "I want to get jacked"},
    {"thoughtText": "I also want to learn piano"},
    {"thoughtText": "Maybe travel to Japan"}
  ],
  "originalText": "I want to get jacked and also learn piano and maybe travel to Japan",
  "count": 3
}
```

**And** when LLM fails after retries
**Then** the response contains the original text as a single thought (graceful fallback):
```json
{
  "separatedThoughts": [
    {"thoughtText": "I want to get jacked and also learn piano and maybe travel to Japan"}
  ],
  "originalText": "I want to get jacked and also learn piano and maybe travel to Japan",
  "count": 1
}
```

**And** the endpoint requires authentication (401 if no JWT)

**And** response JSON uses camelCase (separatedThoughts, thoughtText, originalText)

**And** the endpoint does NOT save thoughts to database (iOS decides whether to save)

**Technical Notes:**
- Follow Architecture "ML Endpoints: /api/v1/ml/separate-thoughts"
- Graceful LLM failure: Return original text as fallback (not error)
- No database writes (preview only, user confirms before saving)
- Pydantic Field aliases for camelCase API
- Authentication required
- Logging: Warning on LLM failure

**Prerequisites:** Story 3.1 (LLM service), Story 2.1 (Schemas)

---

### Story 3.3: Create Batch Thought Creation Endpoint

**User Story:**
As a developer, I want to implement a batch endpoint for creating multiple thoughts at once, so that separated thoughts can be saved efficiently with embeddings.

**Acceptance Criteria:**

**Given** the iOS app needs to save multiple separated thoughts efficiently
**When** I implement the batch creation endpoint
**Then** I add to `app/schemas/thought.py`:

```python
class ThoughtBatchCreate(BaseModel):
    thoughts: List[ThoughtCreate]

class ThoughtBatchResponse(BaseModel):
    thoughts: List[ThoughtResponse]
    count: int
```

**And** I add to `app/api/v1/endpoints/thoughts.py`:

```python
@router.post("/batch", response_model=ThoughtBatchResponse, status_code=201)
async def create_thoughts_batch(
    request: ThoughtBatchCreate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create multiple thoughts at once with batch embedding generation

    More efficient than calling create_thought multiple times
    """

    if not request.thoughts:
        raise HTTPException(status_code=400, detail="No thoughts provided")

    if len(request.thoughts) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 thoughts per batch")

    # Create thoughts in database
    db_thoughts = []
    for thought_data in request.thoughts:
        db_thought = Thought(
            user_id=user.id,
            thought_text=thought_data.thought_text
        )
        db.add(db_thought)
        db_thoughts.append(db_thought)

    db.commit()

    # Refresh all to get IDs
    for db_thought in db_thoughts:
        db.refresh(db_thought)

    # Generate embeddings in batch (more efficient)
    texts = [thought.thought_text for thought in db_thoughts]
    embeddings = embedding_service.generate_embeddings_batch(texts)

    # Add all to FAISS index
    for db_thought, embedding in zip(db_thoughts, embeddings):
        vector_service.add_thought_embedding(db_thought.id, embedding)

    # Save FAISS index after batch
    await vector_service.save_to_storage()

    return ThoughtBatchResponse(
        thoughts=db_thoughts,
        count=len(db_thoughts)
    )
```

**And** I can test the endpoint:

**POST /api/v1/thoughts/batch**
- Request:
```json
{
  "thoughts": [
    {"thoughtText": "I want to get jacked"},
    {"thoughtText": "I also want to learn piano"},
    {"thoughtText": "Maybe travel to Japan"}
  ]
}
```
- Response: 201
```json
{
  "thoughts": [
    {"id": 1, "thoughtText": "I want to get jacked", ...},
    {"id": 2, "thoughtText": "I also want to learn piano", ...},
    {"id": 3, "thoughtText": "Maybe travel to Japan", ...}
  ],
  "count": 3
}
```

**And** embeddings are generated in batch (single call to sentence-transformers, more efficient)

**And** FAISS index is saved once after all thoughts added

**And** the endpoint validates:
- At least 1 thought required (400 if empty)
- Maximum 50 thoughts per batch (400 if exceeded)

**And** all thoughts belong to authenticated user

**Technical Notes:**
- Batch embedding generation more efficient than individual calls
- FAISS save happens once (not debounced)
- Validation: 1-50 thoughts per batch
- Transaction: All thoughts committed together
- Performance improvement over N individual API calls

**Prerequisites:** Story 2.4 (Thoughts endpoint), Story 2.2 (Embedding service)

---

### Story 3.4: Build iOS Separate & Save UI

**User Story:**
As a user, I want to see a "Separate & Save" button that shows me AI-separated thoughts before saving, so that I can review and confirm the separation.

**Acceptance Criteria:**

**Given** I am on the Capture tab
**When** I type or speak a rambling paragraph with multiple thoughts
**Then** I see two buttons:
1. "Save" - saves as-is (existing functionality)
2. "Separate & Save" - AI separates first

**And** when I tap "Separate & Save"
**Then** the app calls `POST /api/v1/ml/separate-thoughts`
**And** I see a loading indicator with text "Separating thoughts..."
**And** the button is disabled during processing

**And** when separation completes successfully
**Then** I navigate to a preview screen showing:
- Title: "Separated Thoughts"
- List of separated thoughts (numbered)
- Each thought is editable
- "Save All" button
- "Cancel" button

**And** I can edit any separated thought before saving

**And** when I tap "Save All"
**Then** the app calls `POST /api/v1/thoughts/batch` with all thoughts
**And** I see a success message "3 thoughts saved!"
**And** I navigate back to Capture screen
**And** the text field is cleared

**And** when I tap "Cancel"
**Then** I return to Capture screen
**And** my original text is preserved

**And** if separation fails (LLM error, network error)
**Then** I see the original text returned as a single thought
**And** I can still save it or go back

**And** if the LLM returns only 1 thought (no separation needed)
**Then** I see a message: "No separation needed - found 1 thought"
**And** I can save it or go back

**Implementation:**

Update `Services/APIService.swift`:

```swift
struct SeparatedThought: Codable {
    let thoughtText: String
}

struct SeparateThoughtsResponse: Codable {
    let separatedThoughts: [SeparatedThought]
    let originalText: String
    let count: Int
}

extension APIService {
    func separateThoughts(text: String) async throws -> SeparateThoughtsResponse {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/ml/separate-thoughts")!
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
            return try JSONDecoder().decode(SeparateThoughtsResponse.self, from: data)
        case 401:
            throw APIError.unauthorized
        default:
            throw APIError.serverError("Failed to separate thoughts")
        }
    }

    func createThoughtsBatch(thoughts: [String]) async throws -> [Thought] {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/thoughts/batch")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let thoughtsData = thoughts.map { ["thoughtText": $0] }
        let body = ["thoughts": thoughtsData]
        request.httpBody = try JSONSerialization.data(withJSONObject: body)

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 201:
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .iso8601
            let batchResponse = try decoder.decode(ThoughtBatchResponse.self, from: data)
            return batchResponse.thoughts
        case 401:
            throw APIError.unauthorized
        default:
            throw APIError.serverError("Failed to save thoughts")
        }
    }
}

struct ThoughtBatchResponse: Codable {
    let thoughts: [Thought]
    let count: Int
}
```

Update `ViewModels/CaptureViewModel.swift`:

```swift
@Observable
class CaptureViewModel {
    // ... existing properties ...
    var isSeparating: Bool = false
    var separatedThoughts: [String]?

    func separateAndSave() async {
        guard !thoughtText.isEmpty else { return }

        isSeparating = true
        error = nil

        do {
            let response = try await APIService.shared.separateThoughts(text: thoughtText)

            // Store separated thoughts for preview
            separatedThoughts = response.separatedThoughts.map { $0.thoughtText }

        } catch {
            self.error = error.localizedDescription
        }

        isSeparating = false
    }

    func saveBatch(thoughts: [String]) async {
        isSaving = true
        error = nil

        do {
            let saved = try await APIService.shared.createThoughtsBatch(thoughts: thoughts)

            // Success
            successMessage = "\(saved.count) thoughts saved!"
            thoughtText = ""
            separatedThoughts = nil

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

Create `Views/Capture/SeparatedThoughtsView.swift`:

```swift
import SwiftUI

struct SeparatedThoughtsView: View {
    @Binding var thoughts: [String]
    let onSave: ([String]) async -> Void
    let onCancel: () -> Void

    @State private var editableThoughts: [String]
    @State private var isSaving = false

    init(thoughts: Binding<[String]>, onSave: @escaping ([String]) async -> Void, onCancel: @escaping () -> Void) {
        self._thoughts = thoughts
        self.onSave = onSave
        self.onCancel = onCancel
        self._editableThoughts = State(initialValue: thoughts.wrappedValue)
    }

    var body: some View {
        NavigationStack {
            VStack {
                if editableThoughts.count == 1 {
                    Text("No separation needed - found 1 thought")
                        .foregroundColor(.secondary)
                        .padding()
                }

                List {
                    ForEach(editableThoughts.indices, id: \.self) { index in
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Thought \(index + 1)")
                                .font(.caption)
                                .foregroundColor(.secondary)

                            TextEditor(text: $editableThoughts[index])
                                .frame(minHeight: 60)
                                .padding(8)
                                .background(Color(.systemGray6))
                                .cornerRadius(8)
                        }
                        .padding(.vertical, 4)
                    }
                }

                HStack(spacing: 16) {
                    Button("Cancel") {
                        onCancel()
                    }
                    .buttonStyle(.bordered)

                    Button(action: {
                        Task {
                            isSaving = true
                            await onSave(editableThoughts)
                            isSaving = false
                        }
                    }) {
                        if isSaving {
                            ProgressView()
                                .frame(maxWidth: .infinity)
                        } else {
                            Text("Save All (\(editableThoughts.count))")
                                .frame(maxWidth: .infinity)
                        }
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(isSaving)
                }
                .padding()
            }
            .navigationTitle("Separated Thoughts")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}
```

Update `Views/Capture/CaptureView.swift`:

```swift
struct CaptureView: View {
    @State private var viewModel = CaptureViewModel()
    @State private var showPermissionAlert = false
    @State private var showSeparatedThoughts = false

    var body: some View {
        NavigationStack {
            VStack(spacing: 16) {
                // ... existing TextEditor and microphone button ...

                // Buttons row
                HStack(spacing: 12) {
                    // Save as-is button
                    Button(action: {
                        Task {
                            await viewModel.saveThought()
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
                    .buttonStyle(.bordered)
                    .disabled(!viewModel.canSave)

                    // Separate & Save button
                    Button(action: {
                        Task {
                            await viewModel.separateAndSave()
                            if viewModel.separatedThoughts != nil {
                                showSeparatedThoughts = true
                            }
                        }
                    }) {
                        if viewModel.isSeparating {
                            HStack {
                                ProgressView()
                                    .scaleEffect(0.8)
                                Text("Separating...")
                            }
                            .frame(maxWidth: .infinity)
                        } else {
                            Text("Separate & Save")
                                .frame(maxWidth: .infinity)
                        }
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(!viewModel.canSave || viewModel.isSeparating)
                }

                Spacer()
            }
            .padding()
            .navigationTitle("Capture")
            .sheet(isPresented: $showSeparatedThoughts) {
                if let thoughts = viewModel.separatedThoughts {
                    SeparatedThoughtsView(
                        thoughts: Binding(
                            get: { thoughts },
                            set: { viewModel.separatedThoughts = $0 }
                        ),
                        onSave: { editedThoughts in
                            await viewModel.saveBatch(thoughts: editedThoughts)
                            showSeparatedThoughts = false
                        },
                        onCancel: {
                            showSeparatedThoughts = false
                        }
                    )
                }
            }
        }
    }
}
```

**And** when I tap "Separate & Save", I see "Separating thoughts..." loading state

**And** separated thoughts appear in a modal sheet with editable fields

**And** I can tap "Save All (3)" to save all thoughts at once

**And** I can tap "Cancel" to return without saving

**Technical Notes:**
- Two-step process: Separate (preview) → Confirm (save)
- Editable thoughts before saving (user can fix AI errors)
- Batch save for efficiency
- Sheet presentation for modal preview
- Loading states for both separation and saving

**Prerequisites:** Story 3.2 (Separation endpoint), Story 3.3 (Batch endpoint), Story 2.6 (Capture UI)

---

## Epic 3 Summary

**Stories Created:** 4 stories
**FR Coverage:** FR4 (Call Agents Mode - Thought Separation) ✅

**Technical Capabilities Established:**
- ✅ LLM service with OpenRouter integration (mistralai/mistral-7b-instruct:free)
- ✅ Retry logic with exponential backoff (100ms, 500ms, 2s)
- ✅ Graceful LLM failure handling (fallback to original text)
- ✅ Thought separation API endpoint (/api/v1/ml/separate-thoughts)
- ✅ Batch thought creation endpoint (/api/v1/thoughts/batch)
- ✅ iOS "Separate & Save" UI with preview and editing
- ✅ Efficient batch embedding generation and FAISS indexing

**Architecture Sections Implemented:**
- LLM Service Integration (OpenRouter free models)
- Error Handling (graceful failures, retry logic)
- ML Endpoints (thought separation)
- Batch Processing (efficient multi-thought creation)
- iOS Modal Workflows (sheet presentation)

**Key Features:**
- AI semantic boundary detection in rambling text
- User preview and editing before saving
- Graceful degradation (LLM fails → original text preserved)
- Efficient batch operations (embeddings + FAISS)

**Ready for Epic 4:** Semantic Organization (Abodes) - automatic clustering, LLM naming, ML modes

---

## Epic 4: Semantic Organization (Abodes)

**Epic Goal:** Enable users to see their thoughts automatically organized into meaningful thematic clusters ("abodes") without manual categorization, with AI-generated names and ML-powered metadata.

**FR Coverage:** FR5 (Semantic Clustering), FR6 (Abode Management), FR11-13 (ML Modes: Tag, Reflection, Novelty), FR14 (Knowledge Graph Structure)

**User Value Statement:** After this epic, users see their scattered thoughts automatically grouped into meaningful themes, each with a descriptive AI-generated name, allowing them to understand what they care about without manual organization.

---

### Story 4.1: Create Abode Model, Schemas, and Knowledge Graph Structure

**User Story:**
As a developer, I want to create the Abode SQLAlchemy model with knowledge graph metadata, so that I can store thematic clusters and track relationships between thoughts and abodes.

**Acceptance Criteria:**

**Given** I need to store abodes and graph relationships
**When** I create the models and schemas
**Then** I create `app/models/abode.py`:

```python
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base

class Abode(Base):
    __tablename__ = "abodes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to thoughts
    thoughts = relationship("Thought", back_populates="abode")
```

**And** I update `app/models/thought.py` to add relationship:

```python
from sqlalchemy.orm import relationship

class Thought(Base):
    # ... existing columns ...

    # Relationship to abode
    abode = relationship("Abode", back_populates="thoughts")
```

**And** I create `app/schemas/abode.py`:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AbodeBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None

class AbodeCreate(AbodeBase):
    pass

class AbodeResponse(AbodeBase):
    id: int
    user_id: str = Field(alias="userId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    thought_count: int = Field(alias="thoughtCount", default=0)

    class Config:
        populate_by_name = True
        from_attributes = True

class AbodeWithThoughts(AbodeResponse):
    thoughts: list['ThoughtResponse'] = []

    class Config:
        populate_by_name = True
        from_attributes = True
```

**And** for knowledge graph structure, I add a new migration to create relationships table:

```sql
-- New migration: add thought_relationships table for graph structure
CREATE TABLE thought_relationships (
    id SERIAL PRIMARY KEY,
    source_thought_id INTEGER NOT NULL REFERENCES thoughts(id) ON DELETE CASCADE,
    target_thought_id INTEGER NOT NULL REFERENCES thoughts(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL,  -- 'semantic_similarity', 'temporal_proximity', 'user_link'
    strength FLOAT NOT NULL,  -- 0.0 to 1.0
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(source_thought_id, target_thought_id, relationship_type)
);

CREATE INDEX idx_thought_relationships_source ON thought_relationships(source_thought_id);
CREATE INDEX idx_thought_relationships_target ON thought_relationships(target_thought_id);
CREATE INDEX idx_thought_relationships_type ON thought_relationships(relationship_type);
```

**And** I can query abodes with thought counts

**And** the knowledge graph structure supports future graph traversal queries

**Technical Notes:**
- Follow Architecture "Database Naming Conventions"
- Abodes table: name (max 255 chars), description (optional)
- Relationships: One-to-many (Abode → Thoughts)
- Knowledge graph: thought_relationships table for future graph RAG
- Relationship types: semantic_similarity (from clustering), temporal_proximity, user_link
- Strength: 0.0-1.0 (cosine similarity or other metric)

**Prerequisites:** Story 2.1 (Thought model), Epic 1 Story 1.3 (Database schema)

---

### Story 4.2: Implement K-means Clustering Algorithm

**User Story:**
As a developer, I want to implement K-means clustering on thought embeddings, so that I can automatically group related thoughts into abodes based on semantic similarity.

**Acceptance Criteria:**

**Given** I need to cluster thoughts into abodes
**When** I implement the clustering service
**Then** I add dependencies to `pyproject.toml`:

```toml
[tool.poetry.dependencies]
scikit-learn = "^1.3.0"
```

**And** I create `app/ml/clustering.py`:

```python
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
import numpy as np
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class ThoughtClusterer:
    def __init__(self, min_thoughts: int = 5, max_clusters: int = 10):
        """
        Initialize clusterer with constraints

        Args:
            min_thoughts: Minimum thoughts needed to perform clustering
            max_clusters: Maximum number of clusters to create
        """
        self.min_thoughts = min_thoughts
        self.max_clusters = max_clusters

    def cluster_kmeans(
        self,
        embeddings: np.ndarray,
        thought_ids: List[int],
        n_clusters: Optional[int] = None
    ) -> List[Tuple[int, int]]:
        """
        Cluster thoughts using K-means

        Args:
            embeddings: numpy array of shape (n_thoughts, 384)
            thought_ids: List of thought IDs corresponding to embeddings
            n_clusters: Number of clusters (auto-determined if None)

        Returns:
            List of (thought_id, cluster_id) tuples
        """
        n_thoughts = len(embeddings)

        if n_thoughts < self.min_thoughts:
            logger.info(f"Not enough thoughts for clustering: {n_thoughts} < {self.min_thoughts}")
            # Return all thoughts in cluster 0
            return [(tid, 0) for tid in thought_ids]

        # Auto-determine optimal number of clusters
        if n_clusters is None:
            n_clusters = self._find_optimal_k(embeddings)

        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings)

        # Build result
        result = [(thought_ids[i], int(labels[i])) for i in range(len(thought_ids))]

        logger.info(f"Clustered {n_thoughts} thoughts into {n_clusters} clusters")
        return result

    def _find_optimal_k(self, embeddings: np.ndarray) -> int:
        """
        Find optimal number of clusters using elbow method + silhouette score

        Returns:
            Optimal number of clusters (between 3 and max_clusters)
        """
        n_thoughts = len(embeddings)

        # Constraints
        min_k = 3
        max_k = min(self.max_clusters, n_thoughts // 2)  # At least 2 thoughts per cluster

        if max_k < min_k:
            return min_k

        # Try different k values and compute silhouette scores
        best_k = min_k
        best_score = -1

        for k in range(min_k, max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(embeddings)

            # Compute silhouette score (higher is better)
            score = silhouette_score(embeddings, labels)

            if score > best_score:
                best_score = score
                best_k = k

        logger.info(f"Optimal k={best_k} with silhouette score={best_score:.3f}")
        return best_k

    def cluster_dbscan(
        self,
        embeddings: np.ndarray,
        thought_ids: List[int],
        eps: float = 0.3,
        min_samples: int = 2
    ) -> List[Tuple[int, int]]:
        """
        Cluster thoughts using DBSCAN (density-based)

        Args:
            embeddings: numpy array of shape (n_thoughts, 384)
            thought_ids: List of thought IDs
            eps: Maximum distance between samples in same cluster
            min_samples: Minimum samples in neighborhood to form cluster

        Returns:
            List of (thought_id, cluster_id) tuples
            Note: cluster_id = -1 for noise points
        """
        n_thoughts = len(embeddings)

        if n_thoughts < self.min_thoughts:
            return [(tid, 0) for tid in thought_ids]

        # Perform DBSCAN clustering
        dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
        labels = dbscan.fit_predict(embeddings)

        # Reassign noise points (-1) to nearest cluster
        unique_labels = set(labels)
        if -1 in unique_labels:
            unique_labels.remove(-1)

        if len(unique_labels) == 0:
            # All noise, put everything in cluster 0
            labels = np.zeros(len(labels), dtype=int)

        # Build result
        result = [(thought_ids[i], int(labels[i])) for i in range(len(thought_ids))]

        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        logger.info(f"DBSCAN clustered {n_thoughts} thoughts into {n_clusters} clusters")
        return result
```

**And** I create `app/services/clustering_service.py`:

```python
from app.ml.clustering import ThoughtClusterer
from app.services.vector_service import vector_service
from app.services.embedding_service import embedding_service
from sqlalchemy.orm import Session
from app.models.thought import Thought
import numpy as np
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class ClusteringService:
    def __init__(self):
        self.clusterer = ThoughtClusterer(min_thoughts=5, max_clusters=10)

    async def cluster_user_thoughts(self, user_id: str, db: Session) -> Dict[int, List[int]]:
        """
        Cluster all thoughts for a user

        Returns:
            Dictionary mapping cluster_id to list of thought_ids
        """
        # Get all thoughts for user
        thoughts = db.query(Thought).filter(Thought.user_id == user_id).all()

        if len(thoughts) < 5:
            logger.info(f"User {user_id} has {len(thoughts)} thoughts, skipping clustering")
            return {}

        # Get embeddings from FAISS
        thought_ids = [t.id for t in thoughts]
        texts = [t.thought_text for t in thoughts]

        # Generate fresh embeddings (in case FAISS is out of sync)
        embeddings_list = embedding_service.generate_embeddings_batch(texts)
        embeddings = np.array(embeddings_list, dtype=np.float32)

        # Perform clustering
        clustered = self.clusterer.cluster_kmeans(embeddings, thought_ids)

        # Group by cluster_id
        clusters: Dict[int, List[int]] = {}
        for thought_id, cluster_id in clustered:
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(thought_id)

        logger.info(f"Created {len(clusters)} clusters for user {user_id}")
        return clusters

# Singleton instance
clustering_service = ClusteringService()
```

**And** I can test clustering:

```python
# Test with sample embeddings
embeddings = np.random.rand(20, 384).astype(np.float32)
thought_ids = list(range(1, 21))

clusterer = ThoughtClusterer()
result = clusterer.cluster_kmeans(embeddings, thought_ids)

assert len(result) == 20
assert all(isinstance(tid, int) and isinstance(cid, int) for tid, cid in result)
```

**And** clustering performs automatically when user has 5+ thoughts

**And** optimal k is determined using silhouette score

**And** clusters are balanced (at least 2 thoughts per cluster on average)

**Technical Notes:**
- Algorithm: K-means (faster, deterministic with random_state)
- Alternative: DBSCAN (density-based, handles noise) - implemented but K-means preferred for MVP
- Optimal k: Silhouette score analysis (3 to max_clusters)
- Minimum thoughts: 5 (below this, no clustering)
- Embeddings: Fresh generation from texts (ensures sync with database)
- Performance: O(n*k*i) where n=thoughts, k=clusters, i=iterations (~10)

**Prerequisites:** Story 2.2 (Embedding service), Story 2.3 (FAISS)

---

### Story 4.3: Implement LLM-Based Abode Naming

**User Story:**
As a developer, I want to use LLM to generate descriptive names for abodes based on thought content, so that users can understand what each cluster represents without reading all thoughts.

**Acceptance Criteria:**

**Given** I have a cluster of related thoughts
**When** I request an abode name
**Then** I add to `app/services/llm_service.py`:

```python
async def generate_abode_name(self, thought_texts: List[str]) -> Optional[str]:
    """
    Generate a descriptive name for an abode based on thought content

    Args:
        thought_texts: List of thought texts in the abode (sample of 5-10)

    Returns:
        Abode name (2-4 words), or None if LLM fails
    """
    # Sample thoughts if too many (use first 10 for performance)
    sample_texts = thought_texts[:10]

    system_prompt = """You are an expert at analyzing themes and creating descriptive labels.
Your task is to generate a short, descriptive name for a collection of related thoughts.

Rules:
- Name should be 2-4 words maximum
- Name should capture the central theme or topic
- Use title case (e.g., "Fitness Goals", "Creative Projects")
- Be specific, not generic (avoid "Various Thoughts", "Random Ideas")
- Return ONLY the name, no explanation or commentary"""

    thoughts_text = "\n".join(f"- {text}" for text in sample_texts)

    user_prompt = f"""Generate a descriptive name for this collection of thoughts:

{thoughts_text}

Return only the name (2-4 words, title case)."""

    response = await self.generate(
        prompt=user_prompt,
        system_prompt=system_prompt,
        temperature=0.5,  # Moderate creativity
        max_tokens=20  # Short response
    )

    if response is None:
        return None

    # Clean up response (remove quotes, extra whitespace)
    name = response.strip().strip('"').strip("'").strip()

    # Validate length (fallback to generic if too long)
    words = name.split()
    if len(words) > 4 or len(name) > 50:
        logger.warning(f"Generated name too long: {name}, using fallback")
        return "Untitled Abode"

    return name
```

**And** I can test abode naming:

```python
# Test with fitness thoughts
thoughts = [
    "I want to get jacked",
    "Need to hit the gym more consistently",
    "My goal is to bench 225 lbs"
]

name = await llm_service.generate_abode_name(thoughts)
assert name is not None
assert len(name.split()) <= 4
# Likely result: "Fitness Goals" or "Strength Training"
```

**And** when LLM fails, fallback name is "Untitled Abode"

**And** names are 2-4 words, title case

**And** names are specific to content (not generic)

**And** only first 10 thoughts used for naming (performance optimization)

**Technical Notes:**
- Temperature: 0.5 (moderate creativity for naming)
- Max tokens: 20 (short output)
- Validation: 2-4 words, max 50 characters
- Graceful failure: "Untitled Abode" fallback
- Sampling: First 10 thoughts (balance quality vs performance)
- Logging: Warning if name validation fails

**Prerequisites:** Story 3.1 (LLM service)

---

### Story 4.4: Create Abodes API Endpoints

**User Story:**
As a developer, I want to implement CRUD API endpoints for abodes, so that iOS can list, view, and manage thematic clusters.

**Acceptance Criteria:**

**Given** iOS needs to interact with abodes
**When** I implement abodes endpoints
**Then** I create `app/api/v1/endpoints/abodes.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.core.database import get_db
from app.schemas.abode import AbodeResponse, AbodeWithThoughts, AbodeCreate
from app.models.abode import Abode
from app.models.thought import Thought
from typing import List

router = APIRouter()

@router.get("", response_model=List[AbodeResponse])
async def list_abodes(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all abodes for authenticated user with thought counts"""
    abodes = db.query(Abode).filter(Abode.user_id == user.id).all()

    # Add thought counts
    result = []
    for abode in abodes:
        thought_count = db.query(Thought).filter(
            Thought.abode_id == abode.id
        ).count()

        abode_dict = {
            **abode.__dict__,
            "thought_count": thought_count
        }
        result.append(AbodeResponse(**abode_dict))

    return result

@router.get("/{abode_id}", response_model=AbodeWithThoughts)
async def get_abode(
    abode_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get single abode with all thoughts"""
    abode = db.query(Abode).filter(
        Abode.id == abode_id,
        Abode.user_id == user.id
    ).first()

    if not abode:
        raise HTTPException(status_code=404, detail="Abode not found")

    # Get thoughts in this abode
    thoughts = db.query(Thought).filter(
        Thought.abode_id == abode_id
    ).order_by(Thought.created_at.desc()).all()

    return AbodeWithThoughts(
        **abode.__dict__,
        thought_count=len(thoughts),
        thoughts=thoughts
    )

@router.post("/{abode_id}/thoughts/{thought_id}", status_code=204)
async def add_thought_to_abode(
    abode_id: int,
    thought_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Manually add a thought to an abode"""
    # Verify abode exists and belongs to user
    abode = db.query(Abode).filter(
        Abode.id == abode_id,
        Abode.user_id == user.id
    ).first()

    if not abode:
        raise HTTPException(status_code=404, detail="Abode not found")

    # Verify thought exists and belongs to user
    thought = db.query(Thought).filter(
        Thought.id == thought_id,
        Thought.user_id == user.id
    ).first()

    if not thought:
        raise HTTPException(status_code=404, detail="Thought not found")

    # Update thought's abode
    thought.abode_id = abode_id
    db.commit()

    return None

@router.delete("/{abode_id}/thoughts/{thought_id}", status_code=204)
async def remove_thought_from_abode(
    abode_id: int,
    thought_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a thought from an abode"""
    # Verify thought exists, belongs to user, and is in this abode
    thought = db.query(Thought).filter(
        Thought.id == thought_id,
        Thought.user_id == user.id,
        Thought.abode_id == abode_id
    ).first()

    if not thought:
        raise HTTPException(status_code=404, detail="Thought not found in this abode")

    # Remove from abode
    thought.abode_id = None
    db.commit()

    return None

@router.post("/trigger-clustering", status_code=202)
async def trigger_clustering(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Manually trigger clustering for user's thoughts
    (Normally runs automatically in background)
    """
    from app.services.clustering_service import clustering_service
    from app.services.llm_service import llm_service

    # Get clusters
    clusters = await clustering_service.cluster_user_thoughts(user.id, db)

    if not clusters:
        return {"message": "Not enough thoughts for clustering"}

    # Create/update abodes for each cluster
    abodes_created = 0
    for cluster_id, thought_ids in clusters.items():
        # Get thoughts in cluster
        thoughts = db.query(Thought).filter(
            Thought.id.in_(thought_ids)
        ).all()

        thought_texts = [t.thought_text for t in thoughts]

        # Generate abode name
        abode_name = await llm_service.generate_abode_name(thought_texts)
        if abode_name is None:
            abode_name = f"Untitled Abode {cluster_id + 1}"

        # Create abode
        abode = Abode(
            user_id=user.id,
            name=abode_name,
            description=f"Auto-generated cluster with {len(thought_ids)} thoughts"
        )
        db.add(abode)
        db.flush()  # Get abode.id

        # Assign thoughts to abode
        for thought in thoughts:
            thought.abode_id = abode.id

        abodes_created += 1

    db.commit()

    return {
        "message": f"Created {abodes_created} abodes",
        "abode_count": abodes_created
    }
```

**And** I register the router in `app/api/v1/api.py`:

```python
from app.api.v1.endpoints import thoughts, ml, abodes

api_router = APIRouter()
api_router.include_router(thoughts.router, prefix="/thoughts", tags=["thoughts"])
api_router.include_router(ml.router, prefix="/ml", tags=["ml"])
api_router.include_router(abodes.router, prefix="/abodes", tags=["abodes"])
```

**And** I can test the endpoints:

**GET /api/v1/abodes**
- Response: 200 with array of abodes (each with thoughtCount)

**GET /api/v1/abodes/{id}**
- Response: 200 with abode + array of thoughts, or 404 if not found

**POST /api/v1/abodes/{abode_id}/thoughts/{thought_id}**
- Response: 204 on success, 404 if abode or thought not found

**DELETE /api/v1/abodes/{abode_id}/thoughts/{thought_id}**
- Response: 204 on success, 404 if not found

**POST /api/v1/abodes/trigger-clustering**
- Response: 202 with message and abode_count
- Creates abodes with AI-generated names
- Assigns thoughts to abodes

**Technical Notes:**
- Follow Architecture "API Endpoints: Abodes"
- Clustering endpoint returns 202 Accepted (async operation feel)
- Thought counts calculated on-demand (acceptable for MVP)
- Manual add/remove for user corrections
- Authentication required on all endpoints

**Prerequisites:** Story 4.1 (Abode model), Story 4.2 (Clustering), Story 4.3 (Naming)

---

### Story 4.5: Implement ML Modes (Tag, Reflection, Novelty)

**User Story:**
As a developer, I want to implement Tag Mode, Reflection Mode, and Novelty Mode using LLM, so that thoughts can have AI-generated metadata for richer organization.

**Acceptance Criteria:**

**Given** I need ML-powered metadata for thoughts
**When** I implement the ML modes
**Then** I add to `app/services/llm_service.py`:

```python
async def generate_tags(self, thought_text: str) -> Optional[List[str]]:
    """
    Generate 2-5 relevant tags for a thought

    Returns:
        List of tags, or None if LLM fails
    """
    system_prompt = """You are an expert at extracting relevant tags from text.
Your task is to generate 2-5 concise tags that categorize the thought.

Rules:
- Return 2-5 tags maximum
- Each tag should be 1-2 words
- Tags should be lowercase
- Return tags as comma-separated list
- No hashtags, just words"""

    user_prompt = f"""Generate 2-5 relevant tags for this thought:

"{thought_text}"

Return only the tags as comma-separated list (e.g., fitness, goals, health)."""

    response = await self.generate(
        prompt=user_prompt,
        system_prompt=system_prompt,
        temperature=0.4,
        max_tokens=50
    )

    if response is None:
        return None

    # Parse comma-separated tags
    tags = [tag.strip().lower() for tag in response.split(',')]
    tags = [tag for tag in tags if tag and len(tag.split()) <= 2]

    # Limit to 5 tags
    return tags[:5]

async def generate_reflection(self, thought_text: str) -> Optional[str]:
    """
    Generate a reflection/insight about a thought

    Returns:
        Reflection text (1-2 sentences), or None if LLM fails
    """
    system_prompt = """You are a thoughtful AI that helps users gain insights about their thoughts.
Your task is to generate a brief reflection or insight.

Rules:
- 1-2 sentences maximum
- Provide a deeper perspective or connection
- Be encouraging and constructive
- Don't just restate the thought"""

    user_prompt = f"""Generate a brief reflection or insight about this thought:

"{thought_text}"

Return 1-2 sentences."""

    response = await self.generate(
        prompt=user_prompt,
        system_prompt=system_prompt,
        temperature=0.7,  # More creative for reflections
        max_tokens=100
    )

    if response is None:
        return None

    return response.strip()

async def score_novelty(self, thought_text: str, existing_thoughts: List[str]) -> Optional[float]:
    """
    Score how novel/important a thought is compared to existing thoughts

    Args:
        thought_text: The new thought to score
        existing_thoughts: Sample of recent thoughts (5-10) for comparison

    Returns:
        Novelty score 0.0-1.0, or None if LLM fails
    """
    # Sample existing thoughts (max 10 for performance)
    sample_existing = existing_thoughts[:10]

    system_prompt = """You are an expert at evaluating novelty and importance of ideas.
Your task is to score how novel and important a thought is compared to existing thoughts.

Score from 0.0 to 1.0:
- 0.0-0.3: Low novelty (very similar to existing thoughts, routine)
- 0.4-0.6: Medium novelty (somewhat new, moderately important)
- 0.7-1.0: High novelty (significantly new, very important)

Return ONLY the numeric score (e.g., 0.75)"""

    existing_text = "\n".join(f"- {text}" for text in sample_existing)

    user_prompt = f"""Score the novelty of this NEW thought:

"{thought_text}"

Compared to these EXISTING thoughts:
{existing_text}

Return only the numeric score (0.0-1.0)."""

    response = await self.generate(
        prompt=user_prompt,
        system_prompt=system_prompt,
        temperature=0.3,  # Low temperature for consistent scoring
        max_tokens=10
    )

    if response is None:
        return None

    # Parse numeric score
    try:
        score = float(response.strip())
        # Clamp to 0.0-1.0
        score = max(0.0, min(1.0, score))
        return score
    except ValueError:
        logger.warning(f"Failed to parse novelty score: {response}")
        return None
```

**And** I create `app/services/mode_service.py`:

```python
from app.services.llm_service import llm_service
from app.models.thought import Thought
from sqlalchemy.orm import Session
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class ModeService:
    async def enrich_thought(self, thought: Thought, db: Session) -> Thought:
        """
        Run all ML modes on a thought to enrich it with metadata

        Args:
            thought: Thought object to enrich
            db: Database session

        Returns:
            Enriched thought (tags, reflection, novelty_score populated)
        """
        # Tag Mode
        tags = await llm_service.generate_tags(thought.thought_text)
        if tags:
            thought.tags = tags
            logger.info(f"Generated {len(tags)} tags for thought {thought.id}")

        # Reflection Mode
        reflection = await llm_service.generate_reflection(thought.thought_text)
        if reflection:
            thought.reflection = reflection
            logger.info(f"Generated reflection for thought {thought.id}")

        # Novelty Mode (compare to recent thoughts)
        recent_thoughts = db.query(Thought).filter(
            Thought.user_id == thought.user_id,
            Thought.id != thought.id
        ).order_by(Thought.created_at.desc()).limit(10).all()

        if recent_thoughts:
            existing_texts = [t.thought_text for t in recent_thoughts]
            novelty = await llm_service.score_novelty(thought.thought_text, existing_texts)
            if novelty is not None:
                thought.novelty_score = novelty
                logger.info(f"Novelty score for thought {thought.id}: {novelty:.2f}")
        else:
            # First thought always has high novelty
            thought.novelty_score = 1.0

        db.commit()
        return thought

# Singleton instance
mode_service = ModeService()
```

**And** I can optionally enrich thoughts after creation (enable via config):

```python
# In app/api/v1/endpoints/thoughts.py create_thought endpoint:
# After creating thought and generating embedding:

# Optional: Enrich with ML modes (can be background job)
if settings.ENABLE_ML_MODES:
    from app.services.mode_service import mode_service
    await mode_service.enrich_thought(db_thought, db)
```

**And** I can test ML modes:

```python
# Test tag generation
tags = await llm_service.generate_tags("I want to get jacked and build muscle")
assert tags is not None
assert len(tags) <= 5
# Likely: ['fitness', 'muscle', 'goals']

# Test reflection
reflection = await llm_service.generate_reflection("I want to get jacked")
assert reflection is not None
assert len(reflection.split()) < 50  # 1-2 sentences

# Test novelty scoring
novelty = await llm_service.score_novelty(
    "I want to learn quantum physics",
    ["I want to get jacked", "Need to practice piano"]
)
assert novelty is not None
assert 0.0 <= novelty <= 1.0
# Likely high (0.7+) since it's different topic
```

**And** ML modes run sequentially (not in parallel for MVP)

**And** graceful failure: If any mode fails, others still execute

**And** modes are optional (can be disabled via config)

**Technical Notes:**
- Follow Architecture "Mode Orchestration: Simple sequential functions"
- Tag Mode: 2-5 lowercase tags, comma-separated
- Reflection Mode: 1-2 sentences, encouraging tone
- Novelty Mode: 0.0-1.0 score vs recent 10 thoughts
- Sequential execution (not framework-based)
- Optional enrichment (config flag ENABLE_ML_MODES)
- Graceful failures: Each mode independent

**Prerequisites:** Story 3.1 (LLM service)

---

### Story 4.6: Build iOS Abode List and Detail Views

**User Story:**
As a user, I want to see a list of my abodes with thought counts, and view all thoughts within an abode, so that I can explore my organized knowledge.

**Acceptance Criteria:**

**Given** I am on the Abodes tab
**When** I view my abodes
**Then** I see a list of abodes with:
- Abode name (AI-generated)
- Thought count (e.g., "12 thoughts")
- Last updated timestamp

**And** when I tap an abode
**Then** I navigate to the abode detail view showing:
- Abode name as title
- List of all thoughts in this abode (newest first)
- Each thought shows: text preview (first 100 chars), timestamp

**And** when I tap a thought in the abode
**Then** I see the full thought with:
- Complete text
- Tags (if available)
- Reflection (if available)
- Novelty score (if available)
- Created timestamp

**And** when I have no abodes yet
**Then** I see a message: "No abodes yet. Capture more thoughts to see them organized!"
**And** I see a "Trigger Clustering" button (for testing)

**And** when I tap "Trigger Clustering"
**Then** the app calls `POST /api/v1/abodes/trigger-clustering`
**And** I see a loading indicator
**And** abodes appear after clustering completes

**Implementation:**

Update `Services/APIService.swift`:

```swift
struct Abode: Codable, Identifiable {
    let id: Int
    let userId: String
    let name: String
    let description: String?
    let thoughtCount: Int
    let createdAt: Date
    let updatedAt: Date
}

struct AbodeWithThoughts: Codable {
    let id: Int
    let userId: String
    let name: String
    let description: String?
    let thoughtCount: Int
    let thoughts: [Thought]
    let createdAt: Date
    let updatedAt: Date
}

extension APIService {
    func listAbodes() async throws -> [Abode] {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/abodes")!
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
            return try decoder.decode([Abode].self, from: data)
        case 401:
            throw APIError.unauthorized
        default:
            throw APIError.serverError("Failed to list abodes")
        }
    }

    func getAbode(id: Int) async throws -> AbodeWithThoughts {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/abodes/\(id)")!
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
            return try decoder.decode(AbodeWithThoughts.self, from: data)
        case 401:
            throw APIError.unauthorized
        case 404:
            throw APIError.serverError("Abode not found")
        default:
            throw APIError.serverError("Failed to get abode")
        }
    }

    func triggerClustering() async throws {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/abodes/trigger-clustering")!
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

Create `ViewModels/AbodeViewModel.swift`:

```swift
import Foundation
import Observation

@Observable
class AbodeViewModel {
    var abodes: [Abode] = []
    var isLoading: Bool = false
    var isClustering: Bool = false
    var error: String?

    func loadAbodes() async {
        isLoading = true
        error = nil

        do {
            abodes = try await APIService.shared.listAbodes()
        } catch {
            self.error = error.localizedDescription
        }

        isLoading = false
    }

    func triggerClustering() async {
        isClustering = true
        error = nil

        do {
            try await APIService.shared.triggerClustering()
            // Reload abodes after clustering
            await loadAbodes()
        } catch {
            self.error = error.localizedDescription
        }

        isClustering = false
    }
}
```

Update `Views/Abodes/AbodeListView.swift`:

```swift
import SwiftUI

struct AbodeListView: View {
    @State private var viewModel = AbodeViewModel()

    var body: some View {
        NavigationStack {
            VStack {
                if viewModel.isLoading {
                    ProgressView()
                } else if viewModel.abodes.isEmpty {
                    VStack(spacing: 16) {
                        Text("No abodes yet")
                            .font(.title3)
                            .foregroundColor(.secondary)

                        Text("Capture more thoughts to see them organized!")
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .multilineTextAlignment(.center)

                        Button("Trigger Clustering") {
                            Task {
                                await viewModel.triggerClustering()
                            }
                        }
                        .buttonStyle(.borderedProminent)
                        .disabled(viewModel.isClustering)

                        if viewModel.isClustering {
                            ProgressView("Clustering...")
                        }
                    }
                    .padding()
                } else {
                    List(viewModel.abodes) { abode in
                        NavigationLink(destination: AbodeDetailView(abodeId: abode.id)) {
                            VStack(alignment: .leading, spacing: 4) {
                                Text(abode.name)
                                    .font(.headline)

                                Text("\(abode.thoughtCount) thoughts")
                                    .font(.caption)
                                    .foregroundColor(.secondary)

                                Text(abode.updatedAt, style: .relative)
                                    .font(.caption2)
                                    .foregroundColor(.secondary)
                            }
                            .padding(.vertical, 4)
                        }
                    }
                }

                if let error = viewModel.error {
                    Text(error)
                        .foregroundColor(.red)
                        .font(.caption)
                        .padding()
                }
            }
            .navigationTitle("Abodes")
            .task {
                await viewModel.loadAbodes()
            }
            .refreshable {
                await viewModel.loadAbodes()
            }
        }
    }
}
```

Create `Views/Abodes/AbodeDetailView.swift`:

```swift
import SwiftUI

struct AbodeDetailView: View {
    let abodeId: Int

    @State private var abode: AbodeWithThoughts?
    @State private var isLoading: Bool = false
    @State private var error: String?

    var body: some View {
        VStack {
            if isLoading {
                ProgressView()
            } else if let abode = abode {
                List(abode.thoughts) { thought in
                    NavigationLink(destination: ThoughtDetailView(thought: thought)) {
                        VStack(alignment: .leading, spacing: 4) {
                            Text(thought.thoughtText.prefix(100) + (thought.thoughtText.count > 100 ? "..." : ""))
                                .font(.body)

                            Text(thought.createdAt, style: .relative)
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                        .padding(.vertical, 4)
                    }
                }
            }

            if let error = error {
                Text(error)
                    .foregroundColor(.red)
                    .font(.caption)
                    .padding()
            }
        }
        .navigationTitle(abode?.name ?? "Abode")
        .navigationBarTitleDisplayMode(.inline)
        .task {
            await loadAbode()
        }
    }

    func loadAbode() async {
        isLoading = true
        error = nil

        do {
            abode = try await APIService.shared.getAbode(id: abodeId)
        } catch {
            self.error = error.localizedDescription
        }

        isLoading = false
    }
}
```

Create `Views/Thoughts/ThoughtDetailView.swift`:

```swift
import SwiftUI

struct ThoughtDetailView: View {
    let thought: Thought

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                // Thought text
                Text(thought.thoughtText)
                    .font(.body)

                Divider()

                // Tags
                if !thought.tags.isEmpty {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Tags")
                            .font(.caption)
                            .foregroundColor(.secondary)

                        HStack {
                            ForEach(thought.tags, id: \.self) { tag in
                                Text(tag)
                                    .font(.caption)
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 4)
                                    .background(Color.blue.opacity(0.1))
                                    .foregroundColor(.blue)
                                    .cornerRadius(4)
                            }
                        }
                    }
                }

                // Reflection
                if let reflection = thought.reflection {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Reflection")
                            .font(.caption)
                            .foregroundColor(.secondary)

                        Text(reflection)
                            .font(.subheadline)
                            .italic()
                    }
                }

                // Novelty score
                if let novelty = thought.noveltyScore {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Novelty Score")
                            .font(.caption)
                            .foregroundColor(.secondary)

                        ProgressView(value: novelty)
                            .tint(novelty > 0.7 ? .green : novelty > 0.4 ? .orange : .gray)

                        Text(String(format: "%.0f%% novel", novelty * 100))
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }

                Divider()

                // Metadata
                Text("Created \(thought.createdAt.formatted())")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .padding()
        }
        .navigationTitle("Thought Details")
        .navigationBarTitleDisplayMode(.inline)
    }
}
```

**And** when I view abodes, I see AI-generated names like "Fitness Goals", "Creative Projects"

**And** I can tap an abode to see all thoughts in that cluster

**And** I can tap a thought to see full details with tags, reflection, novelty

**And** pull-to-refresh reloads the abode list

**And** "Trigger Clustering" button creates abodes when I have 5+ thoughts

**Technical Notes:**
- AbodeListView: Empty state + trigger button for testing
- AbodeDetailView: List of thoughts (newest first)
- ThoughtDetailView: Full metadata display (tags, reflection, novelty)
- Pull-to-refresh on list view
- Relative timestamps ("2 hours ago")
- NavigationLink for drill-down navigation

**Prerequisites:** Story 4.4 (Abodes API), Story 2.5 (APIService)

---

## Epic 4 Summary

**Stories Created:** 6 stories
**FR Coverage:**
- FR5 (Semantic Clustering - Automatic Grouping) ✅
- FR6 (Abode Naming & Management) ✅
- FR11 (ML Mode: Tag Mode) ✅
- FR12 (ML Mode: Reflection Mode) ✅
- FR13 (ML Mode: Novelty Mode) ✅
- FR14 (Knowledge Graph Structure) ✅

**Technical Capabilities Established:**
- ✅ SQLAlchemy Abode model with knowledge graph schema
- ✅ K-means clustering algorithm (optimal k via silhouette score)
- ✅ LLM-based abode naming (2-4 word descriptive titles)
- ✅ Abodes CRUD API endpoints (list, get, add/remove thoughts)
- ✅ ML Modes: Tag (2-5 tags), Reflection (1-2 sentences), Novelty (0.0-1.0 score)
- ✅ Mode orchestration service (sequential execution)
- ✅ iOS Abode list, detail, and thought detail views
- ✅ Manual clustering trigger for testing

**Architecture Sections Implemented:**
- Database relationships (Abode ← Thought)
- Knowledge graph structure (thought_relationships table)
- ML clustering (K-means with automatic k selection)
- Mode orchestration (sequential functions, not framework)
- LLM integration (naming, tags, reflection, novelty)
- iOS drill-down navigation (List → Detail → Thought)

**Key Features:**
- Automatic semantic clustering (5+ thoughts required)
- AI-generated descriptive abode names
- Rich thought metadata (tags, reflections, novelty scores)
- Manual organization (add/remove thoughts from abodes)
- Knowledge graph foundation for future graph RAG

**Ready for Epic 5:** Personalized Discovery - taste learning, action recommendations

---

## Epic 5: Personalized Discovery

**Epic Goal:** Enable users to receive personalized action recommendations based on their unique taste profile learned from saved thoughts, helping them discover experiences and activities aligned with their interests.

**FR Coverage:** FR9 (Discover Mode - Taste Learning), FR10 (Discover Mode - Action Recommendations)

**User Value Statement:** After this epic, users can request recommendations and receive personalized suggestions (content to consume, goals to pursue) that align with their interests, learned from the patterns in their thoughts.

---

### Story 5.1: Implement Taste Profile Analysis Service

**User Story:**
As a developer, I want to analyze embedding patterns to generate a user's taste profile, so that I can understand what topics and themes the user cares about.

**Acceptance Criteria:**

**Given** I need to understand user preferences
**When** I implement taste profile analysis
**Then** I create `app/services/taste_service.py`:

```python
from app.models.thought import Thought
from app.models.abode import Abode
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
        Analyze user's thoughts to generate taste profile

        Returns:
            Dictionary with:
            - top_topics: List of (topic_name, relevance_score) tuples
            - top_tags: Most frequent tags across all thoughts
            - dominant_abodes: Abodes with most thoughts (main interests)
            - embedding_centroid: Average embedding vector (taste center)
        """
        # Get all user thoughts
        thoughts = db.query(Thought).filter(Thought.user_id == user_id).all()

        if len(thoughts) < 3:
            logger.info(f"User {user_id} has {len(thoughts)} thoughts, insufficient for taste profile")
            return {
                "top_topics": [],
                "top_tags": [],
                "dominant_abodes": [],
                "embedding_centroid": None
            }

        # Extract tags
        all_tags = []
        for thought in thoughts:
            if thought.tags:
                all_tags.extend(thought.tags)

        # Count tag frequency
        tag_counts = Counter(all_tags)
        top_tags = tag_counts.most_common(10)  # Top 10 tags

        # Get dominant abodes
        abodes = db.query(Abode).filter(Abode.user_id == user_id).all()
        abode_thought_counts = []
        for abode in abodes:
            count = db.query(Thought).filter(Thought.abode_id == abode.id).count()
            if count > 0:
                abode_thought_counts.append((abode.name, count))

        # Sort by thought count descending
        dominant_abodes = sorted(abode_thought_counts, key=lambda x: x[1], reverse=True)[:5]

        # Generate embedding centroid (average of all embeddings)
        texts = [t.thought_text for t in thoughts]
        embeddings_list = embedding_service.generate_embeddings_batch(texts)
        embeddings = np.array(embeddings_list, dtype=np.float32)

        # Calculate centroid (average embedding)
        centroid = np.mean(embeddings, axis=0)
        centroid_normalized = centroid / np.linalg.norm(centroid)

        # Top topics from abode names + tags
        top_topics = []
        for abode_name, count in dominant_abodes:
            relevance = count / len(thoughts)  # Proportion of thoughts in this abode
            top_topics.append((abode_name, relevance))

        logger.info(f"Generated taste profile for user {user_id}: {len(top_topics)} topics, {len(top_tags)} tags")

        return {
            "top_topics": top_topics,  # [(topic, relevance), ...]
            "top_tags": [tag for tag, count in top_tags],  # [tag1, tag2, ...]
            "dominant_abodes": [name for name, count in dominant_abodes],  # [abode1, abode2, ...]
            "embedding_centroid": centroid_normalized.tolist()  # 384-dim vector
        }

    async def get_taste_summary(self, user_id: str, db: Session) -> str:
        """
        Generate human-readable taste summary

        Returns:
            String like "You care about Fitness Goals, Creative Projects, and Learning"
        """
        profile = await self.generate_taste_profile(user_id, db)

        if not profile["top_topics"]:
            return "Not enough data to understand your interests yet. Capture more thoughts!"

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

**And** I can test taste profile generation:

```python
# Test with sample user
profile = await taste_service.generate_taste_profile(user_id, db)

assert "top_topics" in profile
assert "top_tags" in profile
assert "dominant_abodes" in profile
assert "embedding_centroid" in profile

# Centroid should be 384-dim normalized vector
if profile["embedding_centroid"]:
    assert len(profile["embedding_centroid"]) == 384
    # Check normalized (magnitude ~1.0)
    magnitude = np.linalg.norm(profile["embedding_centroid"])
    assert 0.99 <= magnitude <= 1.01
```

**And** taste profile requires minimum 3 thoughts

**And** top topics are ranked by relevance (proportion of thoughts in abode)

**And** embedding centroid represents the "center" of user's interests in semantic space

**Technical Notes:**
- Taste profile = aggregation of abodes + tags + embedding centroid
- Centroid: Average of all thought embeddings (normalized)
- Top topics: Abode names ranked by thought count
- Top tags: Most frequent tags across all thoughts
- Minimum data: 3 thoughts required
- Profile updates dynamically as new thoughts added

**Prerequisites:** Story 4.1 (Abode model), Story 2.2 (Embedding service)

---

### Story 5.2: Implement Recommendation Generation with RAG + LLM

**User Story:**
As a developer, I want to use RAG reasoning combined with LLM general knowledge to generate personalized recommendations, so that users receive relevant suggestions aligned with their taste.

**Acceptance Criteria:**

**Given** I need to generate personalized recommendations
**When** I implement the recommendation service
**Then** I add to `app/services/llm_service.py`:

```python
async def generate_recommendations(
    self,
    taste_summary: str,
    recommendation_type: str,
    recent_thoughts_sample: List[str]
) -> Optional[Dict]:
    """
    Generate personalized recommendations using RAG + LLM

    Args:
        taste_summary: Human-readable taste profile
        recommendation_type: "content" or "goal"
        recent_thoughts_sample: Sample of recent thoughts for context (5-10)

    Returns:
        Dictionary with:
        - action: The recommended action (e.g., "Watch Blade Runner 2049")
        - reason: Why this recommendation fits the user (1-2 sentences)
        - category: Type of recommendation (movie, book, exercise, etc.)
    """
    # Build context from recent thoughts
    thoughts_context = "\n".join(f"- {text}" for text in recent_thoughts_sample[:10])

    if recommendation_type == "content":
        system_prompt = """You are a personalized recommendation assistant.
Your task is to suggest content (movies, books, music, articles, podcasts) based on user interests.

Rules:
- Suggest ONE specific piece of content
- Be specific (title + creator, e.g., "Watch 'Blade Runner 2049' directed by Denis Villeneuve")
- Explain why it fits their interests (1-2 sentences)
- Choose content that's accessible and well-regarded
- Format as JSON: {"action": "...", "reason": "...", "category": "..."}"""

        user_prompt = f"""Based on this user's interests:

Taste Summary: {taste_summary}

Recent thoughts:
{thoughts_context}

Recommend ONE specific piece of content they would enjoy.

Return JSON with: action (the recommendation), reason (why it fits), category (movie/book/music/etc)."""

    else:  # goal-oriented
        system_prompt = """You are a personalized goal and activity assistant.
Your task is to suggest actionable goals or activities based on user interests.

Rules:
- Suggest ONE specific action or goal
- Be actionable (e.g., "Go for a 30-minute run today", "Practice piano scales for 15 minutes")
- Explain how it aligns with their goals (1-2 sentences)
- Keep it achievable (not overly ambitious)
- Format as JSON: {"action": "...", "reason": "...", "category": "..."}"""

        user_prompt = f"""Based on this user's interests and goals:

Taste Summary: {taste_summary}

Recent thoughts:
{thoughts_context}

Recommend ONE specific action or goal they should pursue today.

Return JSON with: action (the recommendation), reason (why it aligns), category (fitness/learning/creative/etc)."""

    response = await self.generate(
        prompt=user_prompt,
        system_prompt=system_prompt,
        temperature=0.8,  # Higher creativity for diverse recommendations
        max_tokens=200
    )

    if response is None:
        return None

    # Parse JSON response
    try:
        import json
        # Clean response (remove markdown code blocks if present)
        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        recommendation = json.loads(cleaned)

        # Validate structure
        if "action" in recommendation and "reason" in recommendation and "category" in recommendation:
            return recommendation
        else:
            logger.warning(f"Invalid recommendation structure: {recommendation}")
            return None

    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse recommendation JSON: {e}")
        return None
```

**And** I create `app/services/recommendation_service.py`:

```python
from app.services.llm_service import llm_service
from app.services.taste_service import taste_service
from app.models.thought import Thought
from sqlalchemy.orm import Session
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

class RecommendationService:
    async def get_recommendation(
        self,
        user_id: str,
        db: Session,
        recommendation_type: str = "content"
    ) -> Optional[Dict]:
        """
        Generate a personalized recommendation for the user

        Args:
            user_id: User UUID
            db: Database session
            recommendation_type: "content" or "goal"

        Returns:
            Recommendation dict or None if generation fails
        """
        # Generate taste profile
        taste_summary = await taste_service.get_taste_summary(user_id, db)

        # Get recent thoughts for context
        recent_thoughts = db.query(Thought).filter(
            Thought.user_id == user_id
        ).order_by(Thought.created_at.desc()).limit(10).all()

        if len(recent_thoughts) < 3:
            logger.info(f"User {user_id} has insufficient thoughts for recommendations")
            return None

        recent_texts = [t.thought_text for t in recent_thoughts]

        # Generate recommendation
        recommendation = await llm_service.generate_recommendations(
            taste_summary=taste_summary,
            recommendation_type=recommendation_type,
            recent_thoughts_sample=recent_texts
        )

        if recommendation:
            logger.info(f"Generated {recommendation_type} recommendation for user {user_id}: {recommendation['action']}")

        return recommendation

# Singleton instance
recommendation_service = RecommendationService()
```

**And** I can test recommendation generation:

```python
# Test content recommendation
rec = await recommendation_service.get_recommendation(user_id, db, "content")
assert rec is not None
assert "action" in rec
assert "reason" in rec
assert "category" in rec
# Example: {"action": "Watch 'Blade Runner 2049'", "reason": "...", "category": "movie"}

# Test goal recommendation
rec = await recommendation_service.get_recommendation(user_id, db, "goal")
assert rec is not None
# Example: {"action": "Do 20 pushups", "reason": "...", "category": "fitness"}
```

**And** recommendations require minimum 3 thoughts

**And** content recommendations are specific (title + creator)

**And** goal recommendations are actionable and achievable

**And** temperature 0.8 for creative diversity

**Technical Notes:**
- RAG reasoning: Recent thoughts provide context
- LLM synthesis: General knowledge for recommendations
- Two types: content (consume) vs goal (do)
- JSON response format for structured data
- Temperature 0.8: Higher creativity for variety
- Graceful failure: Return None if LLM fails

**Prerequisites:** Story 5.1 (Taste service), Story 3.1 (LLM service)

---

### Story 5.3: Create Discover API Endpoint

**User Story:**
As a developer, I want to implement the `/api/v1/discover` endpoint, so that iOS can request personalized recommendations.

**Acceptance Criteria:**

**Given** iOS needs to fetch recommendations
**When** I implement the discover endpoint
**Then** I create `app/schemas/discover.py`:

```python
from pydantic import BaseModel, Field
from typing import Optional

class DiscoverRequest(BaseModel):
    recommendation_type: str = Field(alias="recommendationType", default="content")
    # "content" or "goal"

    class Config:
        populate_by_name = True

class TasteProfileResponse(BaseModel):
    summary: str
    top_topics: list[tuple[str, float]] = Field(alias="topTopics")
    top_tags: list[str] = Field(alias="topTags")
    dominant_abodes: list[str] = Field(alias="dominantAbodes")

    class Config:
        populate_by_name = True

class RecommendationResponse(BaseModel):
    action: str
    reason: str
    category: str
    taste_summary: str = Field(alias="tasteSummary")

    class Config:
        populate_by_name = True
```

**And** I create `app/api/v1/endpoints/discover.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.schemas.discover import DiscoverRequest, RecommendationResponse, TasteProfileResponse
from app.services.recommendation_service import recommendation_service
from app.services.taste_service import taste_service

router = APIRouter()

@router.post("/recommendation", response_model=RecommendationResponse)
async def get_recommendation(
    request: DiscoverRequest,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a personalized recommendation based on user's taste profile

    Request:
        recommendationType: "content" or "goal"

    Returns:
        Recommendation with action, reason, category, and taste summary
    """
    # Validate recommendation type
    if request.recommendation_type not in ["content", "goal"]:
        raise HTTPException(status_code=400, detail="Invalid recommendation type. Must be 'content' or 'goal'")

    # Generate recommendation
    recommendation = await recommendation_service.get_recommendation(
        user_id=user.id,
        db=db,
        recommendation_type=request.recommendation_type
    )

    if recommendation is None:
        raise HTTPException(
            status_code=503,
            detail="Unable to generate recommendation. Try again or capture more thoughts."
        )

    # Get taste summary for context
    taste_summary = await taste_service.get_taste_summary(user.id, db)

    return RecommendationResponse(
        action=recommendation["action"],
        reason=recommendation["reason"],
        category=recommendation["category"],
        taste_summary=taste_summary
    )

@router.get("/taste-profile", response_model=TasteProfileResponse)
async def get_taste_profile(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's taste profile (for debugging/display)

    Returns:
        Taste profile with topics, tags, and abodes
    """
    profile = await taste_service.generate_taste_profile(user.id, db)
    summary = await taste_service.get_taste_summary(user.id, db)

    return TasteProfileResponse(
        summary=summary,
        top_topics=profile["top_topics"],
        top_tags=profile["top_tags"],
        dominant_abodes=profile["dominant_abodes"]
    )
```

**And** I register the router in `app/api/v1/api.py`:

```python
from app.api.v1.endpoints import thoughts, ml, abodes, discover

api_router = APIRouter()
api_router.include_router(thoughts.router, prefix="/thoughts", tags=["thoughts"])
api_router.include_router(ml.router, prefix="/ml", tags=["ml"])
api_router.include_router(abodes.router, prefix="/abodes", tags=["abodes"])
api_router.include_router(discover.router, prefix="/discover", tags=["discover"])
```

**And** I can test the endpoints:

**POST /api/v1/discover/recommendation**
- Request:
```json
{
  "recommendationType": "content"
}
```
- Response: 200
```json
{
  "action": "Watch 'Blade Runner 2049' directed by Denis Villeneuve",
  "reason": "Based on your interest in sci-fi themes and visual storytelling, this film offers stunning cinematography and deep philosophical questions.",
  "category": "movie",
  "tasteSummary": "You care about Sci-Fi Exploration, Creative Projects, and Philosophy"
}
```

**And** when requesting "goal" type:
```json
{
  "recommendationType": "goal"
}
```
- Response: 200
```json
{
  "action": "Go for a 30-minute run this morning",
  "reason": "Aligns with your fitness goals and helps build consistency with your workout routine.",
  "category": "fitness",
  "tasteSummary": "You care about Fitness Goals, Health, and Personal Growth"
}
```

**GET /api/v1/discover/taste-profile**
- Response: 200 with full taste profile (for debugging)

**And** when user has insufficient data (< 3 thoughts):
- Response: 503 with helpful message

**And** all endpoints require authentication

**Technical Notes:**
- POST /discover/recommendation (type: content or goal)
- GET /discover/taste-profile (optional, for debugging)
- 503 error when insufficient data (graceful, not 500)
- camelCase JSON responses
- Taste summary included in recommendation response

**Prerequisites:** Story 5.2 (Recommendation service), Story 5.1 (Taste service)

---

### Story 5.4: Build iOS Discover View with Recommendation UI

**User Story:**
As a user, I want to tap a button and receive a personalized recommendation based on my interests, so that I can discover new content or pursue meaningful goals.

**Acceptance Criteria:**

**Given** I am on the Discover tab
**When** I view the screen
**Then** I see:
- My taste summary (e.g., "You care about Fitness Goals, Creative Projects")
- Two buttons: "Discover Content" and "Discover Goal"
- A card showing the last recommendation (if any)

**And** when I tap "Discover Content"
**Then** the app calls `POST /api/v1/discover/recommendation` with type "content"
**And** I see a loading indicator
**And** a new recommendation card appears with:
  - Recommendation action (e.g., "Watch 'Blade Runner 2049'")
  - Reason why it fits me
  - Category badge (movie, book, etc.)

**And** when I tap "Discover Goal"
**Then** the app calls `POST /api/v1/discover/recommendation` with type "goal"
**And** a new recommendation card appears with:
  - Action to take (e.g., "Go for a 30-minute run")
  - Reason why it aligns with my goals
  - Category badge (fitness, learning, etc.)

**And** when I don't have enough thoughts yet (< 3)
**Then** I see a message: "Capture more thoughts to unlock personalized recommendations!"
**And** the buttons are disabled

**And** I can request multiple recommendations (each tap generates a new one)

**And** the recommendation card has a clean, card-based design

**Implementation:**

Update `Services/APIService.swift`:

```swift
struct DiscoverRequest: Codable {
    let recommendationType: String
}

struct Recommendation: Codable {
    let action: String
    let reason: String
    let category: String
    let tasteSummary: String
}

extension APIService {
    func getRecommendation(type: String) async throws -> Recommendation {
        guard let session = try? await supabase.auth.session else {
            throw APIError.unauthorized
        }

        let url = URL(string: "\(baseURL)/discover/recommendation")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body = DiscoverRequest(recommendationType: type)
        request.httpBody = try JSONEncoder().encode(body)

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 200:
            return try JSONDecoder().decode(Recommendation.self, from: data)
        case 401:
            throw APIError.unauthorized
        case 503:
            throw APIError.serverError("Not enough data yet. Capture more thoughts!")
        default:
            throw APIError.serverError("Failed to get recommendation")
        }
    }
}
```

Create `ViewModels/DiscoverViewModel.swift`:

```swift
import Foundation
import Observation

@Observable
class DiscoverViewModel {
    var currentRecommendation: Recommendation?
    var isLoading: Bool = false
    var error: String?
    var tasteSummary: String = "Loading your interests..."

    func loadRecommendation(type: String) async {
        isLoading = true
        error = nil

        do {
            let recommendation = try await APIService.shared.getRecommendation(type: type)
            currentRecommendation = recommendation
            tasteSummary = recommendation.tasteSummary
        } catch {
            self.error = error.localizedDescription
        }

        isLoading = false
    }
}
```

Update `Views/Discover/DiscoverView.swift`:

```swift
import SwiftUI

struct DiscoverView: View {
    @State private var viewModel = DiscoverViewModel()

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 24) {
                    // Taste summary
                    VStack(spacing: 8) {
                        Text("Your Interests")
                            .font(.caption)
                            .foregroundColor(.secondary)

                        Text(viewModel.tasteSummary)
                            .font(.headline)
                            .multilineTextAlignment(.center)
                    }
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(12)

                    // Action buttons
                    HStack(spacing: 16) {
                        Button(action: {
                            Task {
                                await viewModel.loadRecommendation(type: "content")
                            }
                        }) {
                            VStack {
                                Image(systemName: "sparkles")
                                    .font(.title)
                                Text("Discover Content")
                                    .font(.caption)
                            }
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.blue.opacity(0.1))
                            .foregroundColor(.blue)
                            .cornerRadius(12)
                        }
                        .disabled(viewModel.isLoading)

                        Button(action: {
                            Task {
                                await viewModel.loadRecommendation(type: "goal")
                            }
                        }) {
                            VStack {
                                Image(systemName: "target")
                                    .font(.title)
                                Text("Discover Goal")
                                    .font(.caption)
                            }
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.green.opacity(0.1))
                            .foregroundColor(.green)
                            .cornerRadius(12)
                        }
                        .disabled(viewModel.isLoading)
                    }

                    // Loading indicator
                    if viewModel.isLoading {
                        ProgressView("Discovering...")
                    }

                    // Error message
                    if let error = viewModel.error {
                        Text(error)
                            .foregroundColor(.red)
                            .font(.caption)
                            .multilineTextAlignment(.center)
                            .padding()
                    }

                    // Recommendation card
                    if let rec = viewModel.currentRecommendation {
                        VStack(alignment: .leading, spacing: 12) {
                            // Category badge
                            Text(rec.category.uppercased())
                                .font(.caption2)
                                .fontWeight(.bold)
                                .foregroundColor(.white)
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(categoryColor(rec.category))
                                .cornerRadius(4)

                            // Action
                            Text(rec.action)
                                .font(.title3)
                                .fontWeight(.semibold)

                            // Reason
                            Text(rec.reason)
                                .font(.body)
                                .foregroundColor(.secondary)
                        }
                        .padding()
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(Color(.systemBackground))
                        .cornerRadius(12)
                        .shadow(color: Color.black.opacity(0.1), radius: 8, x: 0, y: 4)
                    }

                    Spacer()
                }
                .padding()
            }
            .navigationTitle("Discover")
        }
    }

    func categoryColor(_ category: String) -> Color {
        switch category.lowercased() {
        case "movie", "film": return .purple
        case "book": return .brown
        case "music": return .pink
        case "fitness", "exercise": return .green
        case "learning": return .blue
        case "creative": return .orange
        default: return .gray
        }
    }
}
```

**And** when I tap "Discover Content", I get recommendations like:
- "Watch 'Blade Runner 2049' directed by Denis Villeneuve"
- "Read 'Atomic Habits' by James Clear"
- "Listen to 'Random Access Memories' by Daft Punk"

**And** when I tap "Discover Goal", I get recommendations like:
- "Go for a 30-minute run this morning"
- "Practice piano scales for 15 minutes"
- "Write 500 words in your journal"

**And** each recommendation has a color-coded category badge

**And** the taste summary updates with each recommendation

**And** when I don't have enough data, I see a helpful error message

**Technical Notes:**
- Card-based UI with shadows for visual hierarchy
- Color-coded categories (fitness=green, movie=purple, etc.)
- Loading states between requests
- Error handling for insufficient data
- Taste summary displayed prominently
- ScrollView for potential long content

**Prerequisites:** Story 5.3 (Discover API), Story 2.5 (APIService)

---

## Epic 5 Summary

**Stories Created:** 4 stories
**FR Coverage:**
- FR9 (Discover Mode - Taste Learning) ✅
- FR10 (Discover Mode - Action Recommendations) ✅

**Technical Capabilities Established:**
- ✅ Taste profile analysis (topics, tags, abodes, embedding centroid)
- ✅ Recommendation generation (RAG + LLM synthesis)
- ✅ Two recommendation types: content (consume) vs goal (do)
- ✅ Discover API endpoint with taste profile
- ✅ iOS Discover view with card-based UI
- ✅ Minimum data requirement (3 thoughts)

**Architecture Sections Implemented:**
- Taste profile generation (embedding patterns + abode analysis)
- RAG reasoning (recent thoughts provide context)
- LLM synthesis (general knowledge for recommendations)
- JSON response parsing
- iOS card-based UI design

**Key Features:**
- Automatic taste learning from thought patterns
- Personalized content recommendations (movies, books, music)
- Actionable goal recommendations (fitness, learning, creative)
- 70%+ relevance target (via taste profile + RAG context)
- Graceful degradation (insufficient data → helpful message)

**Ready for Epic 6:** RAG-Powered Personal Chat - vector search, streaming responses, confidence-based fallback

---

## Epic 6: RAG-Powered Personal Chat

**Epic Goal:** Enable users to ask natural language questions and receive personalized answers based on their saved thoughts, with streaming responses and intelligent fallback to general knowledge when needed.

**FR Coverage:** FR7 (RAG-Powered Chat Interface), FR8 (Confidence-Based Chat Fallback), FR15 (Streaming LLM Responses)

**User Value Statement:** After this epic, users can chat with their personal knowledge base, asking questions and getting instant answers based on their own thoughts, with real-time streaming responses for a responsive experience.

---

### Story 6.1: Implement RAG Service with Vector Search

**User Story:**
As a developer, I want to implement RAG (Retrieval-Augmented Generation) with FAISS vector search, so that I can retrieve relevant thoughts for a user's question.

**Acceptance Criteria:**

**Given** I need to search thoughts for relevant context
**When** I implement the RAG service
**Then** I create `app/services/rag_service.py`:

```python
from app.services.vector_service import vector_service
from app.services.embedding_service import embedding_service
from app.models.thought import Thought
from sqlalchemy.orm import Session
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, similarity_threshold: float = 0.7):
        """
        Initialize RAG service

        Args:
            similarity_threshold: Minimum similarity for RAG mode (0.7 = 70%)
        """
        self.similarity_threshold = similarity_threshold

    async def retrieve_relevant_thoughts(
        self,
        query: str,
        user_id: str,
        db: Session,
        top_k: int = 5
    ) -> Tuple[List[Thought], float, str]:
        """
        Retrieve relevant thoughts for a query using vector search

        Args:
            query: User's question
            user_id: User UUID
            db: Database session
            top_k: Number of thoughts to retrieve

        Returns:
            Tuple of (thoughts, max_similarity, mode)
            - thoughts: List of relevant Thought objects
            - max_similarity: Highest similarity score (0.0-1.0)
            - mode: "rag" or "direct" based on similarity threshold
        """
        # Generate query embedding
        query_embedding = embedding_service.generate_embedding(query)

        # Search FAISS for similar thoughts
        search_results = vector_service.search_similar(query_embedding, top_k=top_k)

        if not search_results:
            logger.info(f"No search results for query: {query}")
            return [], 0.0, "direct"

        # Extract thought IDs and similarities
        thought_ids = [tid for tid, sim in search_results]
        similarities = [sim for tid, sim in search_results]
        max_similarity = max(similarities) if similarities else 0.0

        # Retrieve thoughts from database
        thoughts = db.query(Thought).filter(
            Thought.id.in_(thought_ids),
            Thought.user_id == user_id  # Ensure user owns these thoughts
        ).all()

        # Sort by similarity (maintain order from FAISS)
        thought_dict = {t.id: t for t in thoughts}
        sorted_thoughts = [thought_dict[tid] for tid in thought_ids if tid in thought_dict]

        # Determine mode based on similarity threshold
        mode = "rag" if max_similarity >= self.similarity_threshold else "direct"

        logger.info(f"Retrieved {len(sorted_thoughts)} thoughts, max similarity: {max_similarity:.3f}, mode: {mode}")

        return sorted_thoughts, max_similarity, mode

    def format_context(self, thoughts: List[Thought]) -> str:
        """
        Format retrieved thoughts into context string for LLM

        Returns:
            Formatted context like:
            "From your thoughts:
            - [Thought 1 text]
            - [Thought 2 text]
            ..."
        """
        if not thoughts:
            return "No relevant thoughts found."

        context_lines = ["From your saved thoughts:"]
        for i, thought in enumerate(thoughts, 1):
            context_lines.append(f"{i}. {thought.thought_text}")

        return "\n".join(context_lines)

# Singleton instance
rag_service = RAGService(similarity_threshold=0.7)
```

**And** I can test RAG retrieval:

```python
# Test retrieval
thoughts, similarity, mode = await rag_service.retrieve_relevant_thoughts(
    query="How do I get stronger?",
    user_id=user_id,
    db=db,
    top_k=5
)

assert isinstance(thoughts, list)
assert 0.0 <= similarity <= 1.0
assert mode in ["rag", "direct"]

# If similarity > 0.7, mode should be "rag"
if similarity >= 0.7:
    assert mode == "rag"
else:
    assert mode == "direct"
```

**And** similarity threshold is 0.7 (70%)

**And** mode = "rag" when similarity ≥ 0.7 (use personal knowledge)

**And** mode = "direct" when similarity < 0.7 (use general knowledge)

**And** top-k retrieval returns 5 most similar thoughts by default

**And** thoughts are filtered to ensure user ownership (security)

**Technical Notes:**
- Follow Architecture "RAG Chat: Vector search + LLM response"
- Similarity threshold: 0.7 (configurable)
- Top-k: 5 thoughts (balance context vs LLM token limit)
- Security: Filter by user_id to prevent data leakage
- Mode switching: Automatic based on similarity score
- Context formatting: Numbered list for clarity

**Prerequisites:** Story 2.3 (FAISS), Story 2.2 (Embeddings)

---

### Story 6.2: Implement Streaming Chat Service with Claude Haiku

**User Story:**
As a developer, I want to implement streaming LLM responses using Claude Haiku, so that users see answers appear in real-time with <2s latency.

**Acceptance Criteria:**

**Given** I need streaming chat responses
**When** I implement the chat service
**Then** I update `app/core/config.py` to add Anthropic settings:

```python
class Settings(BaseSettings):
    # ... existing settings ...
    ANTHROPIC_API_KEY: str
    ANTHROPIC_MODEL: str = "claude-3-haiku-20240307"

    class Config:
        env_file = ".env"
```

**And** I add to `.env`:
```
ANTHROPIC_API_KEY=sk-ant-xxx
```

**And** I add dependencies to `pyproject.toml`:
```toml
[tool.poetry.dependencies]
anthropic = "^0.25.0"
```

**And** I create `app/services/chat_service.py`:

```python
from anthropic import AsyncAnthropic
from app.core.config import settings
from app.services.rag_service import rag_service
from app.models.thought import Thought
from sqlalchemy.orm import Session
from typing import AsyncIterator, List
import logging

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.ANTHROPIC_MODEL

    async def stream_chat_response(
        self,
        query: str,
        user_id: str,
        db: Session
    ) -> AsyncIterator[dict]:
        """
        Stream chat response with RAG or direct mode

        Yields:
            Dictionary chunks with:
            - type: "mode" | "content" | "done"
            - data: mode string | text chunk | final metadata
        """
        # Retrieve relevant thoughts
        thoughts, similarity, mode = await rag_service.retrieve_relevant_thoughts(
            query=query,
            user_id=user_id,
            db=db,
            top_k=5
        )

        # Yield mode first
        yield {"type": "mode", "data": mode, "similarity": similarity}

        # Build prompt based on mode
        if mode == "rag" and thoughts:
            # RAG mode: Use personal knowledge
            context = rag_service.format_context(thoughts)

            system_prompt = """You are Pookie, a personal AI assistant with access to the user's saved thoughts.
Your task is to answer questions based on their personal knowledge.

Rules:
- Use ONLY information from the provided thoughts
- If the thoughts don't contain the answer, say "I don't have that information in your thoughts"
- Be conversational and helpful
- Reference specific thoughts when relevant
- Keep responses concise (2-3 paragraphs max)"""

            user_prompt = f"""{context}

Question: {query}

Answer based on the thoughts above:"""

        else:
            # Direct mode: General knowledge
            system_prompt = """You are Pookie, a helpful AI assistant.
The user asked a question, but their saved thoughts don't contain relevant information.
Provide a general, helpful answer using your knowledge.

Rules:
- Be conversational and helpful
- Keep responses concise (2-3 paragraphs max)
- Acknowledge you're using general knowledge, not their personal thoughts"""

            user_prompt = f"""Question: {query}

(Note: Your saved thoughts don't have information about this topic, so I'm using general knowledge to help.)

Answer:"""

        # Stream response from Claude
        try:
            stream = await self.client.messages.create(
                model=self.model,
                max_tokens=500,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                stream=True
            )

            async for event in stream:
                if event.type == "content_block_delta":
                    if hasattr(event.delta, "text"):
                        yield {"type": "content", "data": event.delta.text}

            # Yield done signal
            yield {"type": "done", "data": {"mode": mode, "similarity": similarity, "thought_count": len(thoughts)}}

        except Exception as e:
            logger.error(f"Chat streaming error: {e}")
            yield {"type": "error", "data": str(e)}

# Singleton instance
chat_service = ChatService()
```

**And** I can test streaming:

```python
# Test streaming response
async for chunk in chat_service.stream_chat_response("How do I get stronger?", user_id, db):
    if chunk["type"] == "mode":
        assert chunk["data"] in ["rag", "direct"]
    elif chunk["type"] == "content":
        assert isinstance(chunk["data"], str)
    elif chunk["type"] == "done":
        assert "mode" in chunk["data"]
        assert "similarity" in chunk["data"]
```

**And** streaming starts with mode indicator

**And** content chunks are yielded as they arrive from Claude

**And** final "done" chunk includes metadata (mode, similarity, thought count)

**And** errors are yielded as error chunks

**And** Claude Haiku model used for cost efficiency (<$0.25 per million tokens)

**Technical Notes:**
- Follow Architecture "Streaming: SSE for real-time chat responses"
- Claude Haiku: Fast, cheap, good quality
- Streaming: AsyncIterator yields chunks as they arrive
- Mode indicator first: Frontend knows whether answer is personal or general
- System prompts: Different for RAG vs direct mode
- Max tokens: 500 (concise responses, ~2-3 paragraphs)
- Error handling: Yield error chunks, don't raise exceptions

**Prerequisites:** Story 6.1 (RAG service)

---

### Story 6.3: Create Streaming Chat API Endpoint with SSE

**User Story:**
As a developer, I want to implement SSE (Server-Sent Events) endpoint for streaming chat responses, so that iOS can receive real-time updates.

**Acceptance Criteria:**

**Given** iOS needs real-time streaming responses
**When** I implement the SSE endpoint
**Then** I create `app/schemas/chat.py`:

```python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
```

**And** I create `app/api/v1/endpoints/chat.py`:

```python
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.core.security import get_current_user
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.schemas.chat import ChatRequest
from app.services.chat_service import chat_service
import json

router = APIRouter()

@router.post("/stream")
async def stream_chat(
    request: ChatRequest,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Stream chat response via Server-Sent Events (SSE)

    Request:
        query: User's question

    Returns:
        SSE stream with events:
        - mode: {"mode": "rag"|"direct", "similarity": 0.0-1.0}
        - content: {"text": "chunk"}
        - done: {"mode": "...", "similarity": ..., "thoughtCount": ...}
        - error: {"error": "message"}
    """

    async def event_generator():
        """Generate SSE events"""
        try:
            async for chunk in chat_service.stream_chat_response(
                query=request.query,
                user_id=user.id,
                db=db
            ):
                # Format as SSE event
                event_type = chunk["type"]
                event_data = json.dumps(chunk)

                yield f"event: {event_type}\n"
                yield f"data: {event_data}\n\n"

        except Exception as e:
            # Send error event
            error_data = json.dumps({"type": "error", "data": str(e)})
            yield f"event: error\n"
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )
```

**And** I register the router in `app/api/v1/api.py`:

```python
from app.api.v1.endpoints import thoughts, ml, abodes, discover, chat

api_router = APIRouter()
api_router.include_router(thoughts.router, prefix="/thoughts", tags=["thoughts"])
api_router.include_router(ml.router, prefix="/ml", tags=["ml"])
api_router.include_router(abodes.router, prefix="/abodes", tags=["abodes"])
api_router.include_router(discover.router, prefix="/discover", tags=["discover"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
```

**And** I can test the endpoint:

**POST /api/v1/chat/stream**
- Request:
```json
{
  "query": "What are my fitness goals?"
}
```
- Response: SSE stream
```
event: mode
data: {"type":"mode","data":"rag","similarity":0.85}

event: content
data: {"type":"content","data":"Based on your thoughts, "}

event: content
data: {"type":"content","data":"you want to get jacked and "}

event: content
data: {"type":"content","data":"bench 225 lbs. "}

event: done
data: {"type":"done","data":{"mode":"rag","similarity":0.85,"thought_count":3}}
```

**And** SSE events are properly formatted (event: type, data: json)

**And** headers prevent caching and buffering

**And** authentication required (JWT in Authorization header)

**And** streaming starts immediately (<2s to first token)

**Technical Notes:**
- Follow Architecture "API Communication: REST + SSE"
- SSE format: `event: type\ndata: json\n\n`
- Headers: no-cache, keep-alive, no buffering
- Authentication: Standard JWT middleware
- Error handling: Send error events, don't break stream
- Performance: <2s latency to first token (target)

**Prerequisites:** Story 6.2 (Chat service)

---

### Story 6.4: Implement iOS SSE Client and Chat UI

**User Story:**
As a user, I want to ask questions and see answers appear in real-time, with an indication of whether Pookie is using my thoughts or general knowledge.

**Acceptance Criteria:**

**Given** I am on the Chat tab
**When** I view the screen
**Then** I see:
- A chat interface with message bubbles
- Text input field at bottom
- Send button

**And** when I type a question and tap Send
**Then** my message appears as a user bubble
**And** a "Pookie is thinking..." indicator appears
**And** Pookie's response starts streaming in real-time
**And** I see a mode indicator: "From your thoughts" or "General knowledge"

**And** as the response streams:
- Each word appears as it's received
- The message bubble grows with new content
- The mode badge is visible (blue for RAG, gray for direct)

**And** when the response completes:
- The thinking indicator disappears
- I can send another message
- The conversation history is preserved

**And** I can scroll through chat history

**And** error handling: If streaming fails, I see "Failed to get response. Please try again."

**Implementation:**

Create `Services/SSEService.swift`:

```swift
import Foundation

class SSEService {
    func streamChat(query: String, token: String, onEvent: @escaping (SSEEvent) -> Void) async throws {
        let url = URL(string: "http://localhost:8000/api/v1/chat/stream")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body = ["query": query]
        request.httpBody = try JSONEncoder().encode(body)

        let (bytes, response) = try await URLSession.shared.bytes(for: request)

        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw APIError.networkError
        }

        var eventType: String?
        var dataBuffer = ""

        for try await line in bytes.lines {
            if line.hasPrefix("event:") {
                eventType = String(line.dropFirst(6).trimmingCharacters(in: .whitespaces))
            } else if line.hasPrefix("data:") {
                dataBuffer = String(line.dropFirst(5).trimmingCharacters(in: .whitespaces))
            } else if line.isEmpty && eventType != nil {
                // Complete event received
                if let event = parseEvent(type: eventType!, data: dataBuffer) {
                    onEvent(event)
                }
                eventType = nil
                dataBuffer = ""
            }
        }
    }

    private func parseEvent(type: String, data: String) -> SSEEvent? {
        guard let jsonData = data.data(using: .utf8),
              let dict = try? JSONSerialization.jsonObject(with: jsonData) as? [String: Any] else {
            return nil
        }

        switch type {
        case "mode":
            if let mode = dict["data"] as? String,
               let similarity = dict["similarity"] as? Double {
                return .mode(mode: mode, similarity: similarity)
            }
        case "content":
            if let text = dict["data"] as? String {
                return .content(text: text)
            }
        case "done":
            return .done
        case "error":
            if let error = dict["data"] as? String {
                return .error(message: error)
            }
        default:
            break
        }

        return nil
    }
}

enum SSEEvent {
    case mode(mode: String, similarity: Double)
    case content(text: String)
    case done
    case error(message: String)
}
```

Create `Models/ChatMessage.swift`:

```swift
import Foundation

struct ChatMessage: Identifiable {
    let id = UUID()
    let text: String
    let isUser: Bool
    let mode: String?  // "rag" or "direct" for assistant messages
    let timestamp: Date

    init(text: String, isUser: Bool, mode: String? = nil) {
        self.text = text
        self.isUser = isUser
        self.mode = mode
        self.timestamp = Date()
    }
}
```

Create `ViewModels/ChatViewModel.swift`:

```swift
import Foundation
import Observation
import Supabase

@Observable
class ChatViewModel {
    var messages: [ChatMessage] = []
    var inputText: String = ""
    var isStreaming: Bool = false
    var error: String?
    private var currentAssistantMessage: String = ""
    private var currentMode: String?

    func sendMessage() async {
        guard !inputText.isEmpty, !isStreaming else { return }

        let userMessage = ChatMessage(text: inputText, isUser: true)
        messages.append(userMessage)

        let query = inputText
        inputText = ""
        isStreaming = true
        error = nil
        currentAssistantMessage = ""
        currentMode = nil

        do {
            guard let session = try? await supabase.auth.session else {
                throw APIError.unauthorized
            }

            let sseService = SSEService()

            try await sseService.streamChat(query: query, token: session.accessToken) { [weak self] event in
                DispatchQueue.main.async {
                    self?.handleEvent(event)
                }
            }

        } catch {
            self.error = "Failed to get response. Please try again."
        }

        isStreaming = false
    }

    private func handleEvent(_ event: SSEEvent) {
        switch event {
        case .mode(let mode, _):
            currentMode = mode

        case .content(let text):
            currentAssistantMessage += text

            // Update or create assistant message
            if let lastIndex = messages.lastIndex(where: { !$0.isUser }) {
                // Update existing message
                messages[lastIndex] = ChatMessage(
                    text: currentAssistantMessage,
                    isUser: false,
                    mode: currentMode
                )
            } else {
                // Create new message
                let assistantMessage = ChatMessage(
                    text: currentAssistantMessage,
                    isUser: false,
                    mode: currentMode
                )
                messages.append(assistantMessage)
            }

        case .done:
            // Finalize message
            break

        case .error(let message):
            error = message
        }
    }
}
```

Update `Views/Chat/ChatView.swift`:

```swift
import SwiftUI

struct ChatView: View {
    @State private var viewModel = ChatViewModel()

    var body: some View {
        NavigationStack {
            VStack {
                // Messages
                ScrollViewReader { proxy in
                    ScrollView {
                        LazyVStack(spacing: 12) {
                            ForEach(viewModel.messages) { message in
                                MessageBubble(message: message)
                                    .id(message.id)
                            }

                            if viewModel.isStreaming {
                                HStack {
                                    ProgressView()
                                        .scaleEffect(0.8)
                                    Text("Pookie is thinking...")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                    Spacer()
                                }
                                .padding(.leading)
                            }
                        }
                        .padding()
                    }
                    .onChange(of: viewModel.messages.count) { _, _ in
                        if let lastMessage = viewModel.messages.last {
                            withAnimation {
                                proxy.scrollTo(lastMessage.id, anchor: .bottom)
                            }
                        }
                    }
                }

                // Error message
                if let error = viewModel.error {
                    Text(error)
                        .foregroundColor(.red)
                        .font(.caption)
                        .padding(.horizontal)
                }

                // Input
                HStack {
                    TextField("Ask Pookie...", text: $viewModel.inputText)
                        .textFieldStyle(.roundedBorder)
                        .disabled(viewModel.isStreaming)

                    Button(action: {
                        Task {
                            await viewModel.sendMessage()
                        }
                    }) {
                        Image(systemName: "arrow.up.circle.fill")
                            .font(.title2)
                            .foregroundColor(viewModel.inputText.isEmpty || viewModel.isStreaming ? .gray : .blue)
                    }
                    .disabled(viewModel.inputText.isEmpty || viewModel.isStreaming)
                }
                .padding()
            }
            .navigationTitle("Chat")
        }
    }
}

struct MessageBubble: View {
    let message: ChatMessage

    var body: some View {
        HStack {
            if message.isUser {
                Spacer()
            }

            VStack(alignment: message.isUser ? .trailing : .leading, spacing: 4) {
                // Mode badge for assistant messages
                if !message.isUser, let mode = message.mode {
                    Text(mode == "rag" ? "From your thoughts" : "General knowledge")
                        .font(.caption2)
                        .foregroundColor(mode == "rag" ? .blue : .secondary)
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(mode == "rag" ? Color.blue.opacity(0.1) : Color(.systemGray6))
                        .cornerRadius(4)
                }

                Text(message.text)
                    .padding(12)
                    .background(message.isUser ? Color.blue : Color(.systemGray6))
                    .foregroundColor(message.isUser ? .white : .primary)
                    .cornerRadius(16)
            }

            if !message.isUser {
                Spacer()
            }
        }
    }
}
```

**And** when I ask "What are my fitness goals?", I see:
- Mode badge: "From your thoughts" (blue)
- Response streams in real-time
- Answer based on my saved thoughts

**And** when I ask "What is quantum physics?", I see:
- Mode badge: "General knowledge" (gray)
- Response streams in real-time
- Answer from Claude's general knowledge

**And** messages appear smoothly as they stream

**And** auto-scroll follows the latest message

**And** I can send multiple messages in succession

**And** the chat history persists during the session

**Technical Notes:**
- SSEService: Native iOS SSE parsing with URLSession.shared.bytes
- Real-time updates: DispatchQueue.main.async for UI updates
- Message bubbles: Different colors for user (blue) vs assistant (gray)
- Mode badges: Visual indicator of knowledge source
- Auto-scroll: ScrollViewReader + onChange
- Loading state: "Pookie is thinking..." indicator
- Error handling: Display errors inline

**Prerequisites:** Story 6.3 (Chat API)

---

## Epic 6 Summary

**Stories Created:** 4 stories
**FR Coverage:**
- FR7 (RAG-Powered Chat Interface) ✅
- FR8 (Confidence-Based Chat Fallback) ✅
- FR15 (Streaming LLM Responses) ✅

**Technical Capabilities Established:**
- ✅ RAG service with FAISS vector search (top-k=5)
- ✅ Confidence-based mode switching (similarity ≥ 0.7 threshold)
- ✅ Streaming chat with Claude Haiku (<2s latency)
- ✅ SSE API endpoint (Server-Sent Events)
- ✅ iOS SSE client with native URLSession
- ✅ Real-time chat UI with message bubbles
- ✅ Mode indicators (RAG vs Direct)

**Architecture Sections Implemented:**
- Vector search (FAISS top-k retrieval)
- RAG pipeline (retrieve → format → LLM)
- Streaming responses (Claude API + SSE)
- iOS SSE integration (URLSession.shared.bytes)
- Real-time UI updates (DispatchQueue.main)

**Key Features:**
- Natural language Q&A over personal thoughts
- Real-time streaming responses (<2s to first token)
- Automatic mode switching based on relevance
- Visual mode indicators (blue = personal, gray = general)
- 80%+ RAG accuracy target (via vector search + LLM)
- Graceful fallback to general knowledge

**MVP Complete!** All 6 epics finished, covering all 15 functional requirements.

---

# Final FR Coverage Matrix

| FR # | Requirement | Epic | Stories | Status |
|------|-------------|------|---------|--------|
| FR1 | User Authentication & Profile Management | Epic 1 | 1.4, 1.5, 1.6 | ✅ Complete |
| FR2 | Thought Capture (Text Input) | Epic 2 | 2.6 | ✅ Complete |
| FR3 | Thought Capture (Voice Input) | Epic 2 | 2.7 | ✅ Complete |
| FR4 | Call Agents Mode - Thought Separation | Epic 3 | 3.1, 3.2, 3.3, 3.4 | ✅ Complete |
| FR5 | Semantic Clustering (Abodes) | Epic 4 | 4.2, 4.3, 4.4 | ✅ Complete |
| FR6 | Abode Naming & Management | Epic 4 | 4.3, 4.4, 4.6 | ✅ Complete |
| FR7 | RAG-Powered Chat Interface | Epic 6 | 6.1, 6.2, 6.3, 6.4 | ✅ Complete |
| FR8 | Confidence-Based Chat Fallback | Epic 6 | 6.1, 6.2 | ✅ Complete |
| FR9 | Discover Mode - Taste Learning | Epic 5 | 5.1 | ✅ Complete |
| FR10 | Discover Mode - Action Recommendations | Epic 5 | 5.2, 5.3, 5.4 | ✅ Complete |
| FR11 | ML Mode: Tag Mode | Epic 4 | 4.5 | ✅ Complete |
| FR12 | ML Mode: Reflection Mode | Epic 4 | 4.5 | ✅ Complete |
| FR13 | ML Mode: Novelty Mode | Epic 4 | 4.5 | ✅ Complete |
| FR14 | Knowledge Graph Structure | Epic 4 | 4.1 | ✅ Complete |
| FR15 | Streaming LLM Responses | Epic 6 | 6.2, 6.3, 6.4 | ✅ Complete |

**Total Coverage:** 15/15 Functional Requirements (100%) ✅

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

