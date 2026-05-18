"""Purchasing-domain read-only summary functions.

Extracted from read_only.py as part of the purchasing-domain split (Issue #54).
Contains get_purchase_summary.
"""

from padiem_ai.erp.read_only_modules.utils import _safe_get_list


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
