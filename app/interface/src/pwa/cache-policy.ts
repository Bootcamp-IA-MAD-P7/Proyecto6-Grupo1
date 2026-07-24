export type CacheStrategy = 'network-only' | 'navigation-fallback' | 'static-cache'

export interface CacheRequestDescriptor {
  method: string
  origin: string
  pathname: string
  mode: string
  destination: string
}

const STATIC_DESTINATIONS = new Set(['style', 'script', 'image', 'font', 'manifest'])

const isApiPath = (pathname: string) => pathname === '/api' || pathname.startsWith('/api/')

export const selectCacheStrategy = (
  request: CacheRequestDescriptor,
  applicationOrigin: string,
): CacheStrategy => {
  if (
    request.method !== 'GET' ||
    request.origin !== applicationOrigin ||
    isApiPath(request.pathname)
  ) {
    return 'network-only'
  }

  if (request.mode === 'navigate') {
    return 'navigation-fallback'
  }

  return STATIC_DESTINATIONS.has(request.destination) ? 'static-cache' : 'network-only'
}
