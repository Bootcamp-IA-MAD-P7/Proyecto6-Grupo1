export type UserRole = 'user' | 'admin'

export interface AuthUser {
  id: string
  name: string
  email: string
  role: UserRole
}

const MOCK_USERS: AuthUser[] = [
  { id: '1', name: 'Ana García', email: 'ana@example.com', role: 'user' },
  { id: '2', name: 'Carlos López', email: 'carlos@example.com', role: 'admin' },
]

const STORAGE_KEY = 'complaint-routing-auth'

export function getStoredUser(): AuthUser | null {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return null
    return JSON.parse(stored) as AuthUser
  } catch {
    return null
  }
}

export function storeUser(user: AuthUser): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(user))
}

export function clearStoredUser(): void {
  localStorage.removeItem(STORAGE_KEY)
}

export async function loginWithMock(
  email: string,
  _password: string,
): Promise<AuthUser> {
  await new Promise((resolve) => setTimeout(resolve, 400))

  const user = MOCK_USERS.find((u) => u.email === email)
  if (!user) {
    throw new Error('Invalid credentials')
  }

  storeUser(user)
  return user
}

export function logoutMock(): void {
  clearStoredUser()
}
