import { cva, type VariantProps } from 'class-variance-authority'

export const badgeVariants = cva(
  'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default: 'border-transparent bg-forest text-white',
        secondary: 'border-transparent bg-sand text-ink',
        destructive: 'border-transparent bg-rust text-white',
        outline: 'text-ink',
        mock: 'border-gold/30 bg-gold/10 text-gold-ink dark:text-gold',
        review: 'border-rust/30 bg-rust-pale text-rust',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  },
)

export type BadgeVariants = VariantProps<typeof badgeVariants>
