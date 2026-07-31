import {
  assertFeedbackCreateRequest,
  parseFeedbackAcceptedResponse,
  parseFeedbackSummaryResponse,
  type FeedbackAcceptedResponse,
  type FeedbackCreateRequest,
  type FeedbackSummaryResponse,
} from '../contracts/feedback'
import { getPredictionApiBaseUrl } from './prediction-api-config'
import { getStoredToken } from './auth-client'

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

export interface FeedbackSummaryClient {
  getSummary(): Promise<FeedbackSummaryResponse>
}

export interface ConfiguredFeedbackSummaryClient {
  client?: FeedbackSummaryClient
  mode: FeedbackClientMode
}

const createLocalFeedbackClient = (baseUrl: string): FeedbackClient => ({
  async recordFeedback(request) {
    assertFeedbackCreateRequest(request)
    const token = getStoredToken()
    if (!token) {
      throw new FeedbackClientUnavailableError()
    }

    let response: Response
    try {
      response = await fetch(`${baseUrl}/api/v1/feedback`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
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

export const createConfiguredFeedbackClient = (apiBaseUrl?: string): ConfiguredFeedbackClient => {
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

export const createConfiguredFeedbackSummaryClient = (
  apiBaseUrl?: string,
): ConfiguredFeedbackSummaryClient => {
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
    client: {
      async getSummary() {
        const token = getStoredToken()
        if (!token) {
          throw new FeedbackClientUnavailableError()
        }

        let response: Response
        try {
          response = await fetch(`${resolvedApiBaseUrl}/api/v1/feedback/summary`, {
            headers: { Authorization: `Bearer ${token}` },
          })
        } catch {
          throw new FeedbackClientUnavailableError()
        }

        if (!response.ok) {
          throw new FeedbackClientUnavailableError()
        }

        try {
          return parseFeedbackSummaryResponse(await response.json())
        } catch {
          throw new FeedbackClientUnavailableError()
        }
      },
    },
    mode: 'local_api',
  }
}
