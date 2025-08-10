import './globals.css'
import type { ReactNode } from 'react'
import { ClerkProvider } from '@clerk/nextjs'
import { dark } from '@clerk/themes'

export const metadata = {
  title: 'AEON',
  description: 'Unified AI business automation platform',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <ClerkProvider
      appearance={{
        baseTheme: dark,
        variables: {
          colorPrimary: '#ffffff',
          colorBackground: '#0a0a0a',
          colorInputBackground: '#1a1a1a',
          colorInputText: '#ffffff',
        },
      }}
    >
      <html lang="en" className="dark">
        <body className="min-h-screen bg-background text-foreground">
          {children}
        </body>
      </html>
    </ClerkProvider>
  )
}

