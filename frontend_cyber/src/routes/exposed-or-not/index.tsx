import { createFileRoute } from "@tanstack/react-router";
import { CardWithLink } from "@components/Card";

export const Route = createFileRoute("/exposed-or-not/")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <div>
      <h1>Breaches1</h1>
      <CardWithLink title="Domains" to={"/exposed-or-not/breaches"}>
        <p>Collection of domains that leaked user data</p>
      </CardWithLink>
      <CardWithLink title="Emails" to={"/exposed-or-not/emails"}>
        <p>Collection of user emails leaked in breaches</p>
      </CardWithLink>
    </div>
  );
}
