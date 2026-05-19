# ERP Read-Only Performance Strategy

**Target Modules:** `padiem_ai/padiem_ai/erp/read_only_modules/`  
**Issue:** #65  
**Date:** 2026-05-19  
**Status:** Design phase — no runtime code changes

---

## 1. Current Risk

The existing read-only helper functions use `limit_page_length=0` in `frappe.get_list()` calls, which disables pagination and fetches **all records** from the table. While acceptable for demo-scale data (tens to hundreds of records), this poses a performance risk in production ERP deployments:

| Risk | Impact |
|------|--------|
| `_safe_get_list()` with `limit_page_length=0` | Full-table scan on every call |
| `_count_records()` uses `frappe.get_list()` + `len()` | Fetches all record names just to count — no SQL `COUNT(*)` |
| Sales Invoice / Payment Entry tables grow unbounded | CEO briefing latency increases linearly with record volume |
| Multiple domain summaries called sequentially | Briefing context assembly latency = sum of all domain query latencies |

---

## 2. Current Affected Functions

| Function | File | Query Pattern | Risk Level |
|----------|------|---------------|------------|
| `_count_records()` | `utils.py` | `frappe.get_list(…, limit_page_length=0)` + `len()` | **High** — full name list fetch for a simple count |
| `_safe_get_list()` | `utils.py` | `frappe.get_list(…, limit_page_length=0)` | **High** — unbounded result set |
| `get_sales_summary()` | `sales.py` | 3x `_safe_get_list()` | High |
| `get_quotation_summary()` | `sales.py` | 1x `_safe_get_list()` | Medium |
| `get_delivery_summary()` | `sales.py` | 1x `_safe_get_list()` | Medium |
| `get_inventory_summary()` | `inventory.py` | 2x `_safe_get_list()` | Medium |
| `get_purchase_summary()` | `purchasing.py` | 1x `_safe_get_list()` | Medium |
| `get_receivables_summary()` | `receivables.py` | 1x `_safe_get_list()` | **High** — returns full invoice detail list |
| `get_payment_summary()` | `payments.py` | 1x `_safe_get_list()` | Medium |
| `get_ceo_briefing_context()` | `context.py` | 7x domain summary orchestration | **High** — aggregates all risks |

---

## 3. Design Principles

```
┌─────────────────────────────────────────────────────────┐
│ Public function signatures   → NEVER change              │
│ Return shapes                → PRESERVE when possible    │
│ ERPNext / Frappe core        → DO NOT modify             │
│ Demo data                    → DO NOT modify             │
│ External AI calls            → DISABLED                  │
│ Full-table list fetch        → AVOID as default strategy │
│ Top-N detail + aggregate     → PREFERRED pattern         │
└─────────────────────────────────────────────────────────┘
```

### Guiding Rules

1. **Signature stability first** — all existing `get_*()` functions keep their signature and return shape. Additive metadata fields (e.g., `truncated`, `limit`, `total_available`) may be added to return dicts without breaking consumers.
2. **Separate detail from aggregate** — full-record details (like `receivables.invoices`) should be limited; aggregate counts/sums should use efficient SQL aggregation.
3. **Count via `frappe.db.count()`** — replace `len(frappe.get_list(…))` with dedicated count query when possible.
4. **Phased rollout** — each change has its own issue/PR with clear compatibility guarantees.

---

## 4. Proposed Strategy

### 4.1 Helper Layer Additions

New helpers in `utils.py`:

```python
# Maximum records returned by detail list queries
DEFAULT_READ_ONLY_LIMIT = 100

def _safe_count_records(doctype: str, filters: dict = None) -> int:
    """Count records using frappe.db.count (SQL COUNT).

    Falls back to _count_records() if frappe.db.count unavailable.
    """

def _safe_get_list_limited(
    doctype: str,
    fields: list = None,
    filters: dict = None,
    limit: int = DEFAULT_READ_ONLY_LIMIT,
    order_by: str = None,
) -> tuple:
    """Same shape as _safe_get_list but with bounded result size.
    Returns (results, total_count, error_or_None) — or kept at (results, error).
    """

def _safe_sum_field(doctype: str, field: str, filters: dict = None) -> float:
    """Aggregate sum of a numeric field using SQL SUM via frappe.db.get_value."""
```

### 4.2 Return Shape Compatibility Strategy

| Current Field | Proposal | Compatibility |
|---------------|----------|---------------|
| `receivables.invoices` (full list) | `receivables.invoices` (top-N, + `invoices_truncated` bool) | Additive — `bool` key added |
| `sales.submitted_invoice_count` | Same field, computed via `_safe_count_records()` | Identical shape |
| `sales.total_invoiced` | Same field, computed via `_safe_sum_field()` | Identical shape |
| `payments.payment_count` | Same field, computed via `_safe_count_records()` | Identical shape |
| Detail items inside each invoice | No change — already scalar or short | N/A |

### 4.3 Cache Strategy (Future Consideration)

- CEO briefing context is read-heavy, write-light → cacheable.
- Future option: short-lived cache (e.g., 60-second TTL) for `get_ceo_briefing_context()`.
- Not included in immediate phases — requires performance benchmark first.

---

## 5. Safe Implementation Phases

### Phase 1: Documentation (this PR)
- ✅ Strategy document approved
- ✅ No runtime code changes

### Phase 2: Helper Foundation (follow-up issue)
- Add `DEFAULT_READ_ONLY_LIMIT` constant
- Add `_safe_count_records()` — count-optimized helper
- Add `_safe_get_list_limited()` — bounded list helper
- Add `_safe_sum_field()` — aggregation helper
- Keep all existing helpers unchanged for backward compat
- New helpers coexist with old ones; no existing call site changes yet

### Phase 3: Summary Function Migration (follow-up issues)
- Convert each `get_*_summary()` to use new helpers
- Convert `get_receivables_summary()` to top-N invoice detail
- Run return-shape compatibility check per function
- One PR per domain (sales, stock, purchasing, receivables, payments)

### Phase 4: Validation (follow-up issue)
- CEO briefing smoke test in ERPNext Docker environment
- Performance benchmark: query latency before/after
- `check_file_size` gate
- Integration test with mock generator

---

## 6. Recommended Follow-Up Issues

| # | Title | Scope |
|---|-------|-------|
| A | Add `_safe_count_records()` and `_safe_sum_field()` to `utils.py` | New helpers, no call site changes |
| B | Add `_safe_get_list_limited()` with `DEFAULT_READ_ONLY_LIMIT` | Bounded list helper |
| C | Migrate `_count_records()` call sites to `_safe_count_records()` | Sales, receivables, context |
| D | Convert `get_receivables_summary()` to top-N invoice detail | Breaks existing invoice list shape? |
| E | Convert `get_sales_summary()` to use aggregation helpers | Same shape, efficient queries |
| F | Convert `get_purchase_summary()`, `get_quotation_summary()`, `get_delivery_summary()` | Same shape |
| G | Convert `get_payment_summary()`, `get_inventory_summary()` | Same shape |
| H | CEO briefing performance smoke checklist in ERPNext runtime | Final validation |

---

## 7. Non-Goals (this PR)

- ❌ **No runtime code changes** — zero modifications to `.py` files
- ❌ **No `limit_page_length` value changes** — not touching any query
- ❌ **No return shape changes** — all `get_*()` output stays as-is
- ❌ **No ERPNext / Frappe core modifications**
- ❌ **No demo data changes**
- ❌ **No cache implementation** (future consideration only)
- ❌ **No benchmarking or profiling** (requires ERPNext runtime)

---

## Summary

| Aspect | Status |
|--------|--------|
| Current risk | Full-table fetches via `limit_page_length=0` |
| Affected functions | 10 functions across read-only modules |
| Strategy | Bounded queries + aggregation helpers + top-N details |
| Implementation phases | 4 phases (Doc → Helpers → Migration → Validation) |
| Return shape stability | Preserved; additive metadata fields only |
| This PR | **Documentation only** — zero runtime changes |