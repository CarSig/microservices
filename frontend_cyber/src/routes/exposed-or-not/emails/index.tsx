import { createFileRoute } from "@tanstack/react-router";
import EmailForm from "../../../components/Form";
// import type { QueryClient } from "@tanstack/react-query";
import { getEmailBreachAnalytic } from "../../../services/breachedEmailsService";
import { useState } from "react";
import type { components } from "../../../types/api";
import { Card } from "../../../components/Card";

type EmailBreachAnalytics = components["schemas"]["EmailBreachAnalytics"];

type Metrics = components["schemas"]["BreachMetrics"];

export const Route = createFileRoute("/exposed-or-not/emails/")({
  // loader: ({ context }) =>
  //   (context as { queryClient: QueryClient }).queryClient.prefetchQuery({
  //     queryKey: ["breached-email"],
  //     queryFn: getEmailBreach,
  //   }),
  component: RouteComponent,
});

function RouteComponent() {
  const [data, setData] = useState<EmailBreachAnalytics | null>(null);
  const onSubmit = async (email: string) => {
    console.log("email:", email);
    const result = await getEmailBreachAnalytic(email);
    console.log("result:", result);
    setData(result);
    // await fetch("/api/subscribe", { method: "POST", body: JSON.stringify({ email }) })
  };

  return (
    <div>
      <h2>Check email</h2>
      <EmailForm onSubmit={onSubmit} />

      {data !== null && <Analytics data={data} />}
    </div>
  );
}

const Analytics = ({ data }: { data: EmailBreachAnalytics }) => {
  const { BreachMetrics, BreachesSummary } = data;

  return (
    <div>
      <BreachMetricsComp metrics={data.BreachMetrics} />
      <div>{JSON.stringify(BreachMetrics)}</div>
      <div>{JSON.stringify(BreachesSummary)}</div>
    </div>
  );
};

const BreachMetricsComp = ({ metrics }: { metrics: Metrics }) => {
  return (
    <Card>
      <h2>Metrics</h2>
      {metrics.get_details.map((detail) => (
        <p>{JSON.stringify(detail)}</p>
      ))}
    </Card>
  );
};
