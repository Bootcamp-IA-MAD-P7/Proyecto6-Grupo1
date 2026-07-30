const LOCAL_API_HOSTS = new Set(['localhost', '127.0.0.1', '[::1]', '::1'])

export class PredictionApiConfigurationError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'PredictionApiConfigurationError'
  }
}

export const getPredictionApiBaseUrl = (
  configuredValue: string | undefined = import.meta.env.VITE_PREDICTION_API_BASE_URL,
): string | undefined => {
  const value = configuredValue?.trim()

  if (!value) {
    // When no explicit URL is configured, use the current origin.
    // This works with the Nginx reverse proxy setup where /api/ is
    // proxied to the backend on the same domain.
    if (typeof window !== 'undefined' && window.location?.origin) {
      return window.location.origin
    }
    return undefined
  }

  let url: URL
  try {
    url = new URL(value)
  } catch {
    throw new PredictionApiConfigurationError('Prediction API URL must be a valid local URL.')
  }

  if (!['http:', 'https:'].includes(url.protocol) || !LOCAL_API_HOSTS.has(url.hostname)) {
    throw new PredictionApiConfigurationError('Prediction API URL must use a local http(s) origin.')
  }

  if (url.username || url.password || url.search || url.hash || url.pathname !== '/') {
    throw new PredictionApiConfigurationError(
      'Prediction API URL must not include credentials, a path, or query data.',
    )
  }

  return url.origin
}
