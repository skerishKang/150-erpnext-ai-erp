# ADR-0001: Use ERPNext as Initial Base

**Status:** Accepted

**Date:** 2026-05-16

## Context

We are building an AI-powered ERP for Korean SMEs. We have two broad options:

1. **Build from scratch** — full control, no legacy, but enormous development effort and time to market.
2. **Use an existing open-source ERP** — faster time to market, proven workflows, but constraints on architecture and customization.

ERPNext is the leading open-source ERP with a mature document model, role-based permissions, workflow engine, REST API, and an active community.

## Decision

Use ERPNext as the initial ERP base for Padiem AI ERP.

We will extend ERPNext through custom apps, hooks, custom fields, and API integrations rather than forking or heavily modifying the core.

## Rationale

- ERPNext provides a **tested ERP structure** (Customer, Item, Quotation, Sales Order, Delivery Note, Purchase Order, Accounting, etc.) out of the box.
- The **document-event model** (via hooks and server scripts) gives clean integration points for AI-driven automation.
- Building ERP workflow ourselves would take **months or years** to reach feature parity.
- We retain the option to **compare against custom development** later — if ERPNext constraints become prohibitive, we can migrate.
- This is a **pragmatic time-to-market decision**, not a reflection of development capability.

## Consequences

**Positive:**
- Rapid start with working quotation → order → delivery → invoicing flow
- Built-in permission system, role management, audit trail
- REST API for AI module integration
- Active community and Frappe framework ecosystem
- Bench CLI for site management and updates

**Negative:**
- Must work within Frappe/ERPNext architectural conventions
- Korean localization (language, tax, accounting) may require custom work
- Upstream updates may conflict with customizations
- ERPNext's UI/UX is form-centric; may need front-end investment for CEO dashboard

## Alternatives Considered

| Alternative | Reason against |
|-------------|----------------|
| Odoo (Community) | Python-based, but license (LGPL) restrictions on competitive modules; heavier architecture |
| Build from scratch (Django/Postgres) | 12–18 month timeline to reach basic ERP workflow parity |
| Adopt a Korean ERP (iU, Duzon) | Closed source, no API/extension flexibility, vendor lock-in |

## Related Documents

- [ERPNext Strategy](../agents/03-technical/erpnext-strategy.md)
- [Architecture: ERPNext Extension Strategy](../architecture/01-erpnext-extension-strategy.md)
