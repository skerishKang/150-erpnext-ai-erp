# ERP Read-Only Refactor Audit

**Target File:** `padiem_ai/padiem_ai/erp/read_only.py`  
**Issue:** #46  
**Audit Date:** 2026-05-19

---

## Current File Metrics

| Metric | Value |
|--------|-------|
| Lines of Code | 322 lines |
| File Size | 8,571 bytes |
| Status | Below 500-line threshold (OK) |

---

## Function Inventory

### Public Functions (Exported)

| Function | Lines | Purpose |
|----------|-------|---------|
| `get_demo_counts()` | 52-76 | Returns DocType → record count mapping for demo entities |
| `get_sales_summary()` | 79-121 | Aggregates Sales Invoice (submitted/draft) and Sales Order data |
| `get_purchase_summary()` | 124-144 | Aggregates Purchase Order totals and counts |
| `get_inventory_summary()` | 147-175 | Returns Item counts (stock vs total) and Stock Entry count |
| `get_receivables_summary()` | 178-200 | Outstanding invoices with customer and amount details |
| `get_quotation_summary()` | 203-223 | Quotation counts and total quoted value |
| `get_delivery_summary()` | 226-243 | Delivery Note count |
| `get_payment_summary()` | 246-268 | Payment Entry aggregates (received vs paid amounts) |
| `get_ceo_briefing_context()` | 271-322 | Assembles complete CEO briefing context |

### Private Helper Functions

| Function | Lines | Purpose |
|----------|-------|---------|
| `_count_records(doctype)` | 13-22 | Count records using `frappe.get_list` |
| `_safe_get_list(doctype, fields, filters)` | 25-49 | Wrapped query with error logging |

---

## Call Sites in Repository

### Runtime Call Sites

| File | Import Statement | Usage |
|------|------------------|-------|
| `padiem_ai/padiem_ai/api/briefing.py` | `from padiem_ai.erp.read_only import get_ceo_briefing_context, get_demo_counts` | `get_ceo_briefing_context()` and `get_demo_counts()` |
| `padiem_ai/padiem_ai/www/ceo_briefing.py` | `from padiem_ai.erp.read_only import get_ceo_briefing_context` | `get_ceo_briefing_context()` |

### Documentation/Example References

| File | Nature | Notes |
|------|--------|-------|
| `padiem_ai/padiem_ai/briefing/mock_generator.py` | Docstring example | Lines 7-8 show usage example in module docstring; no runtime import |

---

## Natural Domain Split Candidates

### 1. Sales Domain
**Functions:** `get_sales_summary()`, `get_ceo_briefing_context()` (sales portion)
**DocTypes:** Sales Invoice, Sales Order, Quotation, Delivery Note
**Output:** Invoiced amounts, outstanding, SO counts

### 2. Stock/Inventory Domain
**Functions:** `get_inventory_summary()`
**DocTypes:** Item, Stock Entry
**Output:** Item counts, stock items, stock entry count

### 3. Purchasing Domain
**Functions:** `get_purchase_summary()`
**DocTypes:** Purchase Order
**Output:** PO counts, total value

### 4. Receivables Domain
**Functions:** `get_receivables_summary()`, `get_payment_summary()`
**DocTypes:** Sales Invoice (outstanding), Payment Entry
**Output:** Outstanding amounts, received/paid totals

### 5. CEO Briefing Context Assembly
**Functions:** `get_ceo_briefing_context()`, `get_demo_counts()`
**Purpose:** Orchestrates all above domains for CEO briefing
**Output:** Combined context dict with counts, sales, purchases, inventory, receivables, quotations, deliveries, payments, warnings

### 6. Shared Read-Only Query Utilities
**Functions:** `_count_records()`, `_safe_get_list()`
**Purpose:** Reusable query helpers for all domains

---

## Proposed Module Structure

```
padiem_ai/padiem_ai/erp/
├── read_only.py           # compatibility facade (re-exports from submodules)
├── read_only_modules/
│   ├── __init__.py        # exports all public functions
│   ├── sales.py           # get_sales_summary, get_quotation_summary, get_delivery_summary
│   ├── stock.py           # get_inventory_summary
│   ├── purchasing.py      # get_purchase_summary
│   ├── receivables.py     # get_receivables_summary, get_payment_summary
│   ├── context.py         # get_ceo_briefing_context, get_demo_counts
│   └── utils.py           # _count_records, _safe_get_list
```

---

## Compatibility Facade Plan

The existing `read_only.py` will remain as a facade that re-exports all public functions:

```python
# padiem_ai/padiem_ai/erp/read_only.py
"""Read-only ERP data access layer (compatibility facade)."""

from padiem_ai.erp.read_only_modules.sales import get_sales_summary, get_quotation_summary, get_delivery_summary
from padiem_ai.erp.read_only_modules.stock import get_inventory_summary
from padiem_ai.erp.read_only_modules.purchasing import get_purchase_summary
from padiem_ai.erp.read_only_modules.receivables import get_receivables_summary, get_payment_summary
from padiem_ai.erp.read_only_modules.context import get_ceo_briefing_context, get_demo_counts

__all__ = [
    "get_demo_counts",
    "get_sales_summary",
    "get_purchase_summary",
    "get_inventory_summary",
    "get_receivables_summary",
    "get_quotation_summary",
    "get_delivery_summary",
    "get_payment_summary",
    "get_ceo_briefing_context",
]
```

This ensures zero breaking changes for existing imports.

---

## Risk Assessment

| Risk | Level | Mitigation |
|------|-------|------------|
| Breaking imports | Low | Compatibility facade preserves all import paths |
| CEO briefing output change | Low | Same functions, same logic, same return types |
| File size growth | Low | Current 322 lines < 500 threshold |
| ERPNext permissions | None | No changes to permission model |
| `read_only.py` ↔ `read_only/` name collision | Medium | Use `read_only_modules/` for internal split while keeping `read_only.py` as facade |

---

## Non-Goals

- ❌ Moving functions between modules (audit only)
- ❌ Changing function signatures or return types
- ❌ Modifying ERPNext core or DocTypes
- ❌ Adding new ERP queries beyond current scope
- ❌ Changing README or onboarding docs
- ❌ Demo data modifications

---

## Follow-Up Implementation Issues

1. **Follow-up A:** Extract sales, quotation, delivery summaries
2. **Follow-up B:** Extract inventory summary
3. **Follow-up C:** Extract purchase summary
4. **Follow-up D:** Extract receivables and payment summaries
5. **Follow-up E:** Extract CEO briefing context assembly
6. **Follow-up F:** Extract shared read-only query utilities
7. **Follow-up G:** Keep read_only.py as compatibility facade and verify imports

---

## Future Validation Commands

```bash
# File size check
python scripts/check_file_size.py --root padiem_ai/padiem_ai --max-lines 500 --warn-lines 350 --top 5

# Python syntax check (if code changes)
python -m py_compile padiem_ai/padiem_ai/erp/read_only.py

# Import verification
python -c "from padiem_ai.erp.read_only import get_ceo_briefing_context; print('OK')"

# All call site verification
python -c "
from padiem_ai.erp.read_only import (
    get_ceo_briefing_context, get_demo_counts,
    get_sales_summary, get_purchase_summary,
    get_inventory_summary, get_receivables_summary,
    get_quotation_summary, get_delivery_summary,
    get_payment_summary
)
print('All imports OK')
"
```

---

## Summary

- **File Size:** 322 lines (within threshold)
- **Public Functions:** 9 functions
- **Private Helpers:** 2 functions
- **Call Sites:** 3 files (2 runtime, 1 documentation)
- **Recommended Split:** 6 domain-based modules
- **Risk Level:** Low (audit phase, no code changes)
