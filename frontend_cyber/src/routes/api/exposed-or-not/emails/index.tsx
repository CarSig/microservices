import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/api/exposed-or-not/emails/')({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Hello "/api/exposed-or-not/emails/"!</div>
}
