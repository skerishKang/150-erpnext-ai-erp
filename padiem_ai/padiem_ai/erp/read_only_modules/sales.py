"""Sales-domain read-only summary functions.

Extracted from read_only.py as part of the sales-domain split (Issue #50).
Contains get_sales_summary, get_quotation_summary, and get_delivery_summary.

Record policy:
- Sales Invoice totals use submitted invoices (`docstatus = 1`).
- Draft invoice count intentionally reports draft invoices (`docstatus = 0`).
- Sales Order, Quotation, and Delivery Note counts/totals remain all-record
  summaries until a runtime/product decision narrows them to submitted records.
"""

from padiem_ai.erp.read_only_modules.utils import (
    _safe_count_records,
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

    quotation_count = _safe_count_records("Quotation")
    total_quoted = _safe_sum_field("Quotation", "grand_total")

    return {
        "quotation_count": quotation_count,
        "total_quoted_value": total_quoted,
    }, warnings


def get_delivery_summary() -> dict:
    """Get delivery note summary.

    Returns:
        tuple: (dict with delivery summary, list of warnings)
    """
    warnings = []

    delivery_note_count = _safe_count_records("Delivery Note")

    return {
        "delivery_note_count": delivery_note_count,
    }, warnings
