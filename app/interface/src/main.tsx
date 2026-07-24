import { QueryProvider } from '@/providers/QueryProvider'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './index.css'

// ✅ Registrar PWA
import { registerSW } from 'virtual:pwa-register'

// Configuración del registro
const updateSW = registerSW({
  onNeedRefresh() {
    // Mostrar notificación de actualización
    if (confirm('Nueva versión disponible. ¿Actualizar?')) {
      updateSW()
    }
  },
  onOfflineReady() {
    console.log('App ready to work offline')
  },
  onRegistered(swUrl) {
    console.log('Service Worker registrado:', swUrl)
  },
  onRegisterError(error) {
    console.error('Error registrando SW:', error)
  },
})

// ✅ Registrar Service Worker en desarrollo
if (import.meta.env.DEV) {
  console.log('🔧 Modo Desarrollo con PWA activa')
  console.log('📍 Visita http://localhost:3000')
  console.log('📱 Abre DevTools → Application → Service Workers')
}

const root = document.getElementById('root')

if (!root) {
  throw new Error('Application root is missing.')
}

createRoot(root).render(
  <StrictMode>
    <QueryProvider>
      <App />
    </QueryProvider>
  </StrictMode>,
)
