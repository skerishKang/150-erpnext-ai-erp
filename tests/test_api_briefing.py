"""Tests for CEO briefing API helpers and response shape."""

import unittest
from unittest.mock import MagicMock, patch

from frappe_stub import ensure_app_path, install_frappe_stub

ensure_app_path()
install_frappe_stub()

from padiem_ai.api import briefing as briefing_api  # noqa: E402


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


class ApiBriefingTests(unittest.TestCase):
    def test_without_raw_context_removes_only_raw_context(self):
        briefing = {
            "title": "CEO Daily Briefing",
            "summary": "ok",
            "sections": [],
            "raw_context": {"secret": "context"},
        }

        result = briefing_api._without_raw_context(briefing)

        self.assertEqual(
            result,
            {
                "title": "CEO Daily Briefing",
                "summary": "ok",
                "sections": [],
            },
        )

    def test_get_counts_uses_permission_gate_and_timestamp(self):
        with patch.object(briefing_api, "require_ceo_briefing_read_permission") as require_perm:
            with patch.object(briefing_api, "get_demo_counts", return_value={"Customer": 1}):
                result = briefing_api.get_counts()

        require_perm.assert_called_once_with()
        self.assertEqual(
            result,
            {
                "success": True,
                "data": {"Customer": 1},
                "timestamp": "2026-05-19 00:00:00",
            },
        )

    def test_get_ceo_briefing_omits_raw_context_from_briefing(self):
        provider = MagicMock()
        provider.health_check.return_value = {"status": "ok"}
        provider.summarize.return_value = "provider summary"
        provider.get_provider_name.return_value = "mock"

        generated_briefing = {
            "title": "CEO Daily Briefing",
            "summary": "summary",
            "sections": [],
            "raw_context": _SAMPLE_CONTEXT,
        }

        with patch.object(briefing_api, "require_ceo_briefing_read_permission") as require_perm:
            with patch.object(briefing_api, "get_ceo_briefing_context", return_value=_SAMPLE_CONTEXT):
                with patch.object(briefing_api, "generate_mock_ceo_briefing", return_value=generated_briefing):
                    with patch.object(briefing_api, "get_selected_provider_name", return_value="mock"):
                        with patch.object(briefing_api, "get_provider_config_status", return_value={"status": "ok"}):
                            with patch.object(briefing_api, "assert_provider_allowed") as assert_allowed:
                                with patch.object(briefing_api, "get_provider", return_value=provider):
                                    result = briefing_api.get_ceo_briefing()

        require_perm.assert_called_once_with()
        assert_allowed.assert_called_once_with("mock")
        self.assertTrue(result["success"])
        self.assertEqual(result["data"], _SAMPLE_CONTEXT)
        self.assertNotIn("raw_context", result["briefing"])
        self.assertFalse(result["provider"]["external_call"])
        self.assertEqual(result["provider_response"]["summary"], "provider summary")


if __name__ == "__main__":
    unittest.main()
