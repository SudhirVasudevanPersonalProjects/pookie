//
//  Circle.swift
//  Pookie
//
//  Created by Dev Agent on 12/9/25.
//

import Foundation

// MARK: - Circle Model

public struct Circle: Codable, Identifiable, Equatable {
    public let id: Int
    public let userId: String
    public let circleName: String
    public let description: String?
    public let careFrequency: Int
    public let centroidEmbedding: [Float]?
    public let createdAt: Date
    public let updatedAt: Date
}

// MARK: - Request/Response Models

public struct CircleCreate: Codable {
    public let circleName: String
    public let description: String?
    public let careFrequency: Int?

    public init(circleName: String, description: String? = nil, careFrequency: Int? = nil) {
        self.circleName = circleName
        self.description = description
        self.careFrequency = careFrequency
    }
}

public struct CircleUpdate: Codable {
    public let circleName: String?
    public let description: String?
    public let careFrequency: Int?

    public init(circleName: String? = nil, description: String? = nil, careFrequency: Int? = nil) {
        self.circleName = circleName
        self.description = description
        self.careFrequency = careFrequency
    }
}

// MARK: - Similar Something Suggestion

public struct SimilarSomethingSuggestion: Codable, Identifiable, Equatable {
    public let somethingId: Int
    public let content: String
    public let similarity: Double

    public var id: Int { somethingId }
}

public struct SuggestionsResponse: Codable {
    public let suggestions: [SimilarSomethingSuggestion]
}
