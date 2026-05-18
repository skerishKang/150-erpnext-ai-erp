import frappe


@frappe.whitelist()
def get_ceo_briefing():
    """CEO Daily Briefing API endpoint.

    Returns a summary of today's key metrics.
    This is a skeleton implementation — actual AI integration comes later.
    """
    frappe.has_permission("Sales Invoice", "read", throw=True)

    return {
        "success": True,
        "data": {},
        "ai_summary": "CEO Daily Briefing skeleton — AI integration pending.",
        "timestamp": frappe.utils.now(),
    }
