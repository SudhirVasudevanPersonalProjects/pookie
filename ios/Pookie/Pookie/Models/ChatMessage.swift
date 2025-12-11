//
//  ChatMessage.swift
//  Pookie
//
//  Model for chat messages.
//

import Foundation

struct ChatMessage: Identifiable, Equatable {
    let id = UUID()
    let content: String
    let isUser: Bool
    let circlesUsed: [String]
    let timestamp: Date

    init(content: String, isUser: Bool, circlesUsed: [String] = [], timestamp: Date = Date()) {
        self.content = content
        self.isUser = isUser
        self.circlesUsed = circlesUsed
        self.timestamp = timestamp
    }
}
