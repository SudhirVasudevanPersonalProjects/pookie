# Story 1.3: Set Up Supabase Project and Database Schema

Status: drafted

**Epic:** 1 - Foundation & Infrastructure Setup
**Story ID:** 1.3
**Story Key:** 1-3-set-up-supabase-project-and-database-schema

## Story

As a developer,
I want to create the Supabase project and define the database schema for users, thoughts, circles, intentions, intention_cares, and stories,
so that the app has a PostgreSQL database ready for storing Circles of Care data (complete action loop: Capture → Circles → Intentions → Actions → Story).

## Acceptance Criteria

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

**And** I create initial migration `alembic/versions/001_initial_schema.py` with Circles of Care tables:

**users table:**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    vibe_profile JSONB,  -- Aggregated preference vector for Discover Mode
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_users_email ON users(email);
```

**thoughts table (captures - Level 0):**
```sql
CREATE TABLE thoughts (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    thought_text TEXT NOT NULL,
    tags TEXT[],
    reflection TEXT,
    novelty_score FLOAT,
    circle_id INTEGER REFERENCES circles(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_thoughts_user_id ON thoughts(user_id);
CREATE INDEX idx_thoughts_created_at ON thoughts(created_at);
CREATE INDEX idx_thoughts_circle_id ON thoughts(circle_id);
```

**circles table (semantic clusters - Level 1):**
```sql
CREATE TABLE circles (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    circle_name TEXT NOT NULL,
    description TEXT,
    care_frequency INTEGER DEFAULT 0,  -- Interaction count/frequency metric
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_circles_user_id ON circles(user_id);
```

**intentions table (action-oriented goals - Level 2):**
```sql
CREATE TABLE intentions (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    intention_text TEXT NOT NULL,
    status TEXT DEFAULT 'active',  -- active, completed, archived
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_intentions_user_id ON intentions(user_id);
CREATE INDEX idx_intentions_status ON intentions(status);
```

**intention_cares table (junction table for many-to-many: intentions ↔ thoughts):**
```sql
CREATE TABLE intention_cares (
    id SERIAL PRIMARY KEY,
    intention_id INTEGER NOT NULL REFERENCES intentions(id) ON DELETE CASCADE,
    thought_id INTEGER NOT NULL REFERENCES thoughts(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(intention_id, thought_id)  -- Prevent duplicate links
);
CREATE INDEX idx_intention_cares_intention_id ON intention_cares(intention_id);
CREATE INDEX idx_intention_cares_thought_id ON intention_cares(thought_id);
```

**stories table (completion log - Level 3):**
```sql
CREATE TABLE stories (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    story_text TEXT NOT NULL,  -- Description of completed action
    intention_id INTEGER REFERENCES intentions(id) ON DELETE SET NULL,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_stories_user_id ON stories(user_id);
CREATE INDEX idx_stories_intention_id ON stories(intention_id);
CREATE INDEX idx_stories_completed_at ON stories(completed_at);
```

**And** I run the migration:
```bash
poetry run alembic upgrade head
```

**And** the schema is created successfully in Supabase PostgreSQL

**And** I can verify tables exist in Supabase Table Editor

## Tasks / Subtasks

- [ ] Create Supabase account and project (AC: 1-2)
  - [ ] Navigate to https://supabase.com/dashboard
  - [ ] Sign up or log in to Supabase
  - [ ] Click "New Project"
  - [ ] Select organization (or create new one)
  - [ ] Configure project: Name="Pookie", Region=closest, Password=secure (generate strong password)
  - [ ] Select Free tier pricing plan
  - [ ] Wait for project provisioning (2-5 minutes)
  - [ ] Verify project appears in dashboard

- [ ] Collect and store Supabase credentials (AC: 3)
  - [ ] In Supabase dashboard, go to Settings > API
  - [ ] Copy "Project URL" → Save as SUPABASE_URL
  - [ ] Copy "Project API keys" > "anon public" → Save as SUPABASE_ANON_KEY
  - [ ] Copy "Project API keys" > "service_role" → Save as SUPABASE_SERVICE_KEY (CRITICAL: Server-side only!)
  - [ ] Store database password in password manager
  - [ ] Save all credentials securely (1Password, Bitwarden, etc.)

- [ ] Update iOS Config.plist with Supabase credentials
  - [ ] Open `ios/Pookie/Pookie/Resources/Config.plist` in Xcode
  - [ ] Replace "YOUR_SUPABASE_URL" with actual Supabase URL
  - [ ] Replace "YOUR_SUPABASE_ANON_KEY" with actual anon key
  - [ ] Verify file is gitignored (`git status` should NOT show it)
  - [ ] Build iOS project to verify no config errors

- [ ] Update backend .env with Supabase credentials
  - [ ] Open `backend/pookie-backend/.env`
  - [ ] Replace placeholder SUPABASE_URL with actual URL
  - [ ] Replace placeholder SUPABASE_ANON_KEY with actual anon key
  - [ ] Replace placeholder SUPABASE_SERVICE_KEY with actual service_role key
  - [ ] Verify file is gitignored (`git status` should NOT show it)

- [ ] Initialize Alembic for database migrations (AC: 4)
  - [ ] Navigate to backend: `cd backend/pookie-backend`
  - [ ] Run `poetry run alembic init alembic`
  - [ ] Verify `alembic/` directory created with:
    - `alembic/versions/` (empty initially)
    - `alembic/env.py` (migration environment)
    - `alembic.ini` (Alembic configuration)
  - [ ] Verify `alembic.ini` created in project root

- [ ] Configure Alembic to use Supabase PostgreSQL
  - [ ] Open `alembic.ini`
  - [ ] Find line: `sqlalchemy.url = driver://user:pass@localhost/dbname`
  - [ ] Replace with: `sqlalchemy.url = postgresql://postgres:PASSWORD@HOST:5432/postgres`
    - Get HOST from Supabase URL (e.g., db.xxx.supabase.co)
    - Get PASSWORD from password manager
  - [ ] Save file
  - [ ] Test connection (will verify in migration run)

- [ ] Create SQLAlchemy models for database tables
  - [ ] Create `app/models/base.py` with declarative base
  - [ ] Create `app/models/user.py` with User model
  - [ ] Create `app/models/thought.py` with Thought model
  - [ ] Create `app/models/circle.py` with Circle model
  - [ ] Update `app/models/__init__.py` to export all models

- [ ] Update Alembic env.py to import models
  - [ ] Open `alembic/env.py`
  - [ ] Add import: `from app.models import Base`
  - [ ] Set `target_metadata = Base.metadata`
  - [ ] Configure async engine if needed

- [ ] Generate initial Alembic migration (AC: 5)
  - [ ] Run: `poetry run alembic revision --autogenerate -m "Initial schema: users, thoughts, circles"`
  - [ ] Verify migration file created in `alembic/versions/`
  - [ ] Open migration file and review:
    - `upgrade()` function creates tables
    - `downgrade()` function drops tables
    - All columns, indexes, foreign keys present
  - [ ] Manually verify against AC schema requirements

- [ ] Run migration to create tables in Supabase (AC: 6)
  - [ ] Run: `poetry run alembic upgrade head`
  - [ ] Verify output shows "Running upgrade -> xxx, Initial schema"
  - [ ] Check for errors (connection issues, syntax errors)
  - [ ] Verify success message

- [ ] Verify tables exist in Supabase dashboard (AC: 7)
  - [ ] Open Supabase dashboard > Table Editor
  - [ ] Verify `users` table exists with columns: id (UUID), email, created_at, updated_at
  - [ ] Verify `thoughts` table exists with all columns from AC
  - [ ] Verify `circles` table exists with all columns from AC
  - [ ] Check indexes created (may not show in UI, but trust migration)
  - [ ] Verify foreign key relationships (thoughts.user_id → users.id, etc.)

- [ ] Test database connection from backend
  - [ ] Create test script: `app/test_db.py`
  - [ ] Test connection: Query `SELECT 1` from database
  - [ ] Test CRUD: Insert test user, select, delete
  - [ ] Verify operations succeed
  - [ ] Clean up test data

- [ ] Update iOS Supabase.swift to use real credentials
  - [ ] Open `ios/Pookie/Pookie/App/Supabase.swift`
  - [ ] Verify Config.plist loading works (add if not present)
  - [ ] Remove hardcoded placeholder values
  - [ ] Build and verify no runtime errors

- [ ] Document credentials and setup in project README
  - [ ] Add section: "Supabase Setup"
  - [ ] Document where credentials are stored
  - [ ] Add warning: NEVER commit .env or Config.plist
  - [ ] Note free tier limits (500MB database, 1GB storage)

## Dev Notes

**🔄 CIRCLES OF CARE EVOLUTION (2025-12-05):**
This story has been updated from the original "Pookie" (thought-capture app) to "Circles of Care" (attention controller). The database schema now implements the complete action loop: **Capture → Circles → Intentions → Actions → Story**.

**Key Schema Changes:**
- Renamed: `abodes` → `circles` (with `care_frequency` field)
- Added: `vibe_profile` JSONB column to `users` table
- Added: `intentions` table (Level 2 - action-oriented goals)
- Added: `intention_cares` junction table (many-to-many: intentions ↔ thoughts/captures)
- Added: `stories` table (Level 3 - completion log)

All architecture references have been updated. This schema implements the 4-level Chamber hierarchy (L0→L1→L2→L3).

### Developer Context & Guardrails

This story establishes the central database for Circles of Care - the source of truth for all user data, captures, circles, intentions, and stories. You are creating the PostgreSQL schema that will power the entire application across both iOS and backend.

**🎯 CRITICAL MISSION:** This database schema will store personal thoughts, AI-generated insights, and semantic relationships. The schema MUST be designed for both relational integrity AND vector operations (future FAISS integration). Every column, index, and foreign key constraint matters for performance and data consistency.

**Convergence Point:** Stories 1.1 (iOS) and 1.2 (Backend) both depend on this story's credentials. After completion, all three platform components (iOS, Backend, Database) will be connected and ready for feature development.

### System Requirements

**Required:**
- **Supabase Account:** Free tier (no credit card required)
- **Internet Connection:** Stable connection for Supabase dashboard access
- **Password Manager:** For storing database password and service_role key securely
- **Completed Stories:** Story 1.2 (Backend with Alembic support)

**Tools:**
- **Alembic:** Database migration tool (installed via Poetry in Story 1.2)
- **SQLAlchemy:** Python ORM for model definitions
- **psycopg2-binary:** PostgreSQL driver for Python

**Verify prerequisites:**
```bash
# Backend must be initialized (Story 1.2)
cd backend/pookie-backend
poetry run python -c "import alembic; print('Alembic ready')"

# SQLAlchemy available
poetry run python -c "import sqlalchemy; print('SQLAlchemy ready')"
```

### Supabase Free Tier Details

**What You Get (Free Forever):**
- **PostgreSQL Database:** 500MB storage
- **Database Connections:** Up to 60 concurrent connections
- **Storage:** 1GB file storage (for FAISS index files in future)
- **Bandwidth:** 2GB egress per month
- **Auth:** Unlimited users
- **API Requests:** Unlimited (with rate limits)
- **Row Level Security:** Full support

**Limits to Be Aware Of:**
- Database size: 500MB (estimated ~50,000-100,000 thoughts at 1KB avg)
- Paused after 1 week of inactivity (wakes up automatically on first request)
- No automatic backups (manual exports only)
- Shared CPU resources

**Cost Monitoring:**
- Current architecture stays within free tier
- sentence-transformers embeddings stored in FAISS (not database)
- Only text + metadata stored in PostgreSQL
- Estimated usage: <50MB for MVP scale

**Source:** [Architecture Document - Cost Management](../architecture.md#cost-estimate)

### Database Schema Deep Dive

**Schema Design Philosophy:**

This schema follows a **hybrid relational-graph model**:
- **Relational:** Standard tables with foreign keys (users, thoughts, circles)
- **Graph-ready:** Structure supports future knowledge graph layer (Epic 4)
- **ML-optimized:** Columns for embeddings metadata, novelty scores, ML-generated tags

**Table Purposes:**

**1. users table:**
- **Purpose:** User accounts, integrates with Supabase Auth
- **Key Design:** UUID primary key matches Supabase auth.users.id
- **Why UUID:** Supabase Auth uses UUID, we match for easy joins
- **Columns:**
  - `id`: UUID (matches Supabase Auth user ID)
  - `email`: User's email (for queries, indexed)
  - `created_at`, `updated_at`: Audit timestamps (UTC)

**2. thoughts table:**
- **Purpose:** Individual thought entries (atomic knowledge units)
- **Key Design:** Central to entire app, connects to everything
- **Columns:**
  - `id`: SERIAL (auto-increment integer for fast lookups)
  - `user_id`: UUID foreign key to users (CASCADE delete)
  - `thought_text`: TEXT (unlimited length, core content)
  - `tags`: TEXT[] array (ML-generated tags from Epic 4)
  - `reflection`: TEXT (ML-generated insights from Epic 4)
  - `novelty_score`: FLOAT 0-1 (importance ranking from Epic 4)
  - `circle_id`: INTEGER nullable (cluster assignment from Epic 4)
  - `created_at`, `updated_at`: Audit timestamps

**3. circles table:**
- **Purpose:** Semantic clusters of related thoughts
- **Key Design:** LLM-named thematic groups
- **Columns:**
  - `id`: SERIAL (auto-increment)
  - `user_id`: UUID foreign key to users (CASCADE delete)
  - `name`: TEXT (LLM-generated cluster name)
  - `description`: TEXT (optional cluster summary)
  - `created_at`, `updated_at`: Audit timestamps

**Foreign Key Relationships:**

```
users (1) ──< thoughts (many)
  │
  └──< circles (many)
       │
       └──< thoughts (many via circle_id)
```

**Cascade Behavior:**
- User deleted → All thoughts deleted (CASCADE)
- User deleted → All circles deleted (CASCADE)
- Circle deleted → Thoughts remain, circle_id set to NULL (SET NULL)

**Index Strategy:**

**Why these specific indexes:**
1. `idx_users_email`: Fast user lookup by email (login, queries)
2. `idx_thoughts_user_id`: Fast "get all thoughts for user" queries
3. `idx_thoughts_created_at`: Time-ordered thought retrieval (recent first)
4. `idx_thoughts_circle_id`: Fast "get all thoughts in circle" queries
5. `idx_circles_user_id`: Fast "get all circles for user" queries

**Missing intentionally:**
- No full-text search index (using FAISS vector search instead)
- No index on thought_text (too large, not queried directly)
- No index on tags/reflection (future optimization if needed)

**Future Schema Evolution (Post-MVP):**

**Epic 4 (Circles) may add:**
- `circle_embeddings` table: Store cluster centroids for similarity
- `thought_relationships` table: Explicit graph edges between thoughts

**Epic 6 (Graph RAG) may add:**
- `knowledge_graph_nodes` table: Thoughts + Circles as graph nodes
- `knowledge_graph_edges` table: Semantic similarity, temporal proximity

### Alembic Migration System

**What is Alembic:**
- Database migration tool for SQLAlchemy
- Version-controls schema changes (like Git for database)
- Generates migrations from SQLAlchemy model changes
- Supports upgrade/downgrade for schema versioning

**Alembic Directory Structure:**

```
backend/pookie-backend/
├── alembic/
│   ├── versions/
│   │   └── 001_xxxx_initial_schema.py  # Your first migration
│   ├── env.py                          # Migration environment config
│   ├── script.py.mako                  # Migration template
│   └── README
├── alembic.ini                         # Alembic configuration
└── app/
    └── models/                         # SQLAlchemy models
```

**Alembic Configuration (alembic.ini):**

**Critical setting - Database URL:**
```ini
[alembic]
sqlalchemy.url = postgresql://postgres:PASSWORD@HOST:5432/postgres
```

**How to construct URL:**
1. Get Supabase URL: `https://xxx.supabase.co`
2. Extract project ID: `xxx`
3. Database host: `db.xxx.supabase.co`
4. Database name: `postgres` (default Supabase database)
5. Username: `postgres` (default Supabase user)
6. Password: From Supabase project creation (stored in password manager)
7. Port: `5432` (PostgreSQL default)

**Full URL format:**
```
postgresql://postgres:YOUR_DB_PASSWORD@db.YOUR_PROJECT_ID.supabase.co:5432/postgres
```

**Security note:** `alembic.ini` will contain password - ensure it's gitignored OR use environment variable:
```ini
sqlalchemy.url = ${DATABASE_URL}
```
Then set `DATABASE_URL` environment variable.

**Alembic env.py Configuration:**

Must import SQLAlchemy models for autogeneration:
```python
# alembic/env.py
from app.models.base import Base  # Declarative base
from app.models import user, thought, circle  # Import all models
target_metadata = Base.metadata
```

**Why this matters:** Alembic compares current database state with `Base.metadata` to generate migrations.

**Alembic Commands:**

```bash
# Initialize Alembic (run once)
poetry run alembic init alembic

# Generate migration from model changes
poetry run alembic revision --autogenerate -m "Description"

# Apply migrations (upgrade to latest)
poetry run alembic upgrade head

# Rollback one migration
poetry run alembic downgrade -1

# Show current version
poetry run alembic current

# Show migration history
poetry run alembic history
```

### SQLAlchemy Model Implementation

**Declarative Base Pattern:**

**app/models/base.py:**
```python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
```

**app/models/user.py:**
```python
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
```

**app/models/thought.py:**
```python
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base

class Thought(Base):
    __tablename__ = "thoughts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    thought_text = Column(Text, nullable=False)
    tags = Column(ARRAY(String), nullable=True)  # PostgreSQL array type
    reflection = Column(Text, nullable=True)
    novelty_score = Column(Float, nullable=True)
    circle_id = Column(Integer, ForeignKey("circles.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships (optional, for ORM queries)
    user = relationship("User", back_populates="thoughts")
    circle = relationship("Circle", back_populates="thoughts")

    def __repr__(self):
        return f"<Thought(id={self.id}, user_id={self.user_id}, text='{self.thought_text[:30]}...')>"
```

**app/models/circle.py:**
```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base

class Circle(Base):
    __tablename__ = "circles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="circles")
    thoughts = relationship("Thought", back_populates="circle")

    def __repr__(self):
        return f"<Circle(id={self.id}, name='{self.name}')>"
```

**app/models/__init__.py:**
```python
from app.models.base import Base
from app.models.user import User
from app.models.thought import Thought
from app.models.circle import Circle

__all__ = ["Base", "User", "Thought", "Circle"]
```

**Key SQLAlchemy Patterns:**

1. **DateTime(timezone=True):** Always use timezone-aware timestamps (UTC)
2. **server_default=func.now():** Database sets timestamp (not Python)
3. **onupdate=func.now():** Auto-update updated_at on row modification
4. **ForeignKey ondelete:** Explicit cascade behavior (CASCADE or SET NULL)
5. **index=True:** Create database index on frequently queried columns
6. **ARRAY(String):** PostgreSQL-specific array type for tags

### Architecture Compliance - Database Naming

**CRITICAL:** Follow exact naming conventions from architecture.

**Tables (from Architecture):**
- ✅ Plural nouns: `users`, `thoughts`, `circles`
- ❌ NOT singular: `user`, `thought`, `circle`

**Columns:**
- ✅ snake_case: `user_id`, `thought_text`, `created_at`, `novelty_score`
- ❌ NOT camelCase: `userId`, `thoughtText`

**Foreign Keys:**
- ✅ Pattern: `{table_singular}_id`
- ✅ Examples: `user_id`, `circle_id`, `thought_id`

**Indexes:**
- ✅ Pattern: `idx_{table}_{column(s)}`
- ✅ Examples: `idx_users_email`, `idx_thoughts_user_id`, `idx_thoughts_created_at`

**Constraints:**
- ✅ Pattern: `{type}_{table}_{column}`
- ✅ Examples: `uq_users_email` (unique), `fk_thoughts_user_id` (foreign key)

**Timestamp Columns:**
- ✅ Always: `created_at`, `updated_at` (not createdAt, updatedAt)
- ✅ Type: `TIMESTAMP WITH TIME ZONE` (always UTC)
- ✅ Default: `DEFAULT NOW()` (database-side timestamp)

**Source:** [Architecture Document - Database Naming Conventions](../architecture.md#database-naming-conventions)

### Supabase Integration with Auth

**Critical Design Decision:**

The `users` table UUID primary key MUST match Supabase Auth's `auth.users.id`.

**How Supabase Auth Works:**
1. User signs up via iOS app → Supabase Auth creates record in `auth.users` table
2. `auth.users.id` is UUID generated by Supabase
3. Our `users` table mirrors this with same UUID
4. JWT token contains `user_id` claim matching this UUID

**Two-Table Pattern:**

```
Supabase Auth Schema (managed by Supabase):
┌─────────────┐
│ auth.users  │
├─────────────┤
│ id (UUID)   │ ← Generated by Supabase
│ email       │
│ ...         │
└─────────────┘

Our Public Schema (we manage):
┌─────────────┐
│ public.users│
├─────────────┤
│ id (UUID)   │ ← MUST match auth.users.id
│ email       │
│ ...         │
└─────────────┘
```

**User Creation Flow:**

**Option 1: Trigger (Recommended for production):**
```sql
-- Create trigger to auto-create public.users on auth signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.users (id, email, created_at)
  VALUES (NEW.id, NEW.email, NOW());
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();
```

**Option 2: Manual creation (Simpler for MVP):**
- Backend creates `public.users` row after successful signup
- Story 1.6 (Auth UI) will handle this

**For This Story:** Just create the schema. Story 1.6 will handle user creation logic.

### Previous Story Intelligence

**From Story 1.1 (iOS Setup):**
- ✅ Created `ios/Pookie/Pookie/Resources/Config.plist` with placeholders
- **Action:** Update Config.plist with real Supabase credentials
- **Pattern:** Load from plist at runtime (Story 1.5 implements loading)

**From Story 1.2 (Backend Setup):**
- ✅ Created `backend/pookie-backend/.env` with placeholders
- ✅ Poetry environment ready for Alembic
- **Action:** Update .env with real Supabase credentials
- **Pattern:** Use Poetry to run Alembic commands

**Credential Distribution:**

```
Supabase Credentials
├── SUPABASE_URL (public, safe to expose)
│   ├── iOS Config.plist ✅
│   └── Backend .env ✅
│
├── SUPABASE_ANON_KEY (public, safe to expose)
│   ├── iOS Config.plist ✅
│   └── Backend .env ✅
│
└── SUPABASE_SERVICE_KEY (🔥 CRITICAL: SERVER-SIDE ONLY! 🔥)
    └── Backend .env ONLY ✅
        ❌ NEVER in iOS (gives full database access)
```

**File System Consistency After This Story:**
```
/Pookie/
├── ios/Pookie/Pookie/Resources/Config.plist (updated with real credentials)
├── backend/pookie-backend/.env (updated with real credentials)
├── backend/pookie-backend/alembic/ (Alembic migration system)
│   └── versions/001_xxxx_initial_schema.py
└── backend/pookie-backend/app/models/ (SQLAlchemy models)
    ├── base.py
    ├── user.py
    ├── thought.py
    └── circle.py
```

### Troubleshooting Guide

**Issue 1: "Supabase project stuck on 'Setting up project...'"**
```
Symptom: Dashboard shows "Setting up project" for >10 minutes
Solution:
1. Wait 15 minutes (provisioning can be slow on free tier)
2. Refresh browser page
3. Check Supabase status: https://status.supabase.com
4. If still stuck after 30 min, delete project and recreate
```

**Issue 2: "Connection refused" when running Alembic**
```bash
# Error: connection to server at "db.xxx.supabase.co" failed
# Cause: Wrong database URL or Supabase project not ready

# Solution 1: Verify database URL format
postgresql://postgres:PASSWORD@db.PROJECT_ID.supabase.co:5432/postgres

# Solution 2: Test connection with psql
psql "postgresql://postgres:PASSWORD@db.PROJECT_ID.supabase.co:5432/postgres"

# Solution 3: Check Supabase project is running (not paused)
# Go to dashboard, verify project status
```

**Issue 3: "ImportError: cannot import name 'Base' from 'app.models'"**
```bash
# Cause: Models not properly structured or import order wrong

# Solution: Verify file structure
# 1. Check app/models/base.py exists with declarative_base
# 2. Check app/models/__init__.py imports Base
# 3. Verify all model files import from app.models.base

# Test import
poetry run python -c "from app.models import Base; print(Base)"
```

**Issue 4: "Target database is not up to date" when running migration**
```bash
# Error: alembic.util.exc.CommandError: Target database is not up to date

# Solution: Check current migration state
poetry run alembic current

# If shows older version, upgrade first
poetry run alembic upgrade head

# If shows no version, stamp with initial revision
poetry run alembic stamp head
```

**Issue 5: "ModuleNotFoundError: No module named 'app'" in alembic/env.py**
```python
# Cause: Alembic can't find app module

# Solution: Update alembic/env.py to add parent directory to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models import Base
```

**Issue 6: "relation 'users' already exists" on migration**
```bash
# Error: sqlalchemy.exc.ProgrammingError: (psycopg2.errors.DuplicateTable)

# Cause: Tables already exist from previous migration attempt

# Solution: Drop tables manually in Supabase SQL Editor
DROP TABLE IF EXISTS thoughts CASCADE;
DROP TABLE IF EXISTS circles CASCADE;
DROP TABLE IF EXISTS users CASCADE;

# Then re-run migration
poetry run alembic upgrade head
```

**Issue 7: "password authentication failed for user 'postgres'"**
```bash
# Cause: Wrong database password in alembic.ini

# Solution:
# 1. Retrieve correct password from password manager
# 2. Update alembic.ini with correct password
# 3. Test connection with psql first to verify password
```

**Issue 8: "Can't locate revision identified by 'xxx'"**
```bash
# Cause: Alembic version mismatch or corrupted migration history

# Solution: Reset Alembic version table
# In Supabase SQL Editor:
DELETE FROM alembic_version;

# Then stamp with current version
poetry run alembic stamp head
```

### Common Pitfalls & How to Avoid

**Pitfall 1: Exposing service_role key in iOS**
- ❌ Adding SUPABASE_SERVICE_KEY to Config.plist
- 🔥 **CRITICAL:** service_role key gives full database access, bypasses RLS
- ✅ Only add SUPABASE_URL and SUPABASE_ANON_KEY to iOS
- ✅ service_role key ONLY in backend .env

**Pitfall 2: Using wrong database host**
- ❌ Using project URL: `https://xxx.supabase.co`
- ✅ Use database host: `db.xxx.supabase.co`
- Pattern: Replace `https://` with `db.` and add `:5432/postgres`

**Pitfall 3: Forgetting to import models in alembic/env.py**
- ❌ Only importing Base without model files
- ✅ Import all model modules: `from app.models import user, thought, circle`
- Why: Alembic needs models loaded to detect schema changes

**Pitfall 4: Not using timezone-aware timestamps**
- ❌ `DateTime()` without timezone
- ✅ `DateTime(timezone=True)` for UTC timestamps
- ✅ `server_default=func.now()` for database-side default

**Pitfall 5: Wrong cascade behavior on foreign keys**
- ❌ No `ondelete` specified (defaults to RESTRICT)
- ✅ `ondelete="CASCADE"` for user_id (delete thoughts with user)
- ✅ `ondelete="SET NULL"` for circle_id (keep thoughts when circle deleted)

**Pitfall 6: Committing database credentials**
- ❌ Accidentally committing .env or Config.plist
- ✅ Verify gitignore before committing
- ✅ Run `git status` to check excluded files

**Pitfall 7: Not testing database connection before migration**
- ❌ Running `alembic upgrade head` without testing connection
- ✅ Test with psql or Python script first
- ✅ Verify Supabase project is fully provisioned

**Pitfall 8: Using singular table names**
- ❌ `__tablename__ = "user"` (singular)
- ✅ `__tablename__ = "users"` (plural)
- Follow architecture convention: always plural for tables

### Verification Checklist

**Supabase Project Setup:**
- [ ] Supabase account created
- [ ] Project "Pookie" created successfully
- [ ] Project fully provisioned (not stuck on "Setting up...")
- [ ] Can access project dashboard
- [ ] Free tier pricing plan confirmed

**Credentials Collected:**
- [ ] SUPABASE_URL saved securely
- [ ] SUPABASE_ANON_KEY saved securely
- [ ] SUPABASE_SERVICE_KEY saved securely
- [ ] Database password saved in password manager
- [ ] All credentials stored in secure password manager (1Password, Bitwarden, etc.)

**iOS Configuration:**
- [ ] `ios/Pookie/Pookie/Resources/Config.plist` updated with SUPABASE_URL
- [ ] Config.plist updated with SUPABASE_ANON_KEY
- [ ] Config.plist does NOT contain service_role key
- [ ] Config.plist is gitignored (`git status` doesn't show it)
- [ ] iOS project builds successfully with new credentials

**Backend Configuration:**
- [ ] `backend/pookie-backend/.env` updated with SUPABASE_URL
- [ ] .env updated with SUPABASE_ANON_KEY
- [ ] .env updated with SUPABASE_SERVICE_KEY
- [ ] .env is gitignored (`git status` doesn't show it)

**Alembic Setup:**
- [ ] `poetry run alembic init alembic` completed
- [ ] `alembic/` directory created
- [ ] `alembic.ini` exists with database URL configured
- [ ] `alembic/env.py` imports Base and all models
- [ ] Database URL in alembic.ini uses correct host (`db.xxx.supabase.co`)

**SQLAlchemy Models:**
- [ ] `app/models/base.py` created with declarative_base
- [ ] `app/models/user.py` created with User model
- [ ] `app/models/thought.py` created with Thought model
- [ ] `app/models/circle.py` created with Circle model
- [ ] `app/models/__init__.py` exports all models
- [ ] All models use correct naming (snake_case, plural tables)

**Migration Execution:**
- [ ] `poetry run alembic revision --autogenerate -m "Initial schema"` successful
- [ ] Migration file created in `alembic/versions/`
- [ ] Migration file reviewed for correctness
- [ ] `poetry run alembic upgrade head` successful
- [ ] No errors during migration execution

**Database Verification:**
- [ ] Supabase Table Editor shows `users` table
- [ ] Supabase Table Editor shows `thoughts` table
- [ ] Supabase Table Editor shows `circles` table
- [ ] All columns present in each table
- [ ] Foreign key relationships visible
- [ ] Can manually insert test data via SQL Editor

**Git Security:**
- [ ] .env NOT in git (`git status` doesn't show it)
- [ ] Config.plist NOT in git (`git status` doesn't show it)
- [ ] alembic.ini NOT committed (if contains password)
- [ ] Only migration files and models committed

### Architecture Alignment & Dependencies

**This story implements:**
- Database Schema Management (architecture.md lines 579-591)
- Database Naming Conventions (architecture.md lines 857-876)
- Authentication & Security: JWT integration (architecture.md lines 593-615)
- Data Architecture patterns (architecture.md lines 577-591)

**Architectural Patterns Followed:**
1. ✅ SQLAlchemy ORM + Alembic migrations
2. ✅ PostgreSQL with snake_case naming
3. ✅ Foreign key cascade behaviors (CASCADE, SET NULL)
4. ✅ Index patterns (idx_{table}_{column})
5. ✅ Timezone-aware timestamps (UTC)
6. ✅ UUID for users (Supabase Auth integration)

**Future Dependencies:**

**Story 1.4 (JWT Middleware) depends on this:**
- Database schema must exist for user authentication
- Users table required for JWT user_id validation
- Supabase credentials in backend .env

**Story 1.5 (iOS AppState) depends on this:**
- Supabase credentials in Config.plist
- Auth SDK needs valid project URL and anon key

**Story 1.6 (Auth UI) depends on this:**
- Users table for account creation
- Database ready for first user signup

**Epic 2 (Thought Capture) depends on this:**
- Thoughts table schema defined
- Backend can insert thoughts via ORM
- Database ready for embeddings metadata

**Epic 4 (Circles) depends on this:**
- Circles table schema defined
- Foreign key relationship to thoughts
- Ready for clustering algorithm

**No conflicts:** This story bridges iOS and Backend - both depend on credentials created here.

### References

**Critical Reference Sections:**

1. **Architecture: Database Schema Management** (architecture.md lines 579-591)
   - SQLAlchemy ORM + Alembic pattern
   - Migration workflow
   - Schema versioning

2. **Architecture: Database Naming Conventions** (architecture.md lines 857-876)
   - Tables: Plural nouns
   - Columns: snake_case
   - Foreign keys: {table_singular}_id
   - Indexes: idx_{table}_{column}

3. **Architecture: Authentication & Security** (architecture.md lines 593-615)
   - Supabase JWT validation pattern
   - service_role vs anon key usage
   - User table integration with auth.users

4. **Architecture: Data Flow** (architecture.md lines 586-591)
   - iOS → FastAPI → Supabase PostgreSQL
   - Supabase Storage for FAISS index

5. **Epic 1 Story 1.3** (epics.md lines 436-525)
   - Acceptance criteria source
   - Schema SQL definitions
   - Prerequisites

6. **Supabase Documentation:**
   - Getting Started: https://supabase.com/docs/guides/getting-started
   - Database Schema: https://supabase.com/docs/guides/database
   - Auth Integration: https://supabase.com/docs/guides/auth

7. **Alembic Documentation:**
   - Tutorial: https://alembic.sqlalchemy.org/en/latest/tutorial.html
   - Autogenerate: https://alembic.sqlalchemy.org/en/latest/autogenerate.html

8. **SQLAlchemy Documentation:**
   - ORM Quickstart: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
   - Column Types: https://docs.sqlalchemy.org/en/20/core/types.html

**Skip:** Architecture sections on ML pipeline, iOS state management, API endpoints - not relevant to this story.

### Project Context Reference

See project-level context for:
- Overall Pookie architecture (dual-platform iOS + Python)
- Free-tier cost constraints (~$0-3/month)
- Database scale assumptions (500MB limit, ~50k-100k thoughts)
- Future schema evolution (graph RAG, knowledge graph)

This database will eventually store:
- Epic 2: Captured thoughts with embeddings metadata
- Epic 3: AI-separated thoughts (LLM-processed)
- Epic 4: Semantic clusters (circles) with ML tags/reflections
- Epic 5: User taste profile data (implicit in thoughts)
- Epic 6: RAG chat history (future enhancement)

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

**Expected files to be created/modified:**
- Supabase Project (cloud - not local files)
- `ios/Pookie/Pookie/Resources/Config.plist` (modified - real credentials)
- `backend/pookie-backend/.env` (modified - real credentials)
- `backend/pookie-backend/alembic.ini` (created)
- `backend/pookie-backend/alembic/` (directory created)
- `backend/pookie-backend/alembic/versions/001_*.py` (migration file)
- `backend/pookie-backend/app/models/base.py` (created)
- `backend/pookie-backend/app/models/user.py` (created)
- `backend/pookie-backend/app/models/thought.py` (created)
- `backend/pookie-backend/app/models/circle.py` (created)
- `backend/pookie-backend/app/models/__init__.py` (modified)

---

**Status:** ready-for-dev

**Ultimate Story Context Complete:** This story provides comprehensive developer guidance for setting up Supabase, defining the database schema with Alembic migrations, and integrating SQLAlchemy ORM models. All critical decisions, security patterns, migration workflows, and architecture alignments have been documented to ensure flawless implementation.

