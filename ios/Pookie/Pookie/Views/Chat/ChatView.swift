//
//  ChatView.swift
//  Pookie
//
//  Created by Dev Agent on 12/6/25.
//

import SwiftUI

/// Placeholder view for RAG-powered personal chat with Claude Haiku.
/// Provides streaming chat interface with vector search over user's thoughts.
/// This feature will be implemented in Epic 6.
struct ChatView: View {
    // MARK: - Body

    var body: some View {
        NavigationStack {
            VStack(spacing: 16) {
                Text("Chat with Pookie, your personal LLM")
                    .font(.body)
                    .foregroundColor(.primary)
                    .accessibilityIdentifier("chatDescriptionText")

                Text("(Coming in Epic 6)")
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .accessibilityIdentifier("chatEpicIndicator")
            }
            .navigationTitle("Chat")
            .accessibilityIdentifier("chatView")
        }
    }
}

// MARK: - Preview

#Preview {
    ChatView()
        .environment(AppState())
}
