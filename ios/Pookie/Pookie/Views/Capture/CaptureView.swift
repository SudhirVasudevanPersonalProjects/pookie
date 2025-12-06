//
//  CaptureView.swift
//  Pookie
//
//  Created by Dev Agent on 12/6/25.
//

import SwiftUI

/// Placeholder view for capturing user thoughts (voice and text).
/// This feature will be implemented in Epic 2. Provides navigation
/// structure and preview of the capture functionality.
struct CaptureView: View {
    // MARK: - Body

    var body: some View {
        NavigationStack {
            VStack(spacing: 16) {
                Text("Capture your thoughts here")
                    .font(.body)
                    .foregroundColor(.primary)
                    .accessibilityIdentifier("captureDescriptionText")

                Text("(Coming in Epic 2)")
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .accessibilityIdentifier("captureEpicIndicator")
            }
            .navigationTitle("Capture")
            .accessibilityIdentifier("captureView")
        }
    }
}

// MARK: - Preview

#Preview {
    CaptureView()
        .environment(AppState())
}
