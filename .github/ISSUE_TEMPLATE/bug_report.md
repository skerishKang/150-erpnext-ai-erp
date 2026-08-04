---
name: Bug report
description: Report a reproducible defect in the ERPNext app, metrics, permissions, AI, or UI
title: "[BUG] "
labels: []
assignees: []
---

## Summary

Describe the defect and the observed business impact.

## Environment

- Repository commit SHA:
- Branch:
- ERPNext version:
- Frappe version:
- Python version:
- Database:
- Browser/OS, if relevant:
- Site type: disposable / staging / production

Do not paste site configuration, credentials, database passwords, cookies, or real customer data.

## Affected area

- [ ] App installation or migration
- [ ] ERP query or metric
- [ ] Permission or Company scope
- [ ] API
- [ ] CEO briefing page
- [ ] AI provider/config
- [ ] Background job
- [ ] Audit record
- [ ] CI or infrastructure
- [ ] Documentation

## Affected DocTypes and Company scope

- DocTypes:
- Requested Company:
- User role:
- User Permission restrictions:
- Multi-company site: yes / no

## Steps to reproduce

1. 
2. 
3. 

## Expected behavior


## Actual behavior


## Metric or data semantics

- Metric ID, if applicable:
- Document status expected:
- Period/date range:
- Currency:
- Expected no-data behavior:
- Was a query failure displayed as zero? yes / no / unknown

## Permission impact

- [ ] Data from another Company may be exposed
- [ ] Restricted user can access data
- [ ] Authorized user is incorrectly denied
- [ ] No permission impact
- Evidence using synthetic or redacted data:

## AI and external-call impact

- Provider:
- External call occurred: yes / no / unknown
- Data classification sent:
- Secret or key exposure suspected: yes / no
- Raw provider output exposed: yes / no

## Logs and evidence

Paste only redacted logs. Include request/run IDs where available.

```text

```

## Reproducibility

- [ ] Every time
- [ ] Intermittent
- [ ] Only in real Frappe runtime
- [ ] Only in unit/stub tests

## Data and migration impact

- Business data changed: yes / no / unknown
- DocType/schema involved:
- Rollback required:
- Backup available:

## Severity

- [ ] P0 — security, cross-company exposure, destructive data issue, or materially false executive metric
- [ ] P1 — core workflow or runtime failure
- [ ] P2 — limited defect or usability problem

## Proposed acceptance criteria

- [ ] Reproduction is converted into a test
- [ ] Authorized and restricted-user behavior is verified
- [ ] No real data or secret is added to the test
- [ ] Runtime result is recorded when applicable
- [ ] Migration and rollback impact is documented
