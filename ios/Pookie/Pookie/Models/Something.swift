//
//  Something.swift
//  Pookie
//
//  Created by Dev Agent on 12/7/25.
//

import Foundation

// MARK: - Content Type Enum

/// Multimodal content type for somethings
///
/// Defines the type of content captured in a something. This enables the app to handle
/// text, images, videos, and URLs with appropriate processing and display logic.
public enum ContentType: String, Codable {
    /// Plain text content - user typed or voice-to-text transcription
    /// Example: "Remember to buy milk"
    case text

    /// Image content - photo captured or selected from library
    /// Requires: mediaUrl pointing to image file
    case image

    /// Video content - recorded or selected from library
    /// Requires: mediaUrl pointing to video file
    case video

    /// URL content - web link or bookmark
    /// Content field contains the URL, mediaUrl may contain preview image
    case url
}

// MARK: - Circle Prediction

/// Circle prediction from centroid similarity
public struct CirclePrediction: Codable, Equatable {
    public let circleId: Int
    public let circleName: String
    public let confidence: Double
}

// MARK: - Something Model

/// Core Something model matching backend API schema
public struct Something: Codable, Identifiable, Equatable {
    public let id: Int
    public let userId: String
    public let content: String?
    public let contentType: ContentType
    public let mediaUrl: String?
    public let meaning: String?
    public let isMeaningUserEdited: Bool
    public let noveltyScore: Double?
    public let suggestedCircles: [CirclePrediction]
    public let createdAt: Date
    public let updatedAt: Date

}

// MARK: - Request/Response Models

/// Request body for creating a new something
public struct SomethingCreate: Codable {
    public let content: String?
    public let contentType: ContentType
    public let mediaUrl: String?
    
    public init(content: String?, contentType: ContentType, mediaUrl: String?) {
        self.content = content
        self.contentType = contentType
        self.mediaUrl = mediaUrl
    }
}

/// Request body for updating something meaning
public struct SomethingUpdateMeaning: Codable {
    public let meaning: String

    public init(meaning: String) {
        self.meaning = meaning
    }
}
