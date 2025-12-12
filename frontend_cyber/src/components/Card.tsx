// src/components/Card.tsx
import type { ReactNode } from "react";
import { Link } from "@tanstack/react-router";

type CardProps = {
  title?: string;
  children: ReactNode;
};

type CardWithLinkProps = CardProps & {
  to: string;
};

export const Card = ({ title, children }: CardProps) => {
  return (
    <div className="w-full max-w-md rounded-xl border border-slate-200 bg-white p-4 shadow-md">
      {title && <h2 className="mb-2 text-lg font-semibold text-slate-800">{title}</h2>}
      <div className="text-sm text-slate-600">{children}</div>
    </div>
  );
};

export const CardWithLink = ({ title, children, to }: CardWithLinkProps) => {
  return (
    <Link to={to} className="no-underline text-inherit">
      <div className="rounded-xl p-4 border shadow hover:shadow-lg transition">
        {title && <h2 className="text-lg font-semibold mb-2">{title}</h2>}
        {children}
      </div>
    </Link>
  );
};
