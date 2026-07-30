import { useState } from 'react'
import { ChevronDown, ChevronUp, Lightbulb } from 'lucide-react'

export default function HelpfulTip() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className="rounded-lg border border-line bg-paper">
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        className="flex w-full items-center gap-2 px-4 py-3 text-left text-sm font-medium text-ink transition-colors hover:bg-sand focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gold focus-visible:ring-offset-2"
        aria-expanded={isOpen}
      >
        <Lightbulb className="h-4 w-4 shrink-0 text-gold-ink" />
        <span>Helpful tip</span>
        {isOpen ? (
          <ChevronUp className="ml-auto h-4 w-4 text-ink-soft" />
        ) : (
          <ChevronDown className="ml-auto h-4 w-4 text-ink-soft" />
        )}
      </button>
      {isOpen && (
        <div className="border-t border-line px-4 py-3 text-sm text-ink-soft">
          <p>
            Incluye el problema y los pasos que ya intentaste para resolverlo.
            Describe los hechos de forma clara y cronológica. No incluyas
            nombres, números de cuenta, direcciones ni otros datos personales
            innecesarios.
          </p>
        </div>
      )}
    </div>
  )
}
