from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# -----------------------------------
# TLS Connection Info
# -----------------------------------

class TLSConnectionInfo(BaseModel):
    tls_version: Optional[str]
    cipher: Optional[List[Any]]  # (cipher_name, protocol, key_size)
    alpn: Optional[str]
    shared_ciphers: Optional[List[Any]]
    compression: Optional[str]
    session_reused: Optional[bool]
    server_hostname: Optional[str]


# -----------------------------------
# Certificate Sub-Models
# -----------------------------------

class SubjectAlternativeName(BaseModel):
    dns: List[str]
    ip: List[str]
    uri: List[str]
    email: List[str]


class KeyUsage(BaseModel):
    digital_signature: Optional[bool]
    content_commitment: Optional[bool]
    key_encipherment: Optional[bool]
    data_encipherment: Optional[bool]
    key_agreement: Optional[bool]
    key_cert_sign: Optional[bool]
    crl_sign: Optional[bool]
    encipher_only: Optional[bool]
    decipher_only: Optional[bool]


class BasicConstraints(BaseModel):
    ca: Optional[bool]
    path_length: Optional[int]


class PublicKeyDetails(BaseModel):
    key_size: Optional[int]
    public_exponent: Optional[int] = None
    modulus_bits: Optional[int] = None
    curve: Optional[str] = None


class SignedCertificateTimestamp(BaseModel):
    version: Optional[int]
    log_id: Optional[str]
    timestamp: Optional[str]
    hash_algorithm: Optional[str]
    signature_algorithm: Optional[str]


# -----------------------------------
# Full Certificate Response
# -----------------------------------

class CertificateInfo(BaseModel):
    serial_number: str
    version: str

    subject: Dict[str, str]
    issuer: Dict[str, str]

    public_key_type: str
    public_key_details: PublicKeyDetails

    signature_algorithm: Optional[str]
    signature_hash: Optional[str]

    not_before: str
    not_after: str
    days_left: int
    lifetime_days: int
    lifetime_used_percent: Optional[float]

    is_self_signed: bool

    subject_alternative_name: SubjectAlternativeName

    key_usage: Optional[KeyUsage]
    extended_key_usage: Optional[List[str]]
    basic_constraints: Optional[BasicConstraints]

    ocsp_urls: List[str]
    issuer_urls: List[str]
    crl_urls: List[str]
    certificate_policies: List[str]

    signed_certificate_timestamps: List[SignedCertificateTimestamp]


# -----------------------------------
# Final API Response Model
# -----------------------------------

class CertificateInspectionResponse(BaseModel):
    domain: str
    success: bool = True
    certificate: CertificateInfo
    tls_connection: TLSConnectionInfo




class ScoreResponse(BaseModel):
    domain: str
    scores: dict[str, int]
    overall_score: float
    explanations: dict[str, str]
    raw_certificate: dict[str, Any]

