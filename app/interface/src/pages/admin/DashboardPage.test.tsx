import { render, screen, within } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import DashboardPage from './DashboardPage'

const jsonResponse = (body: unknown, ok = true) =>
  Promise.resolve({
    json: () => Promise.resolve(body),
    ok,
  } as Response)

const configureLocalApi = () => {
  vi.stubEnv('VITE_PREDICTION_API_BASE_URL', 'http://127.0.0.1:8000')
}

describe('DashboardPage', () => {
  afterEach(() => {
    vi.unstubAllEnvs()
  })

  it('distinguishes an unconfigured local API from shared operational data', async () => {
    vi.stubEnv('VITE_PREDICTION_API_BASE_URL', '')
    render(<DashboardPage />)

    expect(await screen.findAllByText('Not configured')).toHaveLength(2)
    expect(screen.getByText('Not connected')).toBeInTheDocument()
    expect(screen.getByText('Required')).toBeInTheDocument()
    expect(fetch).not.toHaveBeenCalled()
  })

  it('shows a healthy local baseline and an empty aggregate summary', async () => {
    configureLocalApi()
    vi.mocked(fetch).mockImplementation((input) => {
      const url = String(input)
      if (url.endsWith('/health')) {
        return jsonResponse({ status: 'ok', service_version: '0.1.0' })
      }
      return jsonResponse({ items: [] })
    })

    render(<DashboardPage />)

    expect(await screen.findByText('Healthy')).toBeInTheDocument()
    expect(screen.getByText('Baseline available')).toBeInTheDocument()
    expect(await screen.findByText('No activity')).toBeInTheDocument()
    expect(screen.getByText('No local feedback activity is available.')).toBeInTheDocument()
    expect(screen.queryByRole('table')).not.toBeInTheDocument()
  })

  it('shows a degraded service without promoting model evidence', async () => {
    configureLocalApi()
    vi.mocked(fetch).mockImplementation((input) =>
      String(input).endsWith('/health')
        ? jsonResponse({ status: 'degraded', service_version: '0.1.0' })
        : jsonResponse({ items: [] }),
    )

    render(<DashboardPage />)

    expect(await screen.findAllByText('Degraded')).toHaveLength(2)
    expect(screen.queryByText('Baseline available')).not.toBeInTheDocument()
  })

  it('shows recoverable unavailable states after network errors', async () => {
    configureLocalApi()
    vi.mocked(fetch).mockRejectedValue(new Error('private transport detail'))

    render(<DashboardPage />)

    expect(await screen.findAllByText('Unavailable')).toHaveLength(2)
    expect(
      screen.getByText('The aggregate feedback summary is unavailable. Reload to try again.'),
    ).toBeInTheDocument()
    expect(screen.queryByText('private transport detail')).not.toBeInTheDocument()
  })

  it('shows only the aggregate local feedback count', async () => {
    configureLocalApi()
    vi.mocked(fetch).mockImplementation((input) => {
      const url = String(input)
      if (url.endsWith('/health')) {
        return jsonResponse({ status: 'ok', service_version: '0.1.0' })
      }
      return jsonResponse({
        items: [
          {
            model_version: 'baseline-local',
            suggested_class: 'Credit card',
            decision: 'confirmed',
            count: 2,
          },
          {
            model_version: 'baseline-local',
            suggested_class: 'Mortgage',
            decision: 'corrected',
            count: 1,
          },
        ],
      })
    })

    render(<DashboardPage />)

    expect(await screen.findByText('3 reviews')).toBeInTheDocument()
    const table = screen.getByRole('table', { name: /aggregate local feedback/i })
    const rows = within(table).getAllByRole('row')
    expect(rows).toHaveLength(3)
    expect(within(rows[1]!).getByText('baseline-local')).toBeInTheDocument()
    expect(within(rows[1]!).getByText('Credit card')).toBeInTheDocument()
    expect(within(rows[1]!).getByText('confirmed')).toBeInTheDocument()
    expect(within(rows[1]!).getByText('2')).toBeInTheDocument()
    expect(within(rows[2]!).getByText('Mortgage')).toBeInTheDocument()
    expect(within(rows[2]!).getByText('corrected')).toBeInTheDocument()
    expect(within(rows[2]!).getByText('1')).toBeInTheDocument()

    const rendered = document.body.textContent ?? ''
    expect(rendered).not.toMatch(/[0-9a-f]{8}-[0-9a-f]{4}/i)
    expect(rendered).not.toContain('narrative')
    expect(rendered).not.toContain('prediction_id')
    expect(rendered).not.toContain('purpose')
    expect(rendered).not.toContain('created_at')
    expect(rendered).not.toContain('probabilities')
    expect(rendered).not.toContain('Champion')
    expect(rendered).not.toContain('deployed')
    expect(rendered).not.toContain('accuracy')
  })
})
