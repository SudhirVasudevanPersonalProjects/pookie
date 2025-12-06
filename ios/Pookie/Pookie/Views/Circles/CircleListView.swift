//
//  CircleListView.swift
//  Pookie
//
//  Created by Dev Agent on 12/6/25.
//

import SwiftUI

/// Placeholder view for displaying user's circles of care (semantic clusters).
/// Circles (formerly "Abodes") are FAISS-clustered semantic groups of thoughts.
/// This feature will be implemented in Epic 4.
struct CircleListView: View {
    // MARK: - Body

    var body: some View {
        NavigationStack {
            VStack(spacing: 16) {
                Text("Your circles of care will appear here")
                    .font(.body)
                    .foregroundColor(.primary)
                    .accessibilityIdentifier("circlesDescriptionText")

                Text("(Coming in Epic 4)")
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .accessibilityIdentifier("circlesEpicIndicator")
            }
            .navigationTitle("Circles")
            .accessibilityIdentifier("circleListView")
        }
    }
}

// MARK: - Preview

#Preview {
    CircleListView()
        .environment(AppState())
}
