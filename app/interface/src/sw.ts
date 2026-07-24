/// <reference lib="webworker" />
/// <reference types="vite-plugin-pwa/client" />

import { buildPrecacheUrls, selectCacheStrategy } from './pwa/cache-policy'

export {}

interface PrecacheEntry {
  url: string
  revision?: string | null
}

declare const self: ServiceWorkerGlobalScope & {
  __WB_MANIFEST: PrecacheEntry[]
}

const CACHE_PREFIX = 'complaint-routing-'
const CACHE_NAME = `${CACHE_PREFIX}v5`
const OFFLINE_URL = '/offline.html'
const APP_SHELL_URL = '/index.html'

const PRECACHE_URLS = buildPrecacheUrls(
  self.__WB_MANIFEST.map((entry) => entry.url),
  ['/', APP_SHELL_URL, '/app-mark.svg', OFFLINE_URL],
  self.location.origin,
)

self.addEventListener('install', (event) => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE_NAME)
      await cache.addAll(PRECACHE_URLS)
      await self.skipWaiting()
    })(),
  )
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      const cacheNames = await caches.keys()
      await Promise.all(
        cacheNames
          .filter((name) => name.startsWith(CACHE_PREFIX) && name !== CACHE_NAME)
          .map((name) => caches.delete(name)),
      )
      await self.clients.claim()
    })(),
  )
})

const handleNavigation = async (request: Request) => {
  try {
    return await fetch(request)
  } catch {
    const cache = await caches.open(CACHE_NAME)
    return (
      (await cache.match(APP_SHELL_URL)) ??
      (await cache.match(OFFLINE_URL)) ??
      new Response('Application shell is not available offline.', { status: 503 })
    )
  }
}

const handleStaticResource = async (request: Request) => {
  const cache = await caches.open(CACHE_NAME)
  const cachedResponse = await cache.match(request, { ignoreVary: true })

  if (cachedResponse) return cachedResponse

  const networkResponse = await fetch(request)
  if (networkResponse.ok && networkResponse.type === 'basic') {
    await cache.put(request, networkResponse.clone())
  }

  return networkResponse
}

self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)
  const strategy = selectCacheStrategy(
    {
      method: request.method,
      origin: url.origin,
      pathname: url.pathname,
      mode: request.mode,
      destination: request.destination,
    },
    self.location.origin,
  )

  if (strategy === 'navigation-fallback') {
    event.respondWith(handleNavigation(request))
  } else if (strategy === 'static-cache') {
    event.respondWith(handleStaticResource(request))
  }
})
