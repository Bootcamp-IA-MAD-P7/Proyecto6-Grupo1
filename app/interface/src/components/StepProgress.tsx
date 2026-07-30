import { cn } from '@/lib/utils'

const STEPS = ['Describe', 'Review', 'Guidance', 'Next step'] as const

interface StepProgressProps {
  currentStep: 1 | 2 | 3 | 4
}

export default function StepProgress({ currentStep }: StepProgressProps) {
  return (
    <nav aria-label="Progress" className="flex items-center gap-1">
      {STEPS.map((label, index) => {
        const stepNumber = (index + 1) as 1 | 2 | 3 | 4
        const isActive = stepNumber === currentStep
        const isCompleted = stepNumber < currentStep

        return (
          <div key={label} className="flex flex-1 items-center">
            <div
              className={cn(
                'flex items-center gap-2 rounded-lg px-3 py-1.5 text-xs font-medium transition-colors',
                isActive && 'bg-forest text-white',
                isCompleted && 'text-forest',
                !isActive && !isCompleted && 'text-ink-soft',
              )}
              aria-current={isActive ? 'step' : undefined}
            >
              <span
                className={cn(
                  'flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-xs font-bold',
                  (isActive || isCompleted) && 'bg-white text-forest',
                  !isActive && !isCompleted && 'bg-ink-soft/20 text-ink-soft',
                )}
              >
                {stepNumber}
              </span>
              <span className="hidden sm:inline">{label}</span>
            </div>
            {index < STEPS.length - 1 && (
              <div
                className={cn(
                  'mx-1 h-px flex-1',
                  isCompleted ? 'bg-forest' : 'bg-line',
                )}
              />
            )}
          </div>
        )
      })}
    </nav>
  )
}
