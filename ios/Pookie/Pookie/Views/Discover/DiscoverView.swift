//
//  DiscoverView.swift
//  Pookie
//
//  Created by Dev Agent on 12/6/25.
//

import SwiftUI

/// Placeholder view for personalized discovery and recommendations.
/// Uses taste profile analysis and RAG-LLM for personalized suggestions.
/// This feature will be implemented in Epic 5.
struct DiscoverView: View {
    // MARK: - Body

    var body: some View {
        NavigationStack {
            VStack(spacing: 16) {
                Text("Discover new experiences")
                    .font(.body)
                    .foregroundColor(.primary)
                    .accessibilityIdentifier("discoverDescriptionText")

                Text("(Coming in Epic 5)")
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .accessibilityIdentifier("discoverEpicIndicator")
            }
            .navigationTitle("Discover")
            .accessibilityIdentifier("discoverView")
        }
    }
}

// MARK: - Preview

#Preview {
    DiscoverView()
        .environment(AppState())
}
