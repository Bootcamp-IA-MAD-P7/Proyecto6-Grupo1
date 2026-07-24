import type { PredictionResponse } from '../contracts/prediction'
import {
  createContractPredictionClient,
  type PredictionClient,
  type PredictionTransport,
} from './prediction-client'

interface MockPredictionClientOptions {
  latencyMs?: number
}

const wait = (duration: number) =>
  new Promise<void>((resolve) => {
    window.setTimeout(resolve, duration)
  })

export const createMockPredictionClient = (
  options: MockPredictionClientOptions = {},
): PredictionClient => {
  const transport: PredictionTransport = {
    async createPrediction() {
      await wait(options.latencyMs ?? 450)

      const response: PredictionResponse = {
        prediction_id: crypto.randomUUID(),
        predicted_class: 'Credit reporting or other personal consumer reports',
        alternatives: [
          { class_label: 'Debt collection', confidence: null },
          { class_label: 'Credit card', confidence: null },
        ],
        confidence: null,
        review_required: true,
        review_reasons: ['confidence_unavailable'],
        model_version: 'mock-not-a-model',
        taxonomy_version: '1.0',
        created_at: new Date().toISOString(),
        warnings: ['Synthetic response for interface testing. This is not a model prediction.'],
      }

      return response
    },
  }

  return createContractPredictionClient(transport)
}
