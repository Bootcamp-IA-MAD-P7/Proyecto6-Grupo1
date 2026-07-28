import type { PredictionRequest } from '../contracts/prediction'
import {
  PredictionClientError,
  type PredictionErrorCode,
  type PredictionTransport,
} from './prediction-client'

export const DEFAULT_PREDICTION_REQUEST_TIMEOUT_MS = 10_000

interface HttpPredictionTransportOptions {
  baseUrl: string
  fetchImplementation?: typeof fetch
  timeoutMs?: number
}

const errorCodeForStatus = (status: number): PredictionErrorCode => {
  if (status === 400) return 'bad_request'
  if (status === 422) return 'validation_error'
  if (status === 429) return 'rate_limited'
  return 'service_unavailable'
}

const errorMessageForStatus = (status: number): string => {
  if (status === 400 || status === 422) {
    return 'Prediction request could not be accepted.'
  }
  if (status === 429) {
    return 'Prediction service is busy. Please try again later.'
  }
  return 'Prediction service is unavailable. Please try again later.'
}

const endpointFor = (baseUrl: string) => `${baseUrl.replace(/\/+$/, '')}/api/v1/predictions`

export const createHttpPredictionTransport = ({
  baseUrl,
  fetchImplementation = fetch,
  timeoutMs = DEFAULT_PREDICTION_REQUEST_TIMEOUT_MS,
}: HttpPredictionTransportOptions): PredictionTransport => ({
  async createPrediction(request: PredictionRequest): Promise<unknown> {
    const controller = new AbortController()
    const timeout = window.setTimeout(() => controller.abort(), timeoutMs)

    try {
      const response = await fetchImplementation(endpointFor(baseUrl), {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
        signal: controller.signal,
      })

      if (!response.ok) {
        throw new PredictionClientError(
          errorCodeForStatus(response.status),
          errorMessageForStatus(response.status),
        )
      }

      try {
        return await response.json()
      } catch (cause) {
        throw new PredictionClientError(
          'invalid_response',
          'Prediction service returned an incompatible response.',
          { cause },
        )
      }
    } catch (cause) {
      if (cause instanceof PredictionClientError) {
        throw cause
      }

      if (controller.signal.aborted) {
        throw new PredictionClientError(
          'service_unavailable',
          'Prediction service did not respond in time. Please try again later.',
          { cause },
        )
      }

      throw new PredictionClientError(
        'service_unavailable',
        'Prediction service is unavailable. Please try again later.',
        { cause },
      )
    } finally {
      window.clearTimeout(timeout)
    }
  },
})
