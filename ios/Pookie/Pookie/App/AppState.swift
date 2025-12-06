//
//  AppState.swift
//  Pookie
//
//  Created by Dev Agent on 12/5/25.
//

import Foundation
import Supabase

/// Global application state manager using iOS 17+ @Observable pattern.
/// Manages user authentication session and global UI state across the entire app.
@Observable
class AppState {
    // MARK: - Authentication State

    /// Currently authenticated user (from Supabase)
    var currentUser: User?

    /// Active Supabase session (contains JWT token)
    var session: Session?

    /// Computed property: true if user has valid session
    var isAuthenticated: Bool {
        session != nil
    }

    // MARK: - UI State

    /// Global loading indicator (e.g., checking session on app start)
    var isLoading: Bool = false

    /// Global error message to display to user
    var error: String?

    // MARK: - Initialization

    init() {
        // Check for existing session on app launch
        Task {
            await checkSession()
        }
    }

    // MARK: - Session Management

    /// Check if user has an existing session (called on app start)
    func checkSession() async {
        isLoading = true
        defer { isLoading = false }

        do {
            // Supabase SDK checks Keychain for stored session
            let session = try await supabase.auth.session
            self.session = session
            self.currentUser = session.user
        } catch {
            // No active session or session expired
            self.session = nil
            self.currentUser = nil
        }
    }

    /// Update state after successful authentication
    func setSession(_ session: Session) {
        self.session = session
        self.currentUser = session.user
    }

    /// Clear state after sign out
    func clearSession() {
        self.session = nil
        self.currentUser = nil
    }

    /// Set global error message
    func setError(_ message: String) {
        self.error = message
    }

    /// Clear error message
    func clearError() {
        self.error = nil
    }
}
