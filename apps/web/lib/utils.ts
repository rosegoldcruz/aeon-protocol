import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}



export const API_BASE_URL = process.env["NEXT_PUBLIC_BACKEND_URL"] || "http://localhost:8000"
export async function apiRequest(endpoint: string, options: RequestInit = {}, token?: string) {
  const url = `${API_BASE_URL}${endpoint}`
  const baseHeaders: HeadersInit = { "Content-Type": "application/json" }
  const mergedHeaders: HeadersInit = {
    ...baseHeaders,
    ...(options.headers as HeadersInit | undefined),
  }
  if (token) {
    ;(mergedHeaders as Record<string, string>)["Authorization"] = `Bearer ${token}`
  }
  const response = await fetch(url, { ...options, headers: mergedHeaders })
  return response.json()
}


