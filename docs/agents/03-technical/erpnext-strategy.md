# ERPNext Strategy

## Why ERPNext

ERPNext is the **initial base** for Padiem AI ERP.

### Reasons

1. **Time savings:** ERPNext provides core ERP doctypes (Customer, Supplier, Item, Quotation, Sales Order, Purchase Order, Stock, Delivery Note) out of the box.
2. **Proven data model:** Years of refinement in ERP data structures.
3. **Korean localization potential:** Community has Korean translation and some localization work.
4. **Open source:** Full control over the codebase, no vendor lock-in.
5. **API-first:** REST API built in, essential for AI integration.

### What We Use From ERPNext

- Core doctypes and data model
- User authentication and permissions
- Report framework
- Print format system
- REST API
- Workflow engine

### What We Build Custom

- AI integration layer
- CEO daily briefing
- Weekly report generation
- Natural language query engine
- AI quotation drafting
- Accountant-ready document package builder
- Korean-specific customizations

## The Comparison Plan

We use ERPNext to save time **and** to compare against custom development later.

- Phase 1: Build on ERPNext, validate product-market fit
- Phase 2: Measure what ERPNext gives us vs. what we build custom
- Phase 3: Decide whether to stay on ERPNext or build custom

## Important

**We are not using ERPNext because we lack development ability.**

We are using ERPNext because:
- It accelerates initial development
- It provides a proven ERP foundation
- It lets us focus on AI differentiation, not basic ERP plumbing
- The comparison with custom development is a strategic decision, not a technical limitation

## ERPNext Version

- Target: ERPNext v14+ (Frappe framework)
- Deployment: Docker-based
- Database: MariaDB
