"""Read-only ERP shared query utilities.

Extracted from read_only.py to reduce file size and improve modularity.
Provides helper functions for safe ERPNext data access.
"""

import frappe

DEFAULT_READ_ONLY_LIMIT = 100


def _safe_count_records(doctype: str, filters: dict = None) -> int:
    """Count records using frappe.db.count (SQL COUNT).

    Falls back to frappe.get_list with limit_page_length=0 if
    frappe.db.count is unavailable.

    Permission note: frappe.db.count() is NOT permission-aware — it bypasses
    ERPNext's row-level permission system. Use endpoint-level permission gates.

    Args:
        doctype: DocType name
        filters: Optional filter dict

    Returns:
        int: Record count, or 0 on error
    """
    try:
        count_fn = getattr(frappe.db, "count")
    except AttributeError:
        count_fn = None

    if count_fn:
        try:
            return int(count_fn(doctype, filters=filters) or 0)
        except TypeError:
            # Older or test Frappe shims may not support the same count signature.
            pass
        except Exception:
            frappe.log_error(
                title=f"Read-only count failed: {doctype}",
                message=frappe.get_traceback(),
            )
            return 0

    try:
        return len(
            frappe.get_list(
                doctype,
                fields=["name"],
                filters=filters,
                limit_page_length=0,
            )
        )
    except Exception:
        frappe.log_error(
            title=f"Read-only count fallback failed: {doctype}",
            message=frappe.get_traceback(),
        )
        return 0


def _safe_sum_field(doctype: str, field: str, filters: dict = None) -> float:
    """Aggregate sum of a numeric field using SQL SUM.

    Uses frappe.db.get_value with aggregate function for efficiency.
    Does not fetch detail records.

    Permission note: frappe.db.get_value() is NOT permission-aware — it bypasses
    ERPNext's row-level permission system. Use endpoint-level permission gates.

    Args:
        doctype: DocType name
        field: Numeric field to sum (e.g., "grand_total")
        filters: Optional filter dict

    Returns:
        float: Sum of field values, or 0.0 on error / null result
    """
    try:
        result = frappe.db.get_value(
            doctype,
            filters=filters,
            fieldname=f"sum({field})",
        )
        return float(result or 0)
    except Exception:
        frappe.log_error(
            title=f"Read-only sum failed: {doctype}.{field}",
            message=frappe.get_traceback(),
        )
        return 0.0


def _safe_get_list_limited(
    doctype: str,
    fields: list = None,
    filters: dict = None,
    limit: int = DEFAULT_READ_ONLY_LIMIT,
    order_by: str = None,
) -> tuple:
    """Safe bounded wrapper around frappe.get_list with a default limit.

    Unlike the unbounded version, this helper bounds
    the result set to prevent unbounded queries in list-heavy contexts.

    Permission note: frappe.get_list() IS permission-aware — it respects
    ERPNext's row-level permission system and only returns records the
    current user can read.

    Args:
        doctype: DocType name
        fields: Fields to fetch. Defaults to ["name"].
        filters: Filters to apply. Passed as-is.
        limit: Max records. Falls back to DEFAULT_READ_ONLY_LIMIT if None,
            zero, negative, or non-integer.
        order_by: Optional ORDER BY clause (e.g. "modified desc").
            Only passed to frappe.get_list when provided.

    Returns:
        tuple: (results_list, error_message_or_None)
    """
    if not isinstance(limit, int) or limit <= 0:
        limit = DEFAULT_READ_ONLY_LIMIT

    try:
        kwargs = {
            "doctype": doctype,
            "fields": fields or ["name"],
            "filters": filters,
            "limit_page_length": limit,
        }
        if order_by:
            kwargs["order_by"] = order_by

        results = frappe.get_list(**kwargs)
        return results, None
    except Exception:
        frappe.log_error(
            title=f"Read-only bounded query failed: {doctype}",
            message=frappe.get_traceback(),
        )
        return [], f"{doctype} 데이터를 불러오지 못했습니다"
