import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

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
  // Skip auth for public routes and API routes
  if (isPublicApiRoute(req) || isPublicRoute(req)) return

  if (isProtectedRoute(req)) auth().protect()
})

export const config = {
  matcher: ['/((?!.*\\..*|_next).*)', '/', '/(api|trpc)(.*)'],
}
