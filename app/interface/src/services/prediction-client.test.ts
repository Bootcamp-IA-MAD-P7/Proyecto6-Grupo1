import { describe, expect, it } from 'vitest'
import openapi from '../../../../docs/api/openapi.json'
import { CANONICAL_CLASSES, REVIEW_REASONS } from '../contracts/prediction'
import { createContractPredictionClient, type PredictionTransport } from './prediction-client'

const VALID_RESPONSE = {
  prediction_id: '123e4567-e89b-42d3-a456-426614174000',
  predicted_class: 'Debt collection',
  alternatives: [{ class_label: 'Credit card', confidence: null }],
  confidence: null,
  review_required: true,
  review_reasons: ['confidence_unavailable'],
  model_version: 'synthetic-test-version',
  taxonomy_version: '1.0',
  created_at: '2026-07-24T10:00:00.000Z',
  warnings: ['Synthetic fixture.'],
}

describe('PredictionClient contract boundary', () => {
  it('keeps canonical classes and review reasons aligned with OpenAPI', () => {
    const schemas = openapi.components.schemas

    expect(CANONICAL_CLASSES).toEqual(schemas.CanonicalClass.enum)
    expect(REVIEW_REASONS).toEqual(schemas.PredictionResponse.properties.review_reasons.items.enum)
  })

  it('accepts a response that matches the API contract', async () => {
    const transport: PredictionTransport = {
      createPrediction: async () => VALID_RESPONSE,
    }
    const client = createContractPredictionClient(transport)

    await expect(client.createPrediction({ narrative: 'Synthetic complaint.' })).resolves.toEqual(
      VALID_RESPONSE,
    )
  })

  it('rejects an incompatible response at the client boundary', async () => {
    const transport: PredictionTransport = {
      createPrediction: async () => ({
        ...VALID_RESPONSE,
        predicted_class: 'Unknown product',
      }),
    }
    const client = createContractPredictionClient(transport)

    await expect(
      client.createPrediction({ narrative: 'Synthetic complaint.' }),
    ).rejects.toMatchObject({
      name: 'PredictionClientError',
      code: 'invalid_response',
    })
  })

  it('rejects a blank narrative before calling the transport', async () => {
    let transportCalled = false
    const transport: PredictionTransport = {
      createPrediction: async () => {
        transportCalled = true
        return VALID_RESPONSE
      },
    }
    const client = createContractPredictionClient(transport)

    await expect(client.createPrediction({ narrative: '   ' })).rejects.toMatchObject({
      name: 'PredictionClientError',
      code: 'validation_error',
    })
    expect(transportCalled).toBe(false)
  })
})
