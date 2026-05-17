# Data Security Rules

## Early Testing Phase Policy

During early testing, most documentation and sample data **may be committed** to the repository.
This is acceptable because:
- The repository is private
- We are in development, not production
- Sharing context across the team is more valuable than secrecy at this stage

## NEVER Commit These

The following must **never** be committed to the repository, regardless of phase:

| Category | Examples |
|----------|----------|
| API keys | AI provider keys, cloud API keys, service credentials |
| Passwords | Database passwords, admin passwords, service passwords |
| Environment files | `.env`, `.env.local`, `.env.production` |
| Real customer data | Actual customer names, contact info, transaction data |
| Real accounting data | Actual financial statements, invoices, receipts |
| Bank/card data | Bank account numbers, credit card numbers, account credentials |
| Server credentials | SSH keys, server IPs, admin panels, cloud console credentials |
| Certificates | SSL certificates, signing keys, authentication certificates |

## What TO Commit

- Documentation (all docs/ files)
- Sample/fake data for testing
- Configuration templates (`.env.example`)
- Source code
- Prompts and templates
- Infrastructure-as-code (without secrets)

## .gitignore Rules

Always maintain a `.gitignore` that excludes:
```
.env
.env.*
*.key
*.pem
*.p12
secrets/
credentials/
*.credential
```

## If You Accidentally Commit a Secret

1. Immediately rotate/revoke the secret
2. Remove it from git history (not just the latest commit)
3. Force push (if repository is private and no one else has pulled)
4. Document what happened
