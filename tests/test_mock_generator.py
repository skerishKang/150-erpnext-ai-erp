"""Tests for the deterministic CEO briefing generator."""

import unittest

from frappe_stub import ensure_app_path

ensure_app_path()

from padiem_ai.briefing.mock_generator import (  # noqa: E402
    format_count,
    format_currency_krw,
    generate_mock_ceo_briefing,
)


def _sample_context():
    return {
        "counts": {"Customer": 2, "Supplier": 1, "Item": 3},
        "sales": {
            "sales_order_count": 1,
            "total_sales_order_value": 100000,
            "submitted_invoice_count": 2,
            "draft_invoice_count": 1,
            "total_invoiced": 50000,
        },
        "purchases": {"purchase_order_count": 1, "total_purchase_order_value": 30000},
        "inventory": {"total_items": 3, "stock_items": 2, "stock_entry_count": 1},
        "receivables": {"outstanding_invoice_count": 1, "total_outstanding": 20000},
        "quotations": {"quotation_count": 1, "total_quoted_value": 70000},
        "deliveries": {"delivery_note_count": 1},
        "payments": {"total_received": 40000, "total_paid": 10000},
        "warnings": ["1건의 미수금 invoices (총 20,000원)"],
    }


class MockGeneratorTests(unittest.TestCase):
    def test_format_currency_krw_handles_invalid_values(self):
        self.assertEqual(format_currency_krw(108800000), "108,800,000원")
        self.assertEqual(format_currency_krw(None), "0원")
        self.assertEqual(format_currency_krw("not-a-number"), "0원")

    def test_format_count_handles_invalid_values(self):
        self.assertEqual(format_count(3, "건"), "3건")
        self.assertEqual(format_count(None, "건"), "0건")
        self.assertEqual(format_count("not-a-number", "건"), "0건")

    def test_generate_mock_ceo_briefing_shape(self):
        briefing = generate_mock_ceo_briefing(_sample_context())

        self.assertEqual(briefing["title"], "CEO Daily Briefing")
        self.assertIn("summary", briefing)
        self.assertIsInstance(briefing["sections"], list)
        self.assertEqual(len(briefing["sections"]), 5)
        self.assertEqual(briefing["raw_context"], _sample_context())

        section_titles = [section["title"] for section in briefing["sections"]]
        self.assertIn("매출 현황", section_titles)
        self.assertIn("주의 사항", section_titles)


if __name__ == "__main__":
    unittest.main()
