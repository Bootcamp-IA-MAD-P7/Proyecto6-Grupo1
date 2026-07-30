import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Database, Cpu, BarChart } from 'lucide-react'

export default function TrainingPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-ink sm:text-4xl">Training</h1>
        <p className="mt-2 text-ink-soft">Training workflow status and job history.</p>
      </div>

      <Card>
        <CardHeader className="flex flex-row items-center gap-3 space-y-0">
          <Cpu className="h-5 w-5 text-forest-light" />
          <CardTitle>Training workflow status</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between rounded-lg border border-line p-3">
            <div className="flex items-center gap-3">
              <Database className="h-4 w-4 text-ink-soft" />
              <span className="text-sm font-medium text-ink">Dataset connection</span>
            </div>
            <span className="text-sm font-medium text-rust">Not connected</span>
          </div>
          <div className="flex items-center justify-between rounded-lg border border-line p-3">
            <div className="flex items-center gap-3">
              <Cpu className="h-4 w-4 text-ink-soft" />
              <span className="text-sm font-medium text-ink">Execution</span>
            </div>
            <span className="text-sm text-ink-soft">Not implemented</span>
          </div>
          <div className="flex items-center justify-between rounded-lg border border-line p-3">
            <div className="flex items-center gap-3">
              <BarChart className="h-4 w-4 text-ink-soft" />
              <span className="text-sm font-medium text-ink">Results</span>
            </div>
            <span className="text-sm text-ink-soft">No evidence available</span>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
