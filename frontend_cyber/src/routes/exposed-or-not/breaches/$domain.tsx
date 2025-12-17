import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { getBreachByDomain } from "@services/breachesService";

export const Route = createFileRoute("/exposed-or-not/breaches/$domain")({
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  loader: ({ params, context }): any => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const ctx = context as any;
    return ctx.queryClient.prefetchQuery({
      queryKey: ["breach", params.domain],
      queryFn: () => getBreachByDomain(params.domain),
    });
  },
  component: RouteComponent,
});

function RouteComponent() {
  const { domain } = Route.useParams();
  const breachQuery = useQuery({
    queryKey: ["breach", domain],
    queryFn: () => getBreachByDomain(window.location.pathname.split("/").pop()!),
  });

  if (breachQuery.isLoading) return <p>Loading...</p>;
  if (breachQuery.isError) return <p>Error loading breach</p>;

  // const breach = breachQuery?.data?.exposedBreaches?.[0] ?? null;
  const breach = breachQuery?.data ?? null;

  if (!breach) return <p>No breach found for domain: {domain}</p>;
  return (
    <div>
      <h1>Breach Details for {breach?.domain}</h1>
      <div className="mb-5 border-2 p-4 rounded-lg shadow-md">
        <h3>{breach?.domain}</h3>
        <img src={breach?.logo} alt={`${breach?.domain} logo`} className="h-16 mb-4" />
        <p>{breach?.exposure_description}</p>
        <p>
          <strong>Records:</strong> {breach?.exposed_records}
        </p>
        <p>
          <strong>Industry:</strong> {breach?.industry}
        </p>
        <p>
          <strong>Breached Date:</strong> {breach?.breached_date}
        </p>
        <p>
          <strong>Exposed Data:</strong> {breach?.exposed_data.join(", ")}
        </p>
        <p>
          <strong>Password Risk:</strong> {breach?.password_risk}
        </p>
      </div>
    </div>
  );
}
