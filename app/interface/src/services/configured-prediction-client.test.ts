import { describe, expect, it, vi } from 'vitest'
import { createConfiguredPredictionClient } from './configured-prediction-client'

describe('configured prediction client', () => {
  it('uses the contract-valid mock client when no API base URL is supplied', async () => {
    const fetchSpy = vi.spyOn(window, 'fetch')
    const { client, mode } = createConfiguredPredictionClient('')

    const response = await client.createPrediction({ narrative: 'Synthetic mock-mode request.' })

    expect(mode).toBe('mock')
    expect(response.model_version).toBe('mock-not-a-model')
    expect(fetchSpy).not.toHaveBeenCalled()
  })

  it('uses the typed local client only after an explicit API base URL is supplied', () => {
    const { client, mode } = createConfiguredPredictionClient('http://127.0.0.1:8000')

    expect(mode).toBe('local_api')
    expect(client).toHaveProperty('createPrediction')
  })
})
