import { useState, useRef, useMemo, useCallback, type FormEvent } from 'react'
import { PredictionResult } from '@/components/PredictionResult'
import HelpfulTip from '@/components/HelpfulTip'
import { useOnlineStatus, type ConnectivityCheck } from '@/hooks/use-online-status'
import { useVoiceDictation } from '@/hooks/use-voice-dictation'
import { MAX_NARRATIVE_CHARACTERS, type PredictionResponse } from '@/contracts/prediction'
import {
  createConfiguredPredictionClient,
  type PredictionClientMode,
} from '@/services/configured-prediction-client'
import { PredictionClientError, type PredictionClient } from '@/services/prediction-client'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { WifiOff, Mic, MicOff, Send, Sparkles, AlertTriangle } from 'lucide-react'

const SYNTHETIC_EXAMPLE =
  'A payment appears twice on a monthly statement and the card holder cannot resolve the duplicate charge.'
const MAX_NARRATIVE_CHARACTERS_LABEL = MAX_NARRATIVE_CHARACTERS.toLocaleString('en-US')

interface ClassificationPageProps {
  predictionClient?: PredictionClient
  predictionClientMode?: PredictionClientMode
  connectivityCheck?: ConnectivityCheck
}

const safeErrorMessage = (error: unknown) => {
  if (error instanceof PredictionClientError) {
    if (error.code === 'rate_limited') {
      return 'Too many requests. Wait a moment before trying again.'
    }
    if (error.code === 'bad_request' || error.code === 'validation_error') {
      return 'The service could not validate this narrative. Review the text and try again.'
    }
    if (error.code === 'invalid_response') {
      return 'The prediction response could not be safely validated. No recommendation was shown.'
    }
  }
  return 'The prediction service is unavailable. Your narrative was not stored.'
}

export default function ClassificationPage({
  predictionClient,
  predictionClientMode,
  connectivityCheck,
}: ClassificationPageProps) {
  const configuredClient = useMemo(
    () =>
      predictionClient
        ? { client: predictionClient, mode: predictionClientMode }
        : createConfiguredPredictionClient(),
    [predictionClient, predictionClientMode],
  )
  const client = configuredClient.client
  const { isOnline, verifyOnline } = useOnlineStatus(connectivityCheck)
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

    if (narrative.length > MAX_NARRATIVE_CHARACTERS) {
      setValidationMessage(
        `Keep the narrative to ${MAX_NARRATIVE_CHARACTERS_LABEL} characters or fewer.`,
      )
      narrativeRef.current?.focus()
      return
    }

    setIsSubmitting(true)

    try {
      if (!(await verifyOnline())) {
        setRequestError('A connection to the prediction service is required.')
        window.setTimeout(() => errorRef.current?.focus(), 0)
        return
      }

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
    return <PredictionResult result={result} clientMode={configuredClient.mode} onReset={reset} />
  }

  return (
    <div className="space-y-6">
      {!isOnline && (
        <Alert variant="warning">
          <WifiOff className="h-4 w-4" />
          <AlertDescription>
            <strong>You are offline.</strong> A prediction requires a service connection.
          </AlertDescription>
        </Alert>
      )}

      <form onSubmit={handleSubmit} noValidate aria-busy={isSubmitting} className="space-y-6">
        <div className="flex flex-col items-start gap-2 sm:flex-row sm:justify-between sm:gap-4">
          <div>
            <p className="mb-1 text-xs font-bold uppercase tracking-widest text-gold-ink">
              Narrative
            </p>
            <h1 className="text-3xl font-bold tracking-tight text-ink">Describe what happened</h1>
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
            <Sparkles className="h-4 w-4" />
            Use example
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
            placeholder="Enter the complaint narrative..."
            rows={9}
            maxLength={MAX_NARRATIVE_CHARACTERS}
            disabled={isSubmitting}
            className="w-full min-h-56 resize-y rounded-lg border border-line bg-paper p-4 text-ink transition-colors placeholder:text-ink-soft focus:border-forest focus:outline-none focus:ring-2 focus:ring-forest/20 disabled:cursor-wait disabled:opacity-66"
          />
          <div className="flex flex-col gap-1 text-xs text-ink-soft sm:flex-row sm:justify-between">
            <span id="narrative-counter">
              {narrative.length.toLocaleString('en-US')} / {MAX_NARRATIVE_CHARACTERS_LABEL}{' '}
              characters
            </span>
            <span>No text is retained by this prototype.</span>
          </div>
          {isVoiceSupported ? (
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Button
                  type="button"
                  variant={isRecording ? 'destructive' : 'outline'}
                  size="sm"
                  onClick={isRecording ? stopRecording : startRecording}
                  disabled={isSubmitting}
                  aria-describedby="dictation-privacy"
                >
                  {isRecording ? (
                    <>
                      <MicOff className="h-4 w-4" />
                      Stop dictation
                    </>
                  ) : (
                    <>
                      <Mic className="h-4 w-4" />
                      Start dictation
                    </>
                  )}
                </Button>
                {isRecording && (
                  <span role="status" className="flex items-center gap-1 text-xs text-rust">
                    <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-rust" />
                    Listening...
                  </span>
                )}
              </div>
              <p id="dictation-privacy" className="max-w-2xl text-xs text-ink-soft">
                Starting dictation asks for microphone permission. Your browser or speech provider
                may process the audio. This application does not store the audio or transcript;
                review the text before submitting it.
              </p>
            </div>
          ) : (
            <p className="text-xs text-ink-soft">
              Voice dictation is not available in this browser. You can continue typing.
            </p>
          )}
          {voiceError && (
            <p role="alert" className="text-xs text-rust">
              {voiceError}
            </p>
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
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>{requestError}</AlertDescription>
            </Alert>
          </div>
        )}

        <div className="flex flex-col items-start gap-3 sm:flex-row sm:items-center sm:gap-4">
          <Button type="submit" disabled={isSubmitting || !isOnline}>
            <Send className="h-4 w-4" />
            {isSubmitting ? 'Classifying...' : 'Classify complaint'}
          </Button>
          <p className="max-w-sm text-xs text-ink-soft">
            The tool suggests a family. It does not route the complaint or make a final decision.
          </p>
        </div>
        {isSubmitting && (
          <p role="status" aria-live="polite" className="sr-only">
            Creating a recommendation. Please wait.
          </p>
        )}
      </form>

      <div className="flex flex-wrap gap-2">
        <Badge variant="mock">Mock responses</Badge>
        <Badge variant="review">Human review required</Badge>
      </div>

      <HelpfulTip />
    </div>
  )
}
