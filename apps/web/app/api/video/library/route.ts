import { NextResponse } from "next/server";
import { backendFetch } from "@/lib/backend-fetch";

export async function GET() {
  const res = await backendFetch("/v1/library", { method: "GET" });
  return new NextResponse(await res.text(), { status: res.status, headers: { "content-type": res.headers.get("content-type") || "application/json" }});
}
