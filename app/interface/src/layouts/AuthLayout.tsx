import type { ReactNode } from 'react'

interface AuthLayoutProps {
  children: ReactNode
}

export default function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-paper px-4">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <h1 className="font-serif text-2xl font-semibold text-ink">Complaint Routing</h1>
          <p className="mt-1 text-sm text-ink-soft">Decision-support workspace</p>
        </div>
        {children}
      </div>
    </div>
  )
}
