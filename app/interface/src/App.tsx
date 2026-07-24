import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from '@/providers/AuthProvider'
import { useAuth } from '@/hooks/use-auth'
import AuthLayout from '@/layouts/AuthLayout'
import UserLayout from '@/layouts/UserLayout'
import AdminLayout from '@/layouts/AdminLayout'
import LoginPage from '@/pages/auth/LoginPage'
import HomePage from '@/pages/user/HomePage'
import ClassificationPage from '@/pages/user/ClassificationPage'
import DashboardPage from '@/pages/admin/DashboardPage'
import TrainingPage from '@/pages/admin/TrainingPage'
import ModelsPage from '@/pages/admin/ModelsPage'

function ProtectedRoute({
  children,
  requiredRole,
}: {
  children: React.ReactNode
  requiredRole?: 'user' | 'admin'
}) {
  const { isAuthenticated, hasRole } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (requiredRole && !hasRole(requiredRole)) {
    return <Navigate to="/" replace />
  }

  return <>{children}</>
}

function PublicRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, hasRole } = useAuth()

  if (isAuthenticated) {
    return <Navigate to={hasRole('admin') ? '/admin' : '/'} replace />
  }

  return <>{children}</>
}

export default function AppRouter() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route
            path="/login"
            element={
              <PublicRoute>
                <AuthLayout>
                  <LoginPage />
                </AuthLayout>
              </PublicRoute>
            }
          />

          <Route
            element={
              <ProtectedRoute>
                <UserLayout />
              </ProtectedRoute>
            }
          >
            <Route path="/" element={<HomePage />} />
            <Route path="/classify" element={<ClassificationPage />} />
          </Route>

          <Route
            path="/admin"
            element={
              <ProtectedRoute requiredRole="admin">
                <AdminLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<DashboardPage />} />
            <Route path="training" element={<TrainingPage />} />
            <Route path="models" element={<ModelsPage />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}
