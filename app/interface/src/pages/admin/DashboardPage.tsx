import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-serif text-4xl font-semibold text-ink">Admin Dashboard</h1>
        <p className="mt-2 text-ink-soft">System overview and model performance metrics.</p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader>
            <CardTitle>Daily Volume</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="font-serif text-3xl font-semibold text-ink">342</p>
            <p className="text-sm text-ink-soft">Today (mock)</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Accuracy</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="font-serif text-3xl font-semibold text-forest">87.3%</p>
            <p className="text-sm text-ink-soft">Current model</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Avg Response</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="font-serif text-3xl font-semibold text-gold">1.2s</p>
            <p className="text-sm text-ink-soft">Mock latency</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Review Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="font-serif text-3xl font-semibold text-rust">18%</p>
            <p className="text-sm text-ink-soft">Requires review</p>
          </CardContent>
        </Card>
      </div>

      <div className="flex gap-2">
        <Badge variant="mock">Admin view</Badge>
        <Badge variant="mock">Mock data</Badge>
      </div>
    </div>
  )
}
