//
//  IntentionListView.swift
//  Pookie
//
//  Created by Dev Agent on 12/9/25.
//

import SwiftUI

struct IntentionListView: View {
    @StateObject private var viewModel = IntentionViewModel()
    @State private var showingCreateSheet = false
    @State private var newIntentionText = ""

    var body: some View {
        NavigationView {
            ZStack {
                if viewModel.isLoading && viewModel.intentions.isEmpty {
                    ProgressView("Loading intentions...")
                } else {
                    List {
                        if !viewModel.activeIntentions.isEmpty {
                            Section(header: Text("Active")) {
                                ForEach(viewModel.activeIntentions) { intention in
                                    NavigationLink(destination: IntentionDetailView(intentionId: intention.id)) {
                                        IntentionRowView(intention: intention)
                                    }
                                }
                            }
                        }

                        if !viewModel.completedIntentions.isEmpty {
                            Section(header: Text("Completed")) {
                                ForEach(viewModel.completedIntentions) { intention in
                                    NavigationLink(destination: IntentionDetailView(intentionId: intention.id)) {
                                        IntentionRowView(intention: intention)
                                    }
                                }
                            }
                        }

                        if viewModel.intentions.isEmpty && !viewModel.isLoading {
                            Text("No intentions yet. Tap + to create your first intention.")
                                .foregroundColor(.secondary)
                                .italic()
                        }
                    }
                }
            }
            .navigationTitle("Intentions")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showingCreateSheet = true }) {
                        Image(systemName: "plus")
                    }
                }
            }
            .sheet(isPresented: $showingCreateSheet) {
                CreateIntentionSheet(
                    intentionText: $newIntentionText,
                    onSave: {
                        Task {
                            await viewModel.createIntention(text: newIntentionText)
                            newIntentionText = ""
                            showingCreateSheet = false
                        }
                    },
                    onCancel: {
                        newIntentionText = ""
                        showingCreateSheet = false
                    }
                )
            }
            .task {
                await viewModel.loadIntentions()
            }
            .alert("Error", isPresented: .constant(viewModel.errorMessage != nil)) {
                Button("OK") { viewModel.errorMessage = nil }
            } message: {
                Text(viewModel.errorMessage ?? "")
            }
        }
    }
}

struct IntentionRowView: View {
    let intention: Intention

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(intention.intentionText)
                .font(.body)

            HStack {
                Text(intention.status.rawValue.capitalized)
                    .font(.caption)
                    .foregroundColor(.secondary)

                Spacer()

                Text(intention.createdAt, style: .date)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}

struct CreateIntentionSheet: View {
    @Binding var intentionText: String
    let onSave: () -> Void
    let onCancel: () -> Void

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Intention")) {
                    TextField("What do you want to achieve?", text: $intentionText)
                        .textFieldStyle(.plain)
                }

                Section {
                    Text("Intentions are action-oriented goals that guide your daily actions.")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            .navigationTitle("New Intention")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel", action: onCancel)
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Save", action: onSave)
                        .disabled(intentionText.trimmingCharacters(in: .whitespaces).isEmpty)
                }
            }
        }
    }
}
