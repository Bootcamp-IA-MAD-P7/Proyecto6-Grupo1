import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

export default function TrainingPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-serif text-4xl font-semibold text-ink">Training concept</h1>
        <p className="mt-2 text-ink-soft">
          A non-operational layout for discussing a future controlled training workflow.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Training workflow status</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex justify-between">
            <span className="text-sm text-ink-soft">Dataset connection</span>
            <Badge variant="mock">Not connected</Badge>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-ink-soft">Execution</span>
            <span className="text-sm font-medium">Not implemented</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-ink-soft">Results</span>
            <span className="text-sm font-medium">No evidence available</span>
          </div>
        </CardContent>
      </Card>

      <div className="flex gap-2">
        <Badge variant="mock">Proposal only</Badge>
        <Badge variant="review">Cannot start jobs</Badge>
      </div>
    </div>
  )
}
