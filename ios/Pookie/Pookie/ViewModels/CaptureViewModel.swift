//
//  CaptureViewModel.swift
//  Pookie
//
//  Created by Dev Agent on 12/6/25.
//

import Foundation
import Observation

// MARK: - Capture ViewModel

@Observable
public class CaptureViewModel {
    // MARK: - Properties

    public var somethingText: String = ""
    public var isSaving: Bool = false
    public var error: String?
    public var successMessage: String?
    public var needsReauthentication: Bool = false
    public var lastCreatedSomething: Something?

    private var dismissTask: Task<Void, Never>?

    // MARK: - Computed Properties

    public var characterCount: Int {
        somethingText.count
    }

    public var canSave: Bool {
        !somethingText.isEmpty && somethingText.count <= 10000 && !isSaving
    }

    // MARK: - Initialization

    public init() {}

    // MARK: - Methods

    public func saveSomething() async {
        guard canSave else { return }

        isSaving = true
        error = nil
        successMessage = nil
        needsReauthentication = false

        do {
            let something = try await APIService.shared.createSomething(
                content: somethingText,
                contentType: .text
            )
            
            // Store the created something to display predictions
            lastCreatedSomething = something
            print(something)

            // Success - clear text and show confirmation
            somethingText = ""
            successMessage = "Saved!"

            // Auto-dismiss success message after 5 seconds (longer to see predictions)
            // Cancel any previous dismiss task to prevent race conditions
            dismissTask?.cancel()
            dismissTask = Task {
                try? await Task.sleep(nanoseconds: 5_000_000_000)
                if !Task.isCancelled {
                    await MainActor.run {
                        successMessage = nil
                        lastCreatedSomething = nil // Clear predictions too
                    }
                }
            }
        } catch APIError.unauthorized {
            // Special handling for auth errors - signal need for re-authentication
            self.error = "Session expired. Please log in again."
            self.needsReauthentication = true
        } catch {
            self.error = error.localizedDescription
        }

        isSaving = false
    }

    // MARK: - Cleanup

    deinit {
        dismissTask?.cancel()
    }
}
