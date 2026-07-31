import { getPredictionApiBaseUrl } from './prediction-api-config'

export type UserRole = 'user' | 'admin'

export interface AuthUser {
  id: string
  name: string
  email: string
  role: UserRole
}

const STORAGE_KEY = 'claimvox-auth'
const TOKEN_KEY = 'claimvox-token'

export function getStoredUser(): AuthUser | null {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return null
    return JSON.parse(stored) as AuthUser
  } catch {
    return null
  }
}

export function getStoredToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function storeUser(user: AuthUser): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(user))
}

function storeToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearStoredUser(): void {
  localStorage.removeItem(STORAGE_KEY)
  localStorage.removeItem(TOKEN_KEY)
}

export async function loginWithLocalDemo(email: string, password: string): Promise<AuthUser> {
  const baseUrl = getPredictionApiBaseUrl()
  if (!baseUrl) {
    throw new Error('Local authentication is not configured.')
  }

  const response = await fetch(`${baseUrl}/api/v1/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: email, password }),
  })

  if (!response.ok) {
    throw new Error('Invalid credentials')
  }

  const data = await response.json()
  const token: string = data.access_token

  // Store the token
  storeToken(token)

  // Build user object from backend response
  const user: AuthUser = {
    id: token.substring(0, 8),
    name: data.name || email,
    email,
    role: data.role || 'user',
  }

  storeUser(user)
  return user
}

export function logoutLocalDemo(): void {
  clearStoredUser()
}
