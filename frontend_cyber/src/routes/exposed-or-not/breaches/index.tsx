import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import type { QueryClient } from "@tanstack/react-query";
import { getBreaches } from "@services/breachesService";
import { Link } from "@tanstack/react-router";
import { useState, useCallback } from "react";
import type { components } from "@schemaFastAPI";

type BreachSmall = components["schemas"]["BreachSmall"];

export const Route = createFileRoute("/exposed-or-not/breaches/")({
  loader: ({ context }) =>
    // quick cast so TS knows context has queryClient
    (context as { queryClient: QueryClient }).queryClient.prefetchQuery({
      queryKey: ["breaches"],
      queryFn: getBreaches,
    }),
  component: RouteComponent,
});

function RouteComponent() {
  const breachesQuery = useQuery({
    queryKey: ["breaches"],
    queryFn: getBreaches,
  });
  const [breachFilter, setBreachFilter] = useState("");
  const onChangeFilter = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setBreachFilter(e.target.value);
  }, []);

  if (breachesQuery.isLoading) return <p>Loading...</p>;
  if (breachesQuery.isError) return <p>Error loading breaches -- {JSON.stringify(breachesQuery.error)}</p>;

  const breaches = breachesQuery?.data?.exposedBreaches;

  const filteredBreaches = breaches?.filter((b) => b.domain.toLowerCase().includes(breachFilter.toLowerCase()));

  return (
    <div>
      <h1>Breaches</h1>
      <input type="text" placeholder="Search breaches..." className="mb-4 p-2 border rounded w-full" onChange={onChangeFilter} />
      {filteredBreaches?.map((b) => (
        <BreachItem key={b.breach_id} b={b} />
      ))}
    </div>
  );
}

function BreachItem({ b }: { b: BreachSmall }) {
  return (
    <Link to={"/exposed-or-not/breaches/$domain"} params={{ domain: b.domain }} className="no-underline text-inherit">
      <div className="mb-5 border-2 p-4 rounded-lg shadow-md">
        <h3>{b.domain}</h3>
        <p>
          <strong>Records:</strong> {b.exposed_records}
        </p>
        <p>
          <strong>Industry:</strong> {b.industry}
        </p>

        <p>
          <strong>breachedDate:</strong> {b.breached_date}
        </p>
      </div>
    </Link>
  );
}
