# Story 1.1: Initialize iOS Project with Supabase Swift SDK

Status: ready-for-dev

**Epic:** 1 - Foundation & Infrastructure Setup
**Story ID:** 1.1
**Story Key:** 1-1-initialize-ios-project-with-supabase-swift-sdk

## Story

As a developer,
I want to set up the iOS Xcode project with Supabase Swift SDK integrated,
so that I have the foundation for building the SwiftUI app with authentication capabilities.

## Acceptance Criteria

**Given** I need to start the iOS project
**When** I create a new Xcode project in the existing `ios/` directory
**Then** the project is configured as follows:
- Project Location: `/path/to/Pookie/ios/` (creates `ios/Pookie/` subdirectory)
- Product Name: "Pookie"
- Interface: SwiftUI
- Life Cycle: SwiftUI App
- Language: Swift
- Minimum iOS version: iOS 17.0 (for @Observable support)

**And** I add Supabase Swift SDK via Swift Package Manager:
- Package URL: `https://github.com/supabase/supabase-swift`
- Version Rule: "Up to Next Major Version" starting from "2.0.0"
- Package products added: Supabase, Auth, PostgREST, Storage (NOT Realtime or Functions)

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

## Tasks / Subtasks

- [ ] Verify system requirements
  - [ ] macOS Sonoma 14.0+ installed
  - [ ] Xcode 15.0+ installed (run `xcodebuild -version` to verify)
  - [ ] Minimum 10GB free disk space

- [ ] Create new Xcode iOS project (AC: 1)
  - [ ] Open Xcode > File > New > Project > iOS > App
  - [ ] Save location: Navigate to existing `/path/to/Pookie/ios/` directory
  - [ ] Product Name: "Pookie"
  - [ ] Interface: SwiftUI
  - [ ] Life Cycle: SwiftUI App
  - [ ] Language: Swift
  - [ ] Verify project created at `ios/Pookie/Pookie.xcodeproj`

- [ ] Configure minimum iOS deployment target
  - [ ] Select "Pookie" project (top level in navigator)
  - [ ] Select "Pookie" target (under TARGETS)
  - [ ] General tab > Deployment Info > Minimum Deployments: Set to "iOS 17.0"
  - [ ] Verify Build Settings > IPHONEOS_DEPLOYMENT_TARGET = 17.0

- [ ] Add Supabase Swift SDK via Swift Package Manager (AC: 2)
  - [ ] File > Add Package Dependencies in Xcode
  - [ ] Add package URL: `https://github.com/supabase/supabase-swift`
  - [ ] Dependency Rule: Select "Up to Next Major Version"
  - [ ] Version: Enter "2.0.0"
  - [ ] Add package products: Supabase, Auth, PostgREST, Storage (do NOT add Realtime or Functions)
  - [ ] Verify products linked to "Pookie" target (not test target)

- [ ] Verify Swift Package installation
  - [ ] In project navigator, expand "Package Dependencies"
  - [ ] Expand "supabase-swift" and verify version shows 2.x.x
  - [ ] Build Phases > Link Binary With Libraries: Verify all 4 products appear
  - [ ] Check Package.resolved file exists and shows correct version

- [ ] Create project folder structure (AC: 3)
  - [ ] In Finder, navigate to `ios/Pookie/Pookie/`
  - [ ] Create directories: App/, Resources/, Models/, ViewModels/, Views/, Services/
  - [ ] In Xcode, right-click "Pookie" group > Add Files to "Pookie"
  - [ ] Select each folder, check "Create groups" (NOT "Create folder references")
  - [ ] Verify Xcode navigator structure matches filesystem

- [ ] Create Supabase client initialization file (AC: 3)
  - [ ] Right-click App/ group > New File > Swift File
  - [ ] Name: Supabase.swift
  - [ ] Add content: `import Supabase` and SupabaseClient initialization
  - [ ] Add TODO comment: `// TODO: Load from Config.plist in Story 1.5`

- [ ] Create configuration file for secrets (AC: 4)
  - [ ] Right-click Resources/ folder > New File > Property List
  - [ ] Name: Config.plist
  - [ ] Add keys: SupabaseURL (String), SupabaseAnonKey (String)
  - [ ] Add placeholder values with TODO comment
  - [ ] Verify file appears in Resources/ folder

- [ ] Configure .gitignore (AC: 5)
  - [ ] Update existing root `.gitignore` at `/path/to/Pookie/.gitignore`
  - [ ] Add iOS-specific patterns including `**/Config.plist`
  - [ ] Run `git status` and verify Config.plist does NOT appear

- [ ] Verify build (AC: 6)
  - [ ] Select target: "Pookie" (not test targets)
  - [ ] Select destination: "iPhone 15 Pro Simulator" or "Any iOS Device (arm64)"
  - [ ] Press Cmd+B (Product > Build)
  - [ ] Verify build succeeds (green checkmark)
  - [ ] Verify zero errors and zero Supabase-related warnings
  - [ ] Check build log shows "Build Succeeded"

## Dev Notes

### Developer Context & Guardrails

This story establishes the iOS foundation for Pookie. You are creating the first building block that ALL subsequent iOS stories depend on. Follow the architecture patterns exactly to ensure consistency across the entire project.

**Parallel Execution Note:** This story (iOS setup) can run in parallel with Story 1.2 (Backend setup). Both are independent until Story 1.3 (Supabase setup). If context-switching, start both stories simultaneously.

### System Requirements

Before starting, verify your development environment:

**Required:**
- macOS Sonoma 14.0+ (for Xcode 15+)
- Xcode 15.0 or later (required for iOS 17.0 and Swift 5.9)
- Minimum 10GB free disk space (for Xcode + Swift Package Manager dependencies)

**Verify Xcode version:**
```bash
xcodebuild -version
# Should show: Xcode 15.x or later
```

**Critical:** iOS 17.0 and @Observable will NOT work on Xcode 14.x or earlier.

### Project Location & Structure

**Where to Create the Xcode Project:**

The repository already has an `ios/` directory. Create the Xcode project INSIDE this directory:

1. Open Xcode
2. File > New > Project > iOS > App
3. **Save location:** Navigate to `/path/to/Pookie/ios/`
4. **Project name:** "Pookie"
5. **Result:** Creates `/path/to/Pookie/ios/Pookie/` with `Pookie.xcodeproj`

**Verification after creation:**
```
/Pookie/                      # Git repository root
├── ios/                      # iOS platform directory
│   └── Pookie/              # Xcode project folder (created by you)
│       ├── Pookie.xcodeproj
│       ├── Pookie/          # Source code folder
│       │   ├── App/
│       │   ├── Resources/
│       │   └── ...
```

**Do NOT** create the project in `/Pookie/` root or you'll mix iOS and backend files.

### Technical Requirements

**Xcode Project Configuration:**
- **Product Name:** Must be exactly "Pookie"
- **Interface:** SwiftUI (no UIKit, no hybrid approach)
- **Life Cycle:** SwiftUI App (NOT UIKit App Delegate)
- **Language:** Swift only (no Objective-C bridging)
- **Minimum Deployment Target:** iOS 17.0
  - **Critical:** iOS 17+ is REQUIRED for @Observable macro (used in Story 1.5)
  - Requires `import Observation` in files using @Observable
  - Do NOT use older iOS versions or state management will break

**iOS Deployment Target Configuration:**
1. In Xcode project navigator, select "Pookie" project (top level)
2. Select "Pookie" target (under TARGETS)
3. General tab > Deployment Info > Minimum Deployments: Set to "iOS 17.0"
4. **Verify both:** Project AND Target deployment targets are both set to 17.0
5. Confirm in Build Settings: IPHONEOS_DEPLOYMENT_TARGET = 17.0

**Common mistake:** Setting Project deployment target but forgetting Target. Verify BOTH.

**Supabase Swift SDK Integration:**
- **Package URL:** `https://github.com/supabase/supabase-swift`
- **Version:** 2.x.x (see architecture.md lines 310-428 for version details)
- **Package Products to Add:** Supabase, Auth, PostgREST, Storage
- **Do NOT add:** Realtime, Functions (not needed for MVP)

**Swift Package Manager Version Selection:**

In Xcode's "Add Package" dialog:
1. **Dependency Rule:** Select "Up to Next Major Version"
2. **Version:** Enter "2.0.0"
3. This automatically pulls latest 2.x.y patches while avoiding breaking changes in 3.0+

**Package Product Verification:**

After adding the package:
1. In Xcode project navigator, expand "Package Dependencies" > "supabase-swift"
2. Verify these products are checked:
   - ✅ Supabase
   - ✅ Auth
   - ✅ PostgREST
   - ✅ Storage
   - ❌ Realtime (NOT needed)
   - ❌ Functions (NOT needed)
3. In Build Phases > Link Binary With Libraries: Verify all 4 products appear
4. Verify they're linked to "Pookie" target (not test target)

**If products are missing:**
1. Select "Pookie" target > General tab > Frameworks, Libraries, and Embedded Content
2. Click "+" > Add Other > Add Package Product
3. Select missing products

**Troubleshooting: Swift Package Manager Issues**

**Issue: "Failed to resolve package dependencies"**
- Solution: File > Packages > Reset Package Caches, restart Xcode, try again

**Issue: "Repository not found"**
- Solution: Verify URL is exactly `https://github.com/supabase/supabase-swift`

**Issue: "Package product 'Supabase' not found"**
- Solution: Verify version is 2.x.x (not 1.x), use "Up to Next Major Version" from "2.0.0"

**Last resort:**
1. Delete Package Dependencies from project navigator
2. File > Packages > Reset Package Caches
3. Restart Mac and re-add package

### Folder Creation (File System + Xcode Groups)

**Critical:** Create BOTH file system folders AND Xcode groups to keep them in sync.

**Method 1 (Recommended - Creates both):**
1. In Finder, navigate to `ios/Pookie/Pookie/`
2. Create actual directories: `App/`, `Resources/`, `Models/`, `ViewModels/`, `Views/`, `Services/`
3. In Xcode, right-click "Pookie" group > Add Files to "Pookie"
4. Select each folder, check "Create groups" (NOT "Create folder references")

**Method 2 (Xcode only):**
1. Right-click "Pookie" group > New Group
2. Name the group (e.g., "App")
3. Right-click the group > Show in Finder
4. Verify actual directory exists on disk

**Verification:**
- Xcode navigator shows folder structure
- Finder shows matching directories
- **Common mistake:** Creating Xcode groups without file system folders causes files to scatter in root directory

**Final folder structure:**
```
Pookie/
├── App/              # App initialization and shared singletons
├── Models/           # Data models (Thought, Abode, User)
├── ViewModels/       # MVVM ViewModels with @Observable
├── Views/            # SwiftUI views
├── Services/         # API, Auth, Sync services
└── Resources/        # Assets, Config.plist
```

### Required Implementation Files

**1. App/Supabase.swift**

Create this file with exactly this content:
```swift
import Supabase

// Global Supabase client
// TODO: Load URL and key from Config.plist in Story 1.5
let supabase = SupabaseClient(
    supabaseURL: URL(string: "YOUR_SUPABASE_URL")!,
    supabaseKey: "YOUR_SUPABASE_ANON_KEY"
)
```

- **Location:** App/ folder (app-level singletons)
- **Purpose:** Global Supabase client instance
- **Future:** Story 1.5 will refactor to load from Config.plist
- **Pattern:** Global singleton for easy access throughout app (matches Supabase official docs)

**Config.plist Loading Pattern (Story 1.5 will implement):**
```swift
// Future implementation reference
func loadConfig() -> (url: String, key: String) {
    guard let path = Bundle.main.path(forResource: "Config", ofType: "plist"),
          let config = NSDictionary(contentsOfFile: path),
          let url = config["SupabaseURL"] as? String,
          let key = config["SupabaseAnonKey"] as? String else {
        fatalError("Config.plist not found or invalid")
    }
    return (url, key)
}
```

**2. Resources/Config.plist**

Complete XML template (copy-paste this):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>SupabaseURL</key>
    <string>https://YOUR_PROJECT_ID.supabase.co</string>
    <key>SupabaseAnonKey</key>
    <string>eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.YOUR_ANON_KEY_HERE</string>
    <!-- TODO: Replace with actual values from Story 1.3 (Supabase setup) -->
</dict>
</plist>
```

**Xcode creation:**
1. Right-click Resources folder > New File > Property List
2. Name: Config.plist
3. Replace contents with template above
4. Verify .gitignore excludes this file (`git status` should not show it)

**3. .gitignore Configuration**

**Repository Structure:**
- Repo root: `/Pookie/` (contains .git/)
- iOS project: `/Pookie/ios/Pookie/`

**Gitignore Strategy:**
Update the EXISTING root `.gitignore` at `/Pookie/.gitignore` with iOS-specific patterns:

```
# Xcode
build/
*.pbxuser
!default.pbxuser
*.mode1v3
!default.mode1v3
*.mode2v3
!default.mode2v3
*.perspectivev3
!default.perspectivev3
xcuserdata/
*.xccheckout
*.moved-aside
DerivedData/
*.hmap
*.ipa
*.xcuserstate
.swiftpm/
Package.resolved

# iOS Secrets (CRITICAL)
ios/**/Config.plist
**/Config.plist

# Swift Package Manager
.build/
Packages/

# macOS
.DS_Store
```

**Verification:** Run `git status` - Config.plist must NOT appear in the output.

### Supabase SDK Version Compatibility

**Supabase Swift SDK v2.x Breaking Changes:**

If you find tutorials or StackOverflow answers using Supabase Swift SDK, verify they use v2.x syntax.

**v1.x → v2.x changes (avoid v1.x patterns):**
- v1.x used completion handlers: `supabase.auth.signIn(completion: { ... })`
- v2.x uses async/await: `try await supabase.auth.signIn(...)`
- v1.x had different package product names
- v2.x improved type safety and error handling

**For this project:** Greenfield (no migration needed), but be aware when referencing external docs/tutorials.

**Official v2.x Documentation:** https://supabase.com/docs/reference/swift/introduction

### Security Requirements

**Critical:**
- NEVER commit Supabase URL or anon key to git
- Config.plist MUST be in .gitignore
- Verify with `git status` that Config.plist does not appear
- Anon key is safe to use client-side (Supabase Row Level Security protects data)

### Build Verification

**Build Steps:**
1. Select target: "Pookie" (not test targets)
2. Select destination: "iPhone 15 Pro Simulator" or "Any iOS Device (arm64)"
3. Press Cmd+B (Product > Build)

**Success Criteria:**
- Build succeeds (green checkmark in Xcode)
- Zero errors
- Zero warnings related to Supabase SDK
- Build log shows "Build Succeeded"

**First Build Timing:**
The FIRST build after adding Supabase SDK will take 5-10 minutes due to:
- Swift Package Manager fetching dependencies
- Compiling Supabase + dependencies for the first time
- Building for simulator architecture

**Expected behavior:**
- Build progress shows "Compiling..." with package names
- Activity viewer (Xcode top bar) shows progress
- Subsequent builds will be much faster (incremental compilation)

**If stuck >15 minutes:**
1. Check Activity viewer for actual progress
2. Verify network connection (SPM downloads packages)
3. Try Product > Clean Build Folder and rebuild

**Acceptable Warnings (Safe to Ignore):**
- "@MainActor" warnings (will fix in Story 1.5)
- SwiftUI preview warnings (previews not implemented yet)

**Unacceptable Warnings/Errors:**
- "Module 'Supabase' not found"
- "Package resolution failed"
- "Undefined symbols" related to Supabase

## Verification Checklist

Before marking this story complete, verify ALL of the following:

**Project Structure:**
- [ ] Xcode project exists at `ios/Pookie/Pookie.xcodeproj`
- [ ] Folder structure matches architecture: App/, Resources/, Models/, ViewModels/, Views/, Services/
- [ ] Config.plist exists in Resources/ folder
- [ ] .gitignore includes Config.plist pattern
- [ ] Both filesystem and Xcode groups are in sync

**Swift Package Manager:**
- [ ] Package Dependencies shows "supabase-swift 2.x.x"
- [ ] All 4 products linked: Supabase, Auth, PostgREST, Storage
- [ ] Package.resolved exists and shows correct version
- [ ] Products linked to "Pookie" target (not test target)

**Build Configuration:**
- [ ] Minimum Deployment Target: iOS 17.0 (both Project and Target)
- [ ] Build succeeds with Cmd+B (Product > Build)
- [ ] Zero errors, zero Supabase-related warnings
- [ ] Build log shows "Build Succeeded"

**Git Security:**
- [ ] `git status` does NOT show Config.plist (must be gitignored)
- [ ] .gitignore contains `**/Config.plist` pattern

**Code Files:**
- [ ] App/Supabase.swift exists with SupabaseClient initialization
- [ ] Resources/Config.plist exists with SupabaseURL and SupabaseAnonKey keys
- [ ] TODO comments present for future Story 1.5 refactoring

### Architecture Alignment & Dependencies

**This story implements:**
- iOS Project Structure (architecture.md lines 1000-1035)
- iOS Starter Selection (architecture.md lines 310-428)
- Environment Configuration (architecture.md lines 1400-1420)

**Future Dependencies:**
- Story 1.5: AppState.swift (depends on Supabase client created here)
- Story 1.6: Authentication UI (depends on Auth module)
- All Epic 2+ stories depend on this project structure

**No conflicts:** First iOS story - establishes baseline for all future work.

### References

**Critical Reference Sections:**
1. Architecture: iOS Starter Selection (architecture.md lines 310-428) - SPM setup pattern
2. Architecture: iOS Project Structure (architecture.md lines 1000-1035) - Folder hierarchy
3. Epic 1 Story 1.1 (epics.md) - Acceptance criteria source
4. Official Supabase Docs: https://supabase.com/docs/guides/getting-started/quickstarts/ios-swiftui

**Skip:** Architecture sections on backend, graph RAG, modes - not relevant to this story.

---

**Status:** ready-for-dev

This story establishes the iOS foundation that all future stories depend on. Follow the architecture patterns exactly to ensure consistency across the entire project.
