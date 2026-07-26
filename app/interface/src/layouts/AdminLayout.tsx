import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '@/hooks/use-auth'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ThemeToggle } from '@/components/ThemeToggle'
import ProposalNotice from '@/components/ProposalNotice'
import { cn } from '@/lib/utils'

const navItems = [
  { to: '/admin', label: 'Concept overview', end: true },
  { to: '/admin/training', label: 'Training concept' },
  { to: '/admin/models', label: 'Model registry concept' },
]

export default function AdminLayout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="flex min-h-screen flex-col bg-paper md:flex-row">
      <aside className="border-b border-line bg-forest text-white md:w-64 md:border-r md:border-b-0">
        <div className="px-4 pt-4 pb-3 md:p-6">
          <p className="text-lg font-semibold tracking-tight">ClaimVox</p>
          <Badge variant="review" className="mt-2">
            Proposal only
          </Badge>
        </div>
        <nav
          aria-label="Administration navigation"
          className="flex gap-2 overflow-x-auto px-4 pb-4 md:block md:pb-0"
        >
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                cn(
                  'block shrink-0 rounded-md px-4 py-2 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gold focus-visible:ring-offset-2 focus-visible:ring-offset-forest',
                  isActive
                    ? 'bg-white/20 text-white'
                    : 'text-white/70 hover:bg-white/10 hover:text-white',
                )
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex flex-wrap items-center justify-between gap-2 border-b border-line bg-paper px-4 py-3 md:px-6">
          <span className="text-sm font-medium text-ink md:hidden">ClaimVox Admin</span>
          <div className="flex flex-wrap items-center gap-2 md:gap-4">
            <ThemeToggle />
            <span className="text-sm text-ink-soft">
              Mock role: {user?.name} ({user?.role})
            </span>
            <Button variant="ghost" size="sm" onClick={handleLogout}>
              End mock session
            </Button>
          </div>
        </header>
        <main className="flex-1 overflow-auto p-4 md:p-6">
          <div className="mx-auto max-w-6xl space-y-6">
            <ProposalNotice />
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}
