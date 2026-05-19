"""Tests for the deterministic CEO briefing generator."""

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


def test_format_currency_krw_handles_invalid_values():
    assert format_currency_krw(108800000) == "108,800,000원"
    assert format_currency_krw(None) == "0원"
    assert format_currency_krw("not-a-number") == "0원"


def test_format_count_handles_invalid_values():
    assert format_count(3, "건") == "3건"
    assert format_count(None, "건") == "0건"
    assert format_count("not-a-number", "건") == "0건"


def test_generate_mock_ceo_briefing_shape():
    briefing = generate_mock_ceo_briefing(_sample_context())

    assert briefing["title"] == "CEO Daily Briefing"
    assert "summary" in briefing
    assert isinstance(briefing["sections"], list)
    assert len(briefing["sections"]) == 5
    assert briefing["raw_context"] == _sample_context()

    section_titles = [section["title"] for section in briefing["sections"]]
    assert "매출 현황" in section_titles
    assert "주의 사항" in section_titles
