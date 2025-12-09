//
//  ContentView.swift
//  Pookie
//
//  Created by Sudhir V on 12/3/25.
//

import SwiftUI

/// Root view that conditionally displays AuthView or HomeView based on authentication state.
/// Navigation updates automatically when AppState.isAuthenticated changes.
struct ContentView: View {
    // MARK: - State

    @Environment(AppState.self) private var appState

    // MARK: - Body

    var body: some View {
        Group {
            if appState.isLoading {
                // Show loading while checking session
                ProgressView("Loading...")
            } else if appState.isAuthenticated {
                HomeView()
            } else {
                AuthView()
            }
        }
    }
}

#Preview {
    ContentView()
        .environment(AppState())
}
