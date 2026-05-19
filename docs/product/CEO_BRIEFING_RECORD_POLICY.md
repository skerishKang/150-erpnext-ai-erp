# CEO Briefing Record Policy

This document defines the record-selection policy for Padiem AI ERP CEO briefing summaries.

The goal is to prevent executive briefing numbers from mixing draft, submitted, cancelled, closed, and operational records without a clear product decision.

## General rule

CEO briefing metrics must state whether they use one of these scopes:

- **submitted-only**: records with `docstatus = 1`
- **draft-only**: records with `docstatus = 0`
- **open/active**: records with a business status that is still actionable
- **all-record**: all records, only when intentionally used as a catalog or broad operational count

Aggregate helper functions are not permission boundaries. Entry points must enforce read permissions before exposing briefing context.

## Current policy table

| Area | DocType | Current runtime behavior | Policy status | Notes |
|---|---|---|---|---|
| Customers | Customer | all-record count | accepted for catalog count | Represents customer master-data size. |
| Suppliers | Supplier | all-record count | accepted for catalog count | Represents supplier master-data size. |
| Items | Item | all-record count and stock item count | accepted for catalog count | Represents item master-data size. |
| Sales invoices | Sales Invoice | submitted totals, draft count separately | accepted | Submitted invoice totals use `docstatus = 1`; draft count remains separate. |
| Receivables | Sales Invoice | submitted outstanding invoices only | accepted | Outstanding filters should include `docstatus = 1` and `outstanding_amount > 0`. |
| Payments | Payment Entry | submitted payments only | accepted | Payment totals should use `docstatus = 1`. |
| Sales orders | Sales Order | all-record count and total | pending product decision | Needs decision: all, submitted, open, or status-specific. |
| Quotations | Quotation | all-record count and total | pending product decision | Needs decision: all, submitted, open, expired, or converted. |
| Delivery notes | Delivery Note | all-record count | pending product decision | Needs decision: all, submitted, pending, or completed. |
| Purchase orders | Purchase Order | all-record count and total | pending product decision | Needs decision: all, submitted, open, received, or billed. |
| Stock entries | Stock Entry | all-record count | pending product decision | Needs decision: all, submitted, or operational status breakdown. |
| Warehouses | Warehouse | all-record count | accepted for catalog count | Represents warehouse master-data size. |

## Implementation guidance

For pending areas, do not silently change runtime calculations without a separate implementation issue or PR.

Recommended next implementation slices after this policy is accepted:

1. Sales Order policy implementation.
2. Quotation and Delivery Note policy implementation.
3. Purchase Order policy implementation.
4. Stock Entry policy implementation.

Each implementation PR should preserve public response keys unless a breaking change is explicitly documented.

## Non-goals

- This document does not change runtime behavior by itself.
- This document does not enable external AI calls.
- This document does not modify ERPNext/Frappe core.
