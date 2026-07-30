import { Link } from 'react-router-dom'
import { useAuth } from '@/hooks/use-auth'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { FileText, BarChart3, Workflow } from 'lucide-react'

export default function HomePage() {
  const { user, hasRole } = useAuth()

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-ink sm:text-4xl">
          Complaint classification
        </h1>
        <p className="mt-2 text-ink-soft">
          {user
            ? `Session active for ${user.name}.`
            : 'Explore the complaint-classification interface.'}
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card className="group hover:shadow-md transition-shadow duration-200">
          <CardHeader className="flex flex-row items-center gap-3 space-y-0">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-forest/10 text-forest">
              <FileText className="h-5 w-5" />
            </div>
            <CardTitle>Complaint intake</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-ink">Ready</p>
            <p className="mt-1 text-sm text-ink-soft">Use the form to describe a complaint.</p>
          </CardContent>
        </Card>

        <Card className="group hover:shadow-md transition-shadow duration-200">
          <CardHeader className="flex flex-row items-center gap-3 space-y-0">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-forest-light/10 text-forest-light">
              <BarChart3 className="h-5 w-5" />
            </div>
            <CardTitle>Recommendation</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-forest-light">Available</p>
            <p className="mt-1 text-sm text-ink-soft">Suggests a family based on the narrative.</p>
          </CardContent>
        </Card>

        <Card className="group hover:shadow-md transition-shadow duration-200">
          <CardHeader className="flex flex-row items-center gap-3 space-y-0">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-gold/10 text-gold-ink">
              <Workflow className="h-5 w-5" />
            </div>
            <CardTitle>Operational workflow</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-gold-ink">Not connected</p>
            <p className="mt-1 text-sm text-ink-soft">Human review is required for every complaint.</p>
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
              Administration
            </Button>
          </Link>
        )}
      </div>
    </div>
  )
}
