//
//  CaptureView.swift
//  Pookie
//
//  Created by Dev Agent on 12/6/25.
//

import SwiftUI

/// Text capture UI for creating somethings.
/// Allows users to type thoughts and save them with AI-generated meaning.
struct CaptureView: View {
    @State private var viewModel = CaptureViewModel()
    @Environment(AppState.self) private var appState

    // MARK: - Body

    var body: some View {
        NavigationStack {
            mainContent
        }
    }

    // MARK: - View Components

    private var mainContent: some View {
        VStack(spacing: 16) {
            textEditor
            messageView
            suggestedCirclesIfAvailable
            saveButton
            Spacer()
        }
            .padding()
            .navigationTitle("Capture")
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button(action: {
                        Task {
                            do {
                                try await AuthService.shared.signOut()
                                appState.clearSession()
                            } catch {
                                viewModel.error = "Failed to sign out"
                            }
                        }
                    }) {
                        Image(systemName: "rectangle.portrait.and.arrow.right")
                            .foregroundColor(.red)
                    }
                    .accessibilityLabel("Sign out")
                }
            }
            .onTapGesture {
                // Dismiss keyboard when tapping outside TextEditor
                UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
            }
            .onChange(of: viewModel.needsReauthentication) { _, needsAuth in
                if needsAuth {
                    // Clear session when it expires (triggers login screen)
                    appState.clearSession()
                }
            }
            .animation(.easeInOut(duration: 0.3), value: viewModel.successMessage)
            .animation(.easeInOut(duration: 0.3), value: viewModel.lastCreatedSomething)
    }

    private var textEditor: some View {
        TextEditor(text: $viewModel.somethingText)
            .frame(minHeight: 200)
            .padding(8)
            .background(Color(.systemGray6))
            .cornerRadius(8)
            .overlay(placeholderText, alignment: .topLeading)
            .accessibilityLabel("Something text input")
            .accessibilityHint("Type your thought or idea here")
            .accessibilityValue(viewModel.somethingText.isEmpty ? "Empty" : viewModel.somethingText)
    }

    @ViewBuilder
    private var placeholderText: some View {
        if viewModel.somethingText.isEmpty {
            Text("What's on your mind?")
                .foregroundColor(.secondary)
                .padding(.top, 16)
                .padding(.leading, 12)
                .allowsHitTesting(false)
        }
    }

    @ViewBuilder
    private var messageView: some View {
        if let error = viewModel.error {
            MessageBanner(type: .error, message: error)
        } else if let success = viewModel.successMessage {
            MessageBanner(type: .success, message: success)
        }
    }

    @ViewBuilder
    private var suggestedCirclesIfAvailable: some View {
        if let something = viewModel.lastCreatedSomething,
        !something.suggestedCircles.isEmpty {
            SuggestedCirclesView(predictions: Array(viewModel.lastCreatedSomething!.suggestedCircles.prefix(3)))
        }
    }

    private var saveButton: some View {
        Button(action: saveAction) {
            saveButtonLabel
        }
        .buttonStyle(.borderedProminent)
        .disabled(!viewModel.canSave)
        .accessibilityLabel(viewModel.canSave ? "Save something" : "Save button disabled")
        .accessibilityHint(viewModel.canSave ? "Saves your thought" : "Enter text to enable save")
    }

    private func saveAction() {
        UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
        Task {
            await viewModel.saveSomething()
        }
    }

    @ViewBuilder
    private var saveButtonLabel: some View {
        if viewModel.isSaving {
            ProgressView()
                .frame(maxWidth: .infinity)
                .accessibilityLabel("Saving")
        } else {
            Text("Save")
                .frame(maxWidth: .infinity)
        }
    }
}

// MARK: - Message Banner

struct MessageBanner: View {
    enum MessageType {
        case error
        case success

        var icon: String {
            switch self {
            case .error: return "exclamationmark.circle.fill"
            case .success: return "checkmark.circle.fill"
            }
        }

        var color: Color {
            switch self {
            case .error: return .red
            case .success: return .green
            }
        }
    }

    let type: MessageType
    let message: String

    var body: some View {
        HStack {
            Image(systemName: type.icon)
                .foregroundColor(type.color)
            Text(message)
                .font(.subheadline)
                .foregroundColor(type.color)
        }
        .padding()
        .background(type.color.opacity(0.1))
        .cornerRadius(8)
        .transition(.opacity.combined(with: .scale))
    }
}

// MARK: - Suggested Circles Subview

struct SuggestedCirclesView: View {
    let predictions: [CirclePrediction]

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Predicted Circles:")
                .font(.subheadline)
                .fontWeight(.semibold)
                .foregroundColor(.secondary)

            ForEach(predictions, id: \.circleId) { prediction in
                predictionRow(for: prediction)
            }
        }
        .padding()
        .background(Color.blue.opacity(0.05))
        .cornerRadius(12)
        .transition(.move(edge: .bottom).combined(with: .opacity))
    }

    private func predictionRow(for prediction: CirclePrediction) -> some View {
        HStack {
            Image(systemName: "circle.fill")
                .font(.caption)
                .foregroundColor(.blue.opacity(0.6))

            Text(prediction.circleName)
                .font(.body)

            Spacer()

            confidenceBadge(for: prediction.confidence)
        }
        .padding(.vertical, 4)
    }

    private func confidenceBadge(for confidence: Double) -> some View {
        let percentage = Int(confidence * 100)
        return Text("\(percentage)%")
            .font(.caption)
            .foregroundColor(.secondary)
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(Color.blue.opacity(0.1))
            .cornerRadius(8)
    }
}

// MARK: - Preview

#Preview {
    CaptureView()
        .environment(AppState())
}
