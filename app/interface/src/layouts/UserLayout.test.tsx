import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it, vi } from 'vitest'
import UserLayout from './UserLayout'

vi.mock('@/components/ThemeToggle', () => ({
  ThemeToggle: () => <button type="button">Theme</button>,
}))

describe('UserLayout', () => {
  it('keeps the visible navigation focused on local classification', () => {
    render(
      <MemoryRouter>
        <UserLayout />
      </MemoryRouter>,
    )

    expect(screen.getByText('Local classification prototype')).toBeVisible()
    expect(screen.getByRole('link', { name: 'Home' })).toBeVisible()
    expect(screen.getByRole('link', { name: 'Classify' })).toBeVisible()
    expect(screen.queryByRole('link', { name: 'Sign in' })).not.toBeInTheDocument()
    expect(screen.queryByText(/admin/i)).not.toBeInTheDocument()
  })
})
