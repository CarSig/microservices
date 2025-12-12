from fastapi import APIRouter, HTTPException
import ssl
import socket
from datetime import datetime, timezone

from cryptography import x509
from cryptography.x509 import (
    ExtensionOID,
    NameOID,
    AuthorityInformationAccessOID,
)
from cryptography.hazmat.primitives.asymmetric import rsa, ec, ed25519
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import ObjectIdentifier
SCT_OID = ObjectIdentifier("1.3.6.1.4.1.11129.2.4.2")


router = APIRouter(prefix="/certificates", tags=["certificates"])


# ------------------------------------------
# TLS CONNECTION + CERTIFICATE FETCH
# ------------------------------------------
def fetch_connection_and_cert(domain: str):
    ctx = ssl.create_default_context()

    # Always use port 443
    sock = socket.create_connection((domain, 443), timeout=5)
    ssock = ctx.wrap_socket(sock, server_hostname=domain)

    # TLS connection data
    tls_info = {
        "tls_version": ssock.version(),
        "cipher": ssock.cipher(),  # (cipher_name, protocol, key_size)
        "alpn": ssock.selected_alpn_protocol(),
        "shared_ciphers": ssock.shared_ciphers(),
        "compression": ssock.compression(),
        "session_reused": ssock.session_reused,
        "server_hostname": ssock.server_hostname,
    }

    cert_bin = ssock.getpeercert(binary_form=True)
    cert = x509.load_der_x509_certificate(cert_bin)

    return cert, tls_info


# ------------------------------------------
# HELPERS
# ------------------------------------------
def _parse_name(name: x509.Name) -> dict:
    """
    Convert x509.Name into a dict with nice keys.
    """
    mapping = {
        NameOID.COMMON_NAME: "common_name",
        NameOID.ORGANIZATION_NAME: "organization",
        NameOID.ORGANIZATIONAL_UNIT_NAME: "organizational_unit",
        NameOID.COUNTRY_NAME: "country",
        NameOID.STATE_OR_PROVINCE_NAME: "state",
        NameOID.LOCALITY_NAME: "locality",
        NameOID.STREET_ADDRESS: "street",
        NameOID.POSTAL_CODE: "postal_code",
        NameOID.EMAIL_ADDRESS: "email",
    }

    result = {}
    for attr in name:
        key = mapping.get(attr.oid, attr.oid._name)
        # If there are duplicates, last one wins – good enough here
        result[key] = attr.value
    return result


def _safe_utc(dt: datetime) -> datetime:
    """
    Ensure datetime is timezone-aware (UTC).
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


# ------------------------------------------
# PARSE CERTIFICATE FULLY (CLEAN JSON)
# ------------------------------------------
def parse_full_cert(cert: x509.Certificate) -> dict:
    now = datetime.now(timezone.utc)

    subject = _parse_name(cert.subject)
    issuer = _parse_name(cert.issuer)

    # ---- Public key details ----
    pk = cert.public_key()
    if isinstance(pk, rsa.RSAPublicKey):
        key_type = "RSA"
        key_info = {
            "key_size": pk.key_size,
            "public_exponent": pk.public_numbers().e,
            "modulus_bits": pk.public_numbers().n.bit_length(),
        }
    elif isinstance(pk, ec.EllipticCurvePublicKey):
        key_type = "EC"
        key_info = {
            "curve": pk.curve.name,
            "key_size": pk.key_size,
        }
    elif isinstance(pk, ed25519.Ed25519PublicKey):
        key_type = "ED25519"
        key_info = {
            "key_size": 256,
        }
    else:
        key_type = "Unknown"
        key_info = {}

    # ---- Signature ----
    sig_algo = cert.signature_algorithm_oid._name
    sig_hash = None
    if isinstance(cert.signature_hash_algorithm, hashes.HashAlgorithm):
        sig_hash = cert.signature_hash_algorithm.name

    # ---- SAN (clean) ----
    san_dns = []
    san_ip = []
    san_uri = []
    san_email = []

    try:
        san = cert.extensions.get_extension_for_oid(
            ExtensionOID.SUBJECT_ALTERNATIVE_NAME
        ).value

        for item in san:
            if isinstance(item, x509.DNSName):
                san_dns.append(item.value)
            elif isinstance(item, x509.IPAddress):
                san_ip.append(str(item.value))
            elif isinstance(item, x509.UniformResourceIdentifier):
                san_uri.append(item.value)
            elif isinstance(item, x509.RFC822Name):
                san_email.append(item.value)
            else:
                # ignore other exotic types for now
                pass
    except x509.ExtensionNotFound:
        pass

    # ---- Key Usage ----
    # ---- Key Usage ----
    key_usage = None
    try:
        ku = cert.extensions.get_extension_for_oid(
            ExtensionOID.KEY_USAGE
        ).value

        key_usage = {
            "digital_signature": ku.digital_signature,
            "content_commitment": ku.content_commitment,
            "key_encipherment": ku.key_encipherment,
            "data_encipherment": ku.data_encipherment,
            "key_agreement": ku.key_agreement,
            "key_cert_sign": ku.key_cert_sign,
            "crl_sign": ku.crl_sign,
        }

        # Only accessible when key_agreement=True
        if ku.key_agreement:
            key_usage["encipher_only"] = ku.encipher_only
            key_usage["decipher_only"] = ku.decipher_only
        else:
            key_usage["encipher_only"] = None
            key_usage["decipher_only"] = None

    except Exception:
        key_usage = None


    # ---- Extended Key Usage ----
    extended_key_usage = None
    try:
        eku = cert.extensions.get_extension_for_oid(
            ExtensionOID.EXTENDED_KEY_USAGE
        ).value
        extended_key_usage = [oid._name for oid in eku]
    except x509.ExtensionNotFound:
        pass

    # ---- Basic Constraints ----
    basic_constraints = None
    try:
        bc = cert.extensions.get_extension_for_oid(
            ExtensionOID.BASIC_CONSTRAINTS
        ).value
        basic_constraints = {
            "ca": bc.ca,
            "path_length": bc.path_length,
        }
    except x509.ExtensionNotFound:
        pass

    # ---- AIA: OCSP + Issuer URLs ----
    ocsp_urls = []
    issuer_urls = []
    try:
        aia = cert.extensions.get_extension_for_oid(
            ExtensionOID.AUTHORITY_INFORMATION_ACCESS
        ).value

        for desc in aia:
            if desc.access_method == AuthorityInformationAccessOID.OCSP:
                ocsp_urls.append(desc.access_location.value)
            elif desc.access_method == AuthorityInformationAccessOID.CA_ISSUERS:
                issuer_urls.append(desc.access_location.value)
    except x509.ExtensionNotFound:
        pass

    # ---- CRL Distribution Points ----
    crl_urls = []
    try:
        crl_ext = cert.extensions.get_extension_for_oid(
            ExtensionOID.CRL_DISTRIBUTION_POINTS
        ).value

        for dp in crl_ext:
            if dp.full_name:
                for name in dp.full_name:
                    crl_urls.append(name.value)
    except x509.ExtensionNotFound:
        pass

    # ---- Certificate Policies ----
    cert_policies = []
    try:
        policies = cert.extensions.get_extension_for_oid(
            ExtensionOID.CERTIFICATE_POLICIES
        ).value
        for p in policies:
            cert_policies.append(str(p.policy_identifier.dotted_string))
    except x509.ExtensionNotFound:
        pass


    # ---- Signed Certificate Timestamps (SCTs) ----
    SCT_OID = ObjectIdentifier("1.3.6.1.4.1.11129.2.4.2")
    scts = []
    try:
        sct_ext = cert.extensions.get_extension_for_oid(SCT_OID).value
        # New cryptography returns an iterable of SCT objects
        for sct in sct_ext:
            entry = {
                "version": getattr(sct, "version", None),
                "log_id": sct.log_id.hex() if hasattr(sct, "log_id") else None,
                "timestamp": sct.timestamp.isoformat() if hasattr(sct, "timestamp") else None,
                "hash_algorithm": getattr(getattr(sct, "hash_algorithm", None), "name", None),
                "signature_algorithm": getattr(getattr(sct, "signature_algorithm", None), "name", None),
            }
            scts.append(entry)
    except x509.ExtensionNotFound:
        scts = []

    # ---- Validity window ----
    not_before = _safe_utc(cert.not_valid_before)
    not_after = _safe_utc(cert.not_valid_after)
    days_left = (not_after - now).days
    lifetime_days = (not_after - not_before).days
    lifetime_used_pct = round(
        ((now - not_before).total_seconds() /
         (not_after - not_before).total_seconds()) * 100,
        2,
    ) if lifetime_days > 0 else None

    # ---- Build final dict ----
    return {
        # serial as string to avoid JS precision issues
        "serial_number": str(cert.serial_number),
        "version": cert.version.name,

        "subject": subject,
        "issuer": issuer,

        "public_key_type": key_type,
        "public_key_details": key_info,

        "signature_algorithm": sig_algo,
        "signature_hash": sig_hash,

        "not_before": not_before.isoformat(),
        "not_after": not_after.isoformat(),
        "days_left": days_left,
        "lifetime_days": lifetime_days,
        "lifetime_used_percent": lifetime_used_pct,

        "is_self_signed": (cert.issuer == cert.subject),

        "subject_alternative_name": {
            "dns": san_dns,
            "ip": san_ip,
            "uri": san_uri,
            "email": san_email,
        },

        "key_usage": key_usage,
        "extended_key_usage": extended_key_usage,
        "basic_constraints": basic_constraints,

        "ocsp_urls": ocsp_urls,
        "issuer_urls": issuer_urls,
        "crl_urls": crl_urls,
        "certificate_policies": cert_policies,
        "signed_certificate_timestamps": scts,
    }


# ------------------------------------------
# PUBLIC FUNCTION – used by router
# ------------------------------------------
def inspect_domain(domain: str) -> dict:
    cert, tls_info = fetch_connection_and_cert(domain)
    parsed = parse_full_cert(cert)

    return {
        "domain": domain,
        "success": True,
        "certificate": parsed,
        "tls_connection": tls_info,
    }


