//
//  HomeViewTests.swift
//  PookieTests
//
//  Created by Dev Agent on 12/5/25.
//

import XCTest
@testable import Pookie
import Supabase

/// Unit tests for HomeView placeholder home screen
/// Note: Full UI interaction testing requires XCUITest framework.
/// These tests verify the underlying state management for sign out functionality.
final class HomeViewTests: XCTestCase {
    var appState: AppState!

    override func setUp() {
        super.setUp()
        appState = AppState()
    }

    override func tearDown() {
        appState = nil
        super.tearDown()
    }

    // MARK: - Sign Out State Management Tests

    /// Test that clearSession properly clears authentication state during sign out
    func testSignOutClearsAppStateSession() {
        // Set up authenticated state
        let mockUser = User(
            id: UUID(),
            appMetadata: [:],
            userMetadata: ["email": "test@example.com"],
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

        // Verify authenticated before sign out
        XCTAssertTrue(appState.isAuthenticated, "Should be authenticated before sign out")

        // Simulate sign out (HomeView calls appState.clearSession())
        appState.clearSession()

        // Verify state cleared correctly
        XCTAssertNil(appState.session, "Session should be nil after sign out")
        XCTAssertNil(appState.currentUser, "Current user should be nil after sign out")
        XCTAssertFalse(appState.isAuthenticated, "Should not be authenticated after sign out")
    }

    /// Test that user email is accessible from AppState when authenticated
    func testHomeViewCanAccessUserEmail() {
        // Create user with email
        let mockUser = User(
            id: UUID(),
            appMetadata: [:],
            userMetadata: [:],
            aud: "authenticated",
            email: "user@example.com",
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

        // Verify email is accessible (HomeView displays this)
        XCTAssertNotNil(appState.currentUser?.email, "User email should be accessible when authenticated")
        XCTAssertEqual(appState.currentUser?.email, "user@example.com", "Email should match authenticated user")
    }

    /// Test that AppState maintains authenticated state until clearSession is called
    func testAuthenticatedStatePersistedUntilClearSession() {
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

        // Verify authenticated state persists
        XCTAssertTrue(appState.isAuthenticated, "Should remain authenticated")
        XCTAssertNotNil(appState.session, "Session should remain set")

        // Clear session (sign out)
        appState.clearSession()

        // Verify state cleared
        XCTAssertFalse(appState.isAuthenticated, "Should not be authenticated after clearSession")
    }
}
