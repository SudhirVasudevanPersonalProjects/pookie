//
//  ActionViewModel.swift
//  Pookie
//
//  Created by Dev Agent on 12/9/25.
//

import Foundation
import SwiftUI
public import Combine

@MainActor
public class ActionViewModel: ObservableObject {
    @Published public var actions: [Action] = []
    @Published public var isLoading = false
    @Published public var errorMessage: String?

    private let apiService = APIService.shared

    public init() {}

    // MARK: - CRUD Operations

    public func loadActions() async {
        isLoading = true
        errorMessage = nil

        do {
            actions = try await apiService.listActions()
        } catch {
            errorMessage = error.localizedDescription
        }

        isLoading = false
    }

    public func createAction(text: String, timeElapsed: Int, intentionIds: [Int]? = nil) async {
        isLoading = true
        errorMessage = nil

        do {
            let newAction = try await apiService.createAction(
                actionText: text,
                timeElapsed: timeElapsed,
                intentionIds: intentionIds
            )
            actions.insert(newAction, at: 0)
        } catch {
            errorMessage = error.localizedDescription
        }

        isLoading = false
    }

    // MARK: - Helper Methods

    public func totalTimeForIntention(intentionId: Int, intentionDetail: IntentionDetail) -> Int {
        intentionDetail.linkedActions.reduce(0) { $0 + $1.timeElapsed }
    }
}
