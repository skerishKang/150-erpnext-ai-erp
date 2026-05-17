# 17 - Issue Roadmap

## Date

2026-05-18

## Purpose

This document records the current work queue for the ERPNext-based Padiem AI ERP project.

The project has moved past initial repository setup and local ERPNext verification. ERPNext is running locally, the Setup Wizard has been completed, demo data has been planned, CSV files have been prepared, and the first small import tests have started.

This roadmap separates tasks that require Docker/ERPNext runtime from tasks that can be completed as documentation or product planning work.

---

## Current Open Issues

| Issue | Title | Type | Docker Needed | Recommended Order |
|---|---|---|---:|---:|
| #1 | Sprint pause: stop ERPNext Docker safely and record resume commands | Operations | Yes | 1 |
| #2 | Complete Supplier and Item test imports in ERPNext | ERPNext data | Yes | 5 |
| #3 | Run full ERPNext demo dataset import after validation | ERPNext data | Yes | 6 |
| #4 | Define AI ERP feature specification for first demo | Product | No | 2 |
| #5 | Draft first customer proposal for AI ERP pilot | Sales | No | 3 |
| #6 | Design first Padiem AI ERP demo dashboard concept | Product/UI | No | 4 |
| #7 | Plan AI provider abstraction for DeepSeek and future models | Architecture | No | 7 |
| #8 | Prepare Oracle Cloud deployment plan for ERPNext AI ERP | Architecture/Cloud | No | 8 |
| #9 | Document ERPNext custom app strategy for Padiem AI modules | Architecture/ERPNext | No | 9 |

---

## Recommended Execution Order

### Phase A. Pause and stabilize current runtime

1. **Issue #1** — Stop Docker safely and document resume commands.

Reason: The ERPNext local environment is already proven. It does not need to stay running while product and sales documents are prepared.

Deliverable:

- `docs/implementation/15-sprint-pause-and-next-work.md`

---

### Phase B. Work that can proceed without Docker

2. **Issue #4** — Define AI ERP feature specification.

Deliverable:

- `docs/product/ai-feature-spec-v1.md`

3. **Issue #5** — Draft first customer proposal.

Deliverable:

- `docs/sales/04-ai-erp-pilot-proposal-v1.md`

4. **Issue #6** — Design first demo dashboard concept.

Deliverable:

- `docs/product/demo-dashboard-concept-v1.md`

Reason: These three tasks turn the technical ERPNext experiment into a sellable AI ERP pilot concept.

---

### Phase C. Resume ERPNext data work later

5. **Issue #2** — Complete Supplier and Item test imports.

Deliverables:

- Updated `docs/implementation/14-demo-data-test-import-log.md`
- Updated test CSV files if needed

6. **Issue #3** — Run full fictional demo dataset import after validation.

Deliverable:

- `docs/implementation/16-demo-data-full-import-log.md`

Reason: Full import should only happen after the remaining Supplier and Item tests pass.

---

### Phase D. Architecture planning before implementation

7. **Issue #7** — AI provider abstraction design.

Deliverable:

- `docs/architecture/05-ai-provider-abstraction-design.md`

8. **Issue #8** — Oracle Cloud deployment plan.

Deliverable:

- `docs/architecture/06-oracle-cloud-deployment-plan.md`

9. **Issue #9** — ERPNext custom app strategy.

Deliverable:

- `docs/architecture/07-erpnext-custom-app-strategy.md`

Reason: These architecture documents should be completed before building the Padiem AI module.

---

## Work Categories

### Docker-required work

These tasks need ERPNext containers running:

- Supplier test import
- Item test import
- Full fictional demo dataset import
- ERPNext Desk verification
- Future custom app installation testing

### Documentation-only work

These tasks do not require Docker:

- AI ERP feature specification
- Customer proposal
- Demo dashboard concept
- AI provider abstraction design
- Oracle Cloud deployment plan
- ERPNext custom app strategy

---

## Current CTO Recommendation

Stop the Docker environment safely and switch to the documentation/product track first.

The next best work item is:

> Issue #1, then Issue #4, then Issue #5.

This sequence preserves the local ERPNext work while moving the project toward a customer-facing AI ERP pilot.

---

## Guardrails

- Do not delete Docker volumes.
- Do not use real customer data.
- Do not commit backup files.
- Do not commit secrets, API keys, passwords, or `.env` files.
- Do not start AI module implementation before the feature specification and provider abstraction are documented.
- Do not present this as generic automation. The product identity remains ERP: **Padiem AI ERP**.
