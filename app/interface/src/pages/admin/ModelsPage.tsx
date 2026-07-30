import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Box, GitCompare } from 'lucide-react'

export default function ModelsPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-ink sm:text-4xl">Model registry</h1>
        <p className="mt-2 text-ink-soft">Registered models and evaluation results.</p>
      </div>

      <Card>
        <CardHeader className="flex flex-row items-center gap-3 space-y-0">
          <Box className="h-5 w-5 text-forest-light" />
          <CardTitle>No models registered</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="rounded-lg border border-line p-4">
            <p className="text-sm text-ink-soft">
              No model artefacts, evaluation results, lifecycle states or deployment records are
              available.
            </p>
          </div>
          <div className="flex items-start gap-3 rounded-lg border border-line p-4">
            <GitCompare className="mt-0.5 h-4 w-4 shrink-0 text-ink-soft" />
            <p className="text-sm text-ink-soft">
              Comparison is unavailable until criteria and reproducible evidence are available.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
