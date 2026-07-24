import { describe, expect, it } from 'vitest'
import { selectCacheStrategy, type CacheRequestDescriptor } from './cache-policy'

const APP_ORIGIN = 'https://complaints.example'

const request = (overrides: Partial<CacheRequestDescriptor> = {}): CacheRequestDescriptor => ({
  method: 'GET',
  origin: APP_ORIGIN,
  pathname: '/assets/app.js',
  mode: 'cors',
  destination: 'script',
  ...overrides,
})

describe('service worker cache policy', () => {
  it('keeps API requests network-only', () => {
    expect(selectCacheStrategy(request({ pathname: '/api/predictions' }), APP_ORIGIN)).toBe(
      'network-only',
    )
    expect(selectCacheStrategy(request({ pathname: '/api' }), APP_ORIGIN)).toBe('network-only')
  })

  it('keeps writes network-only regardless of destination', () => {
    expect(selectCacheStrategy(request({ method: 'POST' }), APP_ORIGIN)).toBe('network-only')
  })

  it('keeps cross-origin requests network-only', () => {
    expect(selectCacheStrategy(request({ origin: 'https://external.example' }), APP_ORIGIN)).toBe(
      'network-only',
    )
  })

  it('does not cache data fetches with an empty destination', () => {
    expect(selectCacheStrategy(request({ destination: '' }), APP_ORIGIN)).toBe('network-only')
  })

  it('uses the shell fallback for same-origin navigation', () => {
    expect(
      selectCacheStrategy(
        request({ pathname: '/classify', mode: 'navigate', destination: 'document' }),
        APP_ORIGIN,
      ),
    ).toBe('navigation-fallback')
  })

  it('allows only same-origin static resources into runtime cache', () => {
    for (const destination of ['style', 'script', 'image', 'font', 'manifest']) {
      expect(selectCacheStrategy(request({ destination }), APP_ORIGIN)).toBe('static-cache')
    }
  })
})
