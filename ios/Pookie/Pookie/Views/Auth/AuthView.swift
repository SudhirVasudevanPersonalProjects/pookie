//
//  AuthView.swift
//  Pookie
//
//  Created by Dev Agent on 12/5/25.
//

import SwiftUI
import Auth

/// Authentication screen with sign in and sign up functionality.
/// Provides tabbed interface for user authentication using email and password.
struct AuthView: View {
    // MARK: - State

    @Environment(AppState.self) private var appState

    @State private var email: String = ""
    @State private var password: String = ""
    @State private var isLoading: Bool = false
    @State private var error: String? = nil
    @State private var selectedTab: AuthTab = .signIn

    // MARK: - Body

    var body: some View {
        VStack(spacing: 20) {
            // Title
            Text("Welcome to Pookie")
                .font(.largeTitle)
                .fontWeight(.bold)
                .padding(.top, 40)

            // Tab Picker
            Picker("Auth Type", selection: $selectedTab) {
                Text("Sign In").tag(AuthTab.signIn)
                Text("Sign Up").tag(AuthTab.signUp)
            }
            .pickerStyle(.segmented)
            .padding(.horizontal)

            // Form
            VStack(spacing: 16) {
                // Email Field
                TextField("Email", text: $email)
                    .textInputAutocapitalization(.never)
                    .keyboardType(.emailAddress)
                    .autocorrectionDisabled()
                    .textFieldStyle(.roundedBorder)
                    .disabled(isLoading)

                // Password Field
                SecureField("Password", text: $password)
                    .textFieldStyle(.roundedBorder)
                    .disabled(isLoading)

                // Password Hint
                Text("Password must be at least 8 characters")
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, alignment: .leading)

                // Error Message
                if let error = error {
                    Text(error)
                        .foregroundColor(.red)
                        .font(.caption)
                        .multilineTextAlignment(.center)
                }

                // Submit Button
                Button(action: {
                    Task {
                        await authenticate()
                    }
                }) {
                    Text(selectedTab == .signIn ? "Sign In" : "Sign Up")
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(buttonDisabled ? Color.gray : Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
                .disabled(buttonDisabled)

                // Loading Indicator
                if isLoading {
                    ProgressView()
                        .progressViewStyle(.circular)
                }
            }
            .padding(.horizontal, 24)

            Spacer()
        }
    }

    // MARK: - Computed Properties

    /// Button is disabled when loading or fields are empty
    private var buttonDisabled: Bool {
        isLoading || email.isEmpty || password.isEmpty
    }

    // MARK: - Actions

    /// Authenticate user (sign in or sign up based on selectedTab)
    private func authenticate() async {
        // Clear previous error
        error = nil
        isLoading = true

        defer {
            isLoading = false
        }

        do {
            let session: Session

            if selectedTab == .signIn {
                session = try await AuthService.shared.signIn(email: email, password: password)
            } else {
                session = try await AuthService.shared.signUp(email: email, password: password)
            }

            // Update AppState using helper method (NOT direct assignment)
            appState.setSession(session)

        } catch let authError as AuthError {
            // Display user-friendly error from AuthError.errorDescription
            error = authError.localizedDescription
        } catch let unexpectedError {
            // Fallback for unexpected errors
            error = unexpectedError.localizedDescription
        }
    }
}

// MARK: - Supporting Types

/// Authentication tab selection
private enum AuthTab {
    case signIn
    case signUp
}

// MARK: - Preview

#Preview {
    AuthView()
        .environment(AppState())
}
