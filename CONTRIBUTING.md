# Contributing to Padiem AI ERP

## 1. Scope

Padiem AI ERP is an ERPNext application for Korean SMEs. AI features must remain subordinate to ERP permissions, business rules, and human approval.

Before changing code or documentation, read:

1. `AGENTS.md`
2. `docs/agents/README.md`
3. `docs/agents/00-index/agent-reading-order.md`
4. applicable product, technical, and operations documents

## 2. Non-Negotiable Rules

- Do not modify ERPNext or Frappe core.
- Do not commit real customer or production ERP data.
- Do not commit API keys, passwords, site config, database dumps, backups, cookies, or credentials.
- Keep the default provider on `mock` unless a separately approved issue changes the product policy.
- Do not make external AI calls unless the issue and test plan explicitly require them.
- Do not add autonomous ERP write operations without a human-approval design and separate security review.
- Do not treat DocType read permission alone as sufficient for Company or row-level aggregate access.
- Do not return a valid numeric zero when a query failed.

## 3. Issue-First Workflow

Create or select an issue before implementation.

An implementation issue should define:

- problem and evidence
- business impact
- scope and non-scope
- affected DocTypes and modules
- permission and Company impact
- external AI impact
- data classification
- migration and rollback impact
- acceptance criteria
- required tests

Large work should be split into independently reviewable issues.

## 4. Branches

Recommended names:

```text
feat/issue-123-short-description
fix/issue-123-short-description
security/issue-123-short-description
test/issue-123-short-description
docs/issue-123-short-description
refactor/issue-123-short-description
```

Use a current `main` base. Do not continue work on an old superseded branch without comparing it to current `main`.

## 5. Pull Requests

Each PR should:

- link the issue
- explain the exact scope
- list changed files
- state what was intentionally not changed
- record exact head SHA
- identify runtime and migration impact
- state whether an external AI call occurred
- state what data was used
- include tests and commands
- describe permission and Company scenarios
- include rollback or recovery notes

Keep PRs focused. A PR should not mix provider activation, ERP metric changes, UI redesign, and infrastructure changes unless the issue explicitly requires an integrated change.

## 6. Data Rules

Allowed test data:

- synthetic records
- generated Korean business examples
- irreversibly anonymized fixtures approved for testing

Not allowed:

- customer exports
- production screenshots containing identifiers
- real document numbers
- real financial values linked to a company
- personal data
- credentials
- database dumps
- Frappe site folders

When adding fixtures, document why they cannot identify a real person or company.

## 7. ERP Query Changes

Every query change must identify:

- source DocType
- selected fields
- document-status policy
- Company filter
- date/period policy
- currency policy
- permission behavior
- expected no-data result
- expected error result

For aggregates, verify row-level access explicitly. `frappe.db.count()` and aggregate `frappe.db.get_value()` calls are not permission boundaries by themselves.

## 8. API Changes

API PRs must include:

- authentication and permission requirements
- Company and period input validation
- stable success and error contract
- data minimization
- response metadata
- backward-compatibility impact
- rate or workload impact
- safe user-facing error behavior

Do not expose exception text, secrets, raw ERP context, or raw invalid model output to ordinary users.

## 9. AI Provider Changes

Provider PRs must state:

- provider and model
- whether calls are external
- enablement chain
- secret source
- transmitted fields
- redaction or minimization
- timeout and retry
- schema validation
- token/cost limits
- execution metadata
- audit behavior

Live provider tests must use staging, synthetic or approved anonymized data, and a non-production key.

## 10. Background Jobs

Job changes should include:

- idempotency behavior
- duplicate prevention
- timeout
- retry and backoff
- cancellation
- status transitions
- failure recovery
- audit record
- worker and queue impact

## 11. DocType and Migration Changes

For any new or changed DocType:

- include JSON/schema changes
- define role permissions
- define read/write/delete behavior
- define retention
- define migration path
- define rollback limitations
- run install and migrate tests
- verify existing sites are not broken

Completed audit records should not be editable by ordinary users.

## 12. Required Validation

### Documentation-only PR

- links resolve
- issue numbers are correct
- current implementation is not overstated
- no secret or real-data content
- project map updated when required

### Runtime code PR

At minimum:

```bash
python -m py_compile $(find padiem_ai/padiem_ai tests -name '*.py')
python -m unittest discover -s tests -p 'test_*.py'
```

Also run relevant lint, integration, and bench tests when available.

### ERPNext integration PR

Record:

- ERPNext version
- Frappe version
- Python version
- database
- site type
- app installation state
- exact command
- authorized and restricted-user results

## 13. Review Priorities

Review in this order:

1. secrets and data exposure
2. Company and row-level permissions
3. metric correctness and error semantics
4. external AI transfer and audit
5. migration and rollback
6. tests and runtime evidence
7. performance
8. maintainability
9. UI and wording

## 14. Merge Conditions

A PR may merge when:

- scope matches the issue
- required tests pass
- no unresolved security or permission concern remains
- migration and rollback are understood
- runtime evidence is supplied when required
- documentation is updated
- default-safe behavior is preserved

Do not merge because the code only compiles.

## 15. Issue Closure Evidence

Before closing an implementation issue, record:

```text
Issue:
PR:
Merge commit:
Exact tested SHA:
Changed files:
Tests:
Runtime environment:
Permission scenarios:
External AI calls:
Data used:
Migration:
Rollback:
Remaining limitations:
```

## 16. Release Rules

A release must satisfy `docs/implementation/RELEASE_GATES.md`.

Every release should have:

- version and tag
- commit SHA
- changelog
- supported environment
- CI status
- runtime smoke report
- migration instructions
- rollback instructions
- known limitations
- provider and external-data status
