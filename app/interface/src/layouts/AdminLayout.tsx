import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '@/hooks/use-auth'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
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
    <div className="flex min-h-screen bg-paper">
      <aside className="w-64 border-r border-line bg-forest text-white">
        <div className="p-6">
          <h2 className="font-serif text-lg font-semibold">Complaint Routing</h2>
          <Badge variant="review" className="mt-2">
            Proposal only
          </Badge>
        </div>
        <nav className="px-4">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                cn(
                  'block rounded-md px-4 py-2 text-sm font-medium transition-colors',
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
      <div className="flex flex-1 flex-col">
        <header className="flex items-center justify-between border-b border-line bg-paper px-6 py-3">
          <div />
          <div className="flex items-center gap-4">
            <span className="text-sm text-ink-soft">
              Mock role: {user?.name} ({user?.role}) · no authorization
            </span>
            <Button variant="ghost" size="sm" onClick={handleLogout}>
              End mock session
            </Button>
          </div>
        </header>
        <main className="flex-1 overflow-auto p-6">
          <div className="mx-auto max-w-6xl space-y-6">
            <ProposalNotice />
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}
