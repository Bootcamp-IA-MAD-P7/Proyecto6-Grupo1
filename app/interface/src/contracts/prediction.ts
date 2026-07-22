export const CANONICAL_CLASSES = [
  'Checking or savings account',
  'Credit card',
  'Credit reporting or other personal consumer reports',
  'Debt collection',
  'Debt or credit management',
  'Money transfer, virtual currency, or money service',
  'Mortgage',
  'Payday loan, title loan, personal loan, or advance loan',
  'Prepaid card',
  'Student loan',
  'Vehicle loan or lease',
] as const

export type CanonicalClass = (typeof CANONICAL_CLASSES)[number]

export type ReviewReason =
  | 'low_confidence'
  | 'confidence_unavailable'
  | 'out_of_domain'
  | 'language_policy'
  | 'service_policy'

export interface PredictionRequest {
  narrative: string
  client_request_id?: string
}

export interface PredictionAlternative {
  class_label: CanonicalClass
  confidence: number | null
}

export interface PredictionResponse {
  prediction_id: string
  predicted_class: CanonicalClass
  alternatives: PredictionAlternative[]
  confidence: number | null
  review_required: boolean
  review_reasons: ReviewReason[]
  model_version: string
  taxonomy_version: string
  created_at: string
  warnings: string[]
}
