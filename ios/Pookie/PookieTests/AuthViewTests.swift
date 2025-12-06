//
//  AuthViewTests.swift
//  PookieTests
//
//  Created by Dev Agent on 12/5/25.
//

import XCTest
@testable import Pookie
import Supabase

/// Unit tests for AuthView authentication screen
/// Note: Full UI interaction testing requires XCUITest framework.
/// These tests verify the underlying state management and business logic.
final class AuthViewTests: XCTestCase {
    var appState: AppState!

    override func setUp() {
        super.setUp()
        appState = AppState()
    }

    override func tearDown() {
        appState = nil
        super.tearDown()
    }

    // MARK: - AppState Integration Tests

    /// Test that AppState initializes unauthenticated
    func testAppStateInitializesUnauthenticated() {
        XCTAssertNil(appState.session, "AppState should start with no session")
        XCTAssertNil(appState.currentUser, "AppState should start with no user")
        XCTAssertFalse(appState.isAuthenticated, "AppState should not be authenticated initially")
    }

    /// Test that setSession updates authentication state correctly
    func testSetSessionUpdatesAuthenticationState() {
        // Create mock session
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

        // Simulate successful authentication
        appState.setSession(mockSession)

        // Verify state updated correctly
        XCTAssertNotNil(appState.session, "Session should be set after authentication")
        XCTAssertNotNil(appState.currentUser, "Current user should be set after authentication")
        XCTAssertTrue(appState.isAuthenticated, "AppState should be authenticated after setSession")
        XCTAssertEqual(appState.session?.accessToken, "mock-token", "Session token should match")
    }

    /// Test that clearSession removes authentication state
    func testClearSessionRemovesAuthenticationState() {
        // Set up authenticated state
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

        // Clear session
        appState.clearSession()

        // Verify state cleared
        XCTAssertNil(appState.session, "Session should be nil after clearSession")
        XCTAssertNil(appState.currentUser, "Current user should be nil after clearSession")
        XCTAssertFalse(appState.isAuthenticated, "AppState should not be authenticated after clearSession")
    }

    // MARK: - Error State Tests

    /// Test that setError updates error state
    func testSetErrorUpdatesErrorState() {
        let errorMessage = "Invalid credentials"
        appState.setError(errorMessage)

        XCTAssertEqual(appState.error, errorMessage, "Error message should be set correctly")
    }

    /// Test that clearError removes error state
    func testClearErrorRemovesErrorState() {
        appState.setError("Test error")
        appState.clearError()

        XCTAssertNil(appState.error, "Error should be nil after clearError")
    }

    // MARK: - Authentication Flow Tests

    /// Test that authentication updates isAuthenticated computed property
    func testIsAuthenticatedComputedProperty() {
        // Initially not authenticated
        XCTAssertFalse(appState.isAuthenticated, "Should not be authenticated initially")

        // After setSession, should be authenticated
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
        XCTAssertTrue(appState.isAuthenticated, "Should be authenticated after setSession")

        // After clearSession, should not be authenticated
        appState.clearSession()
        XCTAssertFalse(appState.isAuthenticated, "Should not be authenticated after clearSession")
    }
}
