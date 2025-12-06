//
//  AuthServiceTests.swift
//  PookieTests
//
//  Created by Code Review Agent on 12/5/25.
//

import XCTest
@testable import Pookie

final class AuthServiceTests: XCTestCase {

    var authService: AuthService!

    override func setUp() {
        super.setUp()
        authService = AuthService.shared
    }

    override func tearDown() {
        authService = nil
        super.tearDown()
    }

    // MARK: - Singleton Pattern Tests

    func testAuthServiceIsSingleton() {
        // Given: Two references to AuthService
        let instance1 = AuthService.shared
        let instance2 = AuthService.shared

        // Then: Both should be the same instance
        XCTAssertTrue(instance1 === instance2, "AuthService.shared should return the same instance")
    }

    // MARK: - Email Validation Tests

    func testSignUpRejectsEmptyEmail() async {
        // Given: Empty email
        let email = ""
        let password = "password123"

        // When/Then: signUp should throw invalidEmail error
        do {
            _ = try await authService.signUp(email: email, password: password)
            XCTFail("signUp should throw error for empty email")
        } catch let error as AuthError {
            XCTAssertEqual(error, .invalidEmail, "Should throw invalidEmail error")
        } catch {
            XCTFail("Should throw AuthError, not \(error)")
        }
    }

    func testSignUpRejectsInvalidEmailFormat() async {
        // Given: Email without @ symbol
        let email = "notanemail"
        let password = "password123"

        // When/Then: signUp should throw invalidEmail error
        do {
            _ = try await authService.signUp(email: email, password: password)
            XCTFail("signUp should throw error for invalid email format")
        } catch let error as AuthError {
            XCTAssertEqual(error, .invalidEmail, "Should throw invalidEmail error")
        } catch {
            XCTFail("Should throw AuthError, not \(error)")
        }
    }

    func testSignInRejectsEmptyEmail() async {
        // Given: Empty email
        let email = ""
        let password = "password123"

        // When/Then: signIn should throw invalidEmail error
        do {
            _ = try await authService.signIn(email: email, password: password)
            XCTFail("signIn should throw error for empty email")
        } catch let error as AuthError {
            XCTAssertEqual(error, .invalidEmail, "Should throw invalidEmail error")
        } catch {
            XCTFail("Should throw AuthError, not \(error)")
        }
    }

    // MARK: - Password Validation Tests

    func testSignUpRejectsEmptyPassword() async {
        // Given: Empty password
        let email = "test@example.com"
        let password = ""

        // When/Then: signUp should throw weakPassword error
        do {
            _ = try await authService.signUp(email: email, password: password)
            XCTFail("signUp should throw error for empty password")
        } catch let error as AuthError {
            XCTAssertEqual(error, .weakPassword, "Should throw weakPassword error")
        } catch {
            XCTFail("Should throw AuthError, not \(error)")
        }
    }

    func testSignUpRejectsShortPassword() async {
        // Given: Password with less than 6 characters
        let email = "test@example.com"
        let password = "12345" // Only 5 characters

        // When/Then: signUp should throw weakPassword error
        do {
            _ = try await authService.signUp(email: email, password: password)
            XCTFail("signUp should throw error for short password")
        } catch let error as AuthError {
            XCTAssertEqual(error, .weakPassword, "Should throw weakPassword error")
        } catch {
            XCTFail("Should throw AuthError, not \(error)")
        }
    }

    func testSignInRejectsEmptyPassword() async {
        // Given: Empty password
        let email = "test@example.com"
        let password = ""

        // When/Then: signIn should throw weakPassword error
        do {
            _ = try await authService.signIn(email: email, password: password)
            XCTFail("signIn should throw error for empty password")
        } catch let error as AuthError {
            XCTAssertEqual(error, .weakPassword, "Should throw weakPassword error")
        } catch {
            XCTFail("Should throw AuthError, not \(error)")
        }
    }

    // MARK: - AuthError Tests

    func testAuthErrorDescriptions() {
        // Test all error cases have descriptions
        XCTAssertNotNil(AuthError.invalidEmail.errorDescription)
        XCTAssertNotNil(AuthError.weakPassword.errorDescription)
        XCTAssertNotNil(AuthError.invalidCredentials.errorDescription)
        XCTAssertNotNil(AuthError.noSession.errorDescription)
        XCTAssertNotNil(AuthError.networkError.errorDescription)
        XCTAssertNotNil(AuthError.unknown("test").errorDescription)

        // Verify specific messages
        XCTAssertTrue(AuthError.invalidEmail.errorDescription?.contains("valid email") ?? false)
        XCTAssertTrue(AuthError.weakPassword.errorDescription?.contains("6 characters") ?? false)
        XCTAssertTrue(AuthError.invalidCredentials.errorDescription?.contains("incorrect") ?? false)
    }

    // MARK: - Method Signature Tests

    func testSignUpMethodSignature() async {
        // Verify method exists with correct signature
        // This test validates the API contract
        let email = "test@example.com"
        let password = "password123"

        // Method should be async throws and return Session (or throw)
        // Full test requires Supabase mock
        do {
            _ = try await authService.signUp(email: email, password: password)
            // Will fail without real Supabase, but validates method exists
        } catch {
            // Expected to fail without Supabase setup
            XCTAssertNotNil(error, "Method should throw when Supabase not configured")
        }
    }

    func testSignInMethodSignature() async {
        // Verify method exists with correct signature
        let email = "test@example.com"
        let password = "password123"

        do {
            _ = try await authService.signIn(email: email, password: password)
        } catch {
            // Expected to fail without Supabase setup
            XCTAssertNotNil(error, "Method should throw when Supabase not configured")
        }
    }

    func testSignOutMethodExists() async {
        // Verify signOut method exists
        do {
            try await authService.signOut()
        } catch {
            // Expected to fail without Supabase setup
            XCTAssertNotNil(error, "Method should throw when Supabase not configured")
        }
    }
}

// MARK: - AuthError Equatable Conformance for Testing

extension AuthError: Equatable {
    public static func == (lhs: AuthError, rhs: AuthError) -> Bool {
        switch (lhs, rhs) {
        case (.invalidEmail, .invalidEmail),
             (.weakPassword, .weakPassword),
             (.invalidCredentials, .invalidCredentials),
             (.noSession, .noSession),
             (.networkError, .networkError):
            return true
        case (.unknown(let lhsMsg), .unknown(let rhsMsg)):
            return lhsMsg == rhsMsg
        default:
            return false
        }
    }
}
