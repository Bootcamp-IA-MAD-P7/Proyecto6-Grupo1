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

export const REVIEW_REASONS = [
  'low_confidence',
  'confidence_unavailable',
  'out_of_domain',
  'language_policy',
  'service_policy',
] as const

export type ReviewReason = (typeof REVIEW_REASONS)[number]

export interface PredictionRequest {
  narrative: string
  client_request_id?: string
}

export const MAX_NARRATIVE_CHARACTERS = 5000

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

export class PredictionContractError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'PredictionContractError'
  }
}

const UUID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i

const REQUEST_FIELDS = ['narrative', 'client_request_id'] as const
const RESPONSE_FIELDS = [
  'prediction_id',
  'predicted_class',
  'alternatives',
  'confidence',
  'review_required',
  'review_reasons',
  'model_version',
  'taxonomy_version',
  'created_at',
  'warnings',
] as const
const ALTERNATIVE_FIELDS = ['class_label', 'confidence'] as const

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === 'object' && value !== null && !Array.isArray(value)

const hasOnlyFields = (value: Record<string, unknown>, fields: readonly string[]) =>
  Object.keys(value).every((field) => fields.includes(field))

const isCanonicalClass = (value: unknown): value is CanonicalClass =>
  typeof value === 'string' && (CANONICAL_CLASSES as readonly string[]).includes(value)

const isReviewReason = (value: unknown): value is ReviewReason =>
  typeof value === 'string' && (REVIEW_REASONS as readonly string[]).includes(value)

const isNullableConfidence = (value: unknown): value is number | null =>
  value === null || (typeof value === 'number' && value >= 0 && value <= 1)

const isNonEmptyString = (value: unknown): value is string =>
  typeof value === 'string' && value.length > 0

const isPredictionAlternative = (value: unknown): value is PredictionAlternative => {
  if (!isRecord(value) || !hasOnlyFields(value, ALTERNATIVE_FIELDS)) return false

  return isCanonicalClass(value.class_label) && isNullableConfidence(value.confidence)
}

export function assertPredictionRequest(value: unknown): asserts value is PredictionRequest {
  if (!isRecord(value) || !hasOnlyFields(value, REQUEST_FIELDS)) {
    throw new PredictionContractError('Prediction request contains unsupported fields.')
  }

  if (
    typeof value.narrative !== 'string' ||
    !/\S/.test(value.narrative) ||
    value.narrative.length > MAX_NARRATIVE_CHARACTERS
  ) {
    throw new PredictionContractError('Prediction request requires a non-blank narrative.')
  }

  if (
    value.client_request_id !== undefined &&
    (typeof value.client_request_id !== 'string' || value.client_request_id.length > 100)
  ) {
    throw new PredictionContractError('Client request identifier is invalid.')
  }
}

export const parsePredictionResponse = (value: unknown): PredictionResponse => {
  if (!isRecord(value) || !hasOnlyFields(value, RESPONSE_FIELDS)) {
    throw new PredictionContractError('Prediction response contains unsupported fields.')
  }

  const isValid =
    typeof value.prediction_id === 'string' &&
    UUID_PATTERN.test(value.prediction_id) &&
    isCanonicalClass(value.predicted_class) &&
    Array.isArray(value.alternatives) &&
    value.alternatives.every(isPredictionAlternative) &&
    isNullableConfidence(value.confidence) &&
    typeof value.review_required === 'boolean' &&
    Array.isArray(value.review_reasons) &&
    value.review_reasons.every(isReviewReason) &&
    isNonEmptyString(value.model_version) &&
    isNonEmptyString(value.taxonomy_version) &&
    typeof value.created_at === 'string' &&
    value.created_at.includes('T') &&
    !Number.isNaN(Date.parse(value.created_at)) &&
    Array.isArray(value.warnings) &&
    value.warnings.every((warning) => typeof warning === 'string')

  if (!isValid) {
    throw new PredictionContractError('Prediction response does not match the API contract.')
  }

  if (value.confidence === null && value.review_required !== true) {
    throw new PredictionContractError(
      'A response without calibrated confidence requires human review.',
    )
  }

  return value as unknown as PredictionResponse
}
