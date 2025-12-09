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
            VStack(spacing: 16) {
                // Text editor with placeholder
                TextEditor(text: $viewModel.somethingText)
                    .frame(minHeight: 200)
                    .padding(8)
                    .background(Color(.systemGray6))
                    .cornerRadius(8)
                    .overlay(
                        Group {
                            if viewModel.somethingText.isEmpty {
                                Text("What's on your mind?")
                                    .foregroundColor(.secondary)
                                    .padding(.top, 16)
                                    .padding(.leading, 12)
                                    .allowsHitTesting(false)
                            }
                        },
                        alignment: .topLeading
                    )
                    .accessibilityLabel("Something text input")
                    .accessibilityHint("Type your thought or idea here")
                    .accessibilityValue(viewModel.somethingText.isEmpty ? "Empty" : viewModel.somethingText)

                // Error or success message only
                if let error = viewModel.error {
                    HStack {
                        Image(systemName: "exclamationmark.circle.fill")
                            .foregroundColor(.red)
                        Text(error)
                            .font(.subheadline)
                            .foregroundColor(.red)
                    }
                    .padding()
                    .background(Color.red.opacity(0.1))
                    .cornerRadius(8)
                } else if let success = viewModel.successMessage {
                    HStack {
                        Image(systemName: "checkmark.circle.fill")
                            .foregroundColor(.green)
                        Text(success)
                            .font(.subheadline)
                            .foregroundColor(.green)
                    }
                    .padding()
                    .background(Color.green.opacity(0.1))
                    .cornerRadius(8)
                    .transition(.opacity.combined(with: .scale))
                }

                // Save button
                Button(action: {
                    // Dismiss keyboard before saving
                    UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)

                    Task {
                        await viewModel.saveSomething()
                    }
                }) {
                    if viewModel.isSaving {
                        ProgressView()
                            .frame(maxWidth: .infinity)
                            .accessibilityLabel("Saving")
                    } else {
                        Text("Save")
                            .frame(maxWidth: .infinity)
                    }
                }
                .buttonStyle(.borderedProminent)
                .disabled(!viewModel.canSave)
                .accessibilityLabel(viewModel.canSave ? "Save something" : "Save button disabled")
                .accessibilityHint(viewModel.canSave ? "Saves your thought" : "Enter text to enable save")

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
        }
    }
}

// MARK: - Preview

#Preview {
    CaptureView()
        .environment(AppState())
}
