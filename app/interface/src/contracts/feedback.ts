import { CANONICAL_CLASSES, type CanonicalClass } from './prediction'

export const FEEDBACK_DECISIONS = ['confirmed', 'corrected', 'not_actionable'] as const
export const FEEDBACK_PURPOSES = [
  'human_review_quality_assurance',
  'future_retraining_candidate',
] as const

export type FeedbackDecision = (typeof FEEDBACK_DECISIONS)[number]
export type FeedbackPurpose = (typeof FEEDBACK_PURPOSES)[number]

export interface FeedbackCreateRequest {
  prediction_id: string
  model_version: string
  taxonomy_version: string
  suggested_class: CanonicalClass
  reviewed_class?: CanonicalClass
  decision: FeedbackDecision
  purpose: FeedbackPurpose
}

export interface FeedbackAcceptedResponse {
  status: 'recorded'
}

export interface FeedbackSummaryItem {
  model_version: string
  suggested_class: CanonicalClass
  decision: FeedbackDecision
  count: number
}

export interface FeedbackSummaryResponse {
  items: FeedbackSummaryItem[]
}

export class FeedbackContractError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'FeedbackContractError'
  }
}

const UUID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i
const REQUEST_FIELDS = [
  'prediction_id',
  'model_version',
  'taxonomy_version',
  'suggested_class',
  'reviewed_class',
  'decision',
  'purpose',
] as const

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === 'object' && value !== null && !Array.isArray(value)

const hasOnlyFields = (value: Record<string, unknown>, fields: readonly string[]) =>
  Object.keys(value).every((field) => fields.includes(field))

const isCanonicalClass = (value: unknown): value is CanonicalClass =>
  typeof value === 'string' && (CANONICAL_CLASSES as readonly string[]).includes(value)

export function assertFeedbackCreateRequest(
  value: unknown,
): asserts value is FeedbackCreateRequest {
  if (!isRecord(value) || !hasOnlyFields(value, REQUEST_FIELDS)) {
    throw new FeedbackContractError('Feedback request contains unsupported fields.')
  }

  const isValid =
    typeof value.prediction_id === 'string' &&
    UUID_PATTERN.test(value.prediction_id) &&
    typeof value.model_version === 'string' &&
    value.model_version.trim().length > 0 &&
    typeof value.taxonomy_version === 'string' &&
    value.taxonomy_version.trim().length > 0 &&
    isCanonicalClass(value.suggested_class) &&
    (value.reviewed_class === undefined || isCanonicalClass(value.reviewed_class)) &&
    typeof value.decision === 'string' &&
    (FEEDBACK_DECISIONS as readonly string[]).includes(value.decision) &&
    typeof value.purpose === 'string' &&
    (FEEDBACK_PURPOSES as readonly string[]).includes(value.purpose)

  if (!isValid) {
    throw new FeedbackContractError('Feedback request does not match the local contract.')
  }

  if (value.decision === 'corrected' && value.reviewed_class === undefined) {
    throw new FeedbackContractError('Corrected feedback requires a reviewed class.')
  }
  if (value.decision !== 'corrected' && value.reviewed_class !== undefined) {
    throw new FeedbackContractError('Only corrected feedback may include a reviewed class.')
  }
}

export const parseFeedbackAcceptedResponse = (value: unknown): FeedbackAcceptedResponse => {
  if (!isRecord(value) || Object.keys(value).length !== 1 || value.status !== 'recorded') {
    throw new FeedbackContractError('Feedback response does not match the local contract.')
  }
  return { status: 'recorded' }
}

export const parseFeedbackSummaryResponse = (value: unknown): FeedbackSummaryResponse => {
  if (!isRecord(value) || Object.keys(value).length !== 1 || !Array.isArray(value.items)) {
    throw new FeedbackContractError('Feedback summary does not match the local contract.')
  }

  const items = value.items.map((item) => {
    if (
      !isRecord(item) ||
      !hasOnlyFields(item, ['model_version', 'suggested_class', 'decision', 'count']) ||
      Object.keys(item).length !== 4 ||
      typeof item.model_version !== 'string' ||
      item.model_version.trim().length === 0 ||
      !isCanonicalClass(item.suggested_class) ||
      typeof item.decision !== 'string' ||
      !(FEEDBACK_DECISIONS as readonly string[]).includes(item.decision) ||
      typeof item.count !== 'number' ||
      !Number.isInteger(item.count) ||
      item.count < 0
    ) {
      throw new FeedbackContractError('Feedback summary does not match the local contract.')
    }

    return {
      model_version: item.model_version,
      suggested_class: item.suggested_class,
      decision: item.decision as FeedbackDecision,
      count: item.count,
    }
  })

  return { items }
}
