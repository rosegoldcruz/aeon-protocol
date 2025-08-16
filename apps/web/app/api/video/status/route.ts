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
      headers: { Authorization: `Token ${token}` }, // CRITICAL: Token, not Bearer
      cache: "no-store",
    })
    const data = await resp.json()
    if (!resp.ok) {
      return NextResponse.json({ error: data?.detail || "Replicate status failed" }, {
        status: 502,
      })
    }

    // Normalize output handling for different response formats
    let outputUrl: string | null = null;
    if (typeof data.output === "string") outputUrl = data.output;
    else if (Array.isArray(data.output)) {
      outputUrl =
        data.output.find((u: any) => typeof u === "string" && u.endsWith(".mp4")) ??
        data.output.find((u: any) => typeof u === "string") ??
        null;
    } else if (data.output && typeof data.output === "object") {
      outputUrl = (data.output.video || data.output.url || null) as string | null;
    }

    return NextResponse.json({
      id: data.id,
      status: data.status,
      output: outputUrl,
      logs: data.logs ?? null,
      error: data.error ?? null,
    })
  } catch (err: any) {
    return NextResponse.json({ error: err?.message || "Unknown error" }, { status: 500 })
  }
}

