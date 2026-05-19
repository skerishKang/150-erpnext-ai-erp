"""Purchasing-domain read-only summary functions.

Extracted from read_only.py as part of the purchasing-domain split (Issue #54).
Contains get_purchase_summary.

Record policy:
- Purchase Order count and total remain all-record summaries until a
  runtime/product decision narrows them to submitted records.
"""

from padiem_ai.erp.read_only_modules.utils import (
    _safe_count_records,
    _safe_sum_field,
)


def get_purchase_summary() -> dict:
    """Get purchase summary from Purchase Order.

    Returns:
        tuple: (dict with purchase summary, list of warnings)
    """
    warnings = []

    purchase_order_count = _safe_count_records("Purchase Order")
    total_po = _safe_sum_field("Purchase Order", "grand_total")

    return {
        "purchase_order_count": purchase_order_count,
        "total_purchase_order_value": total_po,
    }, warnings
