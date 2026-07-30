import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom'
import { AuthProvider } from '@/providers/AuthProvider'
import { useAuth } from '@/hooks/use-auth'
import AuthLayout from '@/layouts/AuthLayout'
import UserLayout from '@/layouts/UserLayout'
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
  children?: React.ReactNode
  requiredRole?: 'user' | 'admin'
}) {
  const { isAuthenticated, hasRole } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (requiredRole && !hasRole(requiredRole)) {
    return <Navigate to="/" replace />
  }

  return children ? <>{children}</> : <Outlet />
}

export default function AppRouter() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route
            path="/login"
            element={
              <AuthLayout>
                <LoginPage />
              </AuthLayout>
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
            <Route path="/admin" element={<ProtectedRoute requiredRole="admin" />}>
              <Route index element={<DashboardPage />} />
              <Route path="training" element={<TrainingPage />} />
              <Route path="models" element={<ModelsPage />} />
            </Route>
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}
