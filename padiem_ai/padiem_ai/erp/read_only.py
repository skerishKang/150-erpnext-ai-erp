"""Read-only ERP data access layer.

Provides structured summary data from ERPNext for CEO briefing and other features.
Uses frappe.get_all / frappe.get_list only. No inserts, updates, or deletes.
Respects ERPNext permissions.

No external AI API calls. No credentials stored or referenced.
"""

import frappe


def _count_records(doctype: str) -> int:
    """Count records using frappe.get_list (not frappe.db.count).

    Args:
        doctype: DocType name

    Returns:
        int: Record count
    """
    return len(frappe.get_list(doctype, fields=["name"], limit_page_length=0))


def _safe_get_list(doctype: str, fields: list = None, filters: dict = None) -> tuple:
    """Safe wrapper around frappe.get_list that logs errors instead of hiding them.

    Args:
        doctype: DocType name
        fields: Fields to fetch
        filters: Filters to apply

    Returns:
        tuple: (results_list, error_message_or_None)
    """
    try:
        results = frappe.get_list(
            doctype,
            fields=fields or ["name"],
            filters=filters,
            limit_page_length=0,
        )
        return results, None
    except Exception as exc:
        frappe.log_error(
            title=f"Read-only ERP query failed: {doctype}",
            message=frappe.get_traceback(),
        )
        return [], f"{doctype} 조회 실패: {str(exc)}"


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


def get_sales_summary() -> dict:
    """Get sales summary from Sales Invoice and Sales Order.

    Returns:
        tuple: (dict with sales summary, list of warnings)
    """
    warnings = []

    submitted_invoices, err = _safe_get_list(
        "Sales Invoice",
        filters={"docstatus": 1},
        fields=["grand_total", "outstanding_amount", "customer", "posting_date"],
    )
    if err:
        warnings.append(err)

    draft_invoices, err = _safe_get_list(
        "Sales Invoice",
        filters={"docstatus": 0},
        fields=["grand_total", "outstanding_amount", "customer", "posting_date"],
    )
    if err:
        warnings.append(err)

    sales_orders, err = _safe_get_list(
        "Sales Order",
        fields=["grand_total", "customer", "delivery_date", "status"],
    )
    if err:
        warnings.append(err)

    total_invoiced = sum(inv.get("grand_total", 0) for inv in submitted_invoices)
    total_outstanding = sum(inv.get("outstanding_amount", 0) for inv in submitted_invoices)
    total_so = sum(so.get("grand_total", 0) for so in sales_orders)

    return {
        "total_invoiced": total_invoiced,
        "total_outstanding": total_outstanding,
        "submitted_invoice_count": len(submitted_invoices),
        "draft_invoice_count": len(draft_invoices),
        "sales_order_count": len(sales_orders),
        "total_sales_order_value": total_so,
    }, warnings


def get_purchase_summary() -> dict:
    """Get purchase summary from Purchase Order.

    Returns:
        tuple: (dict with purchase summary, list of warnings)
    """
    warnings = []

    purchase_orders, err = _safe_get_list(
        "Purchase Order",
        fields=["grand_total", "supplier", "status"],
    )
    if err:
        warnings.append(err)

    total_po = sum(po.get("grand_total", 0) for po in purchase_orders)

    return {
        "purchase_order_count": len(purchase_orders),
        "total_purchase_order_value": total_po,
    }, warnings


def get_inventory_summary() -> dict:
    """Get inventory summary from Stock Entry and Item.

    Returns:
        tuple: (dict with inventory summary, list of warnings)
    """
    warnings = []

    items, err = _safe_get_list(
        "Item",
        fields=["name", "item_name", "item_group", "is_stock_item"],
    )
    if err:
        warnings.append(err)

    stock_items = [i for i in items if i.get("is_stock_item")]

    stock_entries, err = _safe_get_list(
        "Stock Entry",
        fields=["name", "stock_entry_type", "posting_date", "docstatus"],
    )
    if err:
        warnings.append(err)

    return {
        "total_items": len(items),
        "stock_items": len(stock_items),
        "stock_entry_count": len(stock_entries),
    }, warnings


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


def get_quotation_summary() -> dict:
    """Get quotation summary.

    Returns:
        tuple: (dict with quotation summary, list of warnings)
    """
    warnings = []

    quotations, err = _safe_get_list(
        "Quotation",
        fields=["name", "party_name", "transaction_date", "valid_till", "grand_total", "status"],
    )
    if err:
        warnings.append(err)

    total_quoted = sum(q.get("grand_total", 0) for q in quotations)

    return {
        "quotation_count": len(quotations),
        "total_quoted_value": total_quoted,
    }, warnings


def get_delivery_summary() -> dict:
    """Get delivery note summary.

    Returns:
        tuple: (dict with delivery summary, list of warnings)
    """
    warnings = []

    delivery_notes, err = _safe_get_list(
        "Delivery Note",
        fields=["name", "customer", "posting_date", "docstatus"],
    )
    if err:
        warnings.append(err)

    return {
        "delivery_note_count": len(delivery_notes),
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
