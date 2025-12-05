//
//  Supabase.swift
//  Pookie
//
//  Created by Sudhir V on 12/3/25.
//

import Foundation
import Supabase

// Global Supabase client
// TODO: Load URL and key from Config.plist in Story 1.5
let supabase = SupabaseClient(
    supabaseURL: URL(string: "YOUR_SUPABASE_URL")!,
    supabaseKey: "YOUR_SUPABASE_ANON_KEY"
)
