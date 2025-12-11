//
//  SomethingModelTests.swift
//  PookieTests
//
//  Created by Dev Agent on 12/7/25.
//

import XCTest
@testable import Pookie

final class SomethingModelTests: XCTestCase {

    // MARK: - Something Model Tests

    func testSomethingDecodesFromCamelCaseJSON() throws {
        let json = """
        {
            "id": 123,
            "userId": "550e8400-e29b-41d4-a716-446655440000",
            "content": "My first thought",
            "contentType": "text",
            "mediaUrl": null,
            "meaning": "AI-generated meaning",
            "isMeaningUserEdited": false,
            "noveltyScore": 0.85,
            "createdAt": "2025-12-07T12:34:56.789Z",
            "updatedAt": "2025-12-07T12:34:56.789Z"
        }
        """.data(using: .utf8)!

        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601

        let something = try decoder.decode(Something.self, from: json)

        XCTAssertEqual(something.id, 123)
        XCTAssertEqual(something.userId, "550e8400-e29b-41d4-a716-446655440000")
        XCTAssertEqual(something.content, "My first thought")
        XCTAssertEqual(something.contentType, .text)
        XCTAssertNil(something.mediaUrl)
        XCTAssertEqual(something.meaning, "AI-generated meaning")
        XCTAssertEqual(something.isMeaningUserEdited, false)
        XCTAssertEqual(something.noveltyScore, 0.85)
    }

    func testSomethingDecodesWithNullableFields() throws {
        let json = """
        {
            "id": 456,
            "userId": "user-uuid",
            "content": null,
            "contentType": "image",
            "mediaUrl": "https://example.com/image.jpg",
            "meaning": null,
            "isMeaningUserEdited": false,
            "noveltyScore": null,
            "createdAt": "2025-12-07T10:00:00.000Z",
            "updatedAt": "2025-12-07T10:00:00.000Z"
        }
        """.data(using: .utf8)!

        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601

        let something = try decoder.decode(Something.self, from: json)

        XCTAssertEqual(something.id, 456)
        XCTAssertNil(something.content)
        XCTAssertEqual(something.contentType, .image)
        XCTAssertEqual(something.mediaUrl, "https://example.com/image.jpg")
        XCTAssertNil(something.meaning)
        XCTAssertNil(something.noveltyScore)
    }

    func testContentTypeEnumCases() {
        XCTAssertEqual(ContentType.text.rawValue, "text")
        XCTAssertEqual(ContentType.image.rawValue, "image")
        XCTAssertEqual(ContentType.video.rawValue, "video")
        XCTAssertEqual(ContentType.url.rawValue, "url")
    }

    // MARK: - SomethingCreate Tests

    func testSomethingCreateEncodesToCamelCaseJSON() throws {
        let create = SomethingCreate(
            content: "New thought",
            contentType: .text,
            mediaUrl: nil
        )

        let encoder = JSONEncoder()
        let data = try encoder.encode(create)
        let json = try JSONSerialization.jsonObject(with: data) as! [String: Any]

        XCTAssertEqual(json["content"] as? String, "New thought")
        XCTAssertEqual(json["contentType"] as? String, "text")
        XCTAssertTrue(json.keys.contains("mediaUrl"))
    }

    func testSomethingCreateEncodesWithMediaUrl() throws {
        let create = SomethingCreate(
            content: nil,
            contentType: .video,
            mediaUrl: "https://example.com/video.mp4"
        )

        let encoder = JSONEncoder()
        let data = try encoder.encode(create)
        let json = try JSONSerialization.jsonObject(with: data) as! [String: Any]

        XCTAssertEqual(json["contentType"] as? String, "video")
        XCTAssertEqual(json["mediaUrl"] as? String, "https://example.com/video.mp4")
    }

    // MARK: - SomethingUpdateMeaning Tests

    func testSomethingUpdateMeaningEncodesToJSON() throws {
        let update = SomethingUpdateMeaning(meaning: "User-edited meaning")

        let encoder = JSONEncoder()
        let data = try encoder.encode(update)
        let json = try JSONSerialization.jsonObject(with: data) as! [String: Any]

        XCTAssertEqual(json["meaning"] as? String, "User-edited meaning")
    }
}
