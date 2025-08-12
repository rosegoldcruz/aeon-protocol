import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'
import { NextResponse } from 'next/server'
import type { NextRequest, NextFetchEvent } from 'next/server'

const CLERK_ENABLED = Boolean(process.env['CLERK_PUBLISHABLE_KEY'] && process.env['CLERK_SECRET_KEY'])

const isProtectedRoute = createRouteMatcher([
  '/dashboard(.*)',
  '/agents(.*)',
  '/projects(.*)',
  '/settings(.*)',
  '/studio(.*)',
  '/integrations(.*)',
  '/workflows(.*)'
])

const isPublicApiRoute = createRouteMatcher([
  '/api/init-db'
])

const isPublicRoute = createRouteMatcher([
  '/',
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/api/init-db'
])

export default function middleware(req: NextRequest, event: NextFetchEvent) {
  // No-op middleware when Clerk is not configured or for public routes/methods
  if (!CLERK_ENABLED || req.method === 'OPTIONS' || req.method === 'HEAD' || isPublicApiRoute(req) || isPublicRoute(req)) {
    return NextResponse.next()
  }

  // Invoke Clerk middleware only when needed
  return clerkMiddleware((auth, request) => {
    if (isProtectedRoute(request)) {
      auth().protect()
    }
    return NextResponse.next()
  })(req, event)
}

export const config = {
  // Exclude static files, _next, and images from middleware; include app routes
  matcher: [
    '/((?!_next|.*\\..*|favicon.ico|robots.txt|sitemap.xml).*)',
    '/(api|trpc)(.*)'
  ],
}
