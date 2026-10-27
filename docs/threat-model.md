# Threat model

| Threat | Starter mitigation | Required production control |
|---|---|---|
| Secret committed | `.gitignore`, placeholder `.env.example` | GitHub secret scanning/push protection, rotation, Key Vault |
| Sensitive identifier in prompt | Heuristic marker check | DLP/classifier, policy enforcement, red-team tests |
| SQL injection/destructive SQL | Conservative read-only guard | Native parser/semantic API, least-privilege Snowflake role |
| Restricted-schema query | Relation allow-list | Snowflake grants and policies; never rely on app validation alone |
| Malformed/oversized file | Name/extension/size validation | Malware scan, schema validation, quarantine, reconciliation |
| Duplicate/replayed ingestion | SHA-256 manifest helper | Idempotent keys, watermark transactionality, merge strategy, audit tables |
| Prompt injection in retrieved docs | Not implemented | Curated corpus, provenance, instruction/data separation, output validation |
| Clinical/dosage question | Not implemented beyond basic checks | Explicit out-of-scope policy and approved escalation path |
| Over-broad access | Example grant pattern | Object-level grants, row-access tests, periodic access review |

Regex checks are not reliable PHI detection. HMAC tokens are pseudonymous, not anonymous. SQL regex validation is not a complete SQL parser and may be bypassed. Repository code alone does not establish compliance.
