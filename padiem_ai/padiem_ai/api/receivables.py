import frappe


@frappe.whitelist()
def get_receivables_summary():
    """Receivables Summary API endpoint.

    Returns outstanding receivables summary.
    This is a skeleton implementation — actual AI integration comes later.
    """
    frappe.has_permission("Sales Invoice", "read", throw=True)

    return {
        "success": True,
        "data": {},
        "ai_summary": "Receivables summary skeleton — AI integration pending.",
        "timestamp": frappe.utils.now(),
    }
