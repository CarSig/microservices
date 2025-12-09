import { api } from "../lib/api_exposed";
import type { BreachesResponse } from "../types/breach";
import { toCamelCase } from "../../util/conversions";

export async function getBreaches(): Promise<BreachesResponse> {
  const res = await api.get("/breaches");
  return toCamelCase(res.data);
}

export async function getBreachByDomain(domain: string): Promise<BreachesResponse> {
  const res = await api.get(`/breaches/${domain}`);
  return toCamelCase(res.data);
}
