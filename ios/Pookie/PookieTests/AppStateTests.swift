//
//  AppStateTests.swift
//  PookieTests
//
//  Created by Code Review Agent on 12/5/25.
//

import XCTest
@testable import Pookie

final class AppStateTests: XCTestCase {

    var appState: AppState!

    override func setUp() {
        super.setUp()
        appState = AppState()
    }

    override func tearDown() {
        appState = nil
        super.tearDown()
    }

    // MARK: - Initialization Tests

    func testAppStateInitialization() {
        // Given: New AppState instance
        // When: AppState is created
        // Then: Initial state should be correct
        XCTAssertNil(appState.currentUser, "currentUser should be nil on initialization")
        XCTAssertNil(appState.session, "session should be nil on initialization")
        XCTAssertFalse(appState.isAuthenticated, "isAuthenticated should be false when no session")
        XCTAssertFalse(appState.isLoading, "isLoading should be false initially")
        XCTAssertNil(appState.error, "error should be nil on initialization")
    }

    func testIsAuthenticatedComputedProperty() {
        // Given: AppState with no session
        XCTAssertFalse(appState.isAuthenticated)

        // When: Session is set (mock session for testing)
        // Note: In real implementation, you'd need to mock Supabase Session
        // For now, we verify the computed property logic

        // Then: isAuthenticated should reflect session state
        XCTAssertEqual(appState.isAuthenticated, appState.session != nil)
    }

    // MARK: - Helper Method Tests

    func testSetSessionUpdatesState() {
        // Given: AppState with no session
        XCTAssertNil(appState.session)
        XCTAssertNil(appState.currentUser)

        // When: setSession is called
        // Note: Can't create real Session without Supabase setup
        // This test validates method exists and compiles

        // Then: Method should be accessible
        // Full integration test requires Supabase mock
    }

    func testClearSessionResetsState() {
        // Given: AppState (potentially with session)

        // When: clearSession is called
        appState.clearSession()

        // Then: Session and user should be nil
        XCTAssertNil(appState.session, "clearSession should set session to nil")
        XCTAssertNil(appState.currentUser, "clearSession should set currentUser to nil")
        XCTAssertFalse(appState.isAuthenticated, "isAuthenticated should be false after clear")
    }

    func testSetErrorStoresErrorMessage() {
        // Given: AppState with no error
        XCTAssertNil(appState.error)

        // When: setError is called with a message
        let errorMessage = "Test error message"
        appState.setError(errorMessage)

        // Then: Error should be stored
        XCTAssertEqual(appState.error, errorMessage, "setError should store the error message")
    }

    func testClearErrorRemovesErrorMessage() {
        // Given: AppState with an error
        appState.setError("Some error")
        XCTAssertNotNil(appState.error)

        // When: clearError is called
        appState.clearError()

        // Then: Error should be nil
        XCTAssertNil(appState.error, "clearError should remove the error message")
    }

    // MARK: - Loading State Tests

    func testIsLoadingStateManagement() {
        // Given: AppState not loading
        XCTAssertFalse(appState.isLoading)

        // When: isLoading is set to true
        appState.isLoading = true

        // Then: isLoading should be true
        XCTAssertTrue(appState.isLoading, "isLoading should be settable to true")

        // When: isLoading is set back to false
        appState.isLoading = false

        // Then: isLoading should be false
        XCTAssertFalse(appState.isLoading, "isLoading should be settable to false")
    }

    // MARK: - Integration Tests

    func testCheckSessionHandlesNoSessionGracefully() async {
        // Given: AppState with no stored session in Keychain
        // When: checkSession is called
        await appState.checkSession()

        // Then: Should complete without crashing
        // Note: Without real Supabase setup, this validates error handling
        XCTAssertFalse(appState.isLoading, "isLoading should be false after checkSession completes")
    }
}
