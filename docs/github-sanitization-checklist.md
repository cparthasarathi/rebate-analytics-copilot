# GitHub sanitization checklist

- [ ] Use a private repository until review is complete.
- [ ] Remove customer/client names, personal names, emails, phone numbers, tenant/subscription/account IDs, internal hostnames, IPs and environment URLs.
- [ ] Search for API keys, bearer tokens, passwords, private keys, certificates and connection strings.
- [ ] Ensure no real extracts, logs, screenshots, presentations or customer files are committed.
- [ ] Confirm examples are synthetic and contain no person/patient-level data.
- [ ] Confirm no identifiers, clinical details, diagnoses, prescriptions or dosage data are present.
- [ ] Run a local secret scan and enable GitHub secret scanning + push protection where available.
- [ ] Check Git history as well as the working tree; rotate any exposed secret and clean history.
- [ ] Keep `.env.example` placeholder-only; store secrets in Azure Key Vault / GitHub Actions Secrets.
- [ ] Run tests and review dependencies.
- [ ] Ask Security/Privacy to review the architecture and grants before connecting real data.
- [ ] Do not present this starter as evidence of production compliance.
