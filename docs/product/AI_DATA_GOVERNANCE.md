# AI and ERP Data Governance

## 1. Purpose

This policy defines how Padiem AI ERP may read ERPNext data, build executive metrics, send minimized context to optional AI providers, store briefing records, and handle test data.

The default rule is conservative:

> ERP data remains inside ERPNext unless a company and authorized user explicitly approve a defined external AI use.

## 2. Data Classes

### Class A — public project information

Examples:

- source code
- public documentation
- synthetic examples
- non-sensitive architecture diagrams

May be committed to the public repository after review.

### Class B — internal operational metadata

Examples:

- non-production site identifiers
- application version
- job status
- test execution metadata
- provider name without credentials

May be stored in controlled systems. Public disclosure requires review.

### Class C — confidential ERP business data

Examples:

- customer and supplier identities
- item names and pricing
- quotations and orders
- inventory quantities
- delivery status
- invoices, receivables, and payments
- company financial totals

Must not be committed to the public repository or used in public CI fixtures.

### Class D — restricted personal, financial, and secret data

Examples:

- employee or customer personal information
- bank and payment account details
- API keys and passwords
- site configuration
- database credentials
- backups
- session cookies

Must never be committed, printed, included in issue bodies, or sent to an AI provider without an approved and documented legal/business basis.

## 3. Source of Truth

- ERPNext database: authoritative business data
- Frappe permissions and User Permissions: authoritative access policy
- metric policy documents: authoritative interpretation rules
- `AI Briefing Run`: authoritative record of a generated briefing
- GitHub: source code and synthetic fixtures only
- external AI provider: temporary processor, never the source of truth

## 4. Data Minimization

Only fields required for the approved feature may be read or transmitted.

Preferred external context:

```json
{
  "company_alias": "company-01",
  "period": "2026-08 MTD",
  "currency": "KRW",
  "metrics": {
    "submitted_sales_total": 12500000,
    "outstanding_receivables_total": 2300000,
    "late_delivery_count": 4
  },
  "warnings": [
    "receivables increased from previous period"
  ]
}
```

Avoid sending:

- company legal name
- customer or supplier names
- contact information
- document numbers unless essential
- item-level detail unless explicitly approved
- free-text notes
- attachments
- credentials
- raw database rows

## 5. Company and User Authorization

Before generating a briefing:

1. identify the requested Company
2. verify that the current user may access that Company
3. verify required DocType permissions
4. apply row-level and User Permission constraints
5. verify the requested period
6. verify AI execution permission
7. verify company external-AI opt-in when applicable

A broad role such as `System Manager` should not automatically mean every external AI data transfer is approved.

## 6. Metric Governance

Each metric requires:

- stable metric ID
- business description
- source DocType and field
- document-status policy
- date policy
- Company policy
- currency policy
- permission policy
- error behavior
- policy version

Example:

```text
Metric: sales.total_invoiced
Source: Sales Invoice.grand_total
Status: submitted-only (docstatus=1)
Period: posting_date within requested range
Company: exact authorized company
Currency: company currency
Failure: null + ERP_QUERY_FAILED, never 0
```

## 7. External AI Approval

External AI remains disabled by default.

Approval requires:

- provider approved for the site
- company opt-in
- authorized role
- defined context allowlist
- documented retention and deletion behavior
- cost limit
- approved secret storage
- audit logging
- staging verification with synthetic data

The current DeepSeek implementation must not be activated against real ERP data until #137 and #140 are completed.

## 8. Provider Secrets

Allowed storage:

- environment variables
- Frappe Password fields with restricted access
- approved secret manager

Prohibited:

- source files
- `.env` commits
- issue or PR text
- screenshots
- test fixtures
- normal application logs
- API responses

Configuration status APIs may report only key presence, never the key value.

## 9. Prompt and Context Handling

Every prompt-producing feature must record:

- prompt/template version
- context policy version
- schema version when structured output is used
- whether external transfer occurred
- provider and model
- context hash

Prompt construction must not silently append unrestricted ERP objects.

## 10. Output Handling

AI output is untrusted until validated.

- Human-readable summaries must be clearly identified as AI-assisted.
- Structured output must pass server-side schema validation.
- AI output cannot directly create, submit, cancel, or delete ERP documents in the first version.
- Recommendations must link to source metrics or ERP records where possible.
- Raw invalid model output is restricted to authorized technical review.

## 11. Briefing Records

`AI Briefing Run` should store enough information to audit a result without duplicating the entire ERP database.

Store:

- Company, period, currency
- user and timestamps
- policy/prompt/schema versions
- metric values and statuses
- minimized snapshot or reference
- provider execution metadata
- summary, warnings, and errors

Do not store unnecessary raw personal or financial records.

## 12. Retention

Retention values must be decided before production. Suggested starting points for discussion:

| Data | Candidate retention |
|---|---:|
| application logs without ERP content | 30–90 days |
| provider execution metadata | 1 year |
| briefing runs | aligned with internal management-report policy |
| raw failed AI output | shortest practical period |
| staging fixtures | deleted after test unless synthetic |
| secrets | rotated and revoked, not archived in Git |

These are placeholders, not final legal requirements.

## 13. Test Data

Public tests and CI must use:

- synthetic companies
- synthetic customers and suppliers
- non-real document numbers
- fictitious financial values
- generated Korean business text

Anonymization must prevent practical re-identification. Simple name replacement is insufficient if unique document numbers, phone numbers, amounts, or timestamps remain linked.

## 14. Logging

Application logs may include:

- run ID
- provider name
- status
- safe error code
- latency
- token count

Application logs must not include:

- API keys
- database passwords
- full ERP context
- personal information
- raw provider request headers
- unrestricted provider response bodies

## 15. Incident Response

### Secret exposure

1. revoke and rotate the secret
2. stop affected provider access
3. inspect Git, logs, issues, and artifacts
4. document affected period and systems
5. remove exposed material where feasible
6. add a prevention control

### ERP data sent without approval

1. disable external AI
2. preserve audit evidence
3. identify company, user, provider, fields, and time
4. follow contractual and legal incident procedures
5. request provider deletion where applicable
6. review context policy and permissions

### Cross-company exposure

1. disable the briefing endpoint if needed
2. identify affected metrics and users
3. preserve query and audit evidence
4. correct Company and row-level filters
5. run restricted-user regression tests
6. document remediation before re-enabling

## 16. Repository Rules

Never commit:

- production data
- customer exports
- bench `sites/`
- database dumps
- backups
- `site_config.json`
- `.env`
- credentials
- cookies
- generated provider payloads containing ERP data

## 17. Linked Issues

- #134
- #135
- #136
- #137
- #139
- #140
- #145
