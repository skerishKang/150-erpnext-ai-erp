import frappe


@frappe.whitelist()
def get_accountant_package():
    """Accountant Package Status API endpoint.

    Returns month-end document preparation status.
    This is a skeleton implementation — actual AI integration comes later.
    """
    frappe.has_permission("Sales Invoice", "read", throw=True)

    return {
        "success": True,
        "data": {},
        "ai_summary": "Accountant package skeleton — AI integration pending.",
        "timestamp": frappe.utils.now(),
    }
