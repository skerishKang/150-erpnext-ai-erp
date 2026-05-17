# ERPNext Extension Strategy

## Principle

**Extend, do not fork.**

We use ERPNext as the base platform. We build on top of it using Frappe's extension mechanisms. We avoid deep core modifications that would make upstream upgrades difficult or impossible.

## Extension Mechanisms (Priority Order)

| Priority | Mechanism | When to Use |
|----------|-----------|-------------|
| 1 | **Custom Frappe App** | All Padiem-specific functionality goes in `padiem_ai` app |
| 2 | **Custom Fields** | Add fields to existing ERPNext doctypes via Custom Field |
| 3 | **DocType Extension** | Extend ERPNext doctypes via `_custom` suffix or custom fields |
| 4 | **Frappe Hooks** | Hook into ERPNext events (validate, on_update, on_submit) |
| 5 | **Server Scripts** | Business logic that runs on the server (Frappe Script) |
| 6 | **API Endpoints** | REST API endpoints in the custom app for AI module |
| 7 | **Web Pages / Templates** | Custom web pages for CEO dashboard |
| 8 | **Patches** | Data migration scripts via Frappe patches system |

## What We Customize vs. What We Keep

| Area | Approach |
|------|----------|
| Master data (Customer, Item, Supplier) | Keep ERPNext standard; add custom fields as needed |
| Quotation, Sales Order, Delivery Note | Keep standard; add hooks for AI integration |
| Accounting | Keep standard; defer comprehensive use to post-MVP |
| Permissions and roles | Keep standard ERPNext Role Permission Manager |
| UI/UX — Standard forms | Keep ERPNext standard |
| UI/UX — CEO Dashboard | Build custom web page(s) in `padiem_ai` app |
| Reports | Use ERPNext Report Builder + custom AI-generated reports |

## What We AVOID

| Action | Reason |
|--------|--------|
| ❌ Modifying ERPNext core files | Impossible to upgrade |
| ❌ Forking ERPNext repository | Maintenance burden |
| ❌ Monkey-patching core classes | Breaks silently on upgrade |
| ❌ Direct database manipulation outside Frappe ORM | Bypasses Frappe validations, breaks hooks |

## Custom App Structure (`padiem_ai`)

```
padiem_ai/
├── __init__.py
├── hooks.py              # Frappe hooks
├── padiem_ai/
│   ├── api/              # REST API endpoints
│   │   ├── __init__.py
│   │   ├── briefing.py
│   │   ├── quotation_draft.py
│   │   ├── sales_summary.py
│   │   └── inventory_alert.py
│   ├── ai_adapter/       # AI provider abstraction
│   │   ├── __init__.py
│   │   ├── base.py       # Abstract base class
│   │   ├── deepseek.py
│   │   ├── openai.py
│   │   └── mock.py
│   ├── prompts/          # Prompt templates
│   │   ├── briefing.json
│   │   ├── quotation_draft.json
│   │   └── sales_summary.json
│   ├── data/             # ERP data retrieval
│   │   ├── __init__.py
│   │   ├── quotation_data.py
│   │   ├── sales_data.py
│   │   └── inventory_data.py
│   ├── audit/            # Audit logging
│   │   ├── __init__.py
│   │   └── log.py
│   └── dashboard/        # CEO dashboard
│       ├── __init__.py
│       └── page.py
├── padiem_ai/doctype/    # Custom doctypes
│   ├── AI Provider Config/
│   ├── AI Audit Log/
│   └── Prompt Template/
├── padiem_ai/page/       # Custom pages
│   └── ceo_dashboard/
└── padiem_ai/public/     # Frontend assets
    ├── js/
    └── css/
```

## Upgrade Strategy

1. **Staging-first:** Test ERPNext upgrades in staging before production
2. **Patch custom fields:** Frappe automatically applies custom fields during `bench migrate`
3. **Review hooks:** After upgrade, verify custom hooks still work
4. **Test critical flows:** Quotation → Order → Delivery flow after each upgrade
5. **Rollback plan:** Database backup before upgrade, Docker volume snapshot
