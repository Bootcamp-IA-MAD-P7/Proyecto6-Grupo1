import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '@/hooks/use-auth'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { buttonVariants } from '@/lib/button-variants'
import { cn } from '@/lib/utils'

const navItems = [
  { to: '/', label: 'Home' },
  { to: '/classify', label: 'Classify' },
]

export default function UserLayout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/classify')
  }

  return (
    <div className="flex min-h-screen flex-col bg-paper md:flex-row">
      <aside className="border-b border-line bg-forest text-white md:w-64 md:border-r md:border-b-0">
        <div className="px-4 pt-4 pb-3 md:p-6">
          <p className="font-serif text-lg font-semibold">Complaint Routing</p>
          <Badge variant="mock" className="mt-2">
            Public prototype
          </Badge>
        </div>
        <nav
          aria-label="Primary navigation"
          className="flex gap-2 overflow-x-auto px-4 pb-4 md:block md:pb-0"
        >
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
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
        <header className="flex flex-wrap items-center justify-end gap-2 border-b border-line bg-paper px-4 py-3 md:px-6">
          <div className="flex flex-wrap items-center justify-end gap-2 md:gap-4">
            {user ? (
              <>
                <span className="text-sm text-ink-soft">
                  Mock session: {user.name} ({user.role})
                </span>
                <Button variant="ghost" size="sm" onClick={handleLogout}>
                  End mock session
                </Button>
              </>
            ) : (
              <>
                <span className="text-sm text-ink-soft">Public prototype · no identity</span>
                <Link to="/login" className={cn(buttonVariants({ variant: 'ghost', size: 'sm' }))}>
                  Review mock login
                </Link>
              </>
            )}
          </div>
        </header>
        <main className="flex-1 overflow-auto p-4 md:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
