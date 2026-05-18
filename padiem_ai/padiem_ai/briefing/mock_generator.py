"""Mock CEO Briefing Generator.

Converts read-only ERP context into a deterministic Korean CEO briefing.
No external AI calls. No data modification.

Usage:
    from padiem_ai.briefing.mock_generator import generate_mock_ceo_briefing
    from padiem_ai.erp.read_only import get_ceo_briefing_context

    context = get_ceo_briefing_context()
    briefing = generate_mock_ceo_briefing(context)
"""


def format_currency_krw(value) -> str:
    """Format a number as Korean Won currency string.

    Args:
        value: Numeric value to format

    Returns:
        str: Formatted currency string (e.g., "108,800,000원")
    """
    if value is None:
        return "0원"
    try:
        return f"{int(value):,}원"
    except (ValueError, TypeError):
        return "0원"


def format_count(value, label: str) -> str:
    """Format a count with a Korean label.

    Args:
        value: Count value
        label: Korean label (e.g., "건", "개")

    Returns:
        str: Formatted count string (e.g., "5건")
    """
    if value is None:
        return f"0{label}"
    try:
        return f"{int(value)}{label}"
    except (ValueError, TypeError):
        return f"0{label}"


def generate_briefing_sections(context: dict) -> list:
    """Generate briefing sections from ERP context.

    Args:
        context: Dictionary from get_ceo_briefing_context()

    Returns:
        list: List of section dictionaries with 'title' and 'content'
    """
    sections = []

    # Section 1: Sales
    sales = context.get("sales", {})
    sales_lines = []
    sales_lines.append(f"Sales Order: {format_count(sales.get('sales_order_count', 0), '건')} (총 {format_currency_krw(sales.get('total_sales_order_value', 0))})")
    sales_lines.append(f"Sales Invoice (제출): {format_count(sales.get('submitted_invoice_count', 0), '건')}")
    sales_lines.append(f"Sales Invoice (임시저장): {format_count(sales.get('draft_invoice_count', 0), '건')}")
    if sales.get("total_invoiced", 0) > 0:
        sales_lines.append(f"청구 총액: {format_currency_krw(sales.get('total_invoiced', 0))}")
    sections.append({"title": "매출 현황", "content": "\n".join(sales_lines)})

    # Section 2: Purchases
    purchases = context.get("purchases", {})
    purchase_lines = []
    purchase_lines.append(f"Purchase Order: {format_count(purchases.get('purchase_order_count', 0), '건')} (총 {format_currency_krw(purchases.get('total_purchase_order_value', 0))})")
    sections.append({"title": "구매 현황", "content": "\n".join(purchase_lines)})

    # Section 3: Receivables & Payments
    receivables = context.get("receivables", {})
    payments = context.get("payments", {})
    recv_lines = []
    recv_lines.append(f"미수금: {format_count(receivables.get('outstanding_invoice_count', 0), '건')} (총 {format_currency_krw(receivables.get('total_outstanding', 0))})")
    recv_lines.append(f"입금: {format_currency_krw(payments.get('total_received', 0))}")
    if payments.get("total_paid", 0) > 0:
        recv_lines.append(f"지급: {format_currency_krw(payments.get('total_paid', 0))}")
    sections.append({"title": "미수금 및 입금 현황", "content": "\n".join(recv_lines)})

    # Section 4: Inventory & Operations
    inventory = context.get("inventory", {})
    quotations = context.get("quotations", {})
    deliveries = context.get("deliveries", {})
    inv_lines = []
    inv_lines.append(f"전체 품목: {format_count(inventory.get('total_items', 0), '개')} (재고 관리 대상: {format_count(inventory.get('stock_items', 0), '개')})")
    inv_lines.append(f"Stock Entry: {format_count(inventory.get('stock_entry_count', 0), '건')}")
    inv_lines.append(f"Quotation: {format_count(quotations.get('quotation_count', 0), '건')} (총 {format_currency_krw(quotations.get('total_quoted_value', 0))})")
    inv_lines.append(f"Delivery Note: {format_count(deliveries.get('delivery_note_count', 0), '건')}")
    sections.append({"title": "재고 및 운영 현황", "content": "\n".join(inv_lines)})

    # Section 5: Warnings
    warnings = context.get("warnings", [])
    if warnings:
        warning_lines = [f"- {w}" for w in warnings]
        sections.append({"title": "주의 사항", "content": "\n".join(warning_lines)})
    else:
        sections.append({"title": "주의 사항", "content": "현재 특이사항 없음"})

    return sections


def generate_mock_ceo_briefing(context: dict) -> dict:
    """Generate a deterministic Korean CEO briefing from ERP context.

    Args:
        context: Dictionary from get_ceo_briefing_context()

    Returns:
        dict: Briefing object with title, summary, sections, and raw_context
    """
    sections = generate_briefing_sections(context)

    # Generate summary line
    counts = context.get("counts", {})
    sales = context.get("sales", {})
    receivables = context.get("receivables", {})
    warnings = context.get("warnings", [])

    summary_parts = []
    summary_parts.append(f"고객 {format_count(counts.get('Customer', 0), '개사')}")
    summary_parts.append(f"공급업체 {format_count(counts.get('Supplier', 0), '개사')}")
    summary_parts.append(f"품목 {format_count(counts.get('Item', 0), '개')}")
    if sales.get("sales_order_count", 0) > 0:
        summary_parts.append(f"진행 중인 Sales Order {format_count(sales.get('sales_order_count', 0), '건')}")
    if receivables.get("outstanding_invoice_count", 0) > 0:
        summary_parts.append(f"미수금 {format_count(receivables.get('outstanding_invoice_count', 0), '건')}")
    if warnings:
        summary_parts.append(f"주의事项 {format_count(len(warnings), '건')}")

    summary = " / ".join(summary_parts)

    return {
        "title": "CEO Daily Briefing",
        "summary": summary,
        "sections": sections,
        "raw_context": context,
    }
