//
//  APIService.swift
//  Pookie
//
//  Created by Dev Agent on 12/7/25.
//

import Foundation
import Supabase

/// Backend API service for something CRUD operations.
/// Provides type-safe methods for creating, listing, and updating somethings.
public class APIService {
    // MARK: - Singleton

    /// Shared instance (stateless - safe to share)
    public static let shared = APIService()

    /// Private init (enforces singleton pattern)
    private init() {
        // Load baseURL from Config.plist
        if let path = Bundle.main.path(forResource: "Config", ofType: "plist"),
           let config = NSDictionary(contentsOfFile: path) as? [String: Any],
           let apiBaseURL = config["APIBaseURL"] as? String {
            self.baseURL = apiBaseURL
            #if DEBUG
            print("[APIService] ✅ Loaded API Base URL: \(self.baseURL)")
            #endif
        } else {
            // Fallback to localhost for development if Config.plist is missing
            self.baseURL = "http://localhost:8080/api/v1"
            #if DEBUG
            print("[APIService] ⚠️ Could not load APIBaseURL from Config.plist, using default: \(self.baseURL)")
            #endif
        }

        // Configure URLSession with mobile-optimized timeout
        let configuration = URLSessionConfiguration.default
        configuration.timeoutIntervalForRequest = 15 // 15 seconds for mobile
        configuration.timeoutIntervalForResource = 30
        self.urlSession = URLSession(configuration: configuration)
    }

    // MARK: - Properties

    /// Backend API base URL (includes /api prefix)
    private let baseURL: String

    /// Public accessor for base URL (needed for chat streaming)
    public var apiBaseURL: String { baseURL }

    /// Custom URLSession with configured timeouts
    private let urlSession: URLSession

    /// Get current auth token from Supabase session
    public func getAuthToken() async throws -> String {
        let session = try await supabase.auth.session
        return session.accessToken
    }

    // MARK: - Something Endpoints

    /// Create a new something
    /// - Parameters:
    ///   - content: Text content (optional for non-text content types)
    ///   - contentType: Type of content (text, image, video, url)
    ///   - mediaUrl: URL for media content (optional)
    /// - Returns: Created Something with generated ID and metadata
    /// - Throws: APIError if request fails or unauthorized
    public func createSomething(content: String?, contentType: ContentType, mediaUrl: String? = nil) async throws -> Something {
        // Get session with proper error handling
        let session: Session
        do {
            session = try await supabase.auth.session
        } catch {
            #if DEBUG
            print("[APIService] Failed to get session: \(error)")
            #endif
            throw APIError.unauthorized
        }

        guard let url = URL(string: "\(baseURL)/somethings") else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body = SomethingCreate(content: content, contentType: contentType, mediaUrl: mediaUrl)
        request.httpBody = try JSONEncoder().encode(body)

        #if DEBUG
        print("[APIService] POST \(url.absoluteString)")
        #endif

        let (data, response) = try await urlSession.data(for: request)
        
        #if DEBUG
        if let jsonString = String(data: data, encoding: .utf8) {
            print("[DEBUG] RAW JSON RESPONSE: \(jsonString)")
        }
        #endif
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        #if DEBUG
        print("[APIService] Response status: \(httpResponse.statusCode)")
        #endif
    
        switch httpResponse.statusCode {
        case 201:
            #if DEBUG
            if let responseString = String(data: data, encoding: .utf8) {
                print("[APIService] Success response JSON: \(responseString)")
            }
            #endif
            do {
                return try configuredDecoder().decode(Something.self, from: data)
            } catch {
                #if DEBUG
                print("[APIService] Decoding error: \(error)")
                if let decodingError = error as? DecodingError {
                    switch decodingError {
                    case .keyNotFound(let key, let context):
                        print("Missing key: \(key.stringValue) - \(context.debugDescription)")
                    case .typeMismatch(let type, let context):
                        print("Type mismatch for type \(type) - \(context.debugDescription)")
                    case .valueNotFound(let type, let context):
                        print("Value not found for type \(type) - \(context.debugDescription)")
                    case .dataCorrupted(let context):
                        print("Data corrupted: \(context.debugDescription)")
                    @unknown default:
                        print("Unknown decoding error")
                    }
                }
                #endif
                throw error
            }
        case 401:
            throw APIError.unauthorized
        case 404:
            throw APIError.notFound
        default:
            #if DEBUG
            if let responseString = String(data: data, encoding: .utf8) {
                print("[APIService] Error response: \(responseString)")
            }
            #endif
            throw APIError.serverError("Failed to create something")
        }
    }

    /// List somethings for current user with pagination
    /// - Parameters:
    ///   - skip: Number of records to skip (default: 0)
    ///   - limit: Maximum records to return (default: 100)
    /// - Returns: Array of Something objects ordered by creation date
    /// - Throws: APIError if request fails or unauthorized
    public func listSomethings(skip: Int = 0, limit: Int = 100) async throws -> [Something] {
        // Validate pagination parameters
        guard skip >= 0 else {
            throw APIError.invalidParameters("skip must be >= 0")
        }
        guard limit > 0 && limit <= 100 else {
            throw APIError.invalidParameters("limit must be between 1 and 100")
        }

        // Get session with proper error handling
        let session: Session
        do {
            session = try await supabase.auth.session
        } catch {
            #if DEBUG
            print("[APIService] Failed to get session: \(error)")
            #endif
            throw APIError.unauthorized
        }

        // Build URL with safe query parameter encoding
        guard var urlComponents = URLComponents(string: "\(baseURL)/api/v1/somethings") else {
            throw APIError.invalidURL
        }
        urlComponents.queryItems = [
            URLQueryItem(name: "skip", value: String(skip)),
            URLQueryItem(name: "limit", value: String(limit))
        ]
        guard let url = urlComponents.url else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")

        #if DEBUG
        print("[APIService] GET \(url.absoluteString)")
        #endif

        let (data, response) = try await urlSession.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        #if DEBUG
        print("[APIService] Response status: \(httpResponse.statusCode)")
        #endif

        switch httpResponse.statusCode {
        case 200:
            return try configuredDecoder().decode([Something].self, from: data)
        case 401:
            throw APIError.unauthorized
        case 404:
            throw APIError.notFound
        default:
            #if DEBUG
            if let responseString = String(data: data, encoding: .utf8) {
                print("[APIService] Error response: \(responseString)")
            }
            #endif
            throw APIError.serverError("Failed to list somethings")
        }
    }

    /// Update the meaning of a something
    /// - Parameters:
    ///   - somethingId: ID of the something to update
    ///   - meaning: New meaning text (user-edited)
    /// - Returns: Updated Something with isMeaningUserEdited = true
    /// - Throws: APIError if request fails or unauthorized
    public func updateMeaning(somethingId: Int, meaning: String) async throws -> Something {
        // Get session with proper error handling
        let session: Session
        do {
            session = try await supabase.auth.session
        } catch {
            #if DEBUG
            print("[APIService] Failed to get session: \(error)")
            #endif
            throw APIError.unauthorized
        }

        guard let url = URL(string: "\(baseURL)/api/v1/somethings/\(somethingId)/meaning") else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = "PATCH"
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body = SomethingUpdateMeaning(meaning: meaning)
        request.httpBody = try JSONEncoder().encode(body)

        #if DEBUG
        print("[APIService] PATCH \(url.absoluteString)")
        #endif

        let (data, response) = try await urlSession.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        #if DEBUG
        print("[APIService] Response status: \(httpResponse.statusCode)")
        #endif

        switch httpResponse.statusCode {
        case 200:
            return try configuredDecoder().decode(Something.self, from: data)
        case 401:
            throw APIError.unauthorized
        case 404:
            throw APIError.notFound
        default:
            #if DEBUG
            if let responseString = String(data: data, encoding: .utf8) {
                print("[APIService] Error response: \(responseString)")
            }
            #endif
            throw APIError.serverError("Failed to update meaning")
        }
    }

    // MARK: - Circle Endpoints

    /// Assign a something to a circle
    /// - Parameters:
    ///   - circleId: ID of the circle
    ///   - somethingId: ID of the something to assign
    /// - Throws: APIError if request fails
    public func assignSomethingToCircle(circleId: Int, somethingId: Int) async throws {
        let session = try await supabase.auth.session
        guard let url = URL(string: "\(baseURL)/circles/\(circleId)/somethings/\(somethingId)") else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")

        let (_, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 204:
            return
        case 401:
            throw APIError.unauthorized
        case 404:
            throw APIError.notFound
        default:
            throw APIError.serverError("Failed to assign something to circle")
        }
    }

    /// Remove a something from a circle
    /// - Parameters:
    ///   - circleId: ID of the circle
    ///   - somethingId: ID of the something to remove
    /// - Throws: APIError if request fails
    public func removeSomethingFromCircle(circleId: Int, somethingId: Int) async throws {
        let session = try await supabase.auth.session
        guard let url = URL(string: "\(baseURL)/circles/\(circleId)/somethings/\(somethingId)") else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = "DELETE"
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")

        let (_, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 204:
            return
        case 401:
            throw APIError.unauthorized
        case 404:
            throw APIError.notFound
        default:
            throw APIError.serverError("Failed to remove something from circle")
        }
    }

    /// Get similar somethings for a circle
    /// - Parameters:
    ///   - circleId: ID of the circle
    ///   - topK: Number of suggestions (default: 10)
    /// - Returns: Array of similar something suggestions
    /// - Throws: APIError if request fails
    public func getPredictSimilar(circleId: Int, topK: Int = 10) async throws -> [SimilarSomethingSuggestion] {
        let session = try await supabase.auth.session
        guard var urlComponents = URLComponents(string: "\(baseURL)/circles/\(circleId)/predict-similar") else {
            throw APIError.invalidURL
        }
        urlComponents.queryItems = [URLQueryItem(name: "top_k", value: String(topK))]
        guard let url = urlComponents.url else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 200:
            let suggestionsResponse = try configuredDecoder().decode(SuggestionsResponse.self, from: data)
            return suggestionsResponse.suggestions
        case 401:
            throw APIError.unauthorized
        case 404:
            throw APIError.notFound
        default:
            throw APIError.serverError("Failed to get predictions")
        }
    }

    // MARK: - Intention Endpoints

    /// Create a new intention
    /// - Parameter intentionText: The intention text
    /// - Returns: Created Intention
    /// - Throws: APIError if request fails
    public func createIntention(intentionText: String) async throws -> Intention {
        let session = try await supabase.auth.session
        guard let url = URL(string: "\(baseURL)/intentions") else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body = IntentionCreate(intentionText: intentionText)
        request.httpBody = try JSONEncoder().encode(body)

        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 201:
            return try configuredDecoder().decode(Intention.self, from: data)
        case 401:
            throw APIError.unauthorized
        default:
            throw APIError.serverError("Failed to create intention")
        }
    }

    /// List all intentions for current user
    /// - Returns: Array of Intention objects
    /// - Throws: APIError if request fails
    public func listIntentions() async throws -> [Intention] {
        let session = try await supabase.auth.session
        guard let url = URL(string: "\(baseURL)/intentions") else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 200:
            return try configuredDecoder().decode([Intention].self, from: data)
        case 401:
            throw APIError.unauthorized
        default:
            throw APIError.serverError("Failed to list intentions")
        }
    }

    /// Get intention detail with linked somethings and actions
    /// - Parameter intentionId: ID of the intention
    /// - Returns: IntentionDetail with all relationships
    /// - Throws: APIError if request fails
    public func getIntentionDetail(intentionId: Int) async throws -> IntentionDetail {
        let session = try await supabase.auth.session
        guard let url = URL(string: "\(baseURL)/intentions/\(intentionId)") else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 200:
            return try configuredDecoder().decode(IntentionDetail.self, from: data)
        case 401:
            throw APIError.unauthorized
        case 404:
            throw APIError.notFound
        default:
            throw APIError.serverError("Failed to get intention detail")
        }
    }

    // MARK: - Action Endpoints

    /// Create a new action
    /// - Parameters:
    ///   - actionText: Description of the action
    ///   - timeElapsed: Time in minutes
    ///   - intentionIds: Optional intention IDs to link
    /// - Returns: Created Action
    /// - Throws: APIError if request fails
    public func createAction(actionText: String, timeElapsed: Int, intentionIds: [Int]? = nil) async throws -> Action {
        let session = try await supabase.auth.session
        guard let url = URL(string: "\(baseURL)/actions") else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body = ActionCreate(actionText: actionText, timeElapsed: timeElapsed, intentionIds: intentionIds)
        request.httpBody = try JSONEncoder().encode(body)

        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 201:
            return try configuredDecoder().decode(Action.self, from: data)
        case 401:
            throw APIError.unauthorized
        case 404:
            throw APIError.notFound
        default:
            throw APIError.serverError("Failed to create action")
        }
    }

    /// List all actions for current user
    /// - Returns: Array of Action objects
    /// - Throws: APIError if request fails
    public func listActions() async throws -> [Action] {
        let session = try await supabase.auth.session
        guard let url = URL(string: "\(baseURL)/actions") else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.setValue("Bearer \(session.accessToken)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.networkError
        }

        switch httpResponse.statusCode {
        case 200:
            return try configuredDecoder().decode([Action].self, from: data)
        case 401:
            throw APIError.unauthorized
        default:
            throw APIError.serverError("Failed to list actions")
        }
    }

    // MARK: - Helper Methods

    /// Create a JSONDecoder configured for backend API responses
    /// - Returns: Configured JSONDecoder with iso8601 date strategy
    private func configuredDecoder() -> JSONDecoder {
        let decoder = JSONDecoder()

        decoder.dateDecodingStrategy = .custom { decoder in
            let container = try decoder.singleValueContainer()
            let dateString = try container.decode(String.self)

            // Try ISO8601 with fractional seconds
            let fractional = ISO8601DateFormatter()
            fractional.formatOptions = [.withInternetDateTime, .withFractionalSeconds]

            if let date = fractional.date(from: dateString) {
                return date
            }

            // Try ISO8601 without fractional seconds
            let basic = ISO8601DateFormatter()
            basic.formatOptions = [.withInternetDateTime]

            if let date = basic.date(from: dateString) {
                return date
            }

            throw DecodingError.dataCorruptedError(
                in: container,
                debugDescription: "Invalid ISO8601 date: \(dateString)"
            )
        }

        return decoder
    }

}

// MARK: - API Errors

/// API-specific errors with user-friendly descriptions
public enum APIError: LocalizedError {
    case unauthorized
    case networkError
    case notFound
    case invalidURL
    case invalidParameters(String)
    case serverError(String)

    public var errorDescription: String? {
        switch self {
        case .unauthorized:
            return "Please log in again"
        case .networkError:
            return "Network connection failed"
        case .notFound:
            return "Resource not found"
        case .invalidURL:
            return "Invalid request URL"
        case .invalidParameters(let message):
            return "Invalid parameters: \(message)"
        case .serverError(let message):
            return message
        }
    }
}
