import { NextResponse } from "next/server"

// POST /api/video/generate
// Body: { prompt: string, duration?: number, resolution?: "512p"|"768p"|"1080p" }
// Returns: { id: string, status: string }
export async function POST(request: Request) {
  try {
    const { prompt, duration = 6, resolution = "768p" } = await request.json()

    if (!prompt || typeof prompt !== "string") {
      return NextResponse.json({ error: "Missing prompt" }, { status: 400 })
    }

    const token = process.env["REPLICATE_API_TOKEN"]
    if (!token) {
      return NextResponse.json({ error: "REPLICATE_API_TOKEN not configured" }, { status: 500 })
    }

    // Minimax Hailuo 2 (text-to-video) version id
    const MODEL_VERSION = process.env["REPLICATE_HAILUO_VERSION_ID"] ||
      "d615361988ffcbadecfe52b95dd9302a8d6e1069c908a05104f36b651aea6c95"

    const resp = await fetch("https://api.replicate.com/v1/predictions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`, // CRITICAL: Use Token, not Bearer
        Prefer: "wait=30",
      },
      body: JSON.stringify({
        version: MODEL_VERSION,
        input: {
          prompt,
          duration,
          resolution,
          prompt_optimizer: true,
        },
      }),
    })

    const data = await resp.json()
    if (!resp.ok) {
      return NextResponse.json({ error: data?.error || "Replicate error" }, { status: resp.status })
    }

    return NextResponse.json({ id: data.id as string, status: data.status as string })
  } catch (err: any) {
    return NextResponse.json({ error: err?.message || "Unknown error" }, { status: 500 })
  }
}

