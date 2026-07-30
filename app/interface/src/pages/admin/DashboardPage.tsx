import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
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
    value: 'Required',
    description: 'Classification requires human review.',
    icon: Users,
    color: 'text-rust',
  },
]

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-ink sm:text-4xl">
          Dashboard
        </h1>
        <p className="mt-2 text-ink-soft">
          Overview of the operational status.
        </p>
      </div>

      <div className="grid gap-6 min-w-0 sm:grid-cols-2">
        {stats.map((stat) => (
          <Card key={stat.title} className="group hover:shadow-md transition-shadow duration-200 min-w-0">
            <CardHeader className="flex flex-col items-center gap-3 space-y-0 pb-2 text-center min-w-0">
              <stat.icon className={`h-8 w-8 shrink-0 ${stat.color}`} />
              <CardTitle className="text-sm break-words">{stat.title}</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p className={`text-2xl font-bold break-words ${stat.color}`}>{stat.value}</p>
              <p className="mt-1 text-sm text-ink-soft break-words">{stat.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
