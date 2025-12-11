//
//  Action.swift
//  Pookie
//
//  Created by Dev Agent on 12/9/25.
//

import Foundation

// MARK: - Action Model

public struct Action: Codable, Identifiable, Equatable {
    public let id: Int
    public let userId: String
    public let actionText: String
    public let timeElapsed: Int
    public let completedAt: Date
    public let createdAt: Date
    public let updatedAt: Date
}

// MARK: - Request Models

public struct ActionCreate: Codable {
    public let actionText: String
    public let timeElapsed: Int
    public let intentionIds: [Int]?

    public init(actionText: String, timeElapsed: Int, intentionIds: [Int]? = nil) {
        self.actionText = actionText
        self.timeElapsed = timeElapsed
        self.intentionIds = intentionIds
    }
}
