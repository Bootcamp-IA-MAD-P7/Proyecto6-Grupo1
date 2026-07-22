import { useEffect, useRef } from 'react'
import type { PredictionResponse, ReviewReason } from '../contracts/prediction'

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
    <section className="result-card" aria-labelledby="result-title">
      <div className="result-card__header">
        <div>
          <p className="eyebrow">Simulated result</p>
          <h2 id="result-title" ref={titleRef} tabIndex={-1}>
            {result.predicted_class}
          </h2>
        </div>
        <span className="mode-pill mode-pill--review">Human review required</span>
      </div>

      <div className="result-grid">
        <div>
          <p className="result-label">Model confidence</p>
          <p className="result-value">
            {result.confidence === null
              ? 'Not available'
              : `${Math.round(result.confidence * 100)}%`}
          </p>
          <p className="supporting-copy">
            No percentage is shown unless the model provides calibrated confidence.
          </p>
        </div>
        <div>
          <p className="result-label">Review reason</p>
          <ul className="compact-list">
            {result.review_reasons.map((reason) => (
              <li key={reason}>{REVIEW_REASON_LABELS[reason]}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="alternatives">
        <h3>Other classes to consider</h3>
        <ol>
          {result.alternatives.map((alternative) => (
            <li key={alternative.class_label}>{alternative.class_label}</li>
          ))}
        </ol>
      </div>

      <div className="traceability" aria-label="Prediction traceability">
        <span>Model: {result.model_version}</span>
        <span>Taxonomy: {result.taxonomy_version}</span>
        <span>Reference: {result.prediction_id.slice(0, 8)}</span>
      </div>

      {result.warnings.map((warning) => (
        <p className="notice notice--warning" key={warning} role="status">
          {warning}
        </p>
      ))}

      <p className="decision-note">
        This output supports review. It does not make a final financial or routing decision.
      </p>

      <button className="button button--primary" type="button" onClick={onReset}>
        Start a new classification
      </button>
    </section>
  )
}
