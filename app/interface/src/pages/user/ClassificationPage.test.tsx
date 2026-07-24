import { act, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, describe, it, expect, vi } from 'vitest'
import ClassificationPage from './ClassificationPage'
import type { PredictionResponse } from '@/contracts/prediction'
import { createMockPredictionClient } from '@/services/mock-prediction-client'
import { PredictionClientError, type PredictionClient } from '@/services/prediction-client'

const renderWithRouter = (component: React.ReactNode) => {
  return render(<MemoryRouter>{component}</MemoryRouter>)
}

const SYNTHETIC_RESPONSE: PredictionResponse = {
  prediction_id: '123e4567-e89b-42d3-a456-426614174000',
  predicted_class: 'Debt collection',
  alternatives: [{ class_label: 'Credit card', confidence: null }],
  confidence: null,
  review_required: true,
  review_reasons: ['confidence_unavailable'],
  model_version: 'mock-not-a-model',
  taxonomy_version: '1.0',
  created_at: '2026-07-24T10:00:00.000Z',
  warnings: ['Synthetic fixture. This is not a model prediction.'],
}

interface SpeechResultEvent extends Event {
  results: {
    readonly [index: number]: {
      readonly [index: number]: { transcript: string }
    }
  }
  resultIndex: number
}

interface SpeechErrorEvent extends Event {
  error: string
  message: string
}

class MockSpeechRecognition {
  static instances: MockSpeechRecognition[] = []

  lang = ''
  continuous = false
  interimResults = false
  maxAlternatives = 0
  onresult: ((event: SpeechResultEvent) => void) | null = null
  onerror: ((event: SpeechErrorEvent) => void) | null = null
  onend: (() => void) | null = null
  start = vi.fn()
  stop = vi.fn(() => this.onend?.())

  constructor() {
    MockSpeechRecognition.instances.push(this)
  }

  emitTranscript(transcript: string) {
    this.onresult?.({
      results: { 0: { 0: { transcript } } },
      resultIndex: 0,
    } as unknown as SpeechResultEvent)
  }

  emitError(error: string) {
    this.onerror?.({ error, message: 'Synthetic recognition error' } as SpeechErrorEvent)
  }
}

const setSpeechRecognition = (implementation?: typeof MockSpeechRecognition) => {
  Object.defineProperty(window, 'SpeechRecognition', {
    configurable: true,
    value: implementation,
  })
  Object.defineProperty(window, 'webkitSpeechRecognition', {
    configurable: true,
    value: undefined,
  })
}

afterEach(() => {
  MockSpeechRecognition.instances = []
  setSpeechRecognition(undefined)
})

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
    const client = createMockPredictionClient({ latencyMs: 0 })
    const createPrediction = vi.spyOn(client, 'createPrediction')

    renderWithRouter(<ClassificationPage predictionClient={client} />)

    await user.type(screen.getByLabelText('Complaint narrative'), '  Test complaint text  ')
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))

    expect(createPrediction).toHaveBeenCalledWith({
      narrative: 'Test complaint text',
    })
    expect(
      await screen.findByRole('heading', {
        name: 'Credit reporting or other personal consumer reports',
      }),
    ).toBeInTheDocument()
    expect(screen.getByText('Mock response · demo only')).toBeVisible()
    expect(screen.getByText(/Interface demonstration only/)).toBeVisible()
    expect(screen.getByText('Human review required')).toBeVisible()
    expect(screen.getByText('Calibrated confidence is not available')).toBeVisible()
    expect(screen.getByText('Not available')).toBeVisible()
    expect(screen.queryByText(/\d+%/)).not.toBeInTheDocument()
    expect(screen.queryByText('Model confidence')).not.toBeInTheDocument()
  })

  it('announces progress and prevents duplicate submissions', async () => {
    const user = userEvent.setup()
    let resolvePrediction: (response: PredictionResponse) => void = () => undefined
    const pendingPrediction = new Promise<PredictionResponse>((resolve) => {
      resolvePrediction = resolve
    })
    const client: PredictionClient = {
      createPrediction: vi.fn(() => pendingPrediction),
    }

    renderWithRouter(<ClassificationPage predictionClient={client} />)

    await user.type(screen.getByLabelText('Complaint narrative'), 'Synthetic loading case')
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))

    expect(screen.getByRole('status')).toHaveTextContent(
      'Creating a simulated result. Please wait.',
    )
    expect(screen.getByRole('button', { name: 'Creating simulated result…' })).toBeDisabled()
    expect(screen.getByLabelText('Complaint narrative')).toBeDisabled()
    expect(client.createPrediction).toHaveBeenCalledTimes(1)

    resolvePrediction(SYNTHETIC_RESPONSE)

    expect(await screen.findByRole('heading', { name: 'Debt collection' })).toBeVisible()
  })

  it('starts a new classification without retaining the previous narrative', async () => {
    const user = userEvent.setup()
    const narrative = 'Synthetic narrative that must not be returned'

    renderWithRouter(
      <ClassificationPage predictionClient={createMockPredictionClient({ latencyMs: 0 })} />,
    )

    await user.type(screen.getByLabelText('Complaint narrative'), narrative)
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))
    await screen.findByText('Mock response · demo only')

    expect(screen.queryByText(narrative)).not.toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Start a new classification' }))

    expect(screen.getByLabelText('Complaint narrative')).toHaveValue('')
    await waitFor(() => expect(screen.getByLabelText('Complaint narrative')).toHaveFocus())
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
    const errorAlert = screen
      .getByText(/The simulated prediction service is unavailable/)
      .closest('[role="alert"]')

    expect(errorAlert).not.toHaveTextContent('Test error case')
    expect(errorAlert).not.toHaveTextContent(/internal stack/i)
    expect(screen.queryByText(/internal stack/i)).not.toBeInTheDocument()
    expect(screen.getByLabelText('Complaint narrative')).toHaveValue('Test error case')
    expect(screen.getByRole('button', { name: 'Classify complaint' })).toBeEnabled()
  })

  it('presents a specific rate-limit error without leaking the narrative', async () => {
    const user = userEvent.setup()
    const limitedClient: PredictionClient = {
      createPrediction: vi
        .fn()
        .mockRejectedValue(new PredictionClientError('rate_limited', 'internal limit detail')),
    }

    renderWithRouter(<ClassificationPage predictionClient={limitedClient} />)

    await user.type(screen.getByLabelText('Complaint narrative'), 'Synthetic limited request')
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))

    expect(
      await screen.findByText('Too many requests. Wait a moment before trying again.'),
    ).toBeVisible()
    expect(screen.queryByText(/internal limit detail/i)).not.toBeInTheDocument()
  })

  it('adds a voice transcript to the editable narrative and stops explicitly', async () => {
    const user = userEvent.setup()
    setSpeechRecognition(MockSpeechRecognition)

    renderWithRouter(
      <ClassificationPage predictionClient={createMockPredictionClient({ latencyMs: 0 })} />,
    )

    await user.click(screen.getByRole('button', { name: 'Start dictation' }))

    const recognition = MockSpeechRecognition.instances[0]
    expect(recognition).toBeDefined()
    expect(recognition?.start).toHaveBeenCalledOnce()
    expect(recognition?.lang).toBe(document.documentElement.lang || navigator.language || 'en-US')
    expect(screen.getByRole('status')).toHaveTextContent('Listening…')

    act(() => recognition?.emitTranscript('  Synthetic spoken complaint  '))

    const narrative = screen.getByLabelText('Complaint narrative')
    expect(narrative).toHaveValue('Synthetic spoken complaint')

    await user.type(narrative, ' with an editable ending')
    expect(narrative).toHaveValue('Synthetic spoken complaint with an editable ending')

    await user.click(screen.getByRole('button', { name: 'Stop dictation' }))
    expect(recognition?.stop).toHaveBeenCalledOnce()
    expect(screen.getByRole('button', { name: 'Start dictation' })).toBeEnabled()
  })

  it('keeps keyboard input available when voice dictation is unsupported', () => {
    setSpeechRecognition(undefined)

    renderWithRouter(
      <ClassificationPage predictionClient={createMockPredictionClient({ latencyMs: 0 })} />,
    )

    expect(
      screen.getByText(
        'Voice dictation is not available in this browser. You can continue typing.',
      ),
    ).toBeVisible()
    expect(screen.getByLabelText('Complaint narrative')).toBeEnabled()
    expect(screen.queryByRole('button', { name: 'Start dictation' })).not.toBeInTheDocument()
  })

  it('recovers safely when microphone permission is denied', async () => {
    const user = userEvent.setup()
    setSpeechRecognition(MockSpeechRecognition)

    renderWithRouter(
      <ClassificationPage predictionClient={createMockPredictionClient({ latencyMs: 0 })} />,
    )

    await user.click(screen.getByRole('button', { name: 'Start dictation' }))
    const recognition = MockSpeechRecognition.instances[0]

    act(() => recognition?.emitError('not-allowed'))

    expect(screen.getByRole('alert')).toHaveTextContent(
      'Microphone access was not granted. Continue by typing.',
    )
    expect(screen.getByLabelText('Complaint narrative')).toBeEnabled()
    expect(screen.getByRole('button', { name: 'Start dictation' })).toBeEnabled()
  })

  it('recovers safely from a recognition error', async () => {
    const user = userEvent.setup()
    setSpeechRecognition(MockSpeechRecognition)

    renderWithRouter(
      <ClassificationPage predictionClient={createMockPredictionClient({ latencyMs: 0 })} />,
    )

    await user.click(screen.getByRole('button', { name: 'Start dictation' }))
    const recognition = MockSpeechRecognition.instances[0]

    act(() => recognition?.emitError('network'))

    expect(screen.getByRole('alert')).toHaveTextContent(
      'Voice transcription failed. Continue by typing.',
    )
    expect(screen.getByLabelText('Complaint narrative')).toBeEnabled()
    expect(screen.getByRole('button', { name: 'Start dictation' })).toBeEnabled()
  })
})
