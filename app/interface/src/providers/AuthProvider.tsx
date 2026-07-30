import { useState, useCallback, type ReactNode } from 'react'
import { AuthContext } from '@/hooks/use-auth'
import { type AuthUser, getStoredUser, getStoredToken, loginWithMock, logoutMock } from '@/services/auth-client'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(() => {
    // Only consider authenticated if both user AND token exist
    const storedUser = getStoredUser()
    const storedToken = getStoredToken()
    if (storedUser && storedToken) return storedUser
    // Clear stale data if token is missing
    if (storedUser && !storedToken) logoutMock()
    return null
  })

  const login = useCallback(async (email: string, password: string) => {
    const loggedUser = await loginWithMock(email, password)
    setUser(loggedUser)
  }, [])

  const logout = useCallback(() => {
    logoutMock()
    setUser(null)
  }, [])

  const hasRole = useCallback((role: string) => user?.role === role, [user])

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: user !== null,
        login,
        logout,
        hasRole,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}
