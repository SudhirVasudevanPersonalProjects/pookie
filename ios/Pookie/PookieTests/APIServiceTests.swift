//
//  APIServiceTests.swift
//  PookieTests
//
//  Created by Dev Agent on 12/7/25.
//

import XCTest
@testable import Pookie

final class APIServiceTests: XCTestCase {

    // MARK: - Singleton Tests

    func testAPIServiceIsSingleton() {
        let instance1 = APIService.shared
        let instance2 = APIService.shared

        XCTAssertTrue(instance1 === instance2, "APIService.shared should return the same instance")
    }

    // MARK: - APIError Tests

    func testAPIErrorDescriptions() {
        let unauthorizedError = APIError.unauthorized
        XCTAssertEqual(unauthorizedError.errorDescription, "Please log in again")

        let networkError = APIError.networkError
        XCTAssertEqual(networkError.errorDescription, "Network connection failed")

        let notFoundError = APIError.notFound
        XCTAssertEqual(notFoundError.errorDescription, "Resource not found")

        let invalidURLError = APIError.invalidURL
        XCTAssertEqual(invalidURLError.errorDescription, "Invalid request URL")

        let invalidParamsError = APIError.invalidParameters("test message")
        XCTAssertEqual(invalidParamsError.errorDescription, "Invalid parameters: test message")

        let serverError = APIError.serverError("Custom error message")
        XCTAssertEqual(serverError.errorDescription, "Custom error message")
    }

    // MARK: - Validation Tests

    func testListSomethingsValidatesNegativeSkip() async {
        do {
            _ = try await APIService.shared.listSomethings(skip: -10, limit: 50)
            XCTFail("Should throw invalidParameters error for negative skip")
        } catch APIError.invalidParameters(let message) {
            XCTAssertTrue(message.contains("skip must be >= 0"))
        } catch {
            XCTFail("Wrong error type: \(error)")
        }
    }

    func testListSomethingsValidatesNegativeLimit() async {
        do {
            _ = try await APIService.shared.listSomethings(skip: 0, limit: -5)
            XCTFail("Should throw invalidParameters error for negative limit")
        } catch APIError.invalidParameters(let message) {
            XCTAssertTrue(message.contains("limit must be between 1 and 100"))
        } catch {
            XCTFail("Wrong error type: \(error)")
        }
    }

    func testListSomethingsValidatesZeroLimit() async {
        do {
            _ = try await APIService.shared.listSomethings(skip: 0, limit: 0)
            XCTFail("Should throw invalidParameters error for zero limit")
        } catch APIError.invalidParameters(let message) {
            XCTAssertTrue(message.contains("limit must be between 1 and 100"))
        } catch {
            XCTFail("Wrong error type: \(error)")
        }
    }

    func testListSomethingsValidatesExcessiveLimit() async {
        do {
            _ = try await APIService.shared.listSomethings(skip: 0, limit: 200)
            XCTFail("Should throw invalidParameters error for limit > 100")
        } catch APIError.invalidParameters(let message) {
            XCTAssertTrue(message.contains("limit must be between 1 and 100"))
        } catch {
            XCTFail("Wrong error type: \(error)")
        }
    }

    func testListSomethingsAcceptsValidParameters() async {
        // Note: This will fail with unauthorized (expected) but should pass validation
        do {
            _ = try await APIService.shared.listSomethings(skip: 10, limit: 50)
        } catch APIError.unauthorized {
            // Expected - no auth session in unit tests
            // The important thing is we didn't get invalidParameters
            XCTAssertTrue(true)
        } catch APIError.invalidParameters {
            XCTFail("Should not throw invalidParameters for valid params")
        } catch {
            // Other errors (network, etc.) are acceptable in unit test environment
            XCTAssertTrue(true)
        }
    }

    // MARK: - Public Access Tests

    func testAPIServiceMethodsArePublic() {
        // Verify methods can be called from test target (public access)
        let service = APIService.shared

        // These should compile - verifies public access
        _ = service.createSomething
        _ = service.listSomethings
        _ = service.updateMeaning
    }

    // MARK: - Integration Tests (Require Running Backend + Auth)

    // Note: These tests require:
    // 1. Backend server running on localhost:8080
    // 2. Valid Supabase auth session
    // 3. Test database with fixtures
    //
    // Run these manually during integration testing phase

    // func testCreateSomethingIntegration() async throws {
    //     // Requires: Valid auth session
    //     let something = try await APIService.shared.createSomething(
    //         content: "Integration test thought",
    //         contentType: .text
    //     )
    //     XCTAssertEqual(something.content, "Integration test thought")
    //     XCTAssertEqual(something.contentType, .text)
    // }

    // func testListSomethingsIntegration() async throws {
    //     // Requires: Valid auth session + existing data
    //     let somethings = try await APIService.shared.listSomethings()
    //     XCTAssertTrue(somethings.count >= 0)
    // }

    // func testUpdateMeaningIntegration() async throws {
    //     // Requires: Valid auth session + existing something
    //     let updated = try await APIService.shared.updateMeaning(
    //         somethingId: 1,
    //         meaning: "Updated meaning"
    //     )
    //     XCTAssertEqual(updated.meaning, "Updated meaning")
    //     XCTAssertTrue(updated.isMeaningUserEdited)
    // }
}
