//
//  ContentViewTests.swift
//  PookieTests
//
//  Created by Dev Agent on 12/5/25.
//

import XCTest
@testable import Pookie
import Supabase

/// Unit tests for ContentView conditional navigation
/// Note: Full UI rendering testing requires XCUITest framework.
/// These tests verify the conditional navigation logic based on AppState.isAuthenticated.
final class ContentViewTests: XCTestCase {
    var appState: AppState!

    override func setUp() {
        super.setUp()
        appState = AppState()
    }

    override func tearDown() {
        appState = nil
        super.tearDown()
    }

    // MARK: - Conditional Navigation Logic Tests

    /// Test that isAuthenticated is false when not authenticated (should show AuthView)
    func testContentViewShowsAuthViewWhenNotAuthenticated() {
        // Verify initial state is not authenticated
        XCTAssertFalse(appState.isAuthenticated, "AppState should not be authenticated initially")
        XCTAssertNil(appState.session, "Session should be nil when not authenticated")
        XCTAssertNil(appState.currentUser, "Current user should be nil when not authenticated")

        // ContentView logic: if appState.isAuthenticated { HomeView() } else { AuthView() }
        // Since isAuthenticated is false, AuthView should be shown
    }

    /// Test that isAuthenticated is true when authenticated (should show HomeView)
    func testContentViewShowsHomeViewWhenAuthenticated() {
        // Set authenticated state
        let mockUser = User(
            id: UUID(),
            appMetadata: [:],
            userMetadata: [:],
            aud: "authenticated",
            createdAt: Date(),
            updatedAt: Date()
        )
        let mockSession = Session(
            accessToken: "mock-token",
            tokenType: "bearer",
            expiresIn: 3600,
            expiresAt: Date().addingTimeInterval(3600).timeIntervalSince1970,
            refreshToken: "mock-refresh",
            user: mockUser
        )
        appState.setSession(mockSession)

        // Verify authenticated state
        XCTAssertTrue(appState.isAuthenticated, "AppState should be authenticated after setSession")
        XCTAssertNotNil(appState.session, "Session should be set when authenticated")
        XCTAssertNotNil(appState.currentUser, "Current user should be set when authenticated")

        // ContentView logic: if appState.isAuthenticated { HomeView() } else { AuthView() }
        // Since isAuthenticated is true, HomeView should be shown
    }

    /// Test that navigation updates when authentication state changes
    func testNavigationUpdatesWhenAuthenticationChanges() {
        // Start unauthenticated
        XCTAssertFalse(appState.isAuthenticated, "Should start unauthenticated")

        // Authenticate
        let mockUser = User(
            id: UUID(),
            appMetadata: [:],
            userMetadata: [:],
            aud: "authenticated",
            createdAt: Date(),
            updatedAt: Date()
        )
        let mockSession = Session(
            accessToken: "mock-token",
            tokenType: "bearer",
            expiresIn: 3600,
            expiresAt: Date().addingTimeInterval(3600).timeIntervalSince1970,
            refreshToken: "mock-refresh",
            user: mockUser
        )
        appState.setSession(mockSession)

        // Verify navigation should switch to HomeView
        XCTAssertTrue(appState.isAuthenticated, "Should be authenticated after setSession")

        // Sign out
        appState.clearSession()

        // Verify navigation should switch back to AuthView
        XCTAssertFalse(appState.isAuthenticated, "Should not be authenticated after clearSession")
    }

    /// Test that isAuthenticated computed property reflects session state
    func testIsAuthenticatedComputedProperty() {
        // No session = not authenticated
        appState.session = nil
        XCTAssertFalse(appState.isAuthenticated, "isAuthenticated should be false when session is nil")

        // Has session = authenticated
        let mockUser = User(
            id: UUID(),
            appMetadata: [:],
            userMetadata: [:],
            aud: "authenticated",
            createdAt: Date(),
            updatedAt: Date()
        )
        let mockSession = Session(
            accessToken: "mock-token",
            tokenType: "bearer",
            expiresIn: 3600,
            expiresAt: Date().addingTimeInterval(3600).timeIntervalSince1970,
            refreshToken: "mock-refresh",
            user: mockUser
        )
        appState.session = mockSession
        XCTAssertTrue(appState.isAuthenticated, "isAuthenticated should be true when session exists")

        // Clear session = not authenticated
        appState.session = nil
        XCTAssertFalse(appState.isAuthenticated, "isAuthenticated should be false after clearing session")
    }
}
