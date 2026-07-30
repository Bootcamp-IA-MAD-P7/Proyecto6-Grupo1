import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it, vi } from 'vitest'
import UserLayout from './UserLayout'
import { useAuth } from '@/hooks/use-auth'

vi.mock('@/components/ThemeToggle', () => ({
  ThemeToggle: () => <button type="button">Theme</button>,
}))

vi.mock('@/hooks/use-auth', () => ({
  useAuth: vi.fn(),
}))

const mockedUseAuth = vi.mocked(useAuth)

describe('UserLayout', () => {
  it('keeps the demo sign-in entry visible when no session is active', () => {
    mockedUseAuth.mockReturnValue({
      user: null,
      isAuthenticated: false,
      login: vi.fn(),
      logout: vi.fn(),
      hasRole: () => false,
    })

    render(
      <MemoryRouter>
        <UserLayout />
      </MemoryRouter>,
    )

    expect(screen.getByText('Not signed in')).toBeVisible()
    expect(screen.getByRole('link', { name: 'Sign in' })).toHaveAttribute('href', '/login')
  })

  it('shows user navigation without admin items', () => {
    mockedUseAuth.mockReturnValue({
      user: { id: '1', name: 'Test User', email: 'test@example.com', role: 'user' },
      isAuthenticated: true,
      login: vi.fn(),
      logout: vi.fn(),
      hasRole: (r: string) => r === 'user',
    })

    render(
      <MemoryRouter>
        <UserLayout />
      </MemoryRouter>,
    )

    expect(screen.getByRole('link', { name: 'Home' })).toBeVisible()
    expect(screen.getByRole('link', { name: 'Classify' })).toBeVisible()
    expect(screen.queryByRole('link', { name: 'Dashboard' })).not.toBeInTheDocument()
    expect(screen.queryByRole('link', { name: 'Training' })).not.toBeInTheDocument()
    expect(screen.queryByRole('link', { name: 'Models' })).not.toBeInTheDocument()
    expect(screen.getByText('Test User (user)')).toBeVisible()
    expect(screen.getByRole('button', { name: 'Sign out' })).toBeVisible()
    expect(screen.queryByText(/prototype/i)).not.toBeInTheDocument()
  })

  it('shows admin navigation with all items', () => {
    mockedUseAuth.mockReturnValue({
      user: { id: '2', name: 'Admin User', email: 'admin@example.com', role: 'admin' },
      isAuthenticated: true,
      login: vi.fn(),
      logout: vi.fn(),
      hasRole: (r: string) => r === 'admin',
    })

    render(
      <MemoryRouter>
        <UserLayout />
      </MemoryRouter>,
    )

    expect(screen.getByRole('link', { name: 'Home' })).toBeVisible()
    expect(screen.getByRole('link', { name: 'Classify' })).toBeVisible()
    expect(screen.getByRole('link', { name: 'Dashboard' })).toBeVisible()
    expect(screen.getByRole('link', { name: 'Training' })).toBeVisible()
    expect(screen.getByRole('link', { name: 'Models' })).toBeVisible()
    expect(screen.getByText('Admin User (admin)')).toBeVisible()
  })

  it('shows Settings section with theme toggle', () => {
    mockedUseAuth.mockReturnValue({
      user: { id: '1', name: 'Test User', email: 'test@example.com', role: 'user' },
      isAuthenticated: true,
      login: vi.fn(),
      logout: vi.fn(),
      hasRole: (r: string) => r === 'user',
    })

    render(
      <MemoryRouter>
        <UserLayout />
      </MemoryRouter>,
    )

    expect(screen.getByText('Settings')).toBeVisible()
    expect(screen.getByRole('button', { name: 'Theme' })).toBeVisible()
  })
})
