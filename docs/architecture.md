# Architecture (sanitized)

```text
Approved source systems
  ├─ SaaS APIs (incremental watermark)
  ├─ Contract/ERP batch extracts
  ├─ Third-party SFTP drops (scheduled polling)
  └─ Manual spreadsheet uploads (validation)
            |
            v
Azure Data Factory -> ADLS Gen2 landing (source/date partitioning, audit copy)
            |
            +--> Restricted raw container (tight ACL, approved short retention)
            |        |
            |        v
            |   Tokenization boundary
            |
            v
Snowflake ingestion (COPY INTO / Snowpipe where appropriate)
            |
            v
BRONZE -> SILVER -> GOLD
 raw       conformed    approved commercial model / secure views
                       |
                       +--> BI reporting
                       +--> Copilot / text-to-SQL over governed semantic model
                                - approved SQL only
                                - execute under scoped user/service role
                                - no access to RESTRICTED_DATA
                                - glossary/policy RAG only

RESTRICTED_DATA:
- Separate access boundary for identifier crosswalks.
- No grants to copilot or BI identities.
- Never index this schema into the RAG corpus.
```

## Decisions carried forward from the case study
- Azure is the cloud backbone; Snowflake remains the analytical platform.
- Prove a small number of ingestion patterns rather than onboarding every source in the POC.
- Keep the fact table at claim-line/contract-version/period grain for auditable variance analysis.
- Use fixed-precision decimals for monetary values.
- Resolve historical claims against the contract version active at claim time.
- Separate bronze/silver/gold schemas and their access/retention policies.
- Do not promise sub-second real-time reporting where source feeds are batch/manual; report freshness and an `as_of` timestamp.

Python helpers are demonstrators, not cloud controls. Production boundaries require reviewed Entra ID, managed identity, Key Vault, private networking, Snowflake RBAC, row-access policies, storage ACLs, logging and retention.
