import { FormEvent, useMemo, useRef, useState } from 'react'
import { PredictionResult } from './components/PredictionResult'
import { useOnlineStatus } from './hooks/use-online-status'
import type { PredictionResponse } from './contracts/prediction'
import { createMockPredictionClient } from './services/mock-prediction-client'
import {
  PredictionClientError,
  type PredictionClient,
} from './services/prediction-client'

const SYNTHETIC_EXAMPLE =
  'A payment appears twice on a monthly statement and the card holder cannot resolve the duplicate charge.'

interface AppProps {
  predictionClient?: PredictionClient
}

const safeErrorMessage = (error: unknown) => {
  if (error instanceof PredictionClientError) {
    if (error.code === 'rate_limited') {
      return 'Too many requests. Wait a moment before trying again.'
    }
    if (error.code === 'validation_error') {
      return 'The service could not validate this narrative. Review the text and try again.'
    }
  }

  return 'The simulated prediction service is unavailable. Your narrative was not stored.'
}

export default function App({ predictionClient }: AppProps) {
  const client = useMemo(
    () => predictionClient ?? createMockPredictionClient(),
    [predictionClient],
  )
  const isOnline = useOnlineStatus()
  const narrativeRef = useRef<HTMLTextAreaElement>(null)
  const errorRef = useRef<HTMLDivElement>(null)
  const [narrative, setNarrative] = useState('')
  const [validationMessage, setValidationMessage] = useState('')
  const [requestError, setRequestError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [result, setResult] = useState<PredictionResponse | null>(null)

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setValidationMessage('')
    setRequestError('')

    if (!narrative.trim()) {
      setValidationMessage('Enter a complaint narrative before continuing.')
      narrativeRef.current?.focus()
      return
    }

    if (!isOnline) {
      setRequestError('A connection to the prediction service is required.')
      errorRef.current?.focus()
      return
    }

    setIsSubmitting(true)

    try {
      const response = await client.createPrediction({ narrative: narrative.trim() })
      setNarrative('')
      setResult(response)
    } catch (error) {
      setRequestError(safeErrorMessage(error))
      window.setTimeout(() => errorRef.current?.focus(), 0)
    } finally {
      setIsSubmitting(false)
    }
  }

  const reset = () => {
    setResult(null)
    setRequestError('')
    setValidationMessage('')
    window.setTimeout(() => narrativeRef.current?.focus(), 0)
  }

  return (
    <div className="app-shell">
      <header className="site-header">
        <a className="brand" href="#main-content" aria-label="Complaint Routing home">
          <img src="/app-mark.svg" alt="" width="42" height="42" />
          <span>
            <strong>Complaint Routing</strong>
            <small>Decision-support workspace</small>
          </span>
        </a>
        <div className="header-badges" aria-label="Prototype status">
          <span className="mode-pill">Prototype</span>
          <span className="mode-pill mode-pill--mock">Mock responses</span>
        </div>
      </header>

      <main id="main-content">
        <section className="hero" aria-labelledby="page-title">
          <div>
            <p className="eyebrow">Classify with context. Decide with care.</p>
            <h1 id="page-title">Find the most relevant complaint family</h1>
            <p className="hero__lead">
              Paste a complaint narrative to test the future workflow. Results in this build are
              synthetic and must always be reviewed by a person.
            </p>
          </div>
          <aside className="hero__scope" aria-label="Prototype scope">
            <p>Current scope</p>
            <strong>11 CFPB product families</strong>
            <span>Interface validation only</span>
          </aside>
        </section>

        <div className="language-note" role="note">
          Prototype copy is in English for testing; the product language policy is still open.
        </div>

        {!isOnline && (
          <div className="notice notice--offline" role="status">
            <strong>You are offline.</strong> The workspace shell is available, but a prediction
            requires a service connection. No result will be fabricated.
          </div>
        )}

        <section className="workspace" aria-label="Complaint classification workspace">
          <div className="workspace__form">
            {result ? (
              <PredictionResult result={result} onReset={reset} />
            ) : (
              <form onSubmit={handleSubmit} noValidate>
                <div className="form-heading">
                  <div>
                    <p className="step-label">01 · Narrative</p>
                    <h2>Describe what happened</h2>
                  </div>
                  <button
                    className="text-button"
                    type="button"
                    onClick={() => {
                      setNarrative(SYNTHETIC_EXAMPLE)
                      setValidationMessage('')
                      narrativeRef.current?.focus()
                    }}
                  >
                    Use a synthetic example
                  </button>
                </div>

                <label htmlFor="complaint-narrative">Complaint narrative</label>
                <p className="field-help" id="narrative-help">
                  Include the issue and attempted resolution. Do not enter names, account numbers,
                  addresses or other unnecessary personal data.
                </p>
                <textarea
                  id="complaint-narrative"
                  ref={narrativeRef}
                  value={narrative}
                  onChange={(event) => {
                    setNarrative(event.target.value)
                    if (validationMessage) setValidationMessage('')
                  }}
                  aria-describedby={`narrative-help narrative-counter${validationMessage ? ' narrative-error' : ''}`}
                  aria-invalid={Boolean(validationMessage)}
                  placeholder="Enter the complaint narrative…"
                  rows={9}
                  disabled={isSubmitting}
                />
                <div className="field-meta">
                  <span id="narrative-counter">{narrative.length} characters</span>
                  <span>No text is retained by this prototype.</span>
                </div>

                {validationMessage && (
                  <p className="field-error" id="narrative-error" role="alert">
                    {validationMessage}
                  </p>
                )}

                {requestError && (
                  <div
                    className="notice notice--error"
                    ref={errorRef}
                    role="alert"
                    tabIndex={-1}
                  >
                    {requestError}
                  </div>
                )}

                <div className="form-actions">
                  <button
                    className="button button--primary"
                    type="submit"
                    disabled={isSubmitting || !isOnline}
                  >
                    {isSubmitting ? 'Creating simulated result…' : 'Classify complaint'}
                  </button>
                  <p>
                    The tool suggests a family. It does not route the complaint or make a final
                    decision.
                  </p>
                </div>
              </form>
            )}
          </div>

          <aside className="workspace__guide" aria-labelledby="guide-title">
            <p className="step-label">Before you continue</p>
            <h2 id="guide-title">A safer review flow</h2>
            <ol className="guide-list">
              <li>
                <span>1</span>
                <div>
                  <strong>Remove personal data</strong>
                  <p>Use only the information needed to understand the issue.</p>
                </div>
              </li>
              <li>
                <span>2</span>
                <div>
                  <strong>Review the suggestion</strong>
                  <p>Compare the primary class with the alternatives.</p>
                </div>
              </li>
              <li>
                <span>3</span>
                <div>
                  <strong>Keep human ownership</strong>
                  <p>The operator remains responsible for the next step.</p>
                </div>
              </li>
            </ol>
            <div className="privacy-card">
              <strong>Privacy by default</strong>
              <p>
                This build does not create history, feedback records or cached API responses.
              </p>
            </div>
          </aside>
        </section>
      </main>

      <footer>
        <span>Contract version 0.1.0</span>
        <span>Not connected to a trained model</span>
      </footer>
    </div>
  )
}
