export type CacheStrategy = 'network-only' | 'navigation-fallback' | 'static-cache'

export interface CacheRequestDescriptor {
  method: string
  origin: string
  pathname: string
  mode: string
  destination: string
}

export interface PrecacheDescriptor {
  url: string
  revision?: string | null
}

const STATIC_DESTINATIONS = new Set(['style', 'script', 'image', 'font', 'manifest'])

const isApiPath = (pathname: string) => pathname === '/api' || pathname.startsWith('/api/')

export const buildVersionedCacheName = (prefix: string, entries: PrecacheDescriptor[]): string => {
  const signature = entries
    .map(({ url, revision }) => `${url}:${revision ?? 'content-addressed'}`)
    .sort()
    .join('|')
  let hash = 2166136261

  for (let index = 0; index < signature.length; index += 1) {
    hash = Math.imul(hash ^ signature.charCodeAt(index), 16777619)
  }

  return `${prefix}${(hash >>> 0).toString(16).padStart(8, '0')}`
}

export const buildPrecacheUrls = (
  manifestUrls: string[],
  requiredUrls: string[],
  applicationOrigin: string,
): string[] => [
  ...new Set([...manifestUrls, ...requiredUrls].map((url) => new URL(url, applicationOrigin).href)),
]

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
