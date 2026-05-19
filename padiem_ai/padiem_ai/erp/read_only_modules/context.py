"""CEO briefing context orchestration module.

Provides get_ceo_briefing_context() by orchestrating domain summaries.
No external AI API calls.
"""

from .sales import (
    get_sales_summary,
    get_quotation_summary,
    get_delivery_summary,
)
from .inventory import get_inventory_summary
from .purchasing import get_purchase_summary
from .receivables import (
    get_receivables_summary,
    get_payment_summary,
)
from .utils import _count_records
from .constants import DEMO_COUNT_DOCTYPES


def get_ceo_briefing_context() -> dict:
    """Get structured context for CEO Daily Briefing.

    Returns:
        dict: Complete briefing context with counts, sales, purchases,
              inventory, receivables, quotations, deliveries, payments, and warnings.
    """
    all_warnings = []

    counts = {dt: _count_records(dt) for dt in DEMO_COUNT_DOCTYPES}

    sales, w = get_sales_summary()
    all_warnings.extend(w)

    purchases, w = get_purchase_summary()
    all_warnings.extend(w)

    inventory, w = get_inventory_summary()
    all_warnings.extend(w)

    receivables, w = get_receivables_summary()
    all_warnings.extend(w)

    quotations, w = get_quotation_summary()
    all_warnings.extend(w)

    deliveries, w = get_delivery_summary()
    all_warnings.extend(w)

    payments, w = get_payment_summary()
    all_warnings.extend(w)

    if receivables["outstanding_invoice_count"] > 0:
        all_warnings.append(
            f"{receivables['outstanding_invoice_count']}건의 미수금 invoices "
            f"(총 {receivables['total_outstanding']:,.0f}원)"
        )
    if counts.get("Sales Order", 0) > 0:
        all_warnings.append(f"{counts['Sales Order']}건의 Sales Order 진행 중")

    return {
        "counts": counts,
        "sales": sales,
        "purchases": purchases,
        "inventory": inventory,
        "receivables": receivables,
        "quotations": quotations,
        "deliveries": deliveries,
        "payments": payments,
        "warnings": all_warnings,
    }
