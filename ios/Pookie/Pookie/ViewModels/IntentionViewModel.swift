//
//  IntentionViewModel.swift
//  Pookie
//
//  Created by Dev Agent on 12/9/25.
//

import Foundation
import SwiftUI
public import Combine

@MainActor
public class IntentionViewModel: ObservableObject {
    @Published public var intentions: [Intention] = []
    @Published public var isLoading = false
    @Published public var errorMessage: String?

    private let apiService = APIService.shared

    public init() {}

    // MARK: - CRUD Operations

    public func loadIntentions() async {
        isLoading = true
        errorMessage = nil

        do {
            intentions = try await apiService.listIntentions()
        } catch {
            errorMessage = error.localizedDescription
        }

        isLoading = false
    }

    public func createIntention(text: String) async {
        isLoading = true
        errorMessage = nil

        do {
            let newIntention = try await apiService.createIntention(intentionText: text)
            intentions.insert(newIntention, at: 0)
        } catch {
            errorMessage = error.localizedDescription
        }

        isLoading = false
    }

    public func getIntentionDetail(intentionId: Int) async -> IntentionDetail? {
        do {
            return try await apiService.getIntentionDetail(intentionId: intentionId)
        } catch {
            errorMessage = error.localizedDescription
            return nil
        }
    }

    // MARK: - Computed Properties

    public var activeIntentions: [Intention] {
        intentions.filter { $0.status == .active }
    }

    public var completedIntentions: [Intention] {
        intentions.filter { $0.status == .completed }
    }

    public var archivedIntentions: [Intention] {
        intentions.filter { $0.status == .archived }
    }
}
