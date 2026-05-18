"""Inventory-domain read-only summary functions.

Extracted from read_only.py as part of the inventory-domain split (Issue #52).
Contains get_inventory_summary.
"""

from padiem_ai.erp.read_only_modules.utils import _safe_get_list


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
