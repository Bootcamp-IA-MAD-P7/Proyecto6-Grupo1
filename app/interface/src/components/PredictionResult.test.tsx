import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import type { PredictionResponse } from '@/contracts/prediction'
import { PredictionResult } from './PredictionResult'

const feedbackClientMocks = vi.hoisted(() => ({
  recordFeedback: vi.fn(),
  createConfiguredFeedbackClient: vi.fn(),
}))

vi.mock('@/services/configured-feedback-client', () => ({
  createConfiguredFeedbackClient: feedbackClientMocks.createConfiguredFeedbackClient,
}))

const LOCAL_RESPONSE: PredictionResponse = {
  prediction_id: '00000000-0000-4000-8000-000000000001',
  predicted_class: 'Credit card',
  alternatives: [],
  confidence: 0.78,
  review_required: true,
  review_reasons: [],
  model_version: 'synthetic-baseline-1',
  taxonomy_version: '1.0',
  created_at: '2026-07-29T10:00:00.000Z',
  warnings: [],
}

afterEach(() => {
  vi.clearAllMocks()
})

describe('PredictionResult feedback flow', () => {
  it('records only approved metadata after a local prediction', async () => {
    const user = userEvent.setup()
    feedbackClientMocks.recordFeedback.mockResolvedValue({ status: 'recorded' })
    feedbackClientMocks.createConfiguredFeedbackClient.mockReturnValue({
      mode: 'local_api',
      client: { recordFeedback: feedbackClientMocks.recordFeedback },
    })

    render(<PredictionResult result={LOCAL_RESPONSE} clientMode="local_api" onReset={vi.fn()} />)

    await user.click(screen.getByRole('button', { name: 'Record review' }))

    expect(feedbackClientMocks.recordFeedback).toHaveBeenCalledWith({
      prediction_id: LOCAL_RESPONSE.prediction_id,
      model_version: LOCAL_RESPONSE.model_version,
      taxonomy_version: LOCAL_RESPONSE.taxonomy_version,
      suggested_class: LOCAL_RESPONSE.predicted_class,
      decision: 'confirmed',
      purpose: 'human_review_quality_assurance',
    })
    expect(await screen.findByText(/Feedback was recorded locally/)).toBeVisible()
    expect(screen.getByRole('heading', { name: 'Credit card' })).toBeVisible()
  })

  it('communicates unavailable local feedback without fabricating persistence', () => {
    feedbackClientMocks.createConfiguredFeedbackClient.mockReturnValue({ mode: 'unavailable' })

    render(<PredictionResult result={LOCAL_RESPONSE} clientMode="local_api" onReset={vi.fn()} />)

    expect(screen.getByText(/Local feedback is unavailable/)).toBeVisible()
    expect(screen.queryByRole('button', { name: 'Record review' })).not.toBeInTheDocument()
  })
})
