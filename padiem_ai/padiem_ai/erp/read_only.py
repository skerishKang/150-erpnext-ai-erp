"""Read-only ERP data access layer.

Provides structured summary data from ERPNext for CEO briefing and other features.
Uses frappe.get_all / frappe.get_list only. No inserts, updates, or deletes.
Respects ERPNext permissions.

No external AI API calls. No credentials stored or referenced.
"""

from padiem_ai.erp.read_only_modules.utils import _count_records, _safe_get_list
from padiem_ai.erp.read_only_modules.sales import (
    get_sales_summary,
    get_quotation_summary,
    get_delivery_summary,
)
from padiem_ai.erp.read_only_modules.inventory import get_inventory_summary
from padiem_ai.erp.read_only_modules.purchasing import get_purchase_summary
from padiem_ai.erp.read_only_modules.receivables import (
    get_receivables_summary,
    get_payment_summary,
)


def get_demo_counts() -> dict:
    """Get record counts for all demo DocTypes using frappe.get_list.

    Returns:
        dict: DocType name -> record count
    """
    doctypes = [
        "Customer",
        "Supplier",
        "Item",
        "Quotation",
        "Sales Order",
        "Purchase Order",
        "Stock Entry",
        "Delivery Note",
        "Sales Invoice",
        "Payment Entry",
        "Warehouse",
    ]

    counts = {}
    for dt in doctypes:
        counts[dt] = _count_records(dt)

    return counts


def get_ceo_briefing_context() -> dict:
    """Get structured context for CEO Daily Briefing.

    Returns:
        dict: Complete briefing context with counts, sales, purchases,
              inventory, receivables, quotations, deliveries, payments, and warnings.
    """
    all_warnings = []

    counts = get_demo_counts()

    sales, w = get_sales_summary()
    all_warnings.extend(w)

    purchases, w = get_purchase_summary()
    all_warnings.extend(w)

    inventory, w = get_inventory_summary()
    all_warnings.extend(w)

    receivables, w = get_receivables_summary()
    all_warnings.extend(w)

    quotations, w = get_quotation_summary()
    all_warnings.extend(w)

    deliveries, w = get_delivery_summary()
    all_warnings.extend(w)

    payments, w = get_payment_summary()
    all_warnings.extend(w)

    # Business-level warnings
    if receivables["outstanding_invoice_count"] > 0:
        all_warnings.append(
            f"{receivables['outstanding_invoice_count']}건의 미수금 invoices "
            f"(총 {receivables['total_outstanding']:,.0f}원)"
        )
    if counts.get("Sales Order", 0) > 0:
        all_warnings.append(f"{counts['Sales Order']}건의 Sales Order 진행 중")

    return {
        "counts": counts,
        "sales": sales,
        "purchases": purchases,
        "inventory": inventory,
        "receivables": receivables,
        "quotations": quotations,
        "deliveries": deliveries,
        "payments": payments,
        "warnings": all_warnings,
    }
