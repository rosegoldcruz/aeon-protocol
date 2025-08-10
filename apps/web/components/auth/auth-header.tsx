"use client"

import { UserButton, useUser } from '@clerk/nextjs'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { User, Settings, LogOut } from 'lucide-react'

export function AuthHeader() {
  const { user, isLoaded } = useUser()

  if (!isLoaded) {
    return (
      <div className="flex items-center justify-between p-4 border-b">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 bg-muted rounded-full animate-pulse" />
          <div className="h-4 w-24 bg-muted rounded animate-pulse" />
        </div>
        <div className="h-8 w-8 bg-muted rounded-full animate-pulse" />
      </div>
    )
  }

  return (
    <div className="flex items-center justify-between p-4 border-b">
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2">
          <User className="h-5 w-5 text-muted-foreground" />
          <span className="font-medium">
            {user?.firstName} {user?.lastName}
          </span>
        </div>
        <span className="text-sm text-muted-foreground">
          {user?.emailAddresses[0]?.emailAddress}
        </span>
      </div>
      
      <div className="flex items-center gap-2">
        <UserButton
          appearance={{
            elements: {
              avatarBox: "h-8 w-8",
              userButtonPopoverCard: "bg-background border",
              userButtonPopoverActionButton: "text-foreground hover:bg-muted",
            },
          }}
          afterSignOutUrl="/"
        />
      </div>
    </div>
  )
}
