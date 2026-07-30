import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '@/hooks/use-auth'
import { Button } from '@/components/ui/button'
import { ThemeToggle } from '@/components/ThemeToggle'
import HumanReviewPanel from '@/components/HumanReviewPanel'
import { cn } from '@/lib/utils'
import { Home, FileText, LayoutDashboard, Cpu, Box, LogOut, Settings } from 'lucide-react'

interface NavItem {
  to: string
  label: string
  icon: React.ComponentType<{ className?: string }>
  requiredRole?: 'admin'
  end?: boolean
}

const ALL_NAV_ITEMS: NavItem[] = [
  { to: '/', label: 'Home', icon: Home },
  { to: '/classify', label: 'Classify', icon: FileText },
  { to: '/admin', label: 'Dashboard', icon: LayoutDashboard, requiredRole: 'admin', end: true },
  { to: '/admin/training', label: 'Training', icon: Cpu, requiredRole: 'admin' },
  { to: '/admin/models', label: 'Models', icon: Box, requiredRole: 'admin' },
]

export default function UserLayout() {
  const { user, logout, hasRole } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const visibleItems = ALL_NAV_ITEMS.filter(
    (item) => !item.requiredRole || hasRole(item.requiredRole),
  )

  return (
    <div className="flex min-h-screen flex-col bg-paper md:flex-row">
      <aside className="flex flex-col border-b border-line bg-forest text-white md:w-64 md:border-r md:border-b-0">
        <div className="px-4 pt-4 pb-3 md:p-6">
          <p className="text-lg font-semibold tracking-tight">ClaimVox</p>
        </div>
        <nav
          aria-label="Primary navigation"
          className="flex gap-2 overflow-x-auto px-4 pb-4 md:flex-1 md:flex-col md:pb-0"
        >
          {visibleItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end ?? item.to === '/'}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-2 shrink-0 rounded-lg px-4 py-2.5 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gold focus-visible:ring-offset-2 focus-visible:ring-offset-forest',
                  isActive
                    ? 'bg-white/20 text-white'
                    : 'text-white/70 hover:bg-white/10 hover:text-white',
                )
              }
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="border-t border-white/10 px-4 py-3">
          <div className="flex items-center gap-2">
            <Settings className="h-4 w-4 text-white/70" />
            <span className="text-sm text-white/70">Settings</span>
            <div className="ml-auto">
              <ThemeToggle />
            </div>
          </div>
        </div>
      </aside>
      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex flex-wrap items-center justify-between gap-2 border-b border-line bg-paper px-4 py-3 md:px-6">
          <span className="text-sm font-medium text-ink md:hidden">ClaimVox</span>
          {user ? (
            <div className="flex flex-wrap items-center gap-2 md:gap-4 ml-auto">
              <span className="text-sm text-ink-soft">
                {user.name} ({user.role})
              </span>
              <Button variant="ghost" size="sm" onClick={handleLogout}>
                <LogOut className="h-4 w-4" />
                Sign out
              </Button>
            </div>
          ) : (
            <span className="text-sm text-ink-soft ml-auto">Not signed in</span>
          )}
        </header>
        <main className="flex flex-1 flex-col gap-6 overflow-auto p-4 md:flex-row md:p-6">
          <div className="flex-1">
            <Outlet />
          </div>
          <div className="shrink-0 md:w-72">
            <HumanReviewPanel />
          </div>
        </main>
      </div>
    </div>
  )
}
