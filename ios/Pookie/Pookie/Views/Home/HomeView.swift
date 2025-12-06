//
//  HomeView.swift
//  Pookie
//
//  Created by Dev Agent on 12/5/25.
//

import SwiftUI

/// Main navigation container providing tab-based access to 4 core app sections.
/// Displays after successful authentication. Each tab contains an independent NavigationStack.
/// Tabs: Capture (Epic 2), Circles (Epic 4), Discover (Epic 5), Chat (Epic 6).
struct HomeView: View {
    // MARK: - Properties

    @Environment(AppState.self) private var appState
    @State private var selectedTab = 0

    // MARK: - Body

    var body: some View {
        TabView(selection: $selectedTab) {
            CaptureView()
                .tabItem {
                    Label("Capture", systemImage: "pencil")
                }
                .tag(0)
                .accessibilityIdentifier("captureTab")

            CircleListView()
                .tabItem {
                    Label("Circles", systemImage: "folder")
                }
                .tag(1)
                .accessibilityIdentifier("circlesTab")

            DiscoverView()
                .tabItem {
                    Label("Discover", systemImage: "sparkles")
                }
                .tag(2)
                .accessibilityIdentifier("discoverTab")

            ChatView()
                .tabItem {
                    Label("Chat", systemImage: "message")
                }
                .tag(3)
                .accessibilityIdentifier("chatTab")
        }
        .accessibilityIdentifier("homeTabView")
    }
}

// MARK: - Preview

#Preview {
    HomeView()
        .environment(AppState())
}
