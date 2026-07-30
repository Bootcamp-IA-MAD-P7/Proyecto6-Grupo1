export default function HumanReviewPanel() {
  return (
    <aside className="rounded-lg border border-line bg-sand p-4 text-sm text-ink">
      <p className="font-semibold">Revisión humana requerida</p>
      <p className="mt-1 text-ink-soft">
        La sugerencia requiere revisión humana. La clasificación, derivación y
        decisión final pertenecen al equipo responsable.
      </p>
    </aside>
  )
}
