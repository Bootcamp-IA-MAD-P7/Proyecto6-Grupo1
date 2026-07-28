import type { ReactNode } from 'react'
import { ThemeToggle } from '@/components/ThemeToggle'

interface AuthLayoutProps {
  children: ReactNode
}

export default function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-paper px-4">
      <div className="absolute top-4 right-4">
        <ThemeToggle />
      </div>
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <h1 className="text-2xl font-semibold tracking-tight text-ink">ClaimVox</h1>
          <p className="mt-1 text-sm text-ink-soft">Authentication concept demo</p>
        </div>
        {children}
      </div>
    </div>
  )
}
