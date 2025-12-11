//
//  Intention.swift
//  Pookie
//
//  Created by Dev Agent on 12/9/25.
//

import Foundation

// MARK: - Intention Status Enum

public enum IntentionStatus: String, Codable, CaseIterable {
    case active
    case completed
    case archived
}

// MARK: - Intention Model

public struct Intention: Codable, Identifiable, Equatable {
    public let id: Int
    public let userId: String
    public let intentionText: String
    public let status: IntentionStatus
    public let createdAt: Date
    public let updatedAt: Date
}

// MARK: - Brief Models for Relations

public struct SomethingBrief: Codable, Identifiable, Equatable {
    public let id: Int
    public let content: String?
    public let meaning: String?
}

public struct ActionBrief: Codable, Identifiable, Equatable {
    public let id: Int
    public let actionText: String
    public let timeElapsed: Int
    public let completedAt: Date
}

// MARK: - Intention Detail Response

public struct IntentionDetail: Codable, Identifiable, Equatable {
    public let id: Int
    public let userId: String
    public let intentionText: String
    public let status: IntentionStatus
    public let createdAt: Date
    public let updatedAt: Date
    public let linkedSomethings: [SomethingBrief]
    public let linkedActions: [ActionBrief]
}

// MARK: - Request Models

public struct IntentionCreate: Codable {
    public let intentionText: String

    public init(intentionText: String) {
        self.intentionText = intentionText
    }
}

public struct IntentionUpdate: Codable {
    public let intentionText: String?
    public let status: IntentionStatus?

    public init(intentionText: String? = nil, status: IntentionStatus? = nil) {
        self.intentionText = intentionText
        self.status = status
    }
}

public struct IntentionCareLinkRequest: Codable {
    public let somethingIds: [Int]

    public init(somethingIds: [Int]) {
        self.somethingIds = somethingIds
    }
}
