import { api } from "@/api/api_exposed";
import type { components } from "@schemaFastAPI";
// import type { components } from "../api/schema";

type Breaches = components["schemas"]["Breaches"];
type Breach = components["schemas"]["Breach"];

export async function getBreaches(): Promise<Breaches> {
  const res = await api.get("/breaches");
  return res.data;
}

export async function getBreachByDomain(domain: string): Promise<Breach> {
  const res = await api.get(`/breaches/${domain}`);
  return res.data;
}
