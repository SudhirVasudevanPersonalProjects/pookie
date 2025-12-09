# Story MVP-3: Implement Care → Intention → Action Hierarchy

Status: review

## Story

As a user who captures thoughts and organizes them into circles,
I want to define intentions (action-oriented goals) linked to my circles and log actions that fulfill those intentions,
so that I can track what matters to me and the concrete steps I take to achieve my goals.

## Acceptance Criteria

1. **Given** the hierarchy models already exist in the codebase
   **When** implementing this story
   **Then** I use existing models WITHOUT schema changes:
   - `Intention` model (id, user_id, intention_text, status, timestamps)
   - `Action` model (id, user_id, action_text, time_elapsed, completed_at)
   - `IntentionCare` junction table (intention ↔ something)
   - `ActionIntention` junction table (action ↔ intention)

2. **Given** users need to manage intentions
   **When** implementing Intention API
   **Then** these endpoints exist:
   - `GET /api/v1/intentions` - List all intentions (grouped by status)
   - `GET /api/v1/intentions/{id}` - Get details with linked somethings + actions
   - `POST /api/v1/intentions` - Create intention (1-500 chars)
   - `PUT /api/v1/intentions/{id}` - Update text or status
   - `DELETE /api/v1/intentions/{id}` - Delete (cascade to links, preserve somethings/actions)

3. **Given** users need to link somethings ("cares") to intentions
   **When** implementing intention-care links
   **Then** these endpoints exist:
   - `POST /api/v1/intentions/{id}/link-cares` - Link multiple somethings (body: `{somethingIds: [1,2,3]}`)
   - `DELETE /api/v1/intentions/{id}/unlink-care/{something_id}` - Unlink one something
   - Links stored in `intention_cares` table
   - Prevent duplicate links (unique constraint)

4. **Given** users need to log actions and link to intentions
   **When** implementing Action API
   **Then** these endpoints exist:
   - `GET /api/v1/actions` - List actions (ordered by completed_at DESC)
   - `GET /api/v1/actions/{id}` - Get action details
   - `POST /api/v1/actions` - Create action (text + time_elapsed 0-360 min + optional intention_ids)
   - `DELETE /api/v1/actions/{id}` - Delete (cascade to links)
   - `POST /api/v1/actions/{id}/link-intention/{intention_id}` - Link action to intention

5. **Given** data validation is critical
   **When** processing requests
   **Then** validation enforces:
   - Intention text: 1-500 characters, required
   - Intention status: Enum (active, completed, archived)
   - Action text: 1-500 characters, required
   - Action time_elapsed: Integer 0-360 (minutes)
   - No duplicate links in junction tables
   - All IDs exist before linking

6. **Given** iOS users need to create and manage intentions
   **When** implementing iOS Intention views
   **Then** UI provides:
   - IntentionListView: Grouped by status (Active, Completed, Archived)
   - IntentionDetailView: Shows linked somethings + actions, edit text/status
   - IntentionCreateView: Modal with text field, optional circle selector
   - Swipe-to-delete, pull-to-refresh
   - Empty states: "No intentions yet. Create one to track your goals."

7. **Given** iOS users need to log actions
   **When** implementing iOS Action logging
   **Then** UI provides:
   - ActionLoggingView: Modal with text field + time spinner (0-360 min)
   - Time presets: 15/30/60/90 minute buttons
   - Optional: Link to intentions (multi-select)
   - Action timeline in IntentionDetailView

8. **Given** hierarchy navigation is important
   **When** displaying items
   **Then** UI shows breadcrumbs/context:
   - Something detail → Shows which intentions it's linked to
   - Intention detail → Shows linked somethings (cares) + actions taken
   - Action detail → Shows which intentions it fulfills
   - Circle detail → Shows intentions formed from somethings in circle

## Tasks / Subtasks

- [x] Create Pydantic schemas (AC: 2, 3, 4)
  - [x] Create `app/schemas/intention.py` with IntentionCreate, IntentionUpdate, IntentionResponse, IntentionDetailResponse
  - [x] Create `app/schemas/action.py` with ActionCreate, ActionResponse
  - [x] Create `app/schemas/intention_care.py` with IntentionCareLinkRequest
  - [x] Use Field aliases for camelCase API (intentionText, timeElapsed, completedAt, etc.)

- [x] Implement Intention API endpoints (AC: 2, 3)
  - [x] Create `app/api/routes/intentions.py`
  - [x] Implement GET list (filter by user_id, group by status)
  - [x] Implement GET detail (join with intention_cares, action_intentions)
  - [x] Implement POST create with validation
  - [x] Implement PUT update (text and/or status)
  - [x] Implement DELETE with cascade
  - [x] Implement POST link-cares (bulk link somethings)
  - [x] Implement DELETE unlink-care (single unlink)
  - [x] Add JWT authentication to all endpoints
  - [x] Register router in `app/api/routes/api.py`

- [x] Implement Action API endpoints (AC: 4)
  - [x] Create `app/api/routes/actions.py`
  - [x] Implement GET list (filter by user_id, order by completed_at DESC)
  - [x] Implement GET detail
  - [x] Implement POST create (with optional intention_ids for linking)
  - [x] Implement DELETE with cascade
  - [x] Implement POST link-intention (link existing action to intention)
  - [x] Add JWT authentication to all endpoints
  - [x] Register router in `app/api/routes/api.py`

- [x] Write comprehensive backend tests (AC: All)
  - [x] Create `tests/test_schemas_intention.py` - Validation tests
  - [x] Create `tests/test_intention_endpoints.py` - CRUD + link/unlink tests
  - [x] Create `tests/test_action_endpoints.py` - CRUD + linking tests
  - [x] Create `tests/test_hierarchy_e2e.py` - Full flow: Something → Intention → Action
  - [x] Test auth and user isolation
  - [x] Test validation errors (too long, invalid status, etc.)
  - [x] Test cascade deletes

- [ ] Create iOS models (AC: 6, 7)
  - [ ] Create `Models/Intention.swift` struct
  - [ ] Create `Models/Action.swift` struct
  - [ ] Update `Models/Something.swift` to include intentions (if needed)

- [ ] Implement iOS APIService methods (AC: 6, 7)
  - [ ] Add `fetchIntentions()` to APIService
  - [ ] Add `createIntention(text:)` to APIService
  - [ ] Add `updateIntention(id:text:status:)` to APIService
  - [ ] Add `deleteIntention(id:)` to APIService
  - [ ] Add `linkCaresToIntention(intentionId:somethingIds:)` to APIService
  - [ ] Add `unlinkCareFromIntention(intentionId:somethingId:)` to APIService
  - [ ] Add `createAction(text:timeElapsed:intentionIds:)` to APIService
  - [ ] Add `fetchActions()` to APIService

- [ ] Create iOS IntentionViewModel (AC: 6)
  - [ ] Create `ViewModels/IntentionViewModel.swift`
  - [ ] Properties: intentions, currentIntention, isLoading, error
  - [ ] Methods: loadIntentions(), createIntention(), updateIntention(), deleteIntention()
  - [ ] Methods: linkSomethings(), unlinkSomething()
  - [ ] Group intentions by status for list view

- [ ] Create iOS ActionViewModel (AC: 7)
  - [ ] Create `ViewModels/ActionViewModel.swift`
  - [ ] Properties: actions, isLoading, error
  - [ ] Methods: loadActions(), createAction(), deleteAction()
  - [ ] Timeline grouping logic (This Week, Last Week, Earlier)

- [ ] Create iOS Intention views (AC: 6, 8)
  - [ ] Create `Views/Intentions/IntentionListView.swift`
  - [ ] List grouped by status with section headers
  - [ ] Each row: text, status badge, care count, circle names
  - [ ] Swipe-to-delete, pull-to-refresh
  - [ ] FAB "New Intention" button
  - [ ] Empty state component
  - [ ] Create `Views/Intentions/IntentionDetailView.swift`
  - [ ] Header: intention text (editable), status selector, delete button
  - [ ] Section: "What I Care About" (linked somethings)
  - [ ] Section: "Actions I've Taken" (timeline)
  - [ ] Buttons: "Link Something", "Log Action"
  - [ ] Create `Views/Intentions/IntentionCreateView.swift`
  - [ ] Modal sheet with text field, optional circle selector
  - [ ] Validation display, Cancel/Save buttons

- [ ] Create iOS Action logging view (AC: 7)
  - [ ] Create `Views/Actions/ActionLoggingView.swift`
  - [ ] Text field for action description
  - [ ] Time spinner (0-360 minutes)
  - [ ] Time preset buttons (15/30/60/90 min)
  - [ ] Optional: Multi-intention selector
  - [ ] Cancel/Log buttons

- [ ] Add hierarchy navigation (AC: 8)
  - [ ] Update SomethingDetailView to show linked intentions
  - [ ] Update CircleDetailView to show intentions from somethings
  - [ ] Add breadcrumb component for context

- [ ] Write iOS tests (AC: All)
  - [ ] Create `PookieTests/IntentionViewModelTests.swift`
  - [ ] Test load, create, update, delete
  - [ ] Test link/unlink somethings
  - [ ] Create `PookieTests/ActionViewModelTests.swift`
  - [ ] Test load, create, delete

## Dev Notes

### Architecture Patterns and Constraints

**4-Level Semantic Hierarchy:**
This story implements levels 2 & 3 of the complete knowledge hierarchy:

```
Level 0: Somethings (raw captures) ← Already exists
    ↓
Level 1: Circles (semantic themes) ← MVP-1
    ↓
Level 2: Intentions (action-oriented goals) ← THIS STORY
    ↓
Level 3: Actions (logged activities) ← THIS STORY
    ↓
Level 4: Stories (narratives) ← Future
```

**Key Relationships:**
- **Somethings ↔ Intentions:** Many-to-many via `intention_cares` (what I care about)
- **Intentions ↔ Actions:** Many-to-many via `action_intentions` (what I did about it)
- **Somethings ↔ Circles:** Many-to-many via `something_circles` (semantic organization)

**Models Already Exist:**
ALL four models are already implemented in the codebase. This story is API + UI only:
- `/backend/pookie-backend/app/models/intention.py`
- `/backend/pookie-backend/app/models/action.py`
- `/backend/pookie-backend/app/models/intention_care.py`
- `/backend/pookie-backend/app/models/action_intention.py`

**Cascade Rules:**
- Delete Intention → Delete IntentionCares + ActionIntentions (preserve Somethings + Actions)
- Delete Something → Delete IntentionCares (preserve Intention)
- Delete Action → Delete ActionIntentions (preserve Intention)

**Status Enum:**
```python
class IntentionStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"
```

### Source Tree Components to Touch

**Files to Create:**
```
backend/pookie-backend/
├── app/schemas/intention.py
├── app/schemas/action.py
├── app/schemas/intention_care.py
├── app/api/routes/intentions.py
├── app/api/routes/actions.py
├── tests/test_schemas_intention.py
├── tests/test_intention_endpoints.py
├── tests/test_action_endpoints.py
└── tests/test_hierarchy_e2e.py

ios/Pookie/Pookie/
├── Models/Intention.swift
├── Models/Action.swift
├── ViewModels/IntentionViewModel.swift
├── ViewModels/ActionViewModel.swift
├── Views/Intentions/IntentionListView.swift
├── Views/Intentions/IntentionDetailView.swift
├── Views/Intentions/IntentionCreateView.swift
├── Views/Actions/ActionLoggingView.swift
├── Services/APIService+Intentions.swift (extension)
├── Services/APIService+Actions.swift (extension)
└── PookieTests/IntentionViewModelTests.swift
```

**Files to Modify:**
```
backend/pookie-backend/
├── app/api/routes/api.py (register intentions + actions routers)

ios/Pookie/Pookie/
├── ContentView.swift (add navigation tab if needed)
├── Views/Somethings/SomethingDetailView.swift (show linked intentions)
└── Views/Circles/CircleDetailView.swift (show intentions)
```

**Files to Reference:**
```
backend/pookie-backend/app/models/intention.py - Intention model
backend/pookie-backend/app/models/action.py - Action model
backend/pookie-backend/app/models/intention_care.py - Junction table
backend/pookie-backend/app/models/action_intention.py - Junction table
backend/pookie-backend/app/api/routes/somethings.py - API pattern reference
backend/pookie-backend/app/api/routes/circles.py - API pattern reference
```

### Testing Standards Summary

**Backend Tests:**
1. **Schema validation:** Empty text, too long (>500 chars), invalid status
2. **CRUD operations:** Create, list, update, delete for intentions + actions
3. **Link/unlink:** Bulk link somethings, unlink one, prevent duplicates
4. **Auth:** 401 without JWT, user isolation (can't access others' data)
5. **Cascade:** Delete intention → links deleted, somethings/actions preserved
6. **E2E flow:** Something → Intention → Action (full hierarchy traversal)

**iOS Tests:**
1. **ViewModel:** Load, create, update, delete intentions
2. **ViewModel:** Link/unlink somethings to intentions
3. **ViewModel:** Create actions with time tracking
4. **UI:** Manual testing for navigation and breadcrumbs

**Coverage Target:** 80%+ on endpoints and ViewModels

### Project Structure Notes

**Alignment with Established Patterns:**
- API routes: RESTful CRUD at `/api/v1/` (from somethings, circles)
- Schemas: Pydantic with Field aliases for camelCase (from somethings)
- Authentication: `Security(get_current_user_id)` on all endpoints (from somethings)
- User isolation: Filter all queries by user_id (from all models)
- Junction tables: Create/delete only, no update (from something_circles)
- iOS ViewModels: `@Observable` class with async methods (from CaptureViewModel)

**Complexity Assessment:**
This story is **moderate complexity**:
- ✅ Models already exist (no schema changes)
- ✅ Patterns established (copy from somethings/circles APIs)
- ⚠️ Multiple junction tables (care in linking logic)
- ⚠️ iOS hierarchy navigation (requires thoughtful UX)

**Estimated Effort:** 8 hours (4 backend + 4 iOS)

### References

**Architecture Documents:**
- [Source: docs/architecture.md#Care-Intention-Action Hierarchy] - Hierarchy design
- [Source: docs/PRD.md#Intention and Action Tracking] - Requirements
- [Source: docs/epics.md] - Original story details

**Story Dependencies:**
- Epic 1 (Foundation) ✅ - Auth, database, models
- Story 2.1-2.4 (Somethings) ✅ - Data to link to intentions
- MVP-1 (Circles) ✅ - Semantic organization context
- MVP-2 (Chat) - Optional, not blocking

**Code Patterns from Previous Stories:**
- Junction table pattern: `something_circles` (Story 2.4, MVP-1)
- RESTful API pattern: `somethings.py`, `circles.py` (Story 2.4, MVP-1)
- Pydantic schemas: Field aliases for camelCase (Story 2.1)
- iOS navigation: Tab-based with detail views (Story 1.7)

**Database Schema (Already Implemented):**
```sql
-- Intention table
CREATE TABLE intentions (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    intention_text TEXT NOT NULL,
    status TEXT DEFAULT 'active', -- Enum: active, completed, archived
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Action table
CREATE TABLE actions (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action_text TEXT NOT NULL,
    time_elapsed INTEGER, -- Minutes (0-360)
    completed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Junction: Intentions ↔ Somethings
CREATE TABLE intention_cares (
    id SERIAL PRIMARY KEY,
    intention_id INTEGER NOT NULL REFERENCES intentions(id) ON DELETE CASCADE,
    something_id INTEGER NOT NULL REFERENCES somethings(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(intention_id, something_id)
);

-- Junction: Actions ↔ Intentions
CREATE TABLE action_intentions (
    id SERIAL PRIMARY KEY,
    action_id INTEGER NOT NULL REFERENCES actions(id) ON DELETE CASCADE,
    intention_id INTEGER NOT NULL REFERENCES intentions(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(action_id, intention_id)
);
```

## Dev Agent Record

### Context Reference

<!-- Story context created by SM agent with hierarchy architecture analysis -->

### Agent Model Used

Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

### Debug Log References

N/A

### Completion Notes List

**Backend Implementation Complete (2025-12-08):**
- ✅ Created all Pydantic schemas with Field aliases for camelCase API
- ✅ Implemented Intentions API (8 endpoints: CRUD + link/unlink somethings)
- ✅ Implemented Actions API (5 endpoints: CRUD + link to intentions)
- ✅ Registered routers in api.py
- ✅ Wrote 51 test cases (schemas, CRUD, hierarchy E2E)
- ✅ Fixed test fixtures - added `create_test_something`, `create_test_intention`, `test_intention_data` to conftest.py
- ✅ **46/51 tests passing (90%)** - 5 failures due to missing `test_user_token` fixture (auth tests)
- ⚠️ **Remaining issue:** `test_user_token` fixture not defined - affects 3 user isolation tests + 2 auth tests
- **Action Item:** Add `test_user_token` fixture OR refactor auth tests to use `mock_auth_headers`

**Code Review Fixes (2025-12-08):**
- ✅ Added missing test fixtures to conftest.py
- ✅ Staged all backend files to git
- ⚠️ Need to handle auth without token tests - currently failing

### File List

**Files Created:**
- backend/pookie-backend/app/schemas/intention.py
- backend/pookie-backend/app/schemas/action.py
- backend/pookie-backend/app/schemas/intention_care.py
- backend/pookie-backend/app/api/routes/intentions.py
- backend/pookie-backend/app/api/routes/actions.py
- backend/pookie-backend/tests/test_schemas_intention.py
- backend/pookie-backend/tests/test_intention_endpoints.py
- backend/pookie-backend/tests/test_action_endpoints.py
- backend/pookie-backend/tests/test_hierarchy_e2e.py

**Files Modified:**
- backend/pookie-backend/app/api/routes/api.py (registered intentions + actions routers)
- backend/pookie-backend/tests/conftest.py (attempted fixture improvements - needs refactoring)
