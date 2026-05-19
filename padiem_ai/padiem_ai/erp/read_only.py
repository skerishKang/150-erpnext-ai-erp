"""Read-only ERP data access layer.

Provides structured summary data from ERPNext for CEO briefing and other features.
Uses frappe.get_all / frappe.get_list only. No inserts, updates, or deletes.
Respects ERPNext permissions.

No external AI API calls. No credentials stored or referenced.
"""

from .read_only_modules.utils import _count_records
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
    """Get record counts for all demo DocTypes using frappe.get_list.

    Returns:
        dict: DocType name -> record count
    """
    counts = {}
    for dt in DEMO_COUNT_DOCTYPES:
        counts[dt] = _count_records(dt)

    return counts
