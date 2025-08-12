import { NextResponse } from "next/server"

// Simple user library persistence in Vercel KV-like fallback using Postgres via Neon if DATABASE_URL is set
// For this codebase, we'll persist to a small JSON file in Edge is not possible; instead use localStorage on client for now.
// This API exists for future server storage; return 501 to indicate client storage is used.

export async function GET() {
  return NextResponse.json({ error: "Server-side library storage not configured" }, { status: 501 })
}

