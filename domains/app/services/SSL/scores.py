
# services/scoring.py

def calculate_scores(cert: dict) -> tuple[dict[str, int], dict[str, str]]:
    scores: dict[str, int] = {}
    explanations: dict[str, str] = {}

    # ---------------- TLS Version ----------------
    tls_version = cert["tls_connection"]["tls_version"]

    if tls_version == "TLSv1.3":
        scores["tls_version"] = 10
        explanations["tls_version"] = "TLS 1.3 is modern and secure."
    elif tls_version == "TLSv1.2":
        scores["tls_version"] = 7
        explanations["tls_version"] = "TLS 1.2 is acceptable but older."
    else:
        scores["tls_version"] = 2
        explanations["tls_version"] = "Outdated TLS version."

    # ---------------- Cipher Strength ----------------
    cipher = cert["tls_connection"]["cipher"][0]

    if "AES_256" in cipher:
        scores["cipher_strength"] = 10
        explanations["cipher_strength"] = "Strong cipher (AES-256-GCM)."
    elif "AES_128" in cipher:
        scores["cipher_strength"] = 8
        explanations["cipher_strength"] = "Good cipher (AES-128-GCM)."
    else:
        scores["cipher_strength"] = 4
        explanations["cipher_strength"] = "Weaker cipher suite."

    # ---------------- Issuer Trust ----------------
    issuer = cert["certificate"]["issuer"].get("organization", "")

    if issuer in {"Let's Encrypt", "DigiCert", "GlobalSign", "Sectigo"}:
        scores["issuer"] = 9
        explanations["issuer"] = f"Trusted CA: {issuer}"
    else:
        scores["issuer"] = 5
        explanations["issuer"] = f"Unusual CA: {issuer}"

    # ---------------- Key Strength ----------------
    key_type = cert["certificate"]["public_key_type"]
    size = cert["certificate"]["public_key_details"]["key_size"]

    if key_type == "EC":
        scores["key_strength"] = 10
        explanations["key_strength"] = "Modern elliptic-curve key."
    elif key_type == "RSA" and size >= 4096:
        scores["key_strength"] = 9
        explanations["key_strength"] = "Strong RSA key (4096-bit)."
    elif key_type == "RSA" and size == 2048:
        scores["key_strength"] = 7
        explanations["key_strength"] = "RSA-2048 is acceptable but old."
    else:
        scores["key_strength"] = 3
        explanations["key_strength"] = "Weak key size."

    # ---------------- Infrastructure Fingerprint ----------------
    cn = cert["certificate"]["subject"].get("common_name", "")

    if "cpanel" in cn or "plesk" in cn:
        scores["infrastructure"] = 4
        explanations["infrastructure"] = "Shared hosting detected (cPanel)."
    else:
        scores["infrastructure"] = 8
        explanations["infrastructure"] = "No shared hosting fingerprints."

    # ---------------- Operational Reliability ----------------
    days_left = cert["certificate"]["days_left"]
    lifetime = cert["certificate"]["lifetime_days"]

    if days_left < 10:
        scores["operations"] = 3
        explanations["operations"] = "Certificate close to expiry."
    elif lifetime <= 90:
        scores["operations"] = 6
        explanations["operations"] = "90-day certs rely on auto-renew."
    else:
        scores["operations"] = 9
        explanations["operations"] = "Long-lifetime certificate."

    return scores, explanations
