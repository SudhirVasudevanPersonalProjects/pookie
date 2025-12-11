//
//  IntentionDetailView.swift
//  Pookie
//
//  Created by Dev Agent on 12/9/25.
//

import SwiftUI

struct IntentionDetailView: View {
    let intentionId: Int
    @StateObject private var viewModel = IntentionViewModel()
    @State private var intentionDetail: IntentionDetail?
    @State private var isLoading = true

    var body: some View {
        ZStack {
            if isLoading {
                ProgressView("Loading...")
            } else if let detail = intentionDetail {
                ScrollView {
                    VStack(alignment: .leading, spacing: 20) {
                        // Header
                        VStack(alignment: .leading, spacing: 8) {
                            Text(detail.intentionText)
                                .font(.title2)
                                .fontWeight(.bold)

                            HStack {
                                StatusBadge(status: detail.status)
                                Spacer()
                                Text("Created \(detail.createdAt, style: .date)")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                        }
                        .padding()
                        .background(Color(uiColor: .secondarySystemBackground))
                        .cornerRadius(12)

                        // Linked Somethings (Cares)
                        if !detail.linkedSomethings.isEmpty {
                            VStack(alignment: .leading, spacing: 12) {
                                Text("Related Somethings")
                                    .font(.headline)

                                ForEach(detail.linkedSomethings) { something in
                                    VStack(alignment: .leading, spacing: 4) {
                                        if let content = something.content {
                                            Text(content)
                                                .font(.body)
                                        }
                                        if let meaning = something.meaning {
                                            Text(meaning)
                                                .font(.caption)
                                                .foregroundColor(.secondary)
                                        }
                                    }
                                    .padding()
                                    .frame(maxWidth: .infinity, alignment: .leading)
                                    .background(Color(uiColor: .tertiarySystemBackground))
                                    .cornerRadius(8)
                                }
                            }
                        }

                        // Linked Actions
                        if !detail.linkedActions.isEmpty {
                            VStack(alignment: .leading, spacing: 12) {
                                HStack {
                                    Text("Actions")
                                        .font(.headline)
                                    Spacer()
                                    Text("\(totalTime(detail.linkedActions)) min total")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                }

                                ForEach(detail.linkedActions) { action in
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
                                            .foregroundColor(.blue)
                                    }
                                    .padding()
                                    .background(Color(uiColor: .tertiarySystemBackground))
                                    .cornerRadius(8)
                                }
                            }
                        }

                        if detail.linkedSomethings.isEmpty && detail.linkedActions.isEmpty {
                            Text("No somethings or actions linked yet.")
                                .foregroundColor(.secondary)
                                .italic()
                                .frame(maxWidth: .infinity, alignment: .center)
                                .padding()
                        }
                    }
                    .padding()
                }
            } else {
                Text("Failed to load intention details")
                    .foregroundColor(.secondary)
            }
        }
        .navigationTitle("Intention")
        .navigationBarTitleDisplayMode(.inline)
        .task {
            intentionDetail = await viewModel.getIntentionDetail(intentionId: intentionId)
            isLoading = false
        }
    }

    private func totalTime(_ actions: [ActionBrief]) -> Int {
        actions.reduce(0) { $0 + $1.timeElapsed }
    }
}

struct StatusBadge: View {
    let status: IntentionStatus

    var body: some View {
        Text(status.rawValue.capitalized)
            .font(.caption)
            .fontWeight(.semibold)
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(badgeColor)
            .foregroundColor(.white)
            .cornerRadius(6)
    }

    private var badgeColor: Color {
        switch status {
        case .active:
            return .green
        case .completed:
            return .blue
        case .archived:
            return .gray
        }
    }
}
