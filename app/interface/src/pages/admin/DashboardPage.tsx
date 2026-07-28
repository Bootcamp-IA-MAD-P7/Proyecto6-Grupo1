import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Database, Activity, Server, Users } from 'lucide-react'

const stats = [
  {
    title: 'Operational data',
    value: 'Not connected',
    description: 'No complaint activity is loaded.',
    icon: Database,
    color: 'text-ink',
  },
  {
    title: 'Model evidence',
    value: 'Not available',
    description: 'No model evaluation is connected.',
    icon: Activity,
    color: 'text-forest-light',
  },
  {
    title: 'Service health',
    value: 'Unavailable',
    description: 'No backend service is configured.',
    icon: Server,
    color: 'text-gold-ink',
  },
  {
    title: 'Human review',
    value: 'Proposed',
    description: 'Workflow and queue rules need approval.',
    icon: Users,
    color: 'text-rust',
  },
]

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-ink sm:text-4xl">
          Administration concept
        </h1>
        <p className="mt-2 text-ink-soft">
          A proposed overview of the information an operations team may need.
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.title} className="group hover:shadow-md transition-shadow duration-200">
            <CardHeader className="flex flex-row items-center gap-3 space-y-0 pb-2">
              <stat.icon className={`h-5 w-5 ${stat.color}`} />
              <CardTitle className="text-sm">{stat.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className={`text-2xl font-bold ${stat.color}`}>{stat.value}</p>
              <p className="mt-1 text-sm text-ink-soft">{stat.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="flex flex-wrap gap-2">
        <Badge variant="mock">Interface concept</Badge>
        <Badge variant="review">No operational data</Badge>
      </div>
    </div>
  )
}
