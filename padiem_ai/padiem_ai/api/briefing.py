"""CEO Daily Briefing API endpoint.

Reads ERPNext demo data via the read-only layer, generates deterministic
mock briefing, and routes through the AI Provider Registry with config guard enforcement.
No external AI calls. No data modification.
"""

import frappe

from padiem_ai.ai.config import (
    assert_provider_allowed,
    get_provider_config_status,
    get_selected_provider_name,
)
from padiem_ai.ai.registry import get_provider
from padiem_ai.briefing.mock_generator import generate_mock_ceo_briefing
from padiem_ai.erp.read_only import get_ceo_briefing_context, get_demo_counts


def _require_ceo_briefing_read_permission():
    """Check that the current user has read permission on Sales Invoice."""
    frappe.has_permission("Sales Invoice", "read", throw=True)


@frappe.whitelist()
def get_ceo_briefing():
    """CEO Daily Briefing API endpoint.

    Flow:
    1. Require Sales Invoice read permission
    2. Read ERP context
    3. Generate deterministic briefing
    4. Get selected provider name from config
    5. Assert provider is allowed (config guard)
    6. Resolve provider through registry
    7. Call mock provider only
    8. Return provider config status

    Read-only access. No data modification. No external AI calls.
    """
    _require_ceo_briefing_read_permission()

    # Step 1: Read ERP data
    context = get_ceo_briefing_context()

    # Step 2: Generate deterministic briefing
    briefing = generate_mock_ceo_briefing(context)

    # Step 3: Get selected provider and enforce config guard
    provider_name = get_selected_provider_name()
    provider_config = get_provider_config_status(provider_name)
    assert_provider_allowed(provider_name)

    # Step 4: Resolve provider through registry and call
    provider = get_provider(provider_name)
    provider_health = provider.health_check()
    provider_summary = provider.summarize(context=briefing, prompt_template="ceo_daily_briefing")

    provider_info = {
        "name": provider.get_provider_name(),
        "status": provider_health.get("status", "unknown"),
        "external_call": False,
    }

    provider_response = {
        "summary": provider_summary,
        "model": provider.get_provider_name(),
        "source": "provider_registry",
    }

    return {
        "success": True,
        "data": context,
        "briefing": briefing,
        "provider": provider_info,
        "provider_config": provider_config,
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
