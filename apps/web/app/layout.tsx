import './globals.css'
import type { ReactNode } from 'react'
import { ClerkProvider } from '@clerk/nextjs'
import { ErrorBoundary } from '@/components/error-boundary'

export const metadata = {
  title: 'AEON',
  description: 'Unified AI business automation platform',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en" className="dark">
        <body className="min-h-screen bg-background text-foreground">
          <ErrorBoundary>
            {children}
          </ErrorBoundary>
        </body>
      </html>
    </ClerkProvider>
  )
}

