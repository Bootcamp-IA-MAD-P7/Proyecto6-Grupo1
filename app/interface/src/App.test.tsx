import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import { createMockPredictionClient } from './services/mock-prediction-client'
import {
  PredictionClientError,
  type PredictionClient,
} from './services/prediction-client'

describe('Complaint Routing prototype', () => {
  beforeEach(() => {
    Object.defineProperty(navigator, 'onLine', {
      configurable: true,
      value: true,
    })
  })

  it('identifies the mock and exposes an accessible narrative form', () => {
    render(<App predictionClient={createMockPredictionClient({ latencyMs: 0 })} />)

    expect(screen.getByRole('heading', { name: /find the most relevant/i })).toBeVisible()
    expect(screen.getByText('Mock responses')).toBeVisible()
    expect(screen.getByLabelText('Complaint narrative')).toBeEnabled()
    expect(screen.getByRole('button', { name: 'Classify complaint' })).toBeEnabled()
  })

  it('rejects a whitespace-only narrative and returns focus to the field', async () => {
    const user = userEvent.setup()
    render(<App predictionClient={createMockPredictionClient({ latencyMs: 0 })} />)

    const narrative = screen.getByLabelText('Complaint narrative')
    await user.type(narrative, '   ')
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))

    expect(screen.getByRole('alert')).toHaveTextContent(
      'Enter a complaint narrative before continuing.',
    )
    expect(narrative).toHaveFocus()
  })

  it('shows a synthetic result without fabricated confidence or narrative echo', async () => {
    const user = userEvent.setup()
    const inputText = 'Synthetic complaint text that must not be echoed in the result.'
    render(<App predictionClient={createMockPredictionClient({ latencyMs: 0 })} />)

    await user.type(screen.getByLabelText('Complaint narrative'), inputText)
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))

    expect(
      await screen.findByRole('heading', {
        name: 'Credit reporting or other personal consumer reports',
      }),
    ).toHaveFocus()
    expect(screen.getByText('Simulated result')).toBeVisible()
    expect(screen.getByText('Human review required')).toBeVisible()
    expect(screen.getByText('Not available')).toBeVisible()
    expect(screen.queryByText(inputText)).not.toBeInTheDocument()
    expect(screen.getByText(/not a model prediction/i)).toBeVisible()
  })

  it('does not fabricate a result while offline', () => {
    Object.defineProperty(navigator, 'onLine', {
      configurable: true,
      value: false,
    })

    render(<App predictionClient={createMockPredictionClient({ latencyMs: 0 })} />)

    expect(screen.getByText('You are offline.')).toBeVisible()
    expect(screen.getByRole('button', { name: 'Classify complaint' })).toBeDisabled()
    expect(screen.queryByText('Simulated result')).not.toBeInTheDocument()
  })

  it('presents a safe service error without internal details', async () => {
    const user = userEvent.setup()
    const failingClient: PredictionClient = {
      createPrediction: vi.fn().mockRejectedValue(
        new PredictionClientError('service_unavailable', 'internal stack and request body'),
      ),
    }
    render(<App predictionClient={failingClient} />)

    await user.type(screen.getByLabelText('Complaint narrative'), 'Synthetic service error case')
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(
        'The simulated prediction service is unavailable. Your narrative was not stored.',
      )
    })
    expect(screen.queryByText(/internal stack/i)).not.toBeInTheDocument()
  })
})
