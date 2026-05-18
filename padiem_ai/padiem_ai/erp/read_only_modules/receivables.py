"""Receivables-domain read-only summary functions.

Extracted from read_only.py as part of the receivables-domain split (Issue #56).
Contains get_receivables_summary and get_payment_summary.
"""

from padiem_ai.erp.read_only_modules.utils import _safe_get_list


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
