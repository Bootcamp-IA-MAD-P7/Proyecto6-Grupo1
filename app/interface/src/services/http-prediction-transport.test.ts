import { describe, expect, it, vi } from 'vitest'
import { createHttpPredictionTransport } from './http-prediction-transport'
import { createContractPredictionClient } from './prediction-client'

const VALID_RESPONSE = {
  prediction_id: '123e4567-e89b-42d3-a456-426614174000',
  predicted_class: 'Debt collection',
  alternatives: [{ class_label: 'Credit card', confidence: null }],
  confidence: null,
  review_required: true,
  review_reasons: ['confidence_unavailable'],
  model_version: 'synthetic-test-version',
  taxonomy_version: '1.0',
  created_at: '2026-07-28T10:00:00.000Z',
  warnings: ['Synthetic fixture.'],
}

const asFetch = (implementation: ReturnType<typeof vi.fn>) =>
  implementation as unknown as typeof fetch

describe('HTTP prediction transport', () => {
  it('posts only the typed JSON request to the versioned endpoint', async () => {
    const fetchImplementation = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => VALID_RESPONSE,
    })
    const transport = createHttpPredictionTransport({
      baseUrl: 'http://127.0.0.1:8000/',
      fetchImplementation: asFetch(fetchImplementation),
    })

    await expect(
      transport.createPrediction({ narrative: 'Synthetic input for transport verification.' }),
    ).resolves.toEqual(VALID_RESPONSE)

    expect(fetchImplementation).toHaveBeenCalledWith(
      'http://127.0.0.1:8000/api/v1/predictions',
      expect.objectContaining({
        method: 'POST',
        headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify({ narrative: 'Synthetic input for transport verification.' }),
      }),
    )
  })

  it.each([
    [400, 'bad_request'],
    [422, 'validation_error'],
    [429, 'rate_limited'],
    [500, 'service_unavailable'],
  ] as const)('maps status %i to the safe %s category', async (status, code) => {
    const transport = createHttpPredictionTransport({
      baseUrl: 'http://localhost:8000',
      fetchImplementation: asFetch(vi.fn().mockResolvedValue({ ok: false, status })),
    })

    await expect(
      transport.createPrediction({ narrative: 'Synthetic request.' }),
    ).rejects.toMatchObject({
      name: 'PredictionClientError',
      code,
    })
  })

  it('maps a timeout to a safe unavailable-service error', async () => {
    vi.useFakeTimers()
    const fetchImplementation = vi.fn(
      (_url: string, init: RequestInit) =>
        new Promise((_resolve, reject) => {
          init.signal?.addEventListener('abort', () =>
            reject(new DOMException('Aborted', 'AbortError')),
          )
        }),
    )
    const transport = createHttpPredictionTransport({
      baseUrl: 'http://localhost:8000',
      fetchImplementation: asFetch(fetchImplementation),
      timeoutMs: 10,
    })

    const request = transport.createPrediction({ narrative: 'Synthetic request.' })
    const rejection = expect(request).rejects.toMatchObject({ code: 'service_unavailable' })
    await vi.advanceTimersByTimeAsync(10)
    await rejection
    vi.useRealTimers()
  })

  it('rejects malformed JSON through the existing contract boundary', async () => {
    const transport = createHttpPredictionTransport({
      baseUrl: 'http://localhost:8000',
      fetchImplementation: asFetch(
        vi.fn().mockResolvedValue({ ok: true, json: async () => ({ invalid: true }) }),
      ),
    })
    const client = createContractPredictionClient(transport)

    await expect(
      client.createPrediction({ narrative: 'Synthetic request.' }),
    ).rejects.toMatchObject({
      name: 'PredictionClientError',
      code: 'invalid_response',
    })
  })
})
