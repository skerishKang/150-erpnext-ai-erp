"""CEO Briefing web route.

Provides a minimal web page at /ceo_briefing that displays the mock CEO briefing
with provider registry routing info. No external AI calls. No data modification.
"""

import frappe

from padiem_ai.ai.registry import get_provider
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

        # Step 1: Read ERP data
        erp_context = get_ceo_briefing_context()

        # Step 2: Generate deterministic briefing
        briefing = generate_mock_ceo_briefing(erp_context)

        # Step 3: Get provider info (mock only, no external call)
        provider = get_provider("mock")
        provider_health = provider.health_check()

        context.briefing = briefing
        context.provider_info = {
            "name": provider.get_provider_name(),
            "status": provider_health.get("status", "unknown"),
            "external_call": False,
        }
        context.error = None
    except frappe.PermissionError:
        context.briefing = None
        context.provider_info = None
        context.error = "Sales Invoice 읽기 권한이 없습니다."
    except Exception as exc:
        frappe.log_error(title="CEO Briefing page error", message=frappe.get_traceback())
        context.briefing = None
        context.provider_info = None
        context.error = f"브리핑 생성 중 오류가 발생했습니다: {str(exc)}"
