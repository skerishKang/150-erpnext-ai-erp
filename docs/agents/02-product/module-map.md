# Module Map

## ERPNext to Padiem AI ERP Module Mapping

This maps ERPNext's built-in modules to Padiem AI ERP's module structure.

### Direct Mapping (Use ERPNext Module)

| Padiem Module | ERPNext Module | Notes |
|---------------|----------------|-------|
| Customer management | CRM + Selling | Customer master, contact, address |
| Supplier management | Buying | Supplier master, purchase history |
| Item management | Stock | Item catalog, pricing, categories |
| Quotation management | Selling | Quotation doctype |
| Sales order management | Selling | Sales Order doctype |
| Purchase order management | Buying | Purchase Order doctype |
| Inventory status | Stock | Stock Ledger, Bin, Warehouse |
| Delivery tracking | Stock | Delivery Note, Shipment |

### Requires Customization

| Padiem Module | ERPNext Base | Customization Needed |
|---------------|--------------|---------------------|
| Sales and receivables view | Accounts + Selling | Custom dashboard combining sales invoices and payments |
| CEO daily briefing | None (custom) | AI-generated summary from multiple modules |
| Weekly report generation | None (custom) | AI-generated report from ERP data |
| AI natural-language query | None (custom) | AI layer that queries ERPNext API |
| AI quotation draft | Selling | AI layer that generates quotation from natural language |
| Accountant-ready package | Accounts | Export tool for accountant documents |

### Not In ERPNext (Custom Build)

| Padiem Module | Description |
|---------------|-------------|
| AI query engine | Natural language to ERPNext API translation |
| AI briefing engine | Daily/weekly summary generation |
| Accountant package builder | Document export for external accountant |

## Module Dependencies

```
Customer Management ──┐
                      ├── Quotation ── Sales Order ── Delivery
Item Management ──────┘       │              │
                              │              │
Supplier Management ── Purchase Order         │
                              │              │
                      Inventory Status ──────┘
                              │
                      Sales & Receivables ── CEO Briefing
                                              Weekly Report
```

## ERPNext Module Usage Summary

- **Selling:** Quotation, Sales Order, Customer
- **Buying:** Purchase Order, Supplier
- **Stock:** Item, Inventory, Delivery Note, Warehouse
- **Accounts:** Sales Invoice (read-only for receivables view)
- **CRM:** Customer master data
- **Custom:** AI features, CEO briefing, weekly reports, accountant package
