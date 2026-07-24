import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

export default function ModelsPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-serif text-4xl font-semibold text-ink">Model registry concept</h1>
        <p className="mt-2 text-ink-soft">
          A proposed place to review evidence before approving a future model.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>No models registered</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <p className="text-sm text-ink-soft">
            This prototype has no model artefacts, evaluation results, lifecycle states or
            deployment records.
          </p>
          <p className="text-sm text-ink-soft">
            Comparison will remain unavailable until the team approves criteria and supplies
            reproducible evidence.
          </p>
        </CardContent>
      </Card>

      <div className="flex gap-2">
        <Badge variant="mock">Registry proposal</Badge>
        <Badge variant="review">Comparison unavailable</Badge>
      </div>
    </div>
  )
}
