"""CEO Daily Briefing API endpoint.

Reads ERPNext demo data via the read-only layer, generates deterministic
mock briefing, and routes through the AI Provider Registry (mock provider only).
No external AI calls. No data modification.
"""

import frappe

from padiem_ai.ai.registry import get_provider
from padiem_ai.briefing.mock_generator import generate_mock_ceo_briefing
from padiem_ai.erp.read_only import get_ceo_briefing_context, get_demo_counts


def _require_ceo_briefing_read_permission():
    """Check that the current user has read permission on Sales Invoice."""
    frappe.has_permission("Sales Invoice", "read", throw=True)


def _get_provider_info(provider_name: str = "mock") -> dict:
    """Get provider metadata without making external calls.

    Args:
        provider_name: Provider name (default: "mock")

    Returns:
        dict: Provider metadata
    """
    provider = get_provider(provider_name)
    health = provider.health_check()

    return {
        "name": provider.get_provider_name(),
        "status": health.get("status", "unknown"),
        "external_call": False,
    }


def _get_mock_provider_response(briefing: dict, provider_name: str = "mock") -> dict:
    """Get a mock provider response by passing briefing context to the mock provider.

    This does NOT call any external AI provider. It only exercises the
    provider registry path with the mock provider.

    Args:
        briefing: The deterministic briefing object
        provider_name: Provider name (default: "mock")

    Returns:
        dict: Mock provider response
    """
    provider = get_provider(provider_name)

    # Use the mock provider's summarize method
    summary_text = provider.summarize(
        context=briefing,
        prompt_template="ceo_daily_briefing",
    )

    return {
        "summary": summary_text,
        "model": provider.get_provider_name(),
        "source": "provider_registry",
    }


@frappe.whitelist()
def get_ceo_briefing():
    """CEO Daily Briefing API endpoint.

    Returns:
        - data: raw ERP context
        - briefing: deterministic mock briefing object
        - provider: provider metadata (mock only)
        - provider_response: mock provider response
        - ai_summary: disclaimer message
        - timestamp

    Read-only access. No data modification. No external AI calls.
    """
    _require_ceo_briefing_read_permission()

    # Step 1: Read ERP data
    context = get_ceo_briefing_context()

    # Step 2: Generate deterministic briefing
    briefing = generate_mock_ceo_briefing(context)

    # Step 3: Route through provider registry (mock only)
    provider_info = _get_provider_info("mock")
    provider_response = _get_mock_provider_response(briefing, "mock")

    return {
        "success": True,
        "data": context,
        "briefing": briefing,
        "provider": provider_info,
        "provider_response": provider_response,
        "ai_summary": "Mock provider response — no external AI call.",
        "timestamp": frappe.utils.now(),
    }


@frappe.whitelist()
def get_counts():
    """Get demo data counts.

    Returns record counts for all demo DocTypes.
    Read-only access. Permission check required.
    """
    _require_ceo_briefing_read_permission()

    counts = get_demo_counts()

    return {
        "success": True,
        "data": counts,
        "timestamp": frappe.utils.now(),
    }
