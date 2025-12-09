import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/api/exposed-or-not/breaches/')({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Hello "/exposed-or-not/breaches/"!</div>
}
