"""Shared ERP permission helpers for read-only briefing access."""

import frappe

from padiem_ai.erp.read_only_modules.constants import CEO_BRIEFING_READ_DOCTYPES


def require_ceo_briefing_read_permission() -> None:
    """Require read permission for every DocType used by CEO briefing."""
    for doctype in CEO_BRIEFING_READ_DOCTYPES:
        frappe.has_permission(doctype, "read", throw=True)
