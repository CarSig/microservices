import React, { useMemo, useState } from "react";

type EmailFormProps = {
  onSubmit: (email: string) => void | Promise<void>;
  initialEmail?: string;
  label?: string;
  placeholder?: string;
  submitText?: string;
  disabled?: boolean;
  className?: string;
};

function isValidEmail(email: string) {
  // pragmatic, not RFC-perfect
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
}

export default function EmailForm({
  onSubmit,
  initialEmail = "",
  label = "Email",
  placeholder = "you@example.com",
  submitText = "Submit",
  disabled = false,
  className,
}: EmailFormProps) {
  const [email, setEmail] = useState(initialEmail);
  const [touched, setTouched] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [serverError, setServerError] = useState<string | null>(null);

  const trimmed = useMemo(() => email.trim(), [email]);
  const valid = useMemo(() => isValidEmail(trimmed), [trimmed]);
  const showError = touched && !valid;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setTouched(true);
    setServerError(null);

    if (!valid || disabled) return;

    try {
      setSubmitting(true);
      await onSubmit(trimmed);
    } catch (err) {
      setServerError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className={className} noValidate>
      <label style={{ display: "block", marginBottom: 6, fontWeight: 600 }}>{label}</label>

      <input
        type="email"
        inputMode="email"
        autoComplete="email"
        value={email}
        disabled={disabled || submitting}
        placeholder={placeholder}
        onChange={(e) => setEmail(e.target.value)}
        onBlur={() => setTouched(true)}
        aria-invalid={showError ? "true" : "false"}
        aria-describedby="email-help email-error"
        style={{
          width: "100%",
          padding: "10px 12px",
          borderRadius: 10,
          border: showError ? "1px solid #d33" : "1px solid #ccc",
          outline: "none",
        }}
      />

      <div id="email-help" style={{ marginTop: 6, fontSize: 12, opacity: 0.75 }}>
        We’ll only use this to contact you.
      </div>

      {showError && (
        <div id="email-error" style={{ marginTop: 6, fontSize: 12, color: "#d33" }}>
          Please enter a valid email address.
        </div>
      )}

      {serverError && <div style={{ marginTop: 6, fontSize: 12, color: "#d33" }}>{serverError}</div>}

      <button
        type="submit"
        disabled={disabled || submitting || !valid}
        style={{
          marginTop: 12,
          padding: "10px 14px",
          borderRadius: 10,
          border: "1px solid #000",
          background: disabled || submitting || !valid ? "#eee" : "#fff",
          cursor: disabled || submitting || !valid ? "not-allowed" : "pointer",
          fontWeight: 600,
        }}
      >
        {submitting ? "Submitting…" : submitText}
      </button>
    </form>
  );
}
