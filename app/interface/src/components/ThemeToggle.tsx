import { Moon, Sun, Monitor } from 'lucide-react'
import { useTheme } from '@/providers/ThemeProvider'
import { Button } from '@/components/ui/button'

const THEME_ORDER: Array<'light' | 'dark' | 'system'> = ['light', 'dark', 'system']

const LABELS: Record<string, string> = {
  light: 'Light theme',
  dark: 'Dark theme',
  system: 'System theme',
}

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  const cycleTheme = () => {
    const currentIndex = THEME_ORDER.indexOf(theme)
    const nextIndex = (currentIndex + 1) % THEME_ORDER.length
    setTheme(THEME_ORDER[nextIndex]!)
  }

  const Icon = theme === 'dark' ? Moon : theme === 'light' ? Sun : Monitor

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={cycleTheme}
      aria-label={LABELS[theme]}
      title={LABELS[theme]}
    >
      <Icon className="h-4 w-4" />
    </Button>
  )
}
