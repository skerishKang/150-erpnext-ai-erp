import frappe


@frappe.whitelist()
def search(query: str = ""):
    """Natural-language ERP Query API endpoint.

    Accepts a Korean or English query and returns ERP data.
    This is a skeleton implementation — actual AI integration comes later.
    """
    return {
        "success": True,
        "data": {},
        "ai_summary": f"Query received: '{query}' — AI integration pending.",
        "timestamp": frappe.utils.now(),
    }
