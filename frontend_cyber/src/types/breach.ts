export interface Breach {
  breachID: string;
  breachedDate: string;
  domain: string;
  exposedData: string[];
  exposedRecords: number;
  exposureDescription: string;
  industry: string;
  logo: string;
  passwordRisk: string;
  referenceURL: string | null;
  searchable: boolean;
  sensitive: boolean;
  verified: boolean;
}

export interface BreachesResponse {
  exposedBreaches: Breach[];
}
