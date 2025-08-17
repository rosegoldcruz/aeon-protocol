import { NextResponse } from "next/server";
import { backendFetch } from "@/lib/backend-fetch";

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const id = searchParams.get("id");
  const res = await backendFetch(`/v1/jobs/${id}`, { method: "GET" });
  return new NextResponse(await res.text(), { status: res.status, headers: { "content-type": res.headers.get("content-type") || "application/json" }});
}
