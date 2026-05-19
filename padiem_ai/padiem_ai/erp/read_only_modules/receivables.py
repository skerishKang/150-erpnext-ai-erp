"""Receivables-domain read-only summary functions.

Extracted from read_only.py as part of the receivables-domain split (Issue #56).
Contains get_receivables_summary and get_payment_summary.
"""

from padiem_ai.erp.read_only_modules.utils import (
    DEFAULT_READ_ONLY_LIMIT,
    _safe_count_records,
    _safe_get_list_limited,
    _safe_sum_field,
)


def get_receivables_summary() -> dict:
    """Get receivables summary from Sales Invoice.

    Returns:
        tuple: (dict with receivables summary, list of warnings)
    """
    warnings = []

    outstanding_filters = {"outstanding_amount": (">", 0)}

    outstanding_invoice_count = _safe_count_records(
        "Sales Invoice",
        filters=outstanding_filters,
    )

    total_outstanding = _safe_sum_field(
        "Sales Invoice",
        "outstanding_amount",
        filters=outstanding_filters,
    )

    invoices, err = _safe_get_list_limited(
        "Sales Invoice",
        filters=outstanding_filters,
        fields=["name", "customer", "outstanding_amount", "due_date", "posting_date"],
        limit=DEFAULT_READ_ONLY_LIMIT,
        order_by="due_date asc",
    )
    if err:
        warnings.append(err)

    return {
        "outstanding_invoice_count": outstanding_invoice_count,
        "total_outstanding": total_outstanding,
        "invoices": invoices,
    }, warnings


def get_payment_summary() -> dict:
    """Get payment entry summary.

    Returns:
        tuple: (dict with payment summary, list of warnings)
    """
    warnings = []

    payment_count = _safe_count_records("Payment Entry")
    total_received = _safe_sum_field(
        "Payment Entry", "paid_amount", filters={"payment_type": "Receive"}
    )
    total_paid = _safe_sum_field(
        "Payment Entry", "paid_amount", filters={"payment_type": "Pay"}
    )

    return {
        "payment_count": payment_count,
        "total_received": total_received,
        "total_paid": total_paid,
    }, warnings
