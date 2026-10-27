# Governed Rebate Analytics & Copilot — GitHub Starter

A sanitized starter repository based on the uploaded case-study solution. It contains no client credentials, patient data, real identifiers, or environment-specific endpoints.

## Case-study-aligned design
- Azure Data Factory orchestrates extraction and landing into ADLS Gen2.
- Snowflake hosts separate `BRONZE`, `SILVER`, `GOLD`, and `RESTRICTED_DATA` schemas.
- A tokenization boundary keeps direct identifiers out of shared analytical layers.
- Copilot/reporting consumption is restricted to approved commercial rebate metrics.
- RAG is limited to approved business glossary/policy content; clinical/dosage questions are out of scope.
- The POC is deliberately narrow. Cloud resources and source connectors are placeholders, not deployed services.

## Security and sanitization
- Never commit `.env`, credentials, keys, tokens, connection strings, source extracts, logs, or real data.
- Use synthetic data only. Keep the repository private until reviewed.
- The HMAC tokenization helper is a demo, not a substitute for a reviewed production tokenization service.
- Regex-based sensitive-data checks and SQL validation are defense-in-depth only, not complete DLP or SQL parsing.
- Enforce access in Snowflake with least-privilege grants and policies; application checks alone are insufficient.

## Layout
```text
app/                  FastAPI demo, config, security and ingestion helpers
sql/                  Illustrative Snowflake schema, grants and gold model
tests/                Unit tests
docs/                 Architecture, threat model, GitHub sanitization checklist
.github/workflows/    Test workflow
.env.example          Placeholder configuration only
Dockerfile            Minimal container for the demo API
```

## Quick start
Python 3.11+ recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.api:app --reload
```

Visit `http://127.0.0.1:8000/health`. Demo endpoints do not connect to Azure or Snowflake.

Run tests: `pytest -q`

## Before connecting real services
1. Create a private GitHub repository.
2. Review `docs/github-sanitization-checklist.md`.
3. Enable GitHub secret scanning and push protection where available.
4. Store real secrets in Azure Key Vault / GitHub Actions Secrets, never source files.
5. Implement private networking, identity federation, audit logging, retention and environment-specific controls.
6. Have Security/Privacy and the Snowflake administrator review the grants and tokenization design.

## Not implemented
Real ADF pipelines, source-system connectors, ADLS provisioning, Event Grid/Snowpipe deployment, Snowflake authentication, Cortex APIs, Power BI, Entra ID, production key management and clinical-data processing are intentionally not implemented.
