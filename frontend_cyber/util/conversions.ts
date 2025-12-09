type Primitive = string | number | boolean | null | undefined;

type Json = Primitive | Json[] | { [key: string]: Json };

export function toCamelCase<T extends Json>(input: T): T {
  if (Array.isArray(input)) {
    return input.map((item) => toCamelCase(item)) as T;
  }

  if (input !== null && typeof input === "object") {
    const output: Record<string, Json> = {};

    for (const key of Object.keys(input)) {
      const camelKey = key.replace(/_([a-z])/g, (_, char) => char.toUpperCase());
      const value = (input as Record<string, Json>)[key];
      output[camelKey] = toCamelCase(value);
    }

    return output as T;
  }

  return input;
}
