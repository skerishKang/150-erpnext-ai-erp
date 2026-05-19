"""Tests for shared ERP permission helpers."""

import unittest

from frappe_stub import ensure_app_path, install_frappe_stub

ensure_app_path()
frappe = install_frappe_stub()

from padiem_ai.erp.permissions import require_ceo_briefing_read_permission  # noqa: E402
from padiem_ai.erp.read_only_modules.constants import CEO_BRIEFING_READ_DOCTYPES  # noqa: E402


class PermissionHelperTests(unittest.TestCase):
    def test_require_ceo_briefing_read_permission_checks_all_doctypes(self):
        frappe.has_permission.reset_mock()

        require_ceo_briefing_read_permission()

        self.assertEqual(frappe.has_permission.call_count, len(CEO_BRIEFING_READ_DOCTYPES))
        checked_doctypes = [call.args[0] for call in frappe.has_permission.call_args_list]
        self.assertEqual(checked_doctypes, list(CEO_BRIEFING_READ_DOCTYPES))
        for call in frappe.has_permission.call_args_list:
            self.assertEqual(call.args[1], "read")
            self.assertEqual(call.kwargs, {"throw": True})


if __name__ == "__main__":
    unittest.main()
