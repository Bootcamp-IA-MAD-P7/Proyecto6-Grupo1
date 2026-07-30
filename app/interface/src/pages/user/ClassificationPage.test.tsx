import { act, render, screen, waitFor, within } from '@testing-library/react'
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

const SYNTHETIC_REAL_RESPONSE_WITH_ALTERNATIVES: PredictionResponse = {
  ...SYNTHETIC_REAL_RESPONSE,
  alternatives: [
    { class_label: 'Credit card', confidence: 0.1 },
    { class_label: 'Debt collection', confidence: 0.08 },
    { class_label: 'Mortgage', confidence: 0.06 },
    { class_label: 'Student loan', confidence: 0.04 },
  ],
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

const goToStep2 = async (user: ReturnType<typeof userEvent.setup>, text = 'Test complaint') => {
  await user.type(screen.getByLabelText('Complaint narrative'), text)
  await user.click(screen.getByRole('button', { name: 'Review text' }))
}

const goToStep3 = async (user: ReturnType<typeof userEvent.setup>, text = 'Test complaint') => {
  await goToStep2(user, text)
  await user.click(screen.getByRole('button', { name: 'Classify complaint' }))
}

describe('ClassificationPage', () => {
  it('renders the narrative form in step 1', () => {
    renderWithRouter(
      <ClassificationPage predictionClient={createMockPredictionClient({ latencyMs: 0 })} />,
    )

    expect(screen.getByRole('heading', { level: 1, name: /describe what happened/i })).toBeVisible()
    expect(screen.getByLabelText('Complaint narrative')).toBeEnabled()
    expect(screen.getByRole('button', { name: 'Review text' })).toBeEnabled()
    expect(screen.getByText('Describe')).toBeVisible()
  })

  it('rejects a whitespace-only narrative', async () => {
    const user = userEvent.setup()
    renderWithRouter(
      <ClassificationPage predictionClient={createMockPredictionClient({ latencyMs: 0 })} />,
    )

    await user.type(screen.getByLabelText('Complaint narrative'), '   ')
    await user.click(screen.getByRole('button', { name: 'Review text' }))

    expect(screen.getByRole('alert')).toHaveTextContent(
      'Enter a complaint narrative before continuing.',
    )
    expect(screen.getByLabelText('Complaint narrative')).toHaveFocus()
  })

  it('communicates the local narrative size limit before sending content', async () => {
    const user = userEvent.setup()
    const client: PredictionClient = { createPrediction: vi.fn() }
    renderWithRouter(<ClassificationPage predictionClient={client} />)

    const narrative = screen.getByLabelText('Complaint narrative')
    expect(narrative).toHaveAttribute('maxlength', '5000')
    await user.type(narrative, 'Synthetic text')

    expect(screen.getByText('14 / 5,000 characters')).toBeVisible()
  })

  it('does not fabricate a result when only the mock client is available', async () => {
    const user = userEvent.setup()
    const client = createMockPredictionClient({ latencyMs: 0 })
    const createPrediction = vi.spyOn(client, 'createPrediction')

    renderWithRouter(<ClassificationPage predictionClient={client} predictionClientMode="mock" />)

    await goToStep2(user, '  Test complaint text  ')
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))

    expect(createPrediction).not.toHaveBeenCalled()
    expect(await screen.findByText(/The prediction service is unavailable/)).toBeVisible()
    expect(
      screen.queryByRole('heading', {
        level: 1,
        name: 'Credit reporting or other personal consumer reports',
      }),
    ).not.toBeInTheDocument()
    expect(screen.getByText('Test complaint text')).toBeVisible()
  })

  it('does not present a degraded backend mock as a local prediction', async () => {
    const user = userEvent.setup()
    const client: PredictionClient = {
      createPrediction: vi.fn().mockResolvedValue({
        ...SYNTHETIC_REAL_RESPONSE,
        model_version: 'mock-v0',
        confidence: null,
        alternatives: [],
      }),
    }

    renderWithRouter(
      <ClassificationPage predictionClient={client} predictionClientMode="local_api" />,
    )

    await goToStep2(user, 'Synthetic degraded-service case')
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))

    expect(client.createPrediction).toHaveBeenCalled()
    expect(await screen.findByText(/The prediction service is unavailable/)).toBeVisible()
    expect(screen.queryByText('Local prediction')).not.toBeInTheDocument()
    expect(screen.getByText('Synthetic degraded-service case')).toBeVisible()
  })

  it('renders a configured service response as advisory human-review support', async () => {
    const user = userEvent.setup()
    const client: PredictionClient = {
      createPrediction: vi.fn().mockResolvedValue(SYNTHETIC_REAL_RESPONSE),
    }

    renderWithRouter(<ClassificationPage predictionClient={client} />)

    await goToStep3(user, 'Synthetic real-service case')

    expect(client.createPrediction).toHaveBeenCalledWith({
      narrative: 'Synthetic real-service case',
    })
    expect(await screen.findByText('Local prediction')).toBeVisible()
    expect(screen.getByText('Human review remains required.')).toBeVisible()
    expect(screen.getAllByText('Human review required').length).toBeGreaterThanOrEqual(1)
    expect(screen.getByText('76%')).toBeVisible()
    expect(screen.queryByText('Interface demonstration only.')).not.toBeInTheDocument()
    expect(screen.getByText('Source: Local API')).toBeVisible()
    expect(screen.getByText('Model version: baseline-lr-C0.1-f8000')).toBeVisible()
  })

  it('limits alternatives and supplies a safe review message when none is provided', async () => {
    const user = userEvent.setup()
    const client: PredictionClient = {
      createPrediction: vi.fn().mockResolvedValue({
        ...SYNTHETIC_REAL_RESPONSE_WITH_ALTERNATIVES,
        review_reasons: [],
      }),
    }

    renderWithRouter(
      <ClassificationPage predictionClient={client} predictionClientMode="local_api" />,
    )

    await goToStep3(user, 'Synthetic UX review case')

    expect(
      await screen.findByText('Human review is required before any routing or final decision.'),
    ).toBeVisible()
    const alternatives = within(screen.getByRole('list'))
    expect(alternatives.getByText('Credit card')).toBeVisible()
    expect(alternatives.getByText('Debt collection')).toBeVisible()
    expect(alternatives.getByText('Mortgage')).toBeVisible()
    expect(alternatives.queryByText('Student loan')).not.toBeInTheDocument()
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

    await goToStep2(user, 'Synthetic loading case')

    expect(screen.getByRole('button', { name: 'Classify complaint' })).toBeVisible()
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))

    expect(screen.getByRole('status')).toHaveTextContent('Creating a recommendation. Please wait.')
    expect(screen.getByRole('button', { name: 'Classifying...' })).toBeDisabled()
    expect(client.createPrediction).toHaveBeenCalledTimes(1)

    resolvePrediction(SYNTHETIC_REAL_RESPONSE)

    expect(await screen.findByRole('heading', { name: 'Debt collection' })).toBeVisible()
  })

  it('starts a new classification without retaining the previous narrative', async () => {
    const user = userEvent.setup()
    const narrative = 'Synthetic narrative that must not be returned'

    const client: PredictionClient = {
      createPrediction: vi.fn().mockResolvedValue(SYNTHETIC_REAL_RESPONSE),
    }
    renderWithRouter(
      <ClassificationPage predictionClient={client} predictionClientMode="local_api" />,
    )

    await goToStep3(user, narrative)
    await screen.findByText('Local prediction')

    await user.click(screen.getByRole('button', { name: 'Continue' }))

    expect(screen.getByRole('heading', { name: /what would you like to do next/i })).toBeVisible()

    await user.click(screen.getByRole('button', { name: 'New classification' }))

    expect(screen.getByLabelText('Complaint narrative')).toHaveValue('')
    await waitFor(() => expect(screen.getByLabelText('Complaint narrative')).toHaveFocus())
  })

  it('shows step 2 with review when text is valid', async () => {
    const user = userEvent.setup()
    renderWithRouter(
      <ClassificationPage predictionClient={createMockPredictionClient({ latencyMs: 0 })} />,
    )

    await goToStep2(user, 'Review this complaint')

    expect(screen.getByRole('heading', { name: /review your narrative/i })).toBeVisible()
    expect(screen.getByText('Review this complaint')).toBeVisible()
    expect(screen.getByRole('button', { name: 'Classify complaint' })).toBeEnabled()
    expect(screen.getByRole('button', { name: 'Back' })).toBeEnabled()
  })

  it('goes back to describe step from review', async () => {
    const user = userEvent.setup()
    renderWithRouter(
      <ClassificationPage predictionClient={createMockPredictionClient({ latencyMs: 0 })} />,
    )

    await goToStep2(user, 'Go back to edit')
    await user.click(screen.getByRole('button', { name: 'Back' }))

    expect(screen.getByRole('heading', { level: 1, name: /describe what happened/i })).toBeVisible()
    expect(screen.getByLabelText('Complaint narrative')).toHaveValue('Go back to edit')
  })

  it('does not fabricate a result while offline', async () => {
    Object.defineProperty(navigator, 'onLine', {
      configurable: true,
      value: false,
    })

    const user = userEvent.setup()
    renderWithRouter(
      <ClassificationPage predictionClient={createMockPredictionClient({ latencyMs: 0 })} />,
    )

    await goToStep2(user)

    expect(screen.getByText('You are offline.')).toBeVisible()
    expect(screen.getByRole('button', { name: 'Classify complaint' })).toBeDisabled()
  })

  it('does not fabricate a result when a real connectivity check fails', async () => {
    const client = createMockPredictionClient({ latencyMs: 0 })
    const createPrediction = vi.spyOn(client, 'createPrediction')

    const user = userEvent.setup()
    renderWithRouter(
      <ClassificationPage
        predictionClient={client}
        connectivityCheck={vi.fn().mockResolvedValue(false)}
      />,
    )

    await goToStep2(user)

    expect(screen.getByText('You are offline.')).toBeVisible()
    expect(createPrediction).not.toHaveBeenCalled()
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

    await goToStep2(user, 'Test error case')
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))

    await waitFor(() => {
      expect(screen.getAllByRole('alert').length).toBeGreaterThanOrEqual(1)
      expect(screen.getByText(/The prediction service is unavailable/)).toBeInTheDocument()
    })
    const errorAlert = screen
      .getByText(/The prediction service is unavailable/)
      .closest('[tabindex="-1"]')

    expect(errorAlert).not.toHaveTextContent('Test error case')
    expect(errorAlert).not.toHaveTextContent(/internal stack/i)
    expect(screen.queryByText(/internal stack/i)).not.toBeInTheDocument()
    expect(screen.getByText('Test error case')).toBeVisible()
    expect(screen.getByRole('button', { name: 'Classify complaint' })).toBeEnabled()
    expect(errorAlert).toHaveFocus()
  })

  it('presents a specific rate-limit error without leaking the narrative', async () => {
    const user = userEvent.setup()
    const limitedClient: PredictionClient = {
      createPrediction: vi
        .fn()
        .mockRejectedValue(new PredictionClientError('rate_limited', 'internal limit detail')),
    }

    renderWithRouter(<ClassificationPage predictionClient={limitedClient} />)

    await goToStep2(user, 'Synthetic limited request')
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))

    expect(
      await screen.findByText('Too many requests. Wait a moment before trying again.'),
    ).toBeVisible()
    expect(screen.queryByText(/internal limit detail/i)).not.toBeInTheDocument()
  })

  it('presents an incompatible service response safely and restores focus to the alert', async () => {
    const user = userEvent.setup()
    const invalidClient: PredictionClient = {
      createPrediction: vi
        .fn()
        .mockRejectedValue(new PredictionClientError('invalid_response', 'internal response body')),
    }

    renderWithRouter(<ClassificationPage predictionClient={invalidClient} />)

    await goToStep2(user, 'Synthetic invalid response case')
    await user.click(screen.getByRole('button', { name: 'Classify complaint' }))

    const error = await screen.findByText(
      'The prediction response could not be safely validated. No recommendation was shown.',
    )
    const errorAlert = error.closest('[tabindex="-1"]')

    expect(errorAlert).toHaveFocus()
    expect(errorAlert).not.toHaveTextContent('internal response body')
    expect(errorAlert).not.toHaveTextContent('Synthetic invalid response case')
    expect(screen.queryByText('Service unavailable')).not.toBeInTheDocument()
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
