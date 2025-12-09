//
//  Supabase.swift
//  Pookie
//
//  Created by Sudhir V on 12/3/25.
//

import Foundation
import Supabase

/// Load Supabase configuration from Config.plist
private func loadSupabaseConfig() -> (url: URL, key: String) {
    guard let path = Bundle.main.path(forResource: "Config", ofType: "plist"),
          let config = NSDictionary(contentsOfFile: path) as? [String: Any],
          let urlString = config["SupabaseURL"] as? String,
          let url = URL(string: urlString),
          let key = config["SupabaseAnonKey"] as? String else {
        fatalError("Failed to load Supabase config from Config.plist")
    }
    return (url, key)
}

// Global Supabase client
let supabase: SupabaseClient = {
    let config = loadSupabaseConfig()
    print("Loaded SupabaseURL =", config.url)
    print("Loaded SupabaseAnonKey =", config.key.prefix(8), "...")
    
    return SupabaseClient(
        supabaseURL: config.url,
        supabaseKey: config.key
    )
}()
