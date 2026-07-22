import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

export default function ClassificationPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-serif text-4xl font-semibold text-ink">Classify Complaint</h1>
        <p className="mt-2 text-ink-soft">
          Enter a complaint narrative to classify it into one of 11 CFPB product families.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Narrative Input</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-ink-soft">
            Complaint form will be implemented in T-026.
          </p>
        </CardContent>
      </Card>

      <div className="flex gap-2">
        <Badge variant="mock">Mock responses</Badge>
        <Badge variant="review">Human review required</Badge>
      </div>
    </div>
  )
}
