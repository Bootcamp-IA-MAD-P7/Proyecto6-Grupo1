import { Link } from 'react-router-dom'
import { useAuth } from '@/hooks/use-auth'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

export default function HomePage() {
  const { user, hasRole } = useAuth()

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-serif text-4xl font-semibold text-ink">Prototype overview</h1>
        <p className="mt-2 text-ink-soft">
          {user
            ? `Mock session active for ${user.name}.`
            : 'Explore the public complaint-routing interface without creating an identity.'}
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Complaint intake</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="font-serif text-2xl font-semibold text-ink">Interface ready</p>
            <p className="text-sm text-ink-soft">Use synthetic text to review the form.</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recommendation</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="font-serif text-2xl font-semibold text-forest">Synthetic only</p>
            <p className="text-sm text-ink-soft">No model or calibrated score exists.</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Operational workflow</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="font-serif text-2xl font-semibold text-gold">Not connected</p>
            <p className="text-sm text-ink-soft">Human review remains a proposed next step.</p>
          </CardContent>
        </Card>
      </div>

      <div className="flex flex-wrap gap-4">
        <Link to="/classify">
          <Button size="lg">Classify a Complaint</Button>
        </Link>
        {hasRole('admin') && (
          <Link to="/admin">
            <Button variant="outline" size="lg">
              Review administration concept
            </Button>
          </Link>
        )}
      </div>

      <div className="flex gap-2">
        <Badge variant="mock">Prototype</Badge>
        <Badge variant="mock">Synthetic responses</Badge>
        {hasRole('admin') && <Badge variant="review">Mock admin role</Badge>}
      </div>
    </div>
  )
}
