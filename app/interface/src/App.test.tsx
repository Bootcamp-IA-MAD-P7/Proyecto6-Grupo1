import { render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it } from 'vitest'
import { ThemeProvider } from '@/providers/ThemeProvider'
import AppRouter from './App'

const renderRoute = (path: string) => {
  window.history.pushState({}, '', path)
  return render(
    <ThemeProvider>
      <AppRouter />
    </ThemeProvider>,
  )
}

const storeMockAdmin = () => {
  localStorage.setItem(
    'claimvox-auth',
    JSON.stringify({
      id: 'synthetic-admin',
      name: 'Synthetic reviewer',
      email: 'reviewer@example.com',
      role: 'admin',
    }),
  )
}

afterEach(() => {
  localStorage.clear()
  window.history.pushState({}, '', '/')
})

describe('application routes', () => {
  it('opens the classification flow without a mock login or stored identity', async () => {
    localStorage.clear()

    renderRoute('/classify')

    expect(
      await screen.findByRole('heading', { level: 1, name: 'Describe what happened' }),
    ).toBeVisible()
    expect(screen.queryByRole('heading', { name: 'ClaimVox' })).not.toBeInTheDocument()
    expect(screen.getAllByText('Public prototype').length).toBeGreaterThanOrEqual(1)
    expect(localStorage.getItem('claimvox-auth')).toBeNull()
  })

  it('keeps the login as an explicitly non-secure proposal', () => {
    renderRoute('/login')

    expect(screen.getByText('Mock authentication proposal only.')).toBeVisible()
    expect(screen.getByText(/provides no real identity, security/i)).toBeVisible()
    expect(screen.getByRole('link', { name: 'Continue without login' })).toHaveAttribute(
      'href',
      '/classify',
    )
  })

  it.each([
    ['/admin', 'Administration concept'],
    ['/admin/training', 'Training concept'],
    ['/admin/models', 'Model registry concept'],
  ])('labels the proposed capability at %s without fabricated results', async (path, heading) => {
    storeMockAdmin()

    renderRoute(path)

    expect(await screen.findByRole('heading', { name: heading })).toBeVisible()
    expect(screen.getByText('Administration concept only')).toBeVisible()
    expect(screen.getByText(/there are no real permissions/i)).toBeVisible()
    expect(document.body).not.toHaveTextContent(/87\.3%|50,000|v1\.1|2026-07-20/i)
  })
})
