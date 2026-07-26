import { RefreshCw } from 'lucide-react'
import { useEffect, useState } from 'react'

export function PWAUpdateNotification() {
  const [showUpdate, setShowUpdate] = useState(false)

  useEffect(() => {
    const handleSWUpdate = () => {
      setShowUpdate(true)
    }

    document.addEventListener('sw-update', handleSWUpdate)

    return () => {
      document.removeEventListener('sw-update', handleSWUpdate)
    }
  }, [])

  if (!showUpdate) return null

  return (
    <div className="fixed bottom-4 right-4 z-50 max-w-sm rounded-xl border border-line bg-paper p-4 shadow-2xl">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-forest/10">
          <RefreshCw className="h-5 w-5 text-forest animate-spin" />
        </div>
        <div className="flex-1">
          <p className="text-sm font-medium text-ink">New version available</p>
          <p className="text-xs text-ink-soft">Click to update the application</p>
        </div>
        <button
          onClick={() => {
            window.location.reload()
          }}
          className="rounded-lg bg-forest px-3 py-1.5 text-sm font-medium text-white transition-colors hover:bg-forest-light"
        >
          Update
        </button>
      </div>
    </div>
  )
}
