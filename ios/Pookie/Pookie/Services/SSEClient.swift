//
//  SSEClient.swift
//  Pookie
//
//  Server-Sent Events client for streaming chat responses.
//  Supports both GET and POST requests for SSE streaming.
//

import Foundation

/// SSE event types from chat stream
enum SSEEvent {
    case token(String)
    case done(circlesUsed: [String])
    case error(String)
}

/// SSE client for streaming chat responses from backend
class SSEClient: NSObject {
    private var dataTask: URLSessionDataTask?
    private var buffer = ""
    private var onEvent: ((SSEEvent) -> Void)?
    private var onComplete: (() -> Void)?

    /// Stream SSE events from chat endpoint
    /// - Parameters:
    ///   - request: URLRequest (can be GET or POST)
    ///   - onEvent: Callback for each SSE event
    ///   - onComplete: Callback when stream completes
    func stream(
        request: URLRequest,
        onEvent: @escaping (SSEEvent) -> Void,
        onComplete: @escaping () -> Void
    ) {
        self.onEvent = onEvent
        self.onComplete = onComplete
        self.buffer = ""

        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 60
        config.timeoutIntervalForResource = 300

        let session = URLSession(configuration: config, delegate: self, delegateQueue: nil)

        dataTask = session.dataTask(with: request)
        dataTask?.resume()
    }

    /// Cancel active stream
    func cancel() {
        dataTask?.cancel()
        dataTask = nil
        buffer = ""
        onEvent = nil
        onComplete = nil
    }

    private func processBuffer() {
        // Process complete SSE events (terminated by \n\n)
        while let range = buffer.range(of: "\n\n") {
            let eventText = String(buffer[..<range.lowerBound])
            buffer.removeSubrange(...range.lowerBound)
            buffer.removeFirst()  // Remove the second \n

            if eventText.isEmpty { continue }

            // Parse SSE event
            if eventText.hasPrefix("data: ") {
                let dataString = String(eventText.dropFirst(6)) // Remove "data: "

                // Parse JSON
                if let data = dataString.data(using: .utf8),
                   let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any] {

                    if let token = json["token"] as? String {
                        onEvent?(.token(token))
                    } else if let done = json["done"] as? Bool, done == true {
                        let circles = (json["circles_used"] as? [String]) ?? []
                        onEvent?(.done(circlesUsed: circles))
                        onComplete?()
                    } else if let error = json["error"] as? String {
                        onEvent?(.error(error))
                        onComplete?()
                    }
                }
            }
        }
    }
}

// MARK: - URLSessionDataDelegate
extension SSEClient: URLSessionDataDelegate {
    func urlSession(_ session: URLSession, dataTask: URLSessionDataTask, didReceive data: Data) {
        if let text = String(data: data, encoding: .utf8) {
            buffer.append(text)
            processBuffer()
        }
    }

    func urlSession(_ session: URLSession, task: URLSessionTask, didCompleteWithError error: Error?) {
        if let error = error {
            onEvent?(.error(error.localizedDescription))
        }
        onComplete?()
    }
}
