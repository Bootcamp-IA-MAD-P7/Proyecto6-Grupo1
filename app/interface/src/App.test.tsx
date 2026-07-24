import { render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it } from 'vitest'
import AppRouter from './App'

const renderRoute = (path: string) => {
  window.history.pushState({}, '', path)
  return render(<AppRouter />)
}

afterEach(() => {
  localStorage.clear()
  window.history.pushState({}, '', '/')
})

describe('application routes', () => {
  it('opens the classification flow without a mock login or stored identity', async () => {
    localStorage.clear()

    renderRoute('/classify')

    expect(await screen.findByRole('heading', { name: 'Describe what happened' })).toBeVisible()
    expect(screen.getByText('Public prototype · no identity')).toBeVisible()
    expect(localStorage.getItem('complaint-routing-auth')).toBeNull()
  })

  it('keeps the login as an explicitly non-secure proposal', () => {
    renderRoute('/login')

    expect(screen.getByText('Mock authentication proposal only.')).toBeVisible()
    expect(screen.getByText(/provides no real identity, security/i)).toBeVisible()
    expect(screen.getByRole('link', { name: 'Continue without mock login' })).toHaveAttribute(
      'href',
      '/classify',
    )
  })
})
