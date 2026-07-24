import { useEffect, useRef } from 'react'
import type { PredictionResponse, ReviewReason } from '@/contracts/prediction'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'

interface PredictionResultProps {
  result: PredictionResponse
  onReset: () => void
}

const REVIEW_REASON_LABELS: Record<ReviewReason, string> = {
  low_confidence: 'Low calibrated confidence',
  confidence_unavailable: 'Calibrated confidence is not available',
  out_of_domain: 'The narrative may be outside the approved domain',
  language_policy: 'The active language policy requires review',
  service_policy: 'The service policy requires review',
}

export function PredictionResult({ result, onReset }: PredictionResultProps) {
  const titleRef = useRef<HTMLHeadingElement>(null)

  useEffect(() => {
    titleRef.current?.focus()
  }, [])

  return (
    <div className="space-y-6">
      <Alert variant="warning">
        <AlertDescription>
          <strong>Interface demonstration only.</strong> This response is synthetic, has no
          calibrated score and cannot route a complaint.
        </AlertDescription>
      </Alert>

      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="mb-1 text-xs font-bold uppercase tracking-widest text-gold">
            Mock response · demo only
          </p>
          <h2 ref={titleRef} tabIndex={-1} className="font-serif text-3xl font-semibold text-ink">
            {result.predicted_class}
          </h2>
        </div>
        <Badge variant="review">Human review required</Badge>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Calibrated confidence</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="font-serif text-2xl">
              {result.confidence === null
                ? 'Not available'
                : `${Math.round(result.confidence * 100)}%`}
            </p>
            <p className="mt-1 text-sm text-ink-soft">
              No percentage is available for this mock response.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Review reason</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-1">
              {result.review_reasons.map((reason) => (
                <li key={reason} className="text-sm">
                  {REVIEW_REASON_LABELS[reason]}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Other classes to consider</CardTitle>
        </CardHeader>
        <CardContent>
          <ol className="list-decimal space-y-1 pl-5">
            {result.alternatives.map((alternative) => (
              <li key={alternative.class_label} className="text-sm">
                {alternative.class_label}
              </li>
            ))}
          </ol>
        </CardContent>
      </Card>

      <div className="flex flex-wrap gap-4 font-mono text-xs text-ink-soft">
        <span>Mock source: {result.model_version}</span>
        <span>Taxonomy: {result.taxonomy_version}</span>
        <span>Reference: {result.prediction_id.slice(0, 8)}</span>
      </div>

      {result.warnings.map((warning) => (
        <Alert key={warning} variant="warning">
          <AlertDescription>{warning}</AlertDescription>
        </Alert>
      ))}

      <p className="text-sm text-ink-soft">
        This output supports review. It does not make a final financial or routing decision.
      </p>

      <Button onClick={onReset}>Start a new classification</Button>
    </div>
  )
}
