# ADR-0003: Exclude Full Accounting from MVP

**Status:** Accepted

**Date:** 2026-05-16

## Context

ERP traditionally includes full accounting: journal entries, ledgers, trial balance, tax filing, VAT reporting, electronic tax invoice issuance, payroll, and statutory reports.

Korean SMEs typically fall into two patterns:

1. **Use an accountant** — the SME handles operations (quotation, order, delivery, inventory, receivables) and sends data to an accountant who handles tax and statutory reporting.
2. **Use accounting software** (Ecount, iU, Duzon, etc.) with built-in accounting.

Building full Korean tax compliance (VAT filing, electronic tax invoices via NTS, payroll tax, year-end settlement) is a massive engineering effort with high regulatory risk.

## Decision

Exclude full accounting, tax filing, VAT filing, payroll, and electronic tax invoice issuance from the MVP.

Include **accountant-ready document preparation** — clean, organized documents that an accountant can use directly for tax filing.

## Rationale

- Most target SMEs already use accountants or accounting software for tax/accounting.
- The core pain is **operations visibility** (quotations, orders, inventory, receivables) — not accounting.
- Korean tax/accounting compliance (NTS integration, electronic tax invoices, year-end settlement) requires deep domain knowledge and months of development.
- "Accountant-ready" output provides value without regulatory risk.
- MVP should solve the operational pain first; accounting integration can follow in a later phase.

## Consequences

**Positive:**
- Faster MVP — no tax compliance engineering
- Lower regulatory risk
- Clear value proposition to CEOs who already use accountants
- Accountants appreciate clean, organized data

**Negative:**
- Customers using integrated accounting may need a separate accounting tool
- Some SMEs may expect full accounting from "ERP"
- Later accounting integration may require data migration

## In-Scope for MVP

- Customer management
- Item/product catalog
- Quotation creation
- Sales orders
- Delivery notes
- Inventory tracking
- Receivables tracking
- Accountant-ready monthly document package (PDF/CSV export)
- AI-generated sales summaries and CEO briefing

## Out-of-Scope for MVP

- Journal entries and general ledger
- VAT calculation and NTS electronic tax invoice
- Payroll and year-end settlement
- Tax filing
- Full double-entry accounting

## Alternatives Considered

| Alternative | Reason against |
|-------------|----------------|
| Include full accounting in MVP | 3–6 month delay, high regulatory risk, most SMEs won't use it |
| Integrate with existing accounting APIs (Ecount, iU) | Each requires separate partnership, API access, ongoing maintenance |

## Related Documents

- [MVP Scope](../agents/02-product/mvp-scope.md)
- [Non-Goals](../agents/01-principles/non-goals.md)
