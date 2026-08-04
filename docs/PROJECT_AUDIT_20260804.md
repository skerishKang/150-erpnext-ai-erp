# Padiem AI ERP Project Audit

- Audit date: 2026-08-04
- Repository: `skerishKang/150-erpnext-ai-erp`
- Default branch: `main`
- Audit baseline: `9d9b62266c40617969bfc76e0698d309cd2eb8b1`
- Repository visibility: public
- Review method: static repository, commit, issue, PR, workflow, and documentation review
- Runtime code changed by this audit: no
- External AI calls made by this audit: no

## 1. Executive Summary

Padiem AI ERP is an ERPNext/Frappe extension project for Korean SMEs. The implemented runtime is currently concentrated on one vertical slice:

```text
ERPNext read-only data
→ domain summaries
→ deterministic CEO briefing
→ AI provider registry
→ API and /ceo_briefing page
```

The project is beyond documentation-only planning. It has application code, modular read-only summaries, a provider abstraction, conservative DeepSeek configuration guards, a minimal web route, 28 recorded unit tests, and a GitHub Actions static validation workflow.

The project is not production-ready. The largest gap is not general code quality; it is the absence of evidence from an actual Frappe/ERPNext bench and site. Installation, migration, route loading, real permissions, aggregate query behavior, and restricted-user behavior remain unverified.

Current classification:

> **Well-governed early ERPNext app MVP with safe AI defaults, but without real runtime proof.**

## 2. Product Scope

### Current product identity

- ERP product built on ERPNext
- AI embedded in ERP workflows
- Primary market: Korean SMEs
- Initial workflow focus: quotations, inventory, delivery, receivables, and reporting
- Implemented first slice: CEO daily briefing

### Current non-goals

- generic chatbot wrapper
- generic automation platform
- ERPNext/Frappe core modification
- full accounting or tax filing
- payroll and VAT filing
- autonomous ERP execution without human approval

## 3. Current Architecture

### Application package

- `padiem_ai/setup.py`
- `padiem_ai/requirements.txt`
- `padiem_ai/padiem_ai/hooks.py`

### Runtime modules

- `ai/`: provider registry, configuration guards, providers
- `api/`: whitelisted API endpoints
- `briefing/`: deterministic briefing generator
- `erp/`: read-only ERP summary functions
- `www/`: web controller and template

### Validation

- Python compile in GitHub Actions
- standard-library `unittest`
- Frappe stub for unit tests
- runtime smoke guide

## 4. Strengths

### 4.1 Safe AI defaults

- `mock` is the active default provider.
- External AI requires a master switch, provider switch, and credentials.
- DeepSeek URL validation blocks HTTP, localhost, private IP ranges, metadata addresses, unexpected ports, query strings, fragments, and unapproved custom hosts.
- Provider health checks do not make live calls.

### 4.2 Development governance

- issue-first work decomposition
- feature branches and pull requests
- detailed PR summaries and safety notes
- explicit reporting of whether external AI calls occurred
- static validation and unit tests
- superseded draft PRs closed rather than silently reused

### 4.3 Modularization

- provider implementations split into focused modules
- configuration split into focused modules with compatibility facades
- ERP read-only logic split by domain
- shared permission helper
- bounded list queries

### 4.4 Security awareness

- all briefing DocTypes are checked at the endpoint boundary
- generic exception text is not returned to page users
- duplicated `raw_context` is removed from the briefing object
- secrets and site configuration are ignored by Git

## 5. Critical Findings

## 5.1 No real ERPNext/Frappe runtime evidence

Open issues #130 and #131 correctly identify the missing runtime layer. Unit tests cannot prove:

- app installation
- canonical import paths
- Frappe route loading
- whitelisted API invocation
- MariaDB aggregate behavior
- actual DocType fields
- user permission enforcement
- company isolation
- Jinja rendering
- migration behavior

Priority: P0.

## 5.2 App packaging and installation contract are uncertain

The Python packaging files are below the repository root. A standard `bench get-app <repository-url>` flow may require special handling. The empty `requirements.txt` is read through `split("\n")`, which may produce an invalid empty dependency entry. Runtime guide commands also contain inconsistent package paths.

Tracked by #133.

## 5.3 DocType permission is not sufficient for row-level isolation

The entry point checks read permission for all used DocTypes. Aggregate helpers use database count and sum functions that are not themselves a Frappe permission boundary. A user allowed to read a DocType but restricted to one Company may receive broader aggregate values.

Tracked by #134.

## 5.4 Query errors become numeric zero

Count and sum failures return `0` or `0.0`. This can make a broken query or denied field appear as zero revenue, zero receivables, or zero inventory.

Tracked by #135.

## 5.5 Metric record policy is incomplete

Sales Invoice and Payment Entry use submitted records in key paths. Sales Order, Quotation, Delivery Note, Purchase Order, and Stock Entry still include all records pending a product decision. Period, timezone, fiscal year, and currency metadata are incomplete.

Tracked by #136.

## 5.6 Provider implementation and provider operation are different

DeepSeek client code exists, but the selected provider is a code constant set to `mock`. There is no approved site-level provider selection, company opt-in, role permission, external-data allowlist, or budget policy.

Tracked by #137.

## 5.7 Synchronous external calls would create worker and cost risk

If DeepSeek becomes selected, the current request path can wait up to 30 seconds. This risks Frappe worker occupation, duplicate calls, duplicate cost, and full-request failure.

Tracked by #138.

## 5.8 No persistent briefing run record

A briefing response is not stored as an auditable ERP document. After ERP data changes, the exact briefing previously shown to management cannot be reconstructed reliably.

Tracked by #139.

## 5.9 Structured-output schema is not enforced

`generate_json()` accepts a schema argument but does not use it to constrain or validate output. Invalid JSON is returned as raw model text with a parse flag.

Tracked by #140.

## 5.10 CI is still static and stub-based

The existing workflow is useful but does not test Frappe, ERPNext, MariaDB, app installation, route behavior, migration, or real permissions.

Tracked by #141.

## 5.11 Public repository documentation is incomplete

The README lacks a verified support matrix and installation procedure. App metadata says MIT but a root license file is absent. Security disclosure and release policy are also incomplete.

Tracked by #142 and #143.

## 5.12 Current page is a minimal diagnostic page

The current page does not yet provide company/period/currency context, comparisons, drill-down, run history, stale/partial/error states, or production accessibility.

Tracked by #144.

## 6. Risk Model

| Risk | Current level | Required control |
|---|---:|---|
| App cannot install in bench | High | #131, #133, #130 |
| Cross-company aggregate exposure | Critical | #134 |
| Broken query displayed as zero | Critical | #135 |
| Incorrect record-state totals | High | #136 |
| Unapproved ERP data sent externally | Critical | #137 |
| External call blocks Frappe worker | High | #138 |
| Briefing cannot be audited | High | #139 |
| Invalid AI JSON accepted | High | #140 |
| Regression undetected by stub tests | High | #141 |
| Public users misunderstand readiness | Medium | #142 |
| Repository lifecycle drift | Medium | #143 |
| Executive UI lacks decision context | Medium | #144 |

## 7. Current Allowed Use

Allowed:

- static code review
- mock provider unit testing
- synthetic or anonymized fixtures
- disposable local or staging bench work
- read-only smoke on non-production ERP data
- documentation and architecture work

Not approved:

- production installation
- real customer ERP data
- multi-company deployment
- live DeepSeek with real ERP context
- autonomous ERP changes
- accounting, tax, payroll, or filing decisions
- claims that the project is a finished AI ERP product

## 8. Recommended Order

```text
#131 provision bench
→ #133 verify package/install contract
→ #130 execute runtime smoke
→ #134 enforce company and row permissions
→ #135 introduce metric error model
→ #136 finalize metric policy
→ #141 add integration CI
→ #139 persist briefing runs
→ #138 move execution to background jobs
→ #137 add approved provider/data policy
→ #140 validate structured output and staging provider
→ #144 improve executive UX
```

## 9. Operations-Ready Definition

The first operations-ready release requires all of the following:

- verified installation on declared ERPNext/Frappe versions
- clean migrate and rollback procedure
- authorized and restricted user runtime evidence
- company-isolated aggregate queries
- error, no-data, and real-zero distinction
- explicit company, period, currency, and freshness metadata
- mock as safe default
- external AI opt-in, minimization, audit, and budget controls
- persistent briefing run record
- background job execution
- integration CI and required checks
- release tag, commit SHA, support matrix, and rollback guide

## 10. Linked Program

Overall EPIC: #145.
