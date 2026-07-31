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
  localStorage.setItem('claimvox-token', 'synthetic-token')
}

afterEach(() => {
  localStorage.clear()
  window.history.pushState({}, '', '/')
})

describe('application routes', () => {
  it('redirects the classification flow to local sign-in without a stored session', async () => {
    localStorage.clear()

    renderRoute('/classify')

    expect(await screen.findByRole('heading', { level: 1, name: 'ClaimVox' })).toBeVisible()
    expect(screen.getByText('ClaimVox demonstration access')).toBeVisible()
    expect(localStorage.getItem('claimvox-auth')).toBeNull()
  })

  it('shows the configured demonstration credentials and their boundary', () => {
    renderRoute('/login')

    expect(screen.getByText(/Demo authentication/i)).toBeVisible()
    expect(screen.getByText(/not a production identity system/i)).toBeVisible()
    expect(screen.getByText(/claimvox2026/i)).toBeVisible()
    expect(screen.queryByRole('link', { name: 'Continue without login' })).not.toBeInTheDocument()
  })

  it.each([
    ['/admin', 'Dashboard', 'Not connected'],
    ['/admin/training', 'Training', 'Not connected'],
    ['/admin/models', 'Model registry', 'No models registered'],
  ])(
    'shows %s page with factual status indicators without fabricated data',
    async (path, heading, status) => {
      storeMockAdmin()

      renderRoute(path)

      expect(await screen.findByRole('heading', { name: heading })).toBeVisible()
      expect(screen.getByText(status)).toBeVisible()
      expect(document.body).not.toHaveTextContent(/87\.3%|50,000|v1\.1|2026-07-20/i)
    },
  )
})
