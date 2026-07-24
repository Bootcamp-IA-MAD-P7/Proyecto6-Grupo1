import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { describe, it, expect, vi } from 'vitest'
import ClassificationPage from './ClassificationPage'
import { createMockPredictionClient } from '@/services/mock-prediction-client'
import { PredictionClientError, type PredictionClient } from '@/services/prediction-client'

const renderWithRouter = (component: React.ReactNode) => {
  return render(<MemoryRouter>{component}</MemoryRouter>)
}

describe('ClassificationPage', () => {
  it('renders the narrative form', () => {
    renderWithRouter(
      <ClassificationPage predictionClient={createMockPredictionClient({ latencyMs: 0 })} />,
    )

    expect(screen.getByRole('heading', { name: /describe what happened/i })).toBeVisible()
    expect(screen.getByLabelText('Complaint narrative')).toBeEnabled()
    expect(screen.getByRole('button', { name: 'Classify complaint' })).toBeEnabled()
  })

  it('rejects a whitespace-only narrative', async () => {
    const user = userEvent.setup()
    renderWithRouter(
      <ClassificationPage predictionClient={createMockPredictionClient({ latencyMs: 0 })} />,
    )

    await user.type(screen.getByLabelText('Complaint narrative'), '   ')
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))

    expect(screen.getByRole('alert')).toHaveTextContent(
      'Enter a complaint narrative before continuing.',
    )
  })

  it('shows a synthetic result', async () => {
    const user = userEvent.setup()
    renderWithRouter(
      <ClassificationPage predictionClient={createMockPredictionClient({ latencyMs: 0 })} />,
    )

    await user.type(screen.getByLabelText('Complaint narrative'), 'Test complaint text')
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))

    expect(
      await screen.findByRole('heading', {
        name: 'Credit reporting or other personal consumer reports',
      }),
    ).toBeInTheDocument()
    expect(screen.getByText('Simulated result')).toBeVisible()
    expect(screen.getByText('Human review required')).toBeVisible()
  })

  it('does not fabricate a result while offline', () => {
    Object.defineProperty(navigator, 'onLine', {
      configurable: true,
      value: false,
    })

    renderWithRouter(
      <ClassificationPage predictionClient={createMockPredictionClient({ latencyMs: 0 })} />,
    )

    expect(screen.getByText('You are offline.')).toBeVisible()
    expect(screen.getByRole('button', { name: 'Classify complaint' })).toBeDisabled()
  })

  it('presents a safe service error', async () => {
    const user = userEvent.setup()
    const failingClient: PredictionClient = {
      createPrediction: vi
        .fn()
        .mockRejectedValue(
          new PredictionClientError('service_unavailable', 'internal stack trace'),
        ),
    }

    renderWithRouter(<ClassificationPage predictionClient={failingClient} />)

    await user.type(screen.getByLabelText('Complaint narrative'), 'Test error case')
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))

    await waitFor(() => {
      expect(screen.getAllByRole('alert').length).toBeGreaterThanOrEqual(1)
      expect(
        screen.getByText(/The simulated prediction service is unavailable/),
      ).toBeInTheDocument()
    })
    expect(screen.queryByText(/internal stack/i)).not.toBeInTheDocument()
  })
})
