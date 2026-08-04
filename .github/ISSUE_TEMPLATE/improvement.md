---
name: Improvement proposal
description: Propose a scoped ERP, AI, security, data, testing, or UX improvement
title: "[IMPROVEMENT] "
labels: []
assignees: []
---

## Problem

What current limitation or risk should be addressed?

## Business outcome

Which Korean SME ERP workflow improves?

- [ ] Quotation
- [ ] Inventory
- [ ] Delivery
- [ ] Receivables
- [ ] Executive reporting
- [ ] App installation or operations
- [ ] Security or permission
- [ ] AI governance
- [ ] Developer experience

## Current evidence

- File/function/route:
- Current behavior:
- Related issue/PR:
- Runtime evidence available: yes / no

## Proposed scope

- 

## Explicit non-scope

- 

## ERP impact

- Affected DocTypes:
- Company scope:
- User Permission impact:
- Document-status policy:
- Period/date policy:
- Currency policy:
- ERPNext/Frappe core changes: must remain no

## AI and data impact

- Provider affected:
- External AI call required: yes / no
- Data classification:
- Fields transmitted:
- Redaction/minimization:
- Secret storage:
- Schema validation:
- Token/cost limit:
- Audit record:

## API and contract impact

- New or changed endpoint:
- Request contract:
- Response contract:
- Error contract:
- Compatibility impact:

## DocType and migration impact

- New/changed DocTypes:
- Migration required:
- Retention and deletion:
- Existing-site compatibility:
- Rollback approach:

## Background-job impact

- Queue:
- Idempotency:
- Timeout:
- Retry/backoff:
- Cancellation:
- Failure recovery:

## Test plan

- [ ] Unit tests
- [ ] Frappe/ERPNext runtime smoke
- [ ] Authorized-user path
- [ ] Restricted-user path
- [ ] Multi-company isolation
- [ ] Query-failure versus zero
- [ ] Migration test
- [ ] UI/accessibility test
- [ ] Synthetic staging provider test

## Safety constraints

- [ ] No production credentials
- [ ] No real customer data in repository or CI
- [ ] Default provider remains mock unless explicitly approved
- [ ] No autonomous ERP write execution
- [ ] No ERPNext/Frappe core modification

## Acceptance criteria

- [ ] 
- [ ] 
- [ ] 

## Completion evidence

- PR:
- Exact tested SHA:
- Commands/tests:
- Runtime environment:
- External AI call status:
- Migration/rollback:
- Remaining limitations:
