import { api } from "../lib/api_exposed";
import type { components } from "../types/api";

type Breaches = components["schemas"]["Breaches"];

export async function getBreaches(): Promise<Breaches> {
  const res = await api.get("/breaches");
  return res.data;
}

export async function getBreachByDomain(domain: string): Promise<Breaches> {
  const res = await api.get(`/breaches/${domain}`);
  return res.data;
}
