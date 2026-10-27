import hashlib
import hmac
import re
from typing import Iterable

_FORBIDDEN_SQL = re.compile(
    r"\b(INSERT|UPDATE|DELETE|MERGE|DROP|ALTER|CREATE|TRUNCATE|CALL|EXEC|COPY|PUT|GET|REMOVE|GRANT|REVOKE|USE|BEGIN|COMMIT|ROLLBACK)\b",
    re.IGNORECASE,
)
_SENSITIVE_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b(?:patient|member)[-_ ]?id\s*[:=]\s*\S+", re.I),
    re.compile(r"\bdate\s+of\s+birth\s*[:=]\s*\S+", re.I),
]


def validate_text(value: str, *, max_length: int = 2000) -> str:
    if not isinstance(value, str):
        raise ValueError("Input must be text.")
    value = value.strip()
    if not value:
        raise ValueError("Input must not be empty.")
    if len(value) > max_length:
        raise ValueError(f"Input exceeds the {max_length}-character limit.")
    if any(ord(ch) < 32 and ch not in "\t\n\r" for ch in value):
        raise ValueError("Input contains unsupported control characters.")
    return value


def detect_sensitive_markers(value: str) -> bool:
    """Heuristic demo check only; not a DLP/PHI detector."""
    return any(pattern.search(value) for pattern in _SENSITIVE_PATTERNS)


def tokenize_identifier(identifier: str, secret: str) -> str:
    """Stable keyed pseudonym for a demo; never log the original identifier."""
    identifier = validate_text(identifier, max_length=256)
    if not secret or len(secret.encode("utf-8")) < 32:
        raise ValueError("Tokenization secret must be at least 32 bytes.")
    digest = hmac.new(secret.encode("utf-8"), identifier.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"tok_{digest}"


def validate_readonly_sql(sql: str, allowed_relations: Iterable[str]) -> str:
    """Basic demo guard; enforce actual authorization in Snowflake too."""
    sql = validate_text(sql, max_length=10000)
    normalized = sql.strip().rstrip(";").strip()
    if "--" in normalized or "/*" in normalized or "*/" in normalized:
        raise ValueError("SQL comments are not permitted.")
    if ";" in normalized:
        raise ValueError("Only one SQL statement is permitted.")
    if not re.match(r"^(SELECT|WITH)\b", normalized, re.IGNORECASE):
        raise ValueError("Only SELECT queries are permitted.")
    if _FORBIDDEN_SQL.search(normalized):
        raise ValueError("SQL contains a forbidden operation.")
    relations = {item.upper() for item in allowed_relations}
    referenced = re.findall(
        r"\b(?:FROM|JOIN)\s+([A-Za-z_][A-Za-z0-9_$]*(?:\.[A-Za-z_][A-Za-z0-9_$]*)?)",
        normalized,
        flags=re.IGNORECASE,
    )
    if not referenced:
        raise ValueError("Query must reference an approved relation.")
    for relation in referenced:
        if relation.upper() not in relations:
            raise ValueError(f"Relation is not approved: {relation}")
    return normalized
