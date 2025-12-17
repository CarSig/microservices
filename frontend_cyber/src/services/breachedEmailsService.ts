import { api } from "../api/api_exposed";
import type { components } from "@schemaFastAPI";

// type Breaches = components["schemas"]["Breaches"];
type EmailBreaches = components["schemas"]["EmailBreaches"];
type EmailBreachAnalytics = components["schemas"]["EmailBreachAnalytics"];

export async function getEmailBreachAnalytic(email: string): Promise<EmailBreachAnalytics> {
  const res = await api.get(`/emails/analytics/${email}`);

  return res.data;
}

export async function getEmailBreach(email: string): Promise<EmailBreaches> {
  const res = await api.get(`/emails/${email}`);
  return res.data;
}
