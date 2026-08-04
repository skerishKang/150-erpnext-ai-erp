## Related issue

Refs #

## Summary

- What changed:
- Why:
- What is intentionally out of scope:

## Changed files

- 

## Risk classification

- [ ] Documentation only
- [ ] ERP read/query behavior
- [ ] Permission or Company scope
- [ ] API contract
- [ ] AI provider or prompt
- [ ] External AI call
- [ ] DocType or migration
- [ ] Background job
- [ ] UI or template
- [ ] Infrastructure or CI

## ERPNext/Frappe environment

- ERPNext version:
- Frappe version:
- Python version:
- Database:
- Site type: none / disposable / staging / production
- `padiem_ai` installed: yes / no / not applicable

## Data safety

- Data used: none / synthetic / anonymized / real
- [ ] No customer or production data is committed
- [ ] No site config, database dump, backup, cookies, or credentials are included
- [ ] Screenshots and logs are checked for identifiers and secrets
- [ ] Public fixtures cannot identify a real person or company

## Permission and Company scope

- Affected DocTypes:
- Requested Company behavior:
- User Permission behavior:
- Authorized-user scenario:
- Restricted-user scenario:
- Multi-company scenario:

- [ ] DocType read permission is not treated as the only aggregate permission boundary
- [ ] Cross-company data exposure was considered
- [ ] Drill-down and API responses respect the same permission scope

## Metric correctness

- Metric IDs affected:
- Document-status policy:
- Period/date policy:
- Currency policy:
- No-data behavior:
- Error behavior:

- [ ] Query failure is not returned as a valid numeric zero
- [ ] Draft, submitted, cancelled, open, and completed records are intentionally handled
- [ ] Company, period, currency, and freshness metadata are preserved where applicable

## AI provider and external data

- Provider:
- Model:
- External call made: yes / no
- Enablement chain:
- Context fields transmitted:
- Redaction/minimization:
- Schema version:
- Token/cost limit:
- Provider request ID recorded: yes / no / not applicable

- [ ] Default provider remains `mock`, or a separately approved issue changes it
- [ ] API key values are not logged or returned
- [ ] Real ERP data was not used for an unapproved live-provider test
- [ ] Raw invalid provider output is not exposed to ordinary users

## DocType and migration

- New/changed DocTypes:
- Migration required: yes / no
- Role permissions:
- Retention/deletion behavior:
- Existing-site compatibility:
- Rollback limitations:

## Background job behavior

- Queue:
- Idempotency key:
- Duplicate prevention:
- Timeout:
- Retry/backoff:
- Cancellation:
- Failure recovery:

## Validation

### Static

```text
Command:
Result:
```

### Unit tests

```text
Command:
Test count:
Result:
```

### ERPNext runtime

```text
Commit SHA:
Site identifier: redacted if needed
Commands:
API result:
Web route result:
Authorized-user result:
Restricted-user result:
```

### External AI

```text
Called: yes/no
Data classification:
Provider:
Result:
Cost/usage:
```

## UI evidence

- [ ] Not applicable
- [ ] Desktop checked
- [ ] Mobile/responsive checked
- [ ] Keyboard checked
- [ ] Error/partial/stale state checked
- Evidence:

## Rollback and recovery

- Rollback steps:
- Data rollback:
- Migration rollback:
- Feature disable switch:

## Security review

- [ ] No ERPNext/Frappe core changes
- [ ] No secret exposure
- [ ] No unapproved external ERP data transfer
- [ ] Safe user-facing errors
- [ ] Audit metadata is complete
- [ ] Autonomous ERP writes are not introduced

## Final evidence

- Head branch:
- Exact head SHA:
- CI run:
- Runtime smoke report:
- Known limitations:
