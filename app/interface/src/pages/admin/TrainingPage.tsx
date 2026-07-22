import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

export default function TrainingPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-serif text-4xl font-semibold text-ink">Training</h1>
        <p className="mt-2 text-ink-soft">
          Model training simulation and configuration.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Last Training Run</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex justify-between">
            <span className="text-sm text-ink-soft">Status</span>
            <Badge variant="mock">Completed (mock)</Badge>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-ink-soft">Accuracy</span>
            <span className="text-sm font-medium">87.3%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-ink-soft">Training samples</span>
            <span className="text-sm font-medium">50,000 (mock)</span>
          </div>
        </CardContent>
      </Card>

      <div className="flex gap-2">
        <Badge variant="mock">Simulation only</Badge>
      </div>
    </div>
  )
}
