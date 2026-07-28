import { createHttpPredictionTransport } from './http-prediction-transport'
import { createMockPredictionClient } from './mock-prediction-client'
import { getPredictionApiBaseUrl } from './prediction-api-config'
import { createContractPredictionClient, type PredictionClient } from './prediction-client'

export type PredictionClientMode = 'local_api' | 'mock'

export interface ConfiguredPredictionClient {
  client: PredictionClient
  mode: PredictionClientMode
}

export const createConfiguredPredictionClient = (
  apiBaseUrl: string | undefined = getPredictionApiBaseUrl(),
): ConfiguredPredictionClient => {
  if (!apiBaseUrl) {
    return {
      client: createMockPredictionClient(),
      mode: 'mock',
    }
  }

  return {
    client: createContractPredictionClient(createHttpPredictionTransport({ baseUrl: apiBaseUrl })),
    mode: 'local_api',
  }
}
