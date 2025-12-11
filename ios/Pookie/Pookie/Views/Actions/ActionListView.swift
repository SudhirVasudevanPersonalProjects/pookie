//
//  ActionListView.swift
//  Pookie
//
//  Created by Dev Agent on 12/9/25.
//

import SwiftUI

struct ActionListView: View {
    @StateObject private var viewModel = ActionViewModel()
    @StateObject private var intentionViewModel = IntentionViewModel()
    @State private var showingCreateSheet = false
    @State private var newActionText = ""
    @State private var newActionTimeElapsed = 15
    @State private var selectedIntentionIds: Set<Int> = []

    var body: some View {
        NavigationView {
            ZStack {
                if viewModel.isLoading && viewModel.actions.isEmpty {
                    ProgressView("Loading actions...")
                } else {
                    List {
                        if !viewModel.actions.isEmpty {
                            ForEach(viewModel.actions) { action in
                                ActionRowView(action: action)
                            }
                        } else if !viewModel.isLoading {
                            Text("No actions yet. Tap + to log your first action.")
                                .foregroundColor(.secondary)
                                .italic()
                        }
                    }
                }
            }
            .navigationTitle("Actions")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showingCreateSheet = true }) {
                        Image(systemName: "plus")
                    }
                }
            }
            .sheet(isPresented: $showingCreateSheet) {
                CreateActionSheet(
                    actionText: $newActionText,
                    timeElapsed: $newActionTimeElapsed,
                    availableIntentions: intentionViewModel.activeIntentions,
                    selectedIntentionIds: $selectedIntentionIds,
                    onSave: {
                        Task {
                            await viewModel.createAction(
                                text: newActionText,
                                timeElapsed: newActionTimeElapsed,
                                intentionIds: Array(selectedIntentionIds)
                            )
                            newActionText = ""
                            newActionTimeElapsed = 15
                            selectedIntentionIds.removeAll()
                            showingCreateSheet = false
                        }
                    },
                    onCancel: {
                        newActionText = ""
                        newActionTimeElapsed = 15
                        selectedIntentionIds.removeAll()
                        showingCreateSheet = false
                    }
                )
            }
            .task {
                await viewModel.loadActions()
                await intentionViewModel.loadIntentions()
            }
            .alert("Error", isPresented: .constant(viewModel.errorMessage != nil)) {
                Button("OK") { viewModel.errorMessage = nil }
            } message: {
                Text(viewModel.errorMessage ?? "")
            }
        }
    }
}

struct ActionRowView: View {
    let action: Action

    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(action.actionText)
                    .font(.body)

                Text(action.completedAt, style: .date)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            Spacer()

            Text("\(action.timeElapsed) min")
                .font(.subheadline)
                .fontWeight(.semibold)
                .foregroundColor(.blue)
        }
        .padding(.vertical, 4)
    }
}

struct CreateActionSheet: View {
    @Binding var actionText: String
    @Binding var timeElapsed: Int
    let availableIntentions: [Intention]
    @Binding var selectedIntentionIds: Set<Int>
    let onSave: () -> Void
    let onCancel: () -> Void

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Action Details")) {
                    TextField("What did you do?", text: $actionText)
                        .textFieldStyle(.plain)

                    Stepper("Time: \(timeElapsed) minutes", value: $timeElapsed, in: 1...360, step: 5)
                }

                if !availableIntentions.isEmpty {
                    Section(header: Text("Link to Intentions (Optional)")) {
                        ForEach(availableIntentions) { intention in
                            Button(action: {
                                if selectedIntentionIds.contains(intention.id) {
                                    selectedIntentionIds.remove(intention.id)
                                } else {
                                    selectedIntentionIds.insert(intention.id)
                                }
                            }) {
                                HStack {
                                    Text(intention.intentionText)
                                        .foregroundColor(.primary)
                                    Spacer()
                                    if selectedIntentionIds.contains(intention.id) {
                                        Image(systemName: "checkmark")
                                            .foregroundColor(.blue)
                                    }
                                }
                            }
                        }
                    }
                }

                Section {
                    Text("Actions are time-tracked activities that contribute to your intentions.")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            .navigationTitle("New Action")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel", action: onCancel)
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Save", action: onSave)
                        .disabled(actionText.trimmingCharacters(in: .whitespaces).isEmpty)
                }
            }
        }
    }
}
