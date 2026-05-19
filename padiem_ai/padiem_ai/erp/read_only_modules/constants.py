"""Read-only ERP shared constants.

Centralizes DocType lists and other constants used across
read-only modules to prevent duplication drift.
"""

DEMO_COUNT_DOCTYPES = (
    "Customer",
    "Supplier",
    "Item",
    "Quotation",
    "Sales Order",
    "Purchase Order",
    "Stock Entry",
    "Delivery Note",
    "Sales Invoice",
    "Payment Entry",
    "Warehouse",
)

CEO_BRIEFING_READ_DOCTYPES = DEMO_COUNT_DOCTYPES
