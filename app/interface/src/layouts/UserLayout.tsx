import { NavLink, Outlet } from 'react-router-dom'
import { Badge } from '@/components/ui/badge'
import { ThemeToggle } from '@/components/ThemeToggle'
import { cn } from '@/lib/utils'
import { Home, FileText } from 'lucide-react'

const navItems = [
  { to: '/', label: 'Home', icon: Home },
  { to: '/classify', label: 'Classify', icon: FileText },
]

export default function UserLayout() {
  return (
    <div className="flex min-h-screen flex-col bg-paper md:flex-row">
      <aside className="border-b border-line bg-forest text-white md:w-64 md:border-r md:border-b-0">
        <div className="px-4 pt-4 pb-3 md:p-6">
          <p className="text-lg font-semibold tracking-tight">ClaimVox</p>
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
      </aside>
      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex flex-wrap items-center justify-between gap-2 border-b border-line bg-paper px-4 py-3 md:px-6">
          <span className="text-sm font-medium text-ink md:hidden">ClaimVox</span>
          <div className="flex flex-wrap items-center gap-2 md:gap-4">
            <ThemeToggle />
            <span className="text-sm text-ink-soft">Local classification prototype</span>
          </div>
        </header>
        <main className="flex-1 overflow-auto p-4 md:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
