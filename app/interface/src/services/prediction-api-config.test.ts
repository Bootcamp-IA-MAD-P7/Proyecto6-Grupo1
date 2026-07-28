import { describe, expect, it } from 'vitest'
import { getPredictionApiBaseUrl, PredictionApiConfigurationError } from './prediction-api-config'

describe('prediction API configuration', () => {
  it('keeps the API absent when no explicit value is provided', () => {
    expect(getPredictionApiBaseUrl('')).toBeUndefined()
  })

  it('normalises an explicit local API origin', () => {
    expect(getPredictionApiBaseUrl(' http://127.0.0.1:8000/ ')).toBe('http://127.0.0.1:8000')
  })

  it.each(['https://example.com', 'ftp://localhost:8000', 'http://localhost:8000/api'])(
    'rejects an unsafe configured URL: %s',
    (value) => {
      expect(() => getPredictionApiBaseUrl(value)).toThrow(PredictionApiConfigurationError)
    },
  )
})
