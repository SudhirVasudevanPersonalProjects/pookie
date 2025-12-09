//
//  PookieApp.swift
//  Pookie
//
//  Created by Sudhir V on 12/3/25.
//

import SwiftUI

@main
struct PookieApp: App {
    @State private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(appState)
        }
    }
}
