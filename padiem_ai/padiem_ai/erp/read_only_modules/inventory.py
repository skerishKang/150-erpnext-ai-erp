"""Inventory-domain read-only summary functions.

Extracted from read_only.py as part of the inventory-domain split (Issue #52).
Contains get_inventory_summary.

Record policy:
- Item totals and stock item counts are all-record catalog summaries.
- Stock Entry count remains an all-record operational summary until a
  runtime/product decision narrows it to submitted records.
"""

from padiem_ai.erp.read_only_modules.utils import _safe_count_records


def get_inventory_summary() -> dict:
    """Get inventory summary from Stock Entry and Item.

    Returns:
        tuple: (dict with inventory summary, list of warnings)
    """
    warnings = []

    total_items = _safe_count_records("Item")
    stock_items = _safe_count_records("Item", filters={"is_stock_item": 1})
    stock_entry_count = _safe_count_records("Stock Entry")

    return {
        "total_items": total_items,
        "stock_items": stock_items,
        "stock_entry_count": stock_entry_count,
    }, warnings
