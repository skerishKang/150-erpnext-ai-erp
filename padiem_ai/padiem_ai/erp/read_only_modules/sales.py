"""Sales-domain read-only summary functions.

Extracted from read_only.py as part of the sales-domain split (Issue #50).
Contains get_sales_summary, get_quotation_summary, and get_delivery_summary.
"""

from padiem_ai.erp.read_only_modules.utils import (
    _safe_count_records,
    _safe_get_list,
    _safe_sum_field,
)


def get_sales_summary() -> dict:
    """Get sales summary from Sales Invoice and Sales Order.

    Returns:
        tuple: (dict with sales summary, list of warnings)
    """
    warnings = []

    submitted_invoice_count = _safe_count_records(
        "Sales Invoice", filters={"docstatus": 1}
    )
    draft_invoice_count = _safe_count_records(
        "Sales Invoice", filters={"docstatus": 0}
    )
    sales_order_count = _safe_count_records("Sales Order")

    total_invoiced = _safe_sum_field(
        "Sales Invoice", "grand_total", filters={"docstatus": 1}
    )
    total_outstanding = _safe_sum_field(
        "Sales Invoice", "outstanding_amount", filters={"docstatus": 1}
    )
    total_so = _safe_sum_field("Sales Order", "grand_total")

    return {
        "total_invoiced": total_invoiced,
        "total_outstanding": total_outstanding,
        "submitted_invoice_count": submitted_invoice_count,
        "draft_invoice_count": draft_invoice_count,
        "sales_order_count": sales_order_count,
        "total_sales_order_value": total_so,
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
