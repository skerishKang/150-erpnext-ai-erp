"""Read-only ERP data access layer.

Provides structured summary data from ERPNext for CEO briefing and other features.
Uses frappe.get_list, frappe.db.count, and frappe.db.get_value.

Permission note:
- frappe.get_list() (used in _safe_get_list_limited) is treated as the
  permission-aware list path.
- frappe.db.count() and frappe.db.get_value(..., fieldname="sum(...)") (used in
  _safe_count_records and _safe_sum_field) are aggregate helper paths and must
  not be relied on as the permission boundary. Callers must gate access at the
  endpoint level via frappe.has_permission() on each returned DocType.

No external AI API calls. No credentials stored or referenced.
"""

from .read_only_modules.utils import _safe_count_records
from .read_only_modules.constants import DEMO_COUNT_DOCTYPES
from .read_only_modules.sales import (
    get_sales_summary,
    get_quotation_summary,
    get_delivery_summary,
)
from .read_only_modules.inventory import get_inventory_summary
from .read_only_modules.purchasing import get_purchase_summary
from .read_only_modules.receivables import (
    get_receivables_summary,
    get_payment_summary,
)
from .read_only_modules.context import get_ceo_briefing_context


def get_demo_counts() -> dict:
    """Get record counts for all demo DocTypes using the read-only count helper.

    Returns:
        dict: DocType name -> record count
    """
    counts = {}
    for dt in DEMO_COUNT_DOCTYPES:
        counts[dt] = _safe_count_records(dt)

    return counts
