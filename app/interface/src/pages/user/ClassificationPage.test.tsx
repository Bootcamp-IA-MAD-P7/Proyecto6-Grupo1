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

const SYNTHETIC_REAL_RESPONSE: PredictionResponse = {
  ...SYNTHETIC_RESPONSE,
  confidence: 0.76,
  model_version: 'baseline-lr-C0.1-f8000',
  review_reasons: ['low_confidence'],
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

const originalCacheStorage = window.caches

afterEach(() => {
  vi.restoreAllMocks()
  MockSpeechRecognition.instances = []
  setSpeechRecognition(undefined)
  Object.defineProperty(window, 'caches', {
    configurable: true,
    value: originalCacheStorage,
  })
})

describe('ClassificationPage', () => {
  it('renders the narrative form', () => {
    renderWithRouter(
      <ClassificationPage predictionClient={createMockPredictionClient({ latencyMs: 0 })} />,
    )

    expect(screen.getByRole('heading', { level: 1, name: /describe what happened/i })).toBeVisible()
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
    expect(screen.getByLabelText('Complaint narrative')).toHaveFocus()
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
    const resultHeading = await screen.findByRole('heading', {
      level: 1,
      name: 'Credit reporting or other personal consumer reports',
    })
    expect(resultHeading).toBeInTheDocument()
    expect(resultHeading).toHaveFocus()
    expect(screen.getByText('Mock response')).toBeVisible()
    expect(screen.getByText(/Interface demonstration only/)).toBeVisible()
    expect(screen.getByText('Human review required')).toBeVisible()
    expect(screen.getByText('Calibrated confidence is not available')).toBeVisible()
    expect(screen.getByText('Not available')).toBeVisible()
    expect(screen.queryByText(/\d+%/)).not.toBeInTheDocument()
    expect(screen.queryByText('Model confidence')).not.toBeInTheDocument()
  })

  it('renders a configured service response as advisory human-review support', async () => {
    const user = userEvent.setup()
    const client: PredictionClient = {
      createPrediction: vi.fn().mockResolvedValue(SYNTHETIC_REAL_RESPONSE),
    }

    renderWithRouter(<ClassificationPage predictionClient={client} />)

    await user.type(screen.getByLabelText('Complaint narrative'), 'Synthetic real-service case')
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))

    expect(client.createPrediction).toHaveBeenCalledWith({
      narrative: 'Synthetic real-service case',
    })
    expect(await screen.findByText('Prediction response')).toBeVisible()
    expect(screen.getByText('Human review remains required.')).toBeVisible()
    expect(screen.getByText('Human review required')).toBeVisible()
    expect(screen.getByText('76%')).toBeVisible()
    expect(screen.queryByText('Interface demonstration only.')).not.toBeInTheDocument()
    expect(screen.getByText('Model: baseline-lr-C0.1-f8000')).toBeVisible()
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
    expect(screen.getByRole('button', { name: 'Classifying...' })).toBeDisabled()
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
    await screen.findByText('Mock response')

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

  it('does not fabricate a result when a real connectivity check fails', async () => {
    const client = createMockPredictionClient({ latencyMs: 0 })
    const createPrediction = vi.spyOn(client, 'createPrediction')

    renderWithRouter(
      <ClassificationPage
        predictionClient={client}
        connectivityCheck={vi.fn().mockResolvedValue(false)}
      />,
    )

    expect(await screen.findByText('You are offline.')).toBeVisible()
    expect(createPrediction).not.toHaveBeenCalled()
    expect(screen.queryByText('Mock response Â· demo only')).not.toBeInTheDocument()
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
    const storageWrite = vi.spyOn(Storage.prototype, 'setItem')
    const cacheOpen = vi.fn()
    const consoleLog = vi.spyOn(console, 'log').mockImplementation(() => undefined)
    const consoleInfo = vi.spyOn(console, 'info').mockImplementation(() => undefined)
    const consoleWarn = vi.spyOn(console, 'warn').mockImplementation(() => undefined)
    const consoleError = vi.spyOn(console, 'error').mockImplementation(() => undefined)
    const initialUrl = window.location.href

    Object.defineProperty(window, 'caches', {
      configurable: true,
      value: { open: cacheOpen },
    })
    setSpeechRecognition(MockSpeechRecognition)

    renderWithRouter(
      <ClassificationPage predictionClient={createMockPredictionClient({ latencyMs: 0 })} />,
    )

    await user.click(screen.getByRole('button', { name: 'Start dictation' }))

    const recognition = MockSpeechRecognition.instances[0]
    expect(recognition).toBeDefined()
    expect(recognition?.start).toHaveBeenCalledOnce()
    expect(recognition?.lang).toBe(document.documentElement.lang || navigator.language || 'en-US')
    expect(screen.getByRole('status')).toHaveTextContent('Listening...')
    expect(screen.getByText(/Your browser or speech provider may process the audio/)).toBeVisible()
    expect(
      screen.getByText(/This application does not store the audio or transcript/),
    ).toBeVisible()

    act(() => recognition?.emitTranscript('  Synthetic spoken complaint  '))

    const narrative = screen.getByLabelText('Complaint narrative')
    expect(narrative).toHaveValue('Synthetic spoken complaint')

    await user.type(narrative, ' with an editable ending')
    expect(narrative).toHaveValue('Synthetic spoken complaint with an editable ending')

    await user.click(screen.getByRole('button', { name: 'Stop dictation' }))
    expect(recognition?.stop).toHaveBeenCalledOnce()
    expect(screen.getByRole('button', { name: 'Start dictation' })).toBeEnabled()
    expect(storageWrite).not.toHaveBeenCalled()
    expect(cacheOpen).not.toHaveBeenCalled()
    expect(window.location.href).toBe(initialUrl)
    expect(consoleLog).not.toHaveBeenCalled()
    expect(consoleInfo).not.toHaveBeenCalled()
    expect(consoleWarn).not.toHaveBeenCalled()
    expect(consoleError).not.toHaveBeenCalled()
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
