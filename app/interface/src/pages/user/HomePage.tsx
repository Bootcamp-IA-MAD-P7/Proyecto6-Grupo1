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
        <h1 className="font-serif text-4xl font-semibold text-ink">Dashboard</h1>
        <p className="mt-2 text-ink-soft">Welcome back, {user?.name}. Select an action below.</p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Total Complaints</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="font-serif text-3xl font-semibold text-ink">1,247</p>
            <p className="text-sm text-ink-soft">Last 30 days (mock)</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Model Accuracy</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="font-serif text-3xl font-semibold text-forest">87.3%</p>
            <p className="text-sm text-ink-soft">Mock metric</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Pending Review</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="font-serif text-3xl font-semibold text-gold">23</p>
            <p className="text-sm text-ink-soft">Requires human review</p>
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
              Admin Dashboard
            </Button>
          </Link>
        )}
      </div>

      <div className="flex gap-2">
        <Badge variant="mock">Prototype</Badge>
        <Badge variant="mock">Mock data</Badge>
        {hasRole('admin') && <Badge variant="review">Admin role</Badge>}
      </div>
    </div>
  )
}
