import {
  assertPredictionRequest,
  parsePredictionResponse,
  type PredictionRequest,
  type PredictionResponse,
} from '../contracts/prediction'

export type PredictionErrorCode =
  'bad_request' | 'validation_error' | 'rate_limited' | 'service_unavailable' | 'invalid_response'

export class PredictionClientError extends Error {
  readonly code: PredictionErrorCode

  constructor(code: PredictionErrorCode, message: string, options?: ErrorOptions) {
    super(message, options)
    this.name = 'PredictionClientError'
    this.code = code
  }
}

export interface PredictionClient {
  createPrediction(request: PredictionRequest): Promise<PredictionResponse>
}

export interface PredictionTransport {
  createPrediction(request: PredictionRequest): Promise<unknown>
}

export const createContractPredictionClient = (
  transport: PredictionTransport,
): PredictionClient => ({
  async createPrediction(request) {
    try {
      assertPredictionRequest(request)
    } catch (cause) {
      throw new PredictionClientError(
        'validation_error',
        'Prediction request does not match the API contract.',
        { cause },
      )
    }

    const response = await transport.createPrediction(request)

    try {
      return parsePredictionResponse(response)
    } catch (cause) {
      throw new PredictionClientError(
        'invalid_response',
        'Prediction service returned an incompatible response.',
        { cause },
      )
    }
  },
})
