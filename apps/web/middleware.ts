import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'
import { NextResponse } from 'next/server'

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

export default clerkMiddleware((auth, req) => {
  // Health check for middleware – return early for OPTIONS and HEAD
  if (req.method === 'OPTIONS' || req.method === 'HEAD') {
    return NextResponse.next()
  }

  // Skip auth for public routes and API routes
  if (isPublicApiRoute(req) || isPublicRoute(req)) {
    return NextResponse.next()
  }

  // Protect only matched routes
  if (isProtectedRoute(req)) {
    auth().protect()
  }

  return NextResponse.next()
})

export const config = {
  // Exclude static files, _next, and images from middleware; include app routes
  matcher: [
    '/((?!_next|.*\\..*|favicon.ico|robots.txt|sitemap.xml).*)',
    '/(api|trpc)(.*)'
  ],
}
