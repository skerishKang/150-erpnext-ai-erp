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


def get_receivables_summary() -> dict:
    """Get receivables summary from Sales Invoice.

    Returns:
        tuple: (dict with receivables summary, list of warnings)
    """
    warnings = []

    invoices, err = _safe_get_list(
        "Sales Invoice",
        filters={"outstanding_amount": (">", 0)},
        fields=["name", "customer", "outstanding_amount", "due_date", "posting_date"],
    )
    if err:
        warnings.append(err)

    total_outstanding = sum(inv.get("outstanding_amount", 0) for inv in invoices)

    return {
        "outstanding_invoice_count": len(invoices),
        "total_outstanding": total_outstanding,
        "invoices": invoices,
    }, warnings


def get_payment_summary() -> dict:
    """Get payment entry summary.

    Returns:
        tuple: (dict with payment summary, list of warnings)
    """
    warnings = []

    payments, err = _safe_get_list(
        "Payment Entry",
        fields=["name", "party", "paid_amount", "posting_date", "payment_type"],
    )
    if err:
        warnings.append(err)

    total_received = sum(p.get("paid_amount", 0) for p in payments if p.get("payment_type") == "Receive")
    total_paid = sum(p.get("paid_amount", 0) for p in payments if p.get("payment_type") == "Pay")

    return {
        "payment_count": len(payments),
        "total_received": total_received,
        "total_paid": total_paid,
    }, warnings


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
