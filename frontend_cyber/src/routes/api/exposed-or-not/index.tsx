import { createFileRoute } from "@tanstack/react-router";
import { CardWithLink } from "../../../components/Card";
// import type { Breach } from "../../../types/breach";

export const Route = createFileRoute("/api/exposed-or-not/")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <div>
      <h1>Breaches</h1>
      <CardWithLink title="Domains" to={"/api/exposed-or-not/breaches"}>
        <p>Collection of domains that leaked user data</p>
      </CardWithLink>
      <CardWithLink title="Emails" to={"/api/exposed-or-not/emails"}>
        <p>Collection of user emails leaked in breaches</p>
      </CardWithLink>
    </div>
  );
}
