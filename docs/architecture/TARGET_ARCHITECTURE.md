# Target Architecture

## 1. Objective

Padiem AI ERP should remain an ERPNext application. ERP permissions, Company boundaries, business document states, and audit records are authoritative. AI may summarize, explain, draft, or recommend; it must not bypass ERP controls.

## 2. Target System

```text
Authenticated ERPNext user
        │
        ▼
CEO Briefing UI / API
        │
        ├── Company and period authorization
        ├── request validation
        └── idempotency key
        │
        ▼
Briefing Orchestrator
        │
        ├── permission-aware ERP metric service
        ├── metric policy registry
        ├── error/freshness model
        └── AI Briefing Run record
        │
        ▼
Frappe background job
        │
        ├── deterministic briefing
        ├── optional approved AI provider
        ├── schema validation
        └── execution metadata
        │
        ▼
Stored result + audit event
        │
        ▼
UI, comparison, and ERP drill-down
```

## 3. Boundaries

### 3.1 ERPNext/Frappe core

- Must not be modified.
- Standard hooks, DocTypes, permissions, background jobs, and APIs should be used.
- Core patches are outside this project.

### 3.2 `padiem_ai` application

Owns:

- briefing policies
- application DocTypes
- provider abstraction
- ERP read-only metric services
- application permissions
- background jobs
- API contracts
- audit and execution metadata
- product UI

Does not own:

- ERPNext accounting correctness
- tax or payroll compliance
- ERPNext core permissions
- external provider infrastructure

### 3.3 ERP data layer

The data layer must:

- accept an explicit authorized Company scope
- respect User Permission and role constraints
- apply document-status and date policies
- return value plus status and provenance
- never convert query failure to a valid business zero
- expose only fields needed by the product

Recommended metric result:

```json
{
  "metric": "sales.total_invoiced",
  "value": 12500000,
  "status": "ok",
  "company": "Example Co",
  "currency": "KRW",
  "period": {
    "from": "2026-08-01",
    "to": "2026-08-04"
  },
  "source": {
    "doctype": "Sales Invoice",
    "policy": "submitted-only",
    "policy_version": "1"
  },
  "generated_at": "2026-08-04T12:00:00+09:00"
}
```

Failure example:

```json
{
  "metric": "sales.total_invoiced",
  "value": null,
  "status": "error",
  "error_code": "ERP_QUERY_FAILED"
}
```

### 3.4 Permission boundary

A DocType-level permission check is necessary but not sufficient.

Every query must also constrain:

- Company
- user-permitted companies
- applicable User Permission values
- relevant business status
- fiscal/date range

Multiple-company aggregation requires a separate explicit authorization path.

### 3.5 Briefing orchestrator

Responsibilities:

- validate company and period
- load metric policy version
- request permission-aware metrics
- determine `success`, `partial`, or `failed`
- create `AI Briefing Run`
- enqueue generation job
- avoid duplicate jobs
- return a stable run identifier

The orchestrator should not contain provider-specific HTTP code.

### 3.6 Background execution

External AI calls must not run synchronously in the normal page request.

The job layer should provide:

- idempotency
- timeout
- limited retry with backoff
- circuit breaker
- cancellation
- provider request ID
- token and cost metadata
- structured error categories

### 3.7 AI provider layer

Provider interface should return both output and execution metadata.

```python
ProviderResult(
    output=...,
    provider="deepseek",
    model="deepseek-chat",
    external_call=True,
    request_id="...",
    latency_ms=1234,
    token_usage={...},
    cost_estimate=0.0,
)
```

Provider rules:

- `mock` remains default.
- Real providers require site and company approval.
- Secrets are never returned by config APIs.
- External context is minimized and redacted.
- Health checks do not make billable calls unless explicitly named as live checks.
- Provider failures do not corrupt the ERP metric snapshot.

### 3.8 Structured output

For machine-consumed output:

- define versioned JSON Schema
- request compatible response mode where available
- validate server-side
- reject invalid values and unknown critical fields
- do not expose raw model output to ordinary users
- cap response length
- record schema version in `AI Briefing Run`

### 3.9 `AI Briefing Run` DocType

Recommended fields:

- name / run ID
- company
- period from/to
- currency
- requested by
- requested/completed timestamps
- status
- data freshness
- metric policy version
- prompt version
- schema version
- context hash
- minimized snapshot or snapshot reference
- provider and model
- external call boolean
- request/response IDs
- latency and token usage
- estimated cost
- summary and warnings
- errors
- retry/supersession linkage

Permissions:

- executives may read approved company runs
- operators may create approved runs
- administrators may inspect technical errors
- ordinary users cannot edit completed audit records

### 3.10 UI

The UI should show:

- company
- period
- currency
- generated time and data freshness
- provider and external-call status
- briefing run status
- metric errors separately from zeros
- comparison with prior period
- drill-down links to permitted ERP records
- human-approved follow-up actions

The UI must not provide autonomous write execution in the first version.

## 4. Deployment Environments

### Development

- synthetic data
- mock provider
- local bench
- unrestricted debugging without secrets

### Integration / CI

- disposable site
- generated fixtures
- no production credentials
- app install/migrate/uninstall tests
- restricted-user permission tests

### Staging

- anonymized representative data
- access-controlled site
- optional approved live provider key
- cost limits
- audit enabled

### Production

Allowed only after release gates pass.

- isolated secrets
- backups and restore proof
- monitoring and alerting
- company and role policy
- external AI opt-in
- rollback procedure

## 5. Target Module Layout

```text
padiem_ai/padiem_ai/
├── ai/
│   ├── config/
│   ├── providers/
│   ├── schemas/
│   └── policy/
├── api/
├── briefing/
│   ├── orchestrator.py
│   ├── deterministic.py
│   ├── jobs.py
│   └── contracts.py
├── erp/
│   ├── metrics/
│   ├── permissions.py
│   ├── policies.py
│   └── contracts.py
├── padiem_ai/doctype/
│   ├── ai_briefing_run/
│   └── ai_settings/
└── www/ or Desk page
```

This is a target direction, not an instruction to restructure everything in one change.

## 6. Migration Strategy

1. Prove current installation and runtime.
2. Add explicit metric contracts without changing public keys immediately.
3. Add Company and permission-aware filters.
4. Add error and freshness metadata.
5. Introduce `AI Briefing Run` behind the mock path.
6. Move generation to background jobs.
7. Add site-level AI settings and external-data policy.
8. Add schema-validated staging provider.
9. Improve UI and drill-down.

## 7. Architectural Decisions Required

Before implementation, create or update ADRs for:

- supported ERPNext/Frappe versions
- repository packaging layout
- company authorization model
- metric contract versioning
- briefing snapshot storage
- provider secret storage
- external-data minimization
- background queue selection
- retention periods
- license ownership

## 8. Linked Issues

- #133–#141
- #145
