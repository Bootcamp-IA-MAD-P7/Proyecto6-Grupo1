import { useState, useRef, useMemo, useCallback, type FormEvent } from 'react'
import { PredictionResult } from '@/components/PredictionResult'
import { useOnlineStatus } from '@/hooks/use-online-status'
import { useVoiceDictation } from '@/hooks/use-voice-dictation'
import type { PredictionResponse } from '@/contracts/prediction'
import { createMockPredictionClient } from '@/services/mock-prediction-client'
import { PredictionClientError, type PredictionClient } from '@/services/prediction-client'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'

const SYNTHETIC_EXAMPLE =
  'A payment appears twice on a monthly statement and the card holder cannot resolve the duplicate charge.'

interface ClassificationPageProps {
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

export default function ClassificationPage({ predictionClient }: ClassificationPageProps) {
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

  const handleTranscript = useCallback((text: string) => {
    setNarrative((prev) => (prev ? `${prev} ${text}` : text))
  }, [])

  const {
    isRecording,
    isSupported: isVoiceSupported,
    startRecording,
    stopRecording,
    error: voiceError,
  } = useVoiceDictation({ onTranscript: handleTranscript })

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

  if (result) {
    return <PredictionResult result={result} onReset={reset} />
  }

  return (
    <div className="space-y-6">
      {!isOnline && (
        <Alert variant="warning">
          <AlertDescription>
            <strong>You are offline.</strong> A prediction requires a service connection.
          </AlertDescription>
        </Alert>
      )}

      <form onSubmit={handleSubmit} noValidate className="space-y-6">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="mb-1 text-xs font-bold uppercase tracking-widest text-gold">
              01 · Narrative
            </p>
            <h2 className="font-serif text-3xl font-semibold text-ink">Describe what happened</h2>
          </div>
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={() => {
              setNarrative(SYNTHETIC_EXAMPLE)
              setValidationMessage('')
              narrativeRef.current?.focus()
            }}
          >
            Use a synthetic example
          </Button>
        </div>

        <div className="space-y-2">
          <label htmlFor="complaint-narrative" className="text-sm font-bold">
            Complaint narrative
          </label>
          <p id="narrative-help" className="max-w-2xl text-sm text-ink-soft">
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
            className="w-full min-h-56 resize-y rounded-lg border border-line bg-white p-4 text-ink transition-colors placeholder:text-ink-soft focus:border-forest focus:outline-none focus:ring-2 focus:ring-forest/20 disabled:cursor-wait disabled:opacity-66"
          />
          <div className="flex justify-between text-xs text-ink-soft">
            <span id="narrative-counter">{narrative.length} characters</span>
            <span>No text is retained by this prototype.</span>
          </div>
          {isVoiceSupported && (
            <div className="flex items-center gap-2">
              <Button
                type="button"
                variant={isRecording ? 'destructive' : 'outline'}
                size="sm"
                onClick={isRecording ? stopRecording : startRecording}
                disabled={isSubmitting}
              >
                {isRecording ? '⏹ Stop recording' : '🎤 Dictate'}
              </Button>
              {isRecording && (
                <span className="animate-pulse text-xs text-rust">Recording…</span>
              )}
            </div>
          )}
          {voiceError && (
            <p className="text-xs text-rust">{voiceError}</p>
          )}
        </div>

        {validationMessage && (
          <p id="narrative-error" role="alert" className="text-sm font-bold text-rust">
            {validationMessage}
          </p>
        )}

        {requestError && (
          <div ref={errorRef} role="alert" tabIndex={-1}>
            <Alert variant="destructive">
              <AlertDescription>{requestError}</AlertDescription>
            </Alert>
          </div>
        )}

        <div className="flex items-center gap-4">
          <Button type="submit" disabled={isSubmitting || !isOnline}>
            {isSubmitting ? 'Creating simulated result…' : 'Classify complaint'}
          </Button>
          <p className="max-w-sm text-xs text-ink-soft">
            The tool suggests a family. It does not route the complaint or make a final decision.
          </p>
        </div>
      </form>

      <div className="flex gap-2">
        <Badge variant="mock">Mock responses</Badge>
        <Badge variant="review">Human review required</Badge>
      </div>
    </div>
  )
}
