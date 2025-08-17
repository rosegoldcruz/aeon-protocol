import { auth } from "@clerk/nextjs/server";
export async function backendFetch(path: string, init?: RequestInit) {
  const { getToken } = auth();
  const token = await getToken({ template: "backend" }); // Clerk JWT for backend audience
  const headers = new Headers(init?.headers || {});
  headers.set("Authorization", `Bearer ${token}`);
  headers.set("Content-Type", headers.get("Content-Type") || "application/json");
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "https://api.aeonprotocol.com"}${path}`, {
    ...init,
    headers,
    cache: "no-store",
  });
  return res;
}

