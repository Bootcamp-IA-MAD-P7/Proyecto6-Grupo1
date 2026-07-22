import type { PredictionRequest, PredictionResponse } from '../contracts/prediction'

export type PredictionErrorCode =
  | 'validation_error'
  | 'rate_limited'
  | 'service_unavailable'

export class PredictionClientError extends Error {
  readonly code: PredictionErrorCode

  constructor(code: PredictionErrorCode, message: string) {
    super(message)
    this.name = 'PredictionClientError'
    this.code = code
  }
}

export interface PredictionClient {
  createPrediction(request: PredictionRequest): Promise<PredictionResponse>
}
