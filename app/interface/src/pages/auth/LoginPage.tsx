import { useState, type FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '@/hooks/use-auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { buttonVariants } from '@/lib/button-variants'
import { cn } from '@/lib/utils'
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
      setError('Invalid credentials. Try ana@example.com (user) or carlos@example.com (admin).')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Alert variant="warning">
        <AlertDescription>
          <strong>Mock authentication proposal only.</strong> This screen uses fixed demo identities
          and accepts any password. It provides no real identity, security, authorization or access
          control.
        </AlertDescription>
      </Alert>
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
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
          placeholder="Enter any password"
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
      <Link to="/classify" className={cn(buttonVariants({ variant: 'outline' }), 'w-full')}>
        Continue without login
      </Link>
      <p className="text-center text-xs text-ink-soft">
        Demo: ana@example.com (user) / carlos@example.com (admin)
      </p>
    </form>
  )
}
