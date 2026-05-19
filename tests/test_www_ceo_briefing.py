"""Tests for the CEO briefing web route."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from frappe_stub import FrappePermissionError, ensure_app_path, install_frappe_stub

ensure_app_path()
frappe = install_frappe_stub()

from padiem_ai.www import ceo_briefing  # noqa: E402


_SAMPLE_CONTEXT = {
    "counts": {"Customer": 1, "Supplier": 1, "Item": 1},
    "sales": {"sales_order_count": 0},
    "purchases": {},
    "inventory": {},
    "receivables": {"outstanding_invoice_count": 0},
    "quotations": {},
    "deliveries": {},
    "payments": {},
    "warnings": [],
}


def test_web_context_success_uses_permission_gate_and_omits_raw_context():
    provider = MagicMock()
    provider.health_check.return_value = {"status": "ok"}
    provider.get_provider_name.return_value = "mock"
    generated_briefing = {
        "title": "CEO Daily Briefing",
        "summary": "summary",
        "sections": [],
        "raw_context": _SAMPLE_CONTEXT,
    }
    context = SimpleNamespace()

    with patch.object(ceo_briefing, "require_ceo_briefing_read_permission") as require_perm:
        with patch.object(ceo_briefing, "get_ceo_briefing_context", return_value=_SAMPLE_CONTEXT):
            with patch.object(ceo_briefing, "generate_mock_ceo_briefing", return_value=generated_briefing):
                with patch.object(ceo_briefing, "get_provider", return_value=provider):
                    ceo_briefing.get_context(context)

    require_perm.assert_called_once_with()
    assert context.title == "CEO Daily Briefing"
    assert context.no_cache == 1
    assert context.error is None
    assert "raw_context" not in context.briefing
    assert context.provider_info == {
        "name": "mock",
        "status": "ok",
        "external_call": False,
    }


def test_web_context_permission_error_is_generic():
    context = SimpleNamespace()

    with patch.object(
        ceo_briefing,
        "require_ceo_briefing_read_permission",
        side_effect=FrappePermissionError("Sales Invoice denied"),
    ):
        ceo_briefing.get_context(context)

    assert context.briefing is None
    assert context.provider_info is None
    assert context.error == "브리핑을 볼 권한이 없습니다."


def test_web_context_generic_error_is_sanitized_and_logged():
    context = SimpleNamespace()
    frappe.log_error.reset_mock()

    with patch.object(
        ceo_briefing,
        "require_ceo_briefing_read_permission",
        side_effect=RuntimeError("internal sql detail"),
    ):
        ceo_briefing.get_context(context)

    assert context.briefing is None
    assert context.provider_info is None
    assert context.error == "브리핑 생성 중 오류가 발생했습니다. 관리자에게 문의해 주세요."
    frappe.log_error.assert_called_once()
