import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

const MOCK_MODELS = [
  { id: 'v1.0', accuracy: 85.2, status: 'archived', date: '2026-07-15' },
  { id: 'v1.1', accuracy: 87.3, status: 'active', date: '2026-07-20' },
  { id: 'v1.2-beta', accuracy: 88.1, status: 'training', date: '2026-07-22' },
]

export default function ModelsPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-serif text-4xl font-semibold text-ink">Models</h1>
        <p className="mt-2 text-ink-soft">Model versions and their performance metrics.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Model Registry</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {MOCK_MODELS.map((model) => (
              <div
                key={model.id}
                className="flex items-center justify-between rounded-lg border border-line p-4"
              >
                <div>
                  <p className="font-medium text-ink">{model.id}</p>
                  <p className="text-sm text-ink-soft">Trained: {model.date}</p>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-sm font-medium">{model.accuracy}%</span>
                  <Badge
                    variant={
                      model.status === 'active'
                        ? 'default'
                        : model.status === 'training'
                          ? 'mock'
                          : 'secondary'
                    }
                  >
                    {model.status}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="flex gap-2">
        <Badge variant="mock">Mock registry</Badge>
      </div>
    </div>
  )
}
