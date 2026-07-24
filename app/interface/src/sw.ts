/// <reference lib="webworker" />
/// <reference types="vite-plugin-pwa/client" />

export {}

interface PrecacheEntry {
  url: string
  revision?: string | null
}

declare const self: ServiceWorkerGlobalScope & {
  __WB_MANIFEST: PrecacheEntry[]
}

const CACHE_NAME = 'complaint-routing-v1'
const OFFLINE_URL = '/offline.html'

// Archivos a cachear
const PRECACHE_URLS = [
  ...new Set([
    ...self.__WB_MANIFEST.map((entry) => entry.url),
    '/',
    '/index.html',
    '/app-mark.svg',
    OFFLINE_URL,
  ]),
]

// ============================================
// INSTALACIÓN
// ============================================
self.addEventListener('install', (event) => {
  event.waitUntil(
    (async () => {
      try {
        const cache = await caches.open(CACHE_NAME)
        await cache.addAll(PRECACHE_URLS)
        await self.skipWaiting()
      } catch (error) {
        console.error('[SW] Error en instalación:', error)
      }
    })(),
  )
})

// ============================================
// ACTIVACIÓN
// ============================================
self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      // Eliminar caches antiguos
      const cacheNames = await caches.keys()
      await Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => {
            console.log('[SW] Eliminando cache antiguo:', name)
            return caches.delete(name)
          }),
      )
      await self.clients.claim()
    })(),
  )
})

// ============================================
// FETCH
// ============================================
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)

  // Ignorar peticiones API
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request).catch(() => {
        return new Response(
          JSON.stringify({
            error: 'Sin conexión',
            offline: true,
          }),
          {
            headers: { 'Content-Type': 'application/json' },
            status: 503,
          },
        )
      }),
    )
    return
  }

  // Estrategia: Stale-While-Revalidate
  event.respondWith(
    (async () => {
      try {
        const cache = await caches.open(CACHE_NAME)
        const cachedResponse = await cache.match(request)

        try {
          // Intentar obtener de red
          const networkResponse = await fetch(request)

          // Actualizar cache si la respuesta es válida
          if (networkResponse && networkResponse.status === 200) {
            cache.put(request, networkResponse.clone())
          }

          return networkResponse
        } catch {
          // Si falla la red, devolver cache
          if (cachedResponse) {
            return cachedResponse
          }

          // Si es una página HTML, mostrar offline
          if (request.headers.get('accept')?.includes('text/html')) {
            return (
              (await cache.match(OFFLINE_URL)) ??
              new Response('Página no disponible offline', { status: 503 })
            )
          }

          // Para otros recursos, devolver error
          return new Response('Recurso no disponible offline', {
            status: 503,
          })
        }
      } catch (error) {
        console.error('[SW] Error en fetch:', error)
        return new Response('Error en el Service Worker', { status: 500 })
      }
    })(),
  )
})
