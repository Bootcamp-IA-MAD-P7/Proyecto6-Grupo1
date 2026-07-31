import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/hooks/use-auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { LogIn } from 'lucide-react'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      await login(email, password)
      navigate('/')
    } catch {
      setError('Invalid credentials. Use admin / claimvox2026.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Alert variant="warning">
        <AlertDescription>
          <strong>Demo authentication.</strong> Use username <code>admin</code> and password{' '}
          <code>claimvox2026</code>. This shared demonstration account is not a production identity
          system.
        </AlertDescription>
      </Alert>
      <div className="space-y-2">
        <Label htmlFor="email">Username</Label>
        <Input
          id="email"
          type="text"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your username"
          required
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="password">Password</Label>
        <Input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter the demo password"
          required
        />
      </div>
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
      <Button type="submit" className="w-full" disabled={isLoading}>
        <LogIn className="h-4 w-4" />
        {isLoading ? 'Signing in...' : 'Sign in'}
      </Button>
      <p className="text-center text-xs text-ink-soft">
        Shared access for the ClaimVox project presentation.
      </p>
    </form>
  )
}
