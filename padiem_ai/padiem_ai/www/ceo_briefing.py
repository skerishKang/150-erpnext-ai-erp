"""CEO Briefing web route.

Provides a minimal web page at /ceo_briefing that displays the mock CEO briefing.
No external AI calls. No data modification.
"""

import frappe

from padiem_ai.briefing.mock_generator import generate_mock_ceo_briefing
from padiem_ai.erp.read_only import get_ceo_briefing_context


def get_context(context):
    """Get context for the CEO briefing web page.

    Args:
        context: Frappe web page context
    """
    context.title = "CEO Daily Briefing"
    context.no_cache = 1

    try:
        frappe.has_permission("Sales Invoice", "read", throw=True)
        erp_context = get_ceo_briefing_context()
        briefing = generate_mock_ceo_briefing(erp_context)
        context.briefing = briefing
        context.error = None
    except frappe.PermissionError:
        context.briefing = None
        context.error = "Sales Invoice 읽기 권한이 없습니다."
    except Exception as exc:
        frappe.log_error(title="CEO Briefing page error", message=frappe.get_traceback())
        context.briefing = None
        context.error = f"브리핑 생성 중 오류가 발생했습니다: {str(exc)}"
