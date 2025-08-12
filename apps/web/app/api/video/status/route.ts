import { NextResponse } from "next/server"

// GET /api/video/status?id=<prediction_id>
export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const id = searchParams.get("id")
    if (!id) return NextResponse.json({ error: "Missing id" }, { status: 400 })

    const token = process.env["REPLICATE_API_TOKEN"]
    if (!token) return NextResponse.json({ error: "REPLICATE_API_TOKEN not configured" }, { status: 500 })

    const resp = await fetch(`https://api.replicate.com/v1/predictions/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    })
    const data = await resp.json()
    if (!resp.ok) {
      return NextResponse.json({ error: data?.error || "Replicate error" }, { status: resp.status })
    }

    // On success, Replicate may require authenticated file fetch. Pass-through URL as-is.
    return NextResponse.json({
      id: data.id,
      status: data.status,
      output: data.output || null,
      logs: data.logs || "",
      error: data.error || null,
    })
  } catch (err: any) {
    return NextResponse.json({ error: err?.message || "Unknown error" }, { status: 500 })
  }
}

