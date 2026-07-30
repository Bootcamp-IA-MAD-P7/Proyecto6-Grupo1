import { useEffect, useMemo, useRef, useState } from 'react'
import {
  CANONICAL_CLASSES,
  type CanonicalClass,
  type PredictionResponse,
  type ReviewReason,
} from '@/contracts/prediction'
import {
  FEEDBACK_DECISIONS,
  FEEDBACK_PURPOSES,
  type FeedbackDecision,
  type FeedbackPurpose,
} from '@/contracts/feedback'
import type { PredictionClientMode } from '@/services/configured-prediction-client'
import { createConfiguredFeedbackClient } from '@/services/configured-feedback-client'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { AlertTriangle, CheckCircle, Info, RotateCcw } from 'lucide-react'

interface PredictionResultProps {
  result: PredictionResponse
  clientMode?: PredictionClientMode
  onReset: () => void
}

const REVIEW_REASON_LABELS: Record<ReviewReason, string> = {
  low_confidence: 'Low calibrated confidence',
  confidence_unavailable: 'Calibrated confidence is not available',
  out_of_domain: 'The narrative may be outside the approved domain',
  language_policy: 'The active language policy requires review',
  service_policy: 'The service policy requires review',
}

export function PredictionResult({ result, clientMode, onReset }: PredictionResultProps) {
  const titleRef = useRef<HTMLHeadingElement>(null)
  const isMockResult = clientMode === 'mock' || result.model_version === 'mock-not-a-model'
  const visibleAlternatives = result.alternatives.slice(0, 3)
  const configuredFeedbackClient = useMemo(() => createConfiguredFeedbackClient(), [])
  const [decision, setDecision] = useState<FeedbackDecision>('confirmed')
  const [purpose, setPurpose] = useState<FeedbackPurpose>('human_review_quality_assurance')
  const [reviewedClass, setReviewedClass] = useState<CanonicalClass | ''>('')
  const [isSavingFeedback, setIsSavingFeedback] = useState(false)
  const [feedbackStatus, setFeedbackStatus] = useState<'idle' | 'recorded' | 'error'>('idle')
  const isLocalPrediction = !isMockResult && clientMode === 'local_api'
  const canRecordFeedback =
    isLocalPrediction &&
    configuredFeedbackClient.mode === 'local_api' &&
    configuredFeedbackClient.client !== undefined

  useEffect(() => {
    titleRef.current?.focus()
  }, [])

  const recordFeedback = async () => {
    if (!configuredFeedbackClient.client || (decision === 'corrected' && !reviewedClass)) {
      return
    }

    const reviewedClassMetadata =
      decision === 'corrected' && reviewedClass ? { reviewed_class: reviewedClass } : {}

    setIsSavingFeedback(true)
    setFeedbackStatus('idle')
    try {
      await configuredFeedbackClient.client.recordFeedback({
        prediction_id: result.prediction_id,
        model_version: result.model_version,
        taxonomy_version: result.taxonomy_version,
        suggested_class: result.predicted_class,
        ...reviewedClassMetadata,
        decision,
        purpose,
      })
      setFeedbackStatus('recorded')
    } catch {
      setFeedbackStatus('error')
    } finally {
      setIsSavingFeedback(false)
    }
  }

  return (
    <div className="space-y-6">
      <Alert variant="warning">
        <AlertTriangle className="h-4 w-4" />
        <AlertDescription>
          {isMockResult ? (
            <strong>El servicio de predicción no está disponible.</strong>
          ) : (
            <>
              <strong>Human review remains required.</strong> This response supports review and
              cannot route a complaint or make a final decision.
            </>
          )}
        </AlertDescription>
      </Alert>

      <div className="flex flex-col items-start gap-2 sm:flex-row sm:justify-between sm:gap-4">
        <div>
          <p className="mb-1 text-xs font-bold uppercase tracking-widest text-gold-ink">
            {isMockResult ? 'Servicio no disponible' : 'Predicción local'}
          </p>
          <h1
            ref={titleRef}
            tabIndex={-1}
            className="text-3xl font-bold tracking-tight text-ink focus:outline-none"
          >
            {result.predicted_class}
          </h1>
        </div>
        <Badge variant="review">Human review required</Badge>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <Card>
          <CardHeader className="flex flex-row items-center gap-2 space-y-0">
            <Info className="h-4 w-4 text-ink-soft" />
            <CardTitle className="text-sm">Calibrated confidence</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">
              {result.confidence === null
                ? 'Not available'
                : `${Math.round(result.confidence * 100)}%`}
            </p>
            <p className="mt-1 text-sm text-ink-soft">
              {isMockResult
                ? 'No percentage is available for this mock response.'
                : 'This score supports review and is not an automatic routing decision.'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center gap-2 space-y-0">
            <AlertTriangle className="h-4 w-4 text-ink-soft" />
            <CardTitle className="text-sm">Review reason</CardTitle>
          </CardHeader>
          <CardContent>
            {result.review_reasons.length > 0 ? (
              <ul className="space-y-1.5">
                {result.review_reasons.map((reason) => (
                  <li key={reason} className="flex items-center gap-2 text-sm">
                    <CheckCircle className="h-3.5 w-3.5 shrink-0 text-ink-soft" />
                    {REVIEW_REASON_LABELS[reason]}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-ink-soft">
                Human review is required before any routing or final decision.
              </p>
            )}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader className="flex flex-row items-center gap-2 space-y-0">
          <Info className="h-4 w-4 text-ink-soft" />
          <CardTitle className="text-sm">Other classes to consider</CardTitle>
        </CardHeader>
        <CardContent>
          {visibleAlternatives.length > 0 ? (
            <ol className="list-decimal space-y-1 pl-5">
              {visibleAlternatives.map((alternative) => (
                <li key={alternative.class_label} className="text-sm">
                  {alternative.class_label}
                </li>
              ))}
            </ol>
          ) : (
            <p className="text-sm text-ink-soft">No alternative classes are available.</p>
          )}
        </CardContent>
      </Card>

      <div className="flex flex-wrap gap-4 rounded-lg bg-sand px-4 py-3 font-mono text-xs text-ink-soft">
        <span>{isMockResult ? 'Source: No disponible' : 'Source: Local API'}</span>
        <span>Model version: {result.model_version}</span>
        <span>Taxonomy: {result.taxonomy_version}</span>
        <span>Reference: {result.prediction_id.slice(0, 8)}</span>
      </div>

      {result.warnings.map((warning) => (
        <Alert key={warning} variant="warning">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{warning}</AlertDescription>
        </Alert>
      ))}

      {isLocalPrediction && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Record human review</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {canRecordFeedback ? (
              <>
                <div className="grid gap-4 sm:grid-cols-2">
                  <label className="space-y-1 text-sm font-bold">
                    Review decision
                    <select
                      value={decision}
                      onChange={(event) => {
                        const nextDecision = event.target.value as FeedbackDecision
                        setDecision(nextDecision)
                        if (nextDecision !== 'corrected') setReviewedClass('')
                      }}
                      className="block w-full rounded-md border border-line bg-paper px-3 py-2 text-sm font-normal"
                    >
                      {FEEDBACK_DECISIONS.map((option) => (
                        <option key={option} value={option}>
                          {option}
                        </option>
                      ))}
                    </select>
                  </label>

                  <label className="space-y-1 text-sm font-bold">
                    Purpose
                    <select
                      value={purpose}
                      onChange={(event) => setPurpose(event.target.value as FeedbackPurpose)}
                      className="block w-full rounded-md border border-line bg-paper px-3 py-2 text-sm font-normal"
                    >
                      {FEEDBACK_PURPOSES.map((option) => (
                        <option key={option} value={option}>
                          {option}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>

                {decision === 'corrected' && (
                  <label className="block space-y-1 text-sm font-bold">
                    Reviewed class
                    <select
                      value={reviewedClass}
                      onChange={(event) => setReviewedClass(event.target.value as CanonicalClass)}
                      className="block w-full rounded-md border border-line bg-paper px-3 py-2 text-sm font-normal"
                    >
                      <option value="">Select the reviewed class</option>
                      {CANONICAL_CLASSES.map((classLabel) => (
                        <option key={classLabel} value={classLabel}>
                          {classLabel}
                        </option>
                      ))}
                    </select>
                  </label>
                )}

                <Button
                  type="button"
                  onClick={recordFeedback}
                  disabled={isSavingFeedback || (decision === 'corrected' && !reviewedClass)}
                >
                  {isSavingFeedback ? 'Saving review...' : 'Record review'}
                </Button>
              </>
            ) : (
              <Alert variant="warning">
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>
                  Local feedback is unavailable. No feedback was recorded and this prediction is
                  unchanged.
                </AlertDescription>
              </Alert>
            )}

            <p className="text-xs text-ink-soft">
              Only model version, classes, decision, and purpose are sent. The narrative, identity,
              free text, and probabilities are not stored.
            </p>

            {feedbackStatus === 'recorded' && (
              <Alert>
                <CheckCircle className="h-4 w-4" />
                <AlertDescription>
                  Feedback was recorded locally. It does not change this prediction or retrain a
                  model automatically.
                </AlertDescription>
              </Alert>
            )}
            {feedbackStatus === 'error' && (
              <Alert variant="destructive" role="alert">
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>
                  Feedback could not be recorded locally. This prediction is unchanged; check the
                  local service and try again.
                </AlertDescription>
              </Alert>
            )}
          </CardContent>
        </Card>
      )}

      <p className="text-sm text-ink-soft">
        This output supports review. It does not make a final financial or routing decision.
      </p>

      <Button onClick={onReset}>
        <RotateCcw className="h-4 w-4" />
        Start a new classification
      </Button>
    </div>
  )
}
