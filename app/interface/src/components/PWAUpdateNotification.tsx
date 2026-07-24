// src/components/PWAUpdateNotification.tsx
import { RefreshCw } from 'lucide-react'
import { useEffect, useState } from 'react'

export function PWAUpdateNotification() {
  const [showUpdate, setShowUpdate] = useState(false)

  useEffect(() => {
    // Escuchar eventos de actualización
    const handleSWUpdate = () => {
      setShowUpdate(true)
    }

    // Registrar listener
    document.addEventListener('sw-update', handleSWUpdate)

    return () => {
      document.removeEventListener('sw-update', handleSWUpdate)
    }
  }, [])

  if (!showUpdate) return null

  return (
    <div className="fixed bottom-4 right-4 z-50 p-4 bg-white rounded-xl shadow-2xl border border-gray-200 max-w-sm">
      <div className="flex items-center gap-3">
        <RefreshCw className="w-5 h-5 text-blue-500 animate-spin" />
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-900">Nueva versión disponible</p>
          <p className="text-xs text-gray-500">Haz clic para actualizar la aplicación</p>
        </div>
        <button
          onClick={() => {
            window.location.reload()
          }}
          className="px-3 py-1.5 bg-blue-500 text-white text-sm font-medium rounded-lg hover:bg-blue-600 transition-colors"
        >
          Actualizar
        </button>
      </div>
    </div>
  )
}
