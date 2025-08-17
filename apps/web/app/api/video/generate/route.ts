import { NextResponse } from "next/server";
import { backendFetch } from "@/lib/backend-fetch";

export async function POST(req: Request) {
  const body = await req.text();
  const res = await backendFetch("/v1/video/generate", { method: "POST", body });
  return new NextResponse(await res.text(), { status: res.status, headers: { "content-type": res.headers.get("content-type") || "application/json" }});
}
