import { createClient, SupabaseClient } from '@supabase/supabase-js';

// It's good practice to ensure your env variables are strings
const supabaseUrl: string = process.env.VITE_SUPABASE_URL || '';
const supabaseAnonKey: string = process.env.VITE_SUPABASE_ANON_KEY || '';

export const supabase: SupabaseClient = createClient(supabaseUrl, supabaseAnonKey);