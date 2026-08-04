# Release Gates

This document defines evidence required before Padiem AI ERP moves between development stages.

## Gate A — Static Development Ready

Required:

- Python compile passes
- unit tests pass
- no secrets or real customer data
- default provider remains `mock`
- external AI calls are not required
- documentation matches the current code

Current status: substantially met.

## Gate B — Installable ERPNext App

Required:

- supported Frappe/ERPNext/Python/database versions declared
- `bench get-app` or approved equivalent succeeds
- `install-app` succeeds
- canonical imports succeed
- `bench migrate` succeeds
- uninstall or rollback procedure is verified
- installation commands are added to README

Blocking issues:

- #131
- #133

## Gate C — Runtime Smoke Ready

Required:

- API methods run in a real site context
- `/ceo_briefing` renders or returns controlled errors
- mock provider is reported accurately
- no external AI call occurs
- authorized and denied permission paths are tested
- exact commit SHA and environment versions are recorded

Blocking issue:

- #130

## Gate D — Internal Read-Only Pilot

Required:

- Company scope is explicit
- User Permission and row restrictions are applied
- cross-company aggregate leakage test passes
- query failure is distinct from zero
- document status, period, currency, timezone, and freshness policies are implemented
- integration tests run on a supported ERPNext version
- only synthetic or approved anonymized pilot data is used

Blocking issues:

- #134
- #135
- #136
- #141

## Gate E — Persistent Briefing Pilot

Required:

- `AI Briefing Run` is stored
- completed runs are protected from normal editing
- run history is permission-aware
- data snapshot strategy and retention are documented
- job status and retry behavior are visible
- duplicate requests do not duplicate work

Blocking issues:

- #138
- #139

## Gate F — External AI Staging

Required:

- company opt-in
- authorized user/role
- provider and model settings
- secure secret storage
- field allowlist and redaction
- no production data in first live test
- JSON Schema validation
- token, cost, timeout, and retry limits
- external call metadata and audit record
- incident shutdown procedure

Blocking issues:

- #137
- #140

## Gate G — Operations-Ready Release

Required:

- all prior applicable gates pass
- README installation and support matrix are verified
- license and security disclosure are clear
- required checks protect `main`
- release tag and changelog exist
- migration and rollback are documented
- monitoring, backup, and restore responsibilities are assigned
- executive UI clearly shows company, period, currency, freshness, provider, and errors
- source ERP drill-down respects permissions

Blocking issues:

- #142
- #143
- #144
- #145

## Evidence Format

Every gate report must include:

```text
Gate:
Status: PASS / FAIL / PARTIAL / BLOCKED
Repository:
Branch:
Commit SHA:
Environment:
ERPNext version:
Frappe version:
Python version:
Database:
Installed apps:
Data classification:
External AI call: yes/no
Commands:
Tests:
Permission scenarios:
Migration impact:
Rollback evidence:
Known limitations:
Linked issues and PRs:
```

## Prohibited Release Claims

Do not call a release production-ready when any of the following is true:

- no real bench/site test
- install path is unverified
- Company isolation is unverified
- query errors can appear as zero
- record-state policy is incomplete
- external AI data policy is absent
- secrets or real ERP data are used in public CI
- rollback has not been tested
- static validation is the only evidence
