"""Read-only ERP data access layer.

Provides structured summary data from ERPNext for CEO briefing and other features.
Uses frappe.get_all / frappe.get_list only. No inserts, updates, or deletes.
Respects ERPNext permissions.

No external AI API calls. No credentials stored or referenced.
"""

import frappe


def get_demo_counts() -> dict:
    """Get record counts for all demo DocTypes.

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
        try:
            counts[dt] = frappe.db.count(dt)
        except Exception:
            counts[dt] = 0

    return counts


def get_sales_summary() -> dict:
    """Get sales summary from Sales Invoice and Sales Order.

    Returns:
        dict: Sales summary with totals and counts
    """
    try:
        invoices = frappe.get_all(
            "Sales Invoice",
            filters={"docstatus": 1},
            fields=["grand_total", "outstanding_amount", "customer", "posting_date"],
        )
        submitted_invoices = invoices
    except Exception:
        submitted_invoices = []

    try:
        draft_invoices = frappe.get_all(
            "Sales Invoice",
            filters={"docstatus": 0},
            fields=["grand_total", "outstanding_amount", "customer", "posting_date"],
        )
    except Exception:
        draft_invoices = []

    try:
        sales_orders = frappe.get_all(
            "Sales Order",
            fields=["grand_total", "customer", "delivery_date", "status"],
        )
    except Exception:
        sales_orders = []

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
    }


def get_purchase_summary() -> dict:
    """Get purchase summary from Purchase Order.

    Returns:
        dict: Purchase summary with totals and counts
    """
    try:
        purchase_orders = frappe.get_all(
            "Purchase Order",
            fields=["grand_total", "supplier", "status"],
        )
    except Exception:
        purchase_orders = []

    total_po = sum(po.get("grand_total", 0) for po in purchase_orders)

    return {
        "purchase_order_count": len(purchase_orders),
        "total_purchase_order_value": total_po,
    }


def get_inventory_summary() -> dict:
    """Get inventory summary from Stock Entry and Item.

    Returns:
        dict: Inventory summary with item count and stock entry info
    """
    try:
        items = frappe.get_all("Item", fields=["name", "item_name", "item_group", "is_stock_item"])
        stock_items = [i for i in items if i.get("is_stock_item")]
    except Exception:
        items = []
        stock_items = []

    try:
        stock_entries = frappe.get_all(
            "Stock Entry",
            fields=["name", "stock_entry_type", "posting_date", "docstatus"],
        )
    except Exception:
        stock_entries = []

    return {
        "total_items": len(items),
        "stock_items": len(stock_items),
        "stock_entry_count": len(stock_entries),
    }


def get_receivables_summary() -> dict:
    """Get receivables summary from Sales Invoice.

    Returns:
        dict: Receivables summary with outstanding amounts
    """
    try:
        invoices = frappe.get_all(
            "Sales Invoice",
            filters={"outstanding_amount": (">", 0)},
            fields=["name", "customer", "outstanding_amount", "due_date", "posting_date"],
        )
    except Exception:
        invoices = []

    total_outstanding = sum(inv.get("outstanding_amount", 0) for inv in invoices)

    return {
        "outstanding_invoice_count": len(invoices),
        "total_outstanding": total_outstanding,
        "invoices": invoices,
    }


def get_quotation_summary() -> dict:
    """Get quotation summary.

    Returns:
        dict: Quotation summary with counts and status
    """
    try:
        quotations = frappe.get_all(
            "Quotation",
            fields=["name", "party_name", "transaction_date", "valid_till", "grand_total", "status"],
        )
    except Exception:
        quotations = []

    total_quoted = sum(q.get("grand_total", 0) for q in quotations)

    return {
        "quotation_count": len(quotations),
        "total_quoted_value": total_quoted,
    }


def get_delivery_summary() -> dict:
    """Get delivery note summary.

    Returns:
        dict: Delivery note summary with counts
    """
    try:
        delivery_notes = frappe.get_all(
            "Delivery Note",
            fields=["name", "customer", "posting_date", "docstatus"],
        )
    except Exception:
        delivery_notes = []

    return {
        "delivery_note_count": len(delivery_notes),
    }


def get_payment_summary() -> dict:
    """Get payment entry summary.

    Returns:
        dict: Payment entry summary with counts and totals
    """
    try:
        payments = frappe.get_all(
            "Payment Entry",
            fields=["name", "party", "paid_amount", "posting_date", "payment_type"],
        )
    except Exception:
        payments = []

    total_received = sum(p.get("paid_amount", 0) for p in payments if p.get("payment_type") == "Receive")
    total_paid = sum(p.get("paid_amount", 0) for p in payments if p.get("payment_type") == "Pay")

    return {
        "payment_count": len(payments),
        "total_received": total_received,
        "total_paid": total_paid,
    }


def get_ceo_briefing_context() -> dict:
    """Get structured context for CEO Daily Briefing.

    Returns:
        dict: Complete briefing context with counts, sales, purchases,
              inventory, receivables, quotations, deliveries, payments, and warnings.
    """
    counts = get_demo_counts()
    sales = get_sales_summary()
    purchases = get_purchase_summary()
    inventory = get_inventory_summary()
    receivables = get_receivables_summary()
    quotations = get_quotation_summary()
    deliveries = get_delivery_summary()
    payments = get_payment_summary()

    warnings = []
    if receivables["outstanding_invoice_count"] > 0:
        warnings.append(
            f"{receivables['outstanding_invoice_count']}건의 미수금 invoices "
            f"(총 {receivables['total_outstanding']:,.0f}원)"
        )
    if counts.get("Sales Order", 0) > 0:
        warnings.append(f"{counts['Sales Order']}건의 Sales Order 진행 중")

    return {
        "counts": counts,
        "sales": sales,
        "purchases": purchases,
        "inventory": inventory,
        "receivables": receivables,
        "quotations": quotations,
        "deliveries": deliveries,
        "payments": payments,
        "warnings": warnings,
    }
