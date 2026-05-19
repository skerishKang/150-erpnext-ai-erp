"""Read-only ERP shared query utilities.

Extracted from read_only.py to reduce file size and improve modularity.
Provides helper functions for safe ERPNext data access.
"""

import frappe


def _count_records(doctype: str) -> int:
    """Count records using frappe.get_list (not frappe.db.count).

    Args:
        doctype: DocType name

    Returns:
        int: Record count
    """
    return len(frappe.get_list(doctype, fields=["name"], limit_page_length=0))


def _safe_get_list(doctype: str, fields: list = None, filters: dict = None) -> tuple:
    """Safe wrapper around frappe.get_list that logs errors instead of hiding them.

    Args:
        doctype: DocType name
        fields: Fields to fetch
        filters: Filters to apply

    Returns:
        tuple: (results_list, error_message_or_None)
    """
    try:
        results = frappe.get_list(
            doctype,
            fields=fields or ["name"],
            filters=filters,
            limit_page_length=0,
        )
        return results, None
    except Exception as exc:
        frappe.log_error(
            title=f"Read-only ERP query failed: {doctype}",
            message=frappe.get_traceback(),
        )
        return [], f"{doctype} 데이터를 불러오지 못했습니다"
