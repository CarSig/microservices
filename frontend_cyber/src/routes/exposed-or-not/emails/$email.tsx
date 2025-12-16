import { createFileRoute } from "@tanstack/react-router";
import { getEmailBreach } from "../../../services/breachedEmailsService";
import { useQuery } from "@tanstack/react-query";

export const Route = createFileRoute("/exposed-or-not/emails/$email")({
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  loader: ({ params, context }): any => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const ctx = context as any;
    return ctx.queryClient.prefetchQuery({
      queryKey: ["breach", params.email],
      queryFn: () => getEmailBreach(params.email),
    });
  },
  component: RouteComponent,
});

function RouteComponent() {
  const { email } = Route.useParams();
  const emailQuery = useQuery({
    queryKey: ["email", email],
    queryFn: () => getEmailBreach(window.location.pathname.split("/").pop()!),
  });

  if (emailQuery.isLoading) return <p>Loading...</p>;
  if (emailQuery.isError) return <p>Error loading email breach</p>;
  const emailData = emailQuery?.data ?? null;

  if (!emailData) return <p>No breach found for email: {email}</p>;
  return (
    <div>
      <h2>Email Breach : {emailData.email}</h2>
      {emailData.breaches[0].map((x) => (
        <EmailItem email={x} key={x} />
      ))}
    </div>
  );
}

const EmailItem = ({ email }: { email: string }) => {
  return (
    <div className="mb-5 border-2 p-4 rounded-lg shadow-md">
      <p>{email}</p>
    </div>
  );
};
