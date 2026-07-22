import { useState, useCallback, type ReactNode } from 'react'
import { AuthContext } from '@/hooks/use-auth'
import {
  type AuthUser,
  getStoredUser,
  loginWithMock,
  logoutMock,
} from '@/services/auth-client'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(() => getStoredUser())

  const login = useCallback(async (email: string, password: string) => {
    const loggedUser = await loginWithMock(email, password)
    setUser(loggedUser)
  }, [])

  const logout = useCallback(() => {
    logoutMock()
    setUser(null)
  }, [])

  const hasRole = useCallback(
    (role: string) => user?.role === role,
    [user],
  )

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
