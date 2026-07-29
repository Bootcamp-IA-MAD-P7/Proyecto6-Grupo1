import {
  assertFeedbackCreateRequest,
  parseFeedbackAcceptedResponse,
  type FeedbackAcceptedResponse,
  type FeedbackCreateRequest,
} from '../contracts/feedback'
import { getPredictionApiBaseUrl } from './prediction-api-config'

export class FeedbackClientUnavailableError extends Error {
  constructor() {
    super('Local feedback is unavailable.')
    this.name = 'FeedbackClientUnavailableError'
  }
}

export interface FeedbackClient {
  recordFeedback(request: FeedbackCreateRequest): Promise<FeedbackAcceptedResponse>
}

export type FeedbackClientMode = 'local_api' | 'unavailable'

export interface ConfiguredFeedbackClient {
  client?: FeedbackClient
  mode: FeedbackClientMode
}

const createLocalFeedbackClient = (baseUrl: string): FeedbackClient => ({
  async recordFeedback(request) {
    assertFeedbackCreateRequest(request)

    let response: Response
    try {
      response = await fetch(`${baseUrl}/api/v1/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
      })
    } catch {
      throw new FeedbackClientUnavailableError()
    }

    if (!response.ok) {
      throw new FeedbackClientUnavailableError()
    }

    return parseFeedbackAcceptedResponse(await response.json())
  },
})

export const createConfiguredFeedbackClient = (
  apiBaseUrl?: string,
): ConfiguredFeedbackClient => {
  let resolvedApiBaseUrl = apiBaseUrl
  if (resolvedApiBaseUrl === undefined) {
    try {
      resolvedApiBaseUrl = getPredictionApiBaseUrl()
    } catch {
      return { mode: 'unavailable' }
    }
  }

  if (!resolvedApiBaseUrl) {
    return { mode: 'unavailable' }
  }

  return {
    client: createLocalFeedbackClient(resolvedApiBaseUrl),
    mode: 'local_api',
  }
}
