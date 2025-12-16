import { createFileRoute } from "@tanstack/react-router";
const baseUrl = import.meta.env.VITE_API_URL;
export const Route = createFileRoute("/")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div className="bg-red-200">Hello {baseUrl}!</div>;
}
