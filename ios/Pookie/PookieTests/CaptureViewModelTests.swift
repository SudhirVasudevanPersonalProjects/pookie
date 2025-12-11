//
//  CaptureViewModelTests.swift
//  PookieTests
//
//  Created by Code Review Agent on 12/7/25.
//

import XCTest
@testable import Pookie

final class CaptureViewModelTests: XCTestCase {

    var viewModel: CaptureViewModel!

    override func setUp() {
        super.setUp()
        viewModel = CaptureViewModel()
    }

    override func tearDown() {
        viewModel = nil
        super.tearDown()
    }

    // MARK: - Character Count Tests

    func testCharacterCount_EmptyText() {
        viewModel.somethingText = ""
        XCTAssertEqual(viewModel.characterCount, 0)
    }

    func testCharacterCount_ShortText() {
        viewModel.somethingText = "Hello"
        XCTAssertEqual(viewModel.characterCount, 5)
    }

    func testCharacterCount_LongText() {
        viewModel.somethingText = String(repeating: "a", count: 500)
        XCTAssertEqual(viewModel.characterCount, 500)
    }

    func testCharacterCount_ComplexCharacters() {
        viewModel.somethingText = "Hello 👋🏼 世界"
        XCTAssertEqual(viewModel.characterCount, 9) // Swift counts grapheme clusters correctly
    }

    // MARK: - canSave Validation Tests

    func testCanSave_EmptyText() {
        viewModel.somethingText = ""
        XCTAssertFalse(viewModel.canSave, "Save should be disabled when text is empty")
    }

    func testCanSave_ValidText() {
        viewModel.somethingText = "Valid thought"
        XCTAssertTrue(viewModel.canSave, "Save should be enabled with valid text")
    }

    func testCanSave_ExceedsLimit() {
        viewModel.somethingText = String(repeating: "a", count: 10001)
        XCTAssertFalse(viewModel.canSave, "Save should be disabled when exceeding 10,000 characters")
    }

    func testCanSave_ExactLimit() {
        viewModel.somethingText = String(repeating: "a", count: 10000)
        XCTAssertTrue(viewModel.canSave, "Save should be enabled at exactly 10,000 characters")
    }

    func testCanSave_WhileSaving() {
        viewModel.somethingText = "Valid thought"
        viewModel.isSaving = true
        XCTAssertFalse(viewModel.canSave, "Save should be disabled while save is in progress")
    }

    // MARK: - State Management Tests

    func testInitialState() {
        XCTAssertEqual(viewModel.somethingText, "")
        XCTAssertFalse(viewModel.isSaving)
        XCTAssertNil(viewModel.error)
        XCTAssertNil(viewModel.successMessage)
        XCTAssertNil(viewModel.lastCreated)
        XCTAssertFalse(viewModel.needsReauthentication)
    }

    func testSaveSomething_EmptyTextGuard() async {
        viewModel.somethingText = ""

        await viewModel.saveSomething()

        // Should not attempt save with empty text
        XCTAssertFalse(viewModel.isSaving)
        XCTAssertNil(viewModel.successMessage)
    }

    func testSaveSomething_ExceedsLimitGuard() async {
        viewModel.somethingText = String(repeating: "a", count: 10001)

        await viewModel.saveSomething()

        // Should not attempt save when exceeding limit
        XCTAssertFalse(viewModel.isSaving)
        XCTAssertNil(viewModel.successMessage)
    }

    // MARK: - Integration Tests (Require Backend Mock)

    // Note: These tests require mocking APIService.shared.createSomething()
    // For now, they are commented out until a mock APIService is implemented

    /*
    func testSaveSomething_Success() async throws {
        // Mock successful API response
        viewModel.somethingText = "Test thought"

        await viewModel.saveSomething()

        XCTAssertEqual(viewModel.successMessage, "Something saved!")
        XCTAssertEqual(viewModel.somethingText, "", "Text should be cleared after save")
        XCTAssertNotNil(viewModel.lastCreated)
        XCTAssertFalse(viewModel.isSaving)
        XCTAssertNil(viewModel.error)
    }

    func testSaveSomething_NetworkError() async throws {
        // Mock network error response
        viewModel.somethingText = "Test thought"

        await viewModel.saveSomething()

        XCTAssertNotNil(viewModel.error)
        XCTAssertEqual(viewModel.somethingText, "Test thought", "Text should be preserved on error")
        XCTAssertNil(viewModel.successMessage)
        XCTAssertFalse(viewModel.isSaving)
    }

    func testSaveSomething_UnauthorizedError() async throws {
        // Mock 401 unauthorized response
        viewModel.somethingText = "Test thought"

        await viewModel.saveSomething()

        XCTAssertTrue(viewModel.needsReauthentication, "Should signal reauthentication needed")
        XCTAssertEqual(viewModel.error, "Session expired. Please log in again.")
        XCTAssertEqual(viewModel.somethingText, "Test thought", "Text should be preserved on error")
        XCTAssertFalse(viewModel.isSaving)
    }
    */
}
