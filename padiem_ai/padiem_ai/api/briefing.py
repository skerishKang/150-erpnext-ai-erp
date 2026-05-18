"""CEO Daily Briefing API endpoint.

Reads ERPNext demo data via the read-only layer and returns structured summary.
No external AI calls. No data modification.
"""

import frappe

from padiem_ai.erp.read_only import get_ceo_briefing_context, get_demo_counts


def _require_ceo_briefing_read_permission():
    """Check that the current user has read permission on Sales Invoice."""
    frappe.has_permission("Sales Invoice", "read", throw=True)


@frappe.whitelist()
def get_ceo_briefing():
    """CEO Daily Briefing API endpoint.

    Returns structured ERP data summary for the CEO dashboard.
    Read-only access. No data modification. No external AI calls.
    """
    _require_ceo_briefing_read_permission()

    context = get_ceo_briefing_context()

    return {
        "success": True,
        "data": context,
        "ai_summary": "CEO Daily Briefing — read-only data layer active. AI integration pending.",
        "timestamp": frappe.utils.now(),
    }


@frappe.whitelist()
def get_counts():
    """Get demo data counts.

    Returns record counts for all demo DocTypes.
    Read-only access. Permission check required.
    """
    _require_ceo_briefing_read_permission()

    counts = get_demo_counts()

    return {
        "success": True,
        "data": counts,
        "timestamp": frappe.utils.now(),
    }
