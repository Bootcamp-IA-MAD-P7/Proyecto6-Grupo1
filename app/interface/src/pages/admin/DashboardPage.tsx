import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-serif text-4xl font-semibold text-ink">Administration concept</h1>
        <p className="mt-2 text-ink-soft">
          A proposed overview of the information an operations team may need.
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader>
            <CardTitle>Operational data</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="font-serif text-2xl font-semibold text-ink">Not connected</p>
            <p className="text-sm text-ink-soft">No complaint activity is loaded.</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Model evidence</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="font-serif text-2xl font-semibold text-forest">Not available</p>
            <p className="text-sm text-ink-soft">No model evaluation is connected.</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Service health</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="font-serif text-2xl font-semibold text-gold">Unavailable</p>
            <p className="text-sm text-ink-soft">No backend service is configured.</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Human review</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="font-serif text-2xl font-semibold text-rust">Proposed</p>
            <p className="text-sm text-ink-soft">Workflow and queue rules need approval.</p>
          </CardContent>
        </Card>
      </div>

      <div className="flex gap-2">
        <Badge variant="mock">Interface concept</Badge>
        <Badge variant="review">No operational data</Badge>
      </div>
    </div>
  )
}
