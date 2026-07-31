import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import type { FeedbackSummaryItem } from '@/contracts/feedback'
import { createConfiguredFeedbackSummaryClient } from '@/services/configured-feedback-client'
import { getPredictionApiBaseUrl } from '@/services/prediction-api-config'
import { Activity, Database, MessageSquareText, Server, Users } from 'lucide-react'
import { useEffect, useState } from 'react'

type HealthState = 'loading' | 'healthy' | 'degraded' | 'unavailable' | 'not_configured'
type FeedbackState = 'loading' | 'available' | 'unavailable' | 'not_configured'
type DatabaseState = 'loading' | 'connected' | 'not_connected' | 'not_configured'

interface DashboardState {
  feedbackCount: number
  feedbackItems: FeedbackSummaryItem[]
  feedbackState: FeedbackState
  healthState: HealthState
  databaseState: DatabaseState
}

const initialState: DashboardState = {
  feedbackCount: 0,
  feedbackItems: [],
  feedbackState: 'loading',
  healthState: 'loading',
  databaseState: 'loading',
}

const staticStats = [
  {
    title: 'Human review',
    value: 'Required',
    description: 'Classification requires human review.',
    icon: Users,
    color: 'text-rust',
  },
]

const databasePresentation = {
  loading: { value: 'Checking...', description: 'Checking database connection.' },
  connected: { value: 'Connected', description: 'PostgreSQL operational database is connected.' },
  not_connected: { value: 'Not connected', description: 'No operational database is connected.' },
  not_configured: { value: 'Not configured', description: 'No local API URL is configured.' },
} satisfies Record<DatabaseState, { value: string; description: string }>

const healthPresentation = {
  loading: {
    serviceValue: 'Checking...',
    serviceDescription: 'Checking the configured local service.',
    modelValue: 'Checking...',
    modelDescription: 'Checking local baseline availability.',
  },
  healthy: {
    serviceValue: 'Healthy',
    serviceDescription: 'The configured local service reports a healthy predictor.',
    modelValue: 'Baseline available',
    modelDescription: 'A local baseline is available; no connected evaluation or promotion exists.',
  },
  degraded: {
    serviceValue: 'Degraded',
    serviceDescription: 'The local service is running without an available baseline predictor.',
    modelValue: 'Degraded',
    modelDescription: 'The local baseline is unavailable; no model evidence is promoted.',
  },
  unavailable: {
    serviceValue: 'Unavailable',
    serviceDescription: 'The local service could not be reached. You can retry by reloading.',
    modelValue: 'Not available',
    modelDescription: 'Baseline availability cannot be confirmed.',
  },
  not_configured: {
    serviceValue: 'Not configured',
    serviceDescription: 'No local API URL is configured.',
    modelValue: 'Not available',
    modelDescription: 'Configure the local API to check baseline availability.',
  },
} satisfies Record<
  HealthState,
  {
    serviceValue: string
    serviceDescription: string
    modelValue: string
    modelDescription: string
  }
>

const feedbackPresentation = (state: FeedbackState, count: number) => {
  if (state === 'loading') {
    return { value: 'Checking...', description: 'Loading aggregate-only local feedback.' }
  }
  if (state === 'not_configured') {
    return { value: 'Not configured', description: 'No local API URL is configured.' }
  }
  if (state === 'unavailable') {
    return {
      value: 'Unavailable',
      description: 'The aggregate summary could not be loaded. You can retry by reloading.',
    }
  }
  if (count === 0) {
    return { value: 'No activity', description: 'No local feedback has been recorded.' }
  }
  return {
    value: `${count} ${count === 1 ? 'review' : 'reviews'}`,
    description: 'Aggregate local feedback counts only.',
  }
}

export default function DashboardPage() {
  const [state, setState] = useState<DashboardState>(initialState)

  useEffect(() => {
    let active = true
    let baseUrl: string | undefined

    try {
      baseUrl = getPredictionApiBaseUrl()
    } catch {
      baseUrl = undefined
    }

    if (!baseUrl) {
      setState({
        feedbackCount: 0,
        feedbackItems: [],
        feedbackState: 'not_configured',
        healthState: 'not_configured',
        databaseState: 'not_configured',
      })
      return () => {
        active = false
      }
    }

    const loadHealth = async () => {
      try {
        const response = await fetch(`${baseUrl}/api/v1/health`)
        if (!response.ok) {
          throw new Error('Health request failed.')
        }
        const body = (await response.json()) as { status?: unknown }
        if (body.status !== 'ok' && body.status !== 'degraded') {
          throw new Error('Health response is invalid.')
        }
        if (active) {
          setState((current) => ({
            ...current,
            healthState: body.status === 'ok' ? 'healthy' : 'degraded',
          }))
        }
      } catch {
        if (active) {
          setState((current) => ({ ...current, healthState: 'unavailable' }))
        }
      }
    }

    const loadDatabase = async () => {
      try {
        const response = await fetch(`${baseUrl}/api/v1/status`)
        if (!response.ok) {
          throw new Error('Status request failed.')
        }
        const body = (await response.json()) as { database_connected?: boolean }
        if (active) {
          setState((current) => ({
            ...current,
            databaseState: body.database_connected ? 'connected' : 'not_connected',
          }))
        }
      } catch {
        if (active) {
          setState((current) => ({ ...current, databaseState: 'not_connected' }))
        }
      }
    }

    const loadFeedback = async () => {
      const configuredClient = createConfiguredFeedbackSummaryClient(baseUrl)
      try {
        const summary = await configuredClient.client?.getSummary()
        if (!summary) {
          throw new Error('Feedback summary client is unavailable.')
        }
        const feedbackCount = summary.items.reduce((total, item) => total + item.count, 0)
        if (active) {
          setState((current) => ({
            ...current,
            feedbackCount,
            feedbackItems: summary.items,
            feedbackState: 'available',
          }))
        }
      } catch {
        if (active) {
          setState((current) => ({ ...current, feedbackState: 'unavailable' }))
        }
      }
    }

    void Promise.all([loadHealth(), loadFeedback(), loadDatabase()])

    return () => {
      active = false
    }
  }, [])

  const health = healthPresentation[state.healthState]
  const feedback = feedbackPresentation(state.feedbackState, state.feedbackCount)
  const database = databasePresentation[state.databaseState]
  const stats = [
    {
      title: 'Operational data',
      value: database.value,
      description: database.description,
      icon: Database,
      color: state.databaseState === 'connected' ? 'text-forest-light' : 'text-ink',
    },
    {
      title: 'Local feedback',
      value: feedback.value,
      description: feedback.description,
      icon: MessageSquareText,
      color: 'text-forest-light',
    },
    {
      title: 'Model evidence',
      value: health.modelValue,
      description: health.modelDescription,
      icon: Activity,
      color: 'text-forest-light',
    },
    {
      title: 'Service health',
      value: health.serviceValue,
      description: health.serviceDescription,
      icon: Server,
      color: 'text-gold-ink',
    },
    staticStats[0]!,
  ]

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-ink sm:text-4xl">Dashboard</h1>
        <p className="mt-2 text-ink-soft">Overview of the operational status.</p>
      </div>

      <div
        className="grid gap-6 min-w-0 sm:grid-cols-2"
        aria-live="polite"
        aria-busy={state.healthState === 'loading' || state.feedbackState === 'loading'}
      >
        {stats.map((stat) => (
          <Card
            key={stat.title}
            className="group hover:shadow-md transition-shadow duration-200 min-w-0"
          >
            <CardHeader className="flex flex-col items-center gap-3 space-y-0 pb-2 text-center min-w-0">
              <stat.icon className={`h-8 w-8 shrink-0 ${stat.color}`} />
              <CardTitle className="text-sm break-words">{stat.title}</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p className={`text-2xl font-bold break-words ${stat.color}`}>{stat.value}</p>
              <p className="mt-1 text-sm text-ink-soft break-words">{stat.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card aria-labelledby="feedback-summary-title">
        <CardHeader>
          <CardTitle id="feedback-summary-title">Local feedback summary</CardTitle>
          <p className="text-sm text-ink-soft">
            Aggregate counts from the configured local service. No individual records are shown.
          </p>
        </CardHeader>
        <CardContent>
          {state.feedbackState === 'loading' && (
            <p role="status" className="text-sm text-ink-soft">
              Loading aggregate feedback...
            </p>
          )}
          {state.feedbackState === 'not_configured' && (
            <p role="status" className="text-sm text-ink-soft">
              Configure the local API to load aggregate feedback.
            </p>
          )}
          {state.feedbackState === 'unavailable' && (
            <p role="alert" className="text-sm text-rust">
              The aggregate feedback summary is unavailable. Reload to try again.
            </p>
          )}
          {state.feedbackState === 'available' && state.feedbackItems.length === 0 && (
            <p role="status" className="text-sm text-ink-soft">
              No local feedback activity is available.
            </p>
          )}
          {state.feedbackState === 'available' && state.feedbackItems.length > 0 && (
            <div className="overflow-x-auto">
              <table className="w-full border-collapse text-left text-sm">
                <caption className="sr-only">
                  Aggregate local feedback by model version, suggested class, and decision
                </caption>
                <thead>
                  <tr className="border-b border-border text-ink-soft">
                    <th scope="col" className="px-3 py-2 font-medium">
                      Model version
                    </th>
                    <th scope="col" className="px-3 py-2 font-medium">
                      Suggested class
                    </th>
                    <th scope="col" className="px-3 py-2 font-medium">
                      Decision
                    </th>
                    <th scope="col" className="px-3 py-2 text-right font-medium">
                      Count
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {state.feedbackItems.map((item, index) => (
                    <tr
                      key={`${item.model_version}-${item.suggested_class}-${item.decision}-${index}`}
                      className="border-b border-border last:border-0"
                    >
                      <td className="px-3 py-3 font-mono text-xs text-ink">{item.model_version}</td>
                      <td className="px-3 py-3 text-ink">{item.suggested_class}</td>
                      <td className="px-3 py-3 text-ink">{item.decision}</td>
                      <td className="px-3 py-3 text-right font-semibold text-ink">{item.count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
