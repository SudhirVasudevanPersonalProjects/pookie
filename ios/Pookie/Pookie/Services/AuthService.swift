//
//  AuthService.swift
//  Pookie
//
//  Created by Dev Agent on 12/5/25.
//

import Foundation
import Supabase

/// Authentication service wrapper for Supabase Auth API.
/// Provides email/password authentication methods with input validation and error handling.
class AuthService {
    // MARK: - Singleton

    /// Shared instance (stateless - safe to share)
    static let shared = AuthService()

    /// Private init (enforces singleton pattern)
    private init() {}

    // MARK: - Authentication Methods

    /// Sign up new user with email and password
    /// - Parameters:
    ///   - email: User's email address
    ///   - password: User's password (min 8 characters)
    /// - Returns: Supabase Session with JWT token (if email confirmation disabled)
    /// - Throws: AuthError if validation fails, signup fails, or email confirmation required
    func signUp(email: String, password: String) async throws -> Session {
        // Input validation
        try validateEmail(email)
        try validatePassword(password)

        do {
            let response = try await supabase.auth.signUp(
                email: email,
                password: password
            )

            // Check if session was returned (happens when email confirmation is disabled)
            if let session = response.session {
                return session
            }

            // No session = email confirmation is enabled
            // User was created but needs to confirm email before signing in
            throw AuthError.emailConfirmationRequired(email: email)

        } catch let error as AuthError {
            throw error
        } catch {
            throw translateSupabaseError(error)
        }
    }

    /// Sign in existing user with email and password
    /// - Parameters:
    ///   - email: User's email address
    ///   - password: User's password
    /// - Returns: Supabase Session with JWT token
    /// - Throws: AuthError if validation fails or credentials invalid
    func signIn(email: String, password: String) async throws -> Session {
        // Input validation
        try validateEmail(email)
        try validatePassword(password)

        do {
            let session = try await supabase.auth.signIn(
                email: email,
                password: password
            )
            return session
        } catch {
            throw translateSupabaseError(error)
        }
    }

    /// Sign out current user (clears session from Keychain)
    /// - Throws: AuthError if sign out fails
    func signOut() async throws {
        do {
            try await supabase.auth.signOut()
        } catch {
            throw AuthError.networkError
        }
    }

    // MARK: - Validation Helpers

    private func validateEmail(_ email: String) throws {
        guard !email.isEmpty else {
            throw AuthError.invalidEmail
        }
        guard email.contains("@") && email.contains(".") else {
            throw AuthError.invalidEmail
        }
    }

    private func validatePassword(_ password: String) throws {
        guard !password.isEmpty else {
            throw AuthError.weakPassword
        }
        guard password.count >= 8 else {
            throw AuthError.weakPassword
        }
    }

    // MARK: - Error Translation

    private func translateSupabaseError(_ error: Error) -> AuthError {
        let errorMessage = error.localizedDescription.lowercased()

        if errorMessage.contains("invalid login credentials") || errorMessage.contains("invalid email or password") {
            return .invalidCredentials
        } else if errorMessage.contains("network") || errorMessage.contains("connection") {
            return .networkError
        } else {
            return .unknown(error.localizedDescription)
        }
    }
}

// MARK: - Error Types

/// Authentication-specific errors with user-friendly descriptions
enum AuthError: LocalizedError {
    case invalidEmail
    case weakPassword
    case invalidCredentials
    case emailConfirmationRequired(email: String)
    case noSession
    case networkError
    case unknown(String)

    var errorDescription: String? {
        switch self {
        case .invalidEmail:
            return "Please enter a valid email address."
        case .weakPassword:
            return "Password must be at least 8 characters long."
        case .invalidCredentials:
            return "Email or password incorrect. Please try again."
        case .emailConfirmationRequired(let email):
            return "Account created! Please check \(email) for a confirmation link, then sign in."
        case .noSession:
            return "No session created after sign up. Please check your email for confirmation."
        case .networkError:
            return "Network error. Please check your connection and try again."
        case .unknown(let message):
            return message
        }
    }
}
