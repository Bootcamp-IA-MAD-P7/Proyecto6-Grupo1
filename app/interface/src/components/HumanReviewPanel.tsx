import { Users } from 'lucide-react'

export default function HumanReviewPanel() {
  return (
    <aside className="rounded-lg border border-line bg-sand p-4 text-sm text-ink">
      <Users className="mb-3 h-10 w-10 text-rust" />
      <p className="font-semibold">Human review required</p>
      <p className="mt-1 text-ink-soft">
        The suggestion requires human review. The classification, routing, and final decision belong
        to the responsible team.
      </p>
    </aside>
  )
}
