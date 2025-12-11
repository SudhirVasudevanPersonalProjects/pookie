//
//  ChatViewModel.swift
//  Pookie
//
//  ViewModel for chat interface with SSE streaming.
//

import Foundation
import Observation

@Observable
class ChatViewModel {
    var messages: [ChatMessage] = []
    var isStreaming = false
    var currentResponse = ""
    var errorMessage: String?

    private let apiService: APIService
    private var sseClient: SSEClient?

    init(apiService: APIService = APIService.shared) {
        self.apiService = apiService
    }

    /// Send a chat message and stream the response
    func sendMessage(_ query: String) {
        guard !query.trimmingCharacters(in: .whitespaces).isEmpty else { return }

        // Add user message
        let userMessage = ChatMessage(content: query, isUser: true)
        messages.append(userMessage)

        // Start streaming response
        isStreaming = true
        currentResponse = ""
        errorMessage = nil

        // Build request
        Task {
            do {
                let token = try await apiService.getAuthToken()
                guard let url = URL(string: "\(apiService.apiBaseURL)/chat/stream") else {
                    handleError("Invalid URL")
                    return
                }

                await sendStreamRequest(url: url, token: token, query: query)
            } catch {
                handleError("Authentication required")
            }
        }
    }

    private func sendStreamRequest(url: URL, token: String, query: String) async {
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("text/event-stream", forHTTPHeaderField: "Accept")

        let body: [String: Any] = [
            "query": query,
            "top_k": 10
        ]

        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: body)
        } catch {
            await MainActor.run {
                handleError("Failed to encode request: \(error.localizedDescription)")
            }
            return
        }

        // Use SSEClient for streaming
        await MainActor.run {
            sseClient = SSEClient()
        }
        var accumulatedCircles: [String] = []

        sseClient?.stream(
            request: request,
            onEvent: { [weak self] event in
                DispatchQueue.main.async {
                    guard let self = self else { return }

                    switch event {
                    case .token(let token):
                        self.currentResponse += token

                    case .done(let circles):
                        accumulatedCircles = circles
                        self.finishStreaming(circles: circles)

                    case .error(let error):
                        self.handleError(error)
                    }
                }
            },
            onComplete: { [weak self] in
                DispatchQueue.main.async {
                    // Stream completed
                    if self?.isStreaming == true && !accumulatedCircles.isEmpty {
                        self?.finishStreaming(circles: accumulatedCircles)
                    }
                }
            }
        )
    }

    private func finishStreaming(circles: [String]) {
        guard !currentResponse.isEmpty else {
            isStreaming = false
            return
        }

        let assistantMessage = ChatMessage(
            content: currentResponse,
            isUser: false,
            circlesUsed: circles
        )
        messages.append(assistantMessage)

        currentResponse = ""
        isStreaming = false
    }

    private func handleError(_ message: String) {
        errorMessage = message
        isStreaming = false
        currentResponse = ""
    }

    /// Cancel active streaming
    func cancelStreaming() {
        sseClient?.cancel()
        isStreaming = false
        currentResponse = ""
    }

    /// Clear all messages
    func clearMessages() {
        messages.removeAll()
        currentResponse = ""
        errorMessage = nil
    }
}
