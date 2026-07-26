import { useEffect, useRef } from 'react'
import type { PredictionResponse, ReviewReason } from '@/contracts/prediction'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { AlertTriangle, CheckCircle, Info, RotateCcw } from 'lucide-react'

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
        <AlertTriangle className="h-4 w-4" />
        <AlertDescription>
          <strong>Interface demonstration only.</strong> This response is synthetic, has no
          calibrated score and cannot route a complaint.
        </AlertDescription>
      </Alert>

      <div className="flex flex-col items-start gap-2 sm:flex-row sm:justify-between sm:gap-4">
        <div>
          <p className="mb-1 text-xs font-bold uppercase tracking-widest text-gold-ink">
            Mock response
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
              No percentage is available for this mock response.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center gap-2 space-y-0">
            <AlertTriangle className="h-4 w-4 text-ink-soft" />
            <CardTitle className="text-sm">Review reason</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-1.5">
              {result.review_reasons.map((reason) => (
                <li key={reason} className="flex items-center gap-2 text-sm">
                  <CheckCircle className="h-3.5 w-3.5 shrink-0 text-ink-soft" />
                  {REVIEW_REASON_LABELS[reason]}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader className="flex flex-row items-center gap-2 space-y-0">
          <Info className="h-4 w-4 text-ink-soft" />
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

      <div className="flex flex-wrap gap-4 rounded-lg bg-sand px-4 py-3 font-mono text-xs text-ink-soft">
        <span>Mock source: {result.model_version}</span>
        <span>Taxonomy: {result.taxonomy_version}</span>
        <span>Reference: {result.prediction_id.slice(0, 8)}</span>
      </div>

      {result.warnings.map((warning) => (
        <Alert key={warning} variant="warning">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{warning}</AlertDescription>
        </Alert>
      ))}

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
