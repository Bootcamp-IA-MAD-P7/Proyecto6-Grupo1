import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'

export default function ProposalNotice() {
  return (
    <Alert variant="warning">
      <AlertTitle>Administration concept only</AlertTitle>
      <AlertDescription>
        These screens preserve ideas for team review. There are no real permissions, operational
        data, training jobs, registered models, comparison results or deployed services.
      </AlertDescription>
    </Alert>
  )
}
