import frappe


@frappe.whitelist()
def draft(customer: str = "", items: str = ""):
    """Quotation Draft Assistant API endpoint.

    Generates a quotation draft based on natural language input.
    This is a skeleton implementation — actual AI integration comes later.
    """
    frappe.has_permission("Quotation", "read", throw=True)

    return {
        "success": True,
        "data": {},
        "ai_summary": "Quotation draft skeleton — AI integration pending.",
        "timestamp": frappe.utils.now(),
    }
