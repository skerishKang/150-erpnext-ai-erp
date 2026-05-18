# Padiem AI

AI ERP for Korean SMEs — Frappe Custom App.

- App name: `padiem_ai`
- Product name: Padiem AI ERP
- ERPNext core: unmodified

## AI Provider Registry

**Active provider**: mock only (no external API calls)

**Placeholder providers** (registered, not implemented):
- kilocode
- opencodego
- nvidia
- deepseek
- mistral
- ollama

Placeholder providers return `NotImplementedError` on generate/summarize calls.
They never make external network calls.

## Status

- PR #20: manual skeleton created
- PR #21: Docker install verification pending
- External API calls: none
- Credentials: none

## API Endpoints (skeleton)

| Endpoint | Description |
|----------|-------------|
| `padiem_ai.api.briefing.get_ceo_briefing` | CEO Daily Briefing |
| `padiem_ai.api.query.search` | Natural-language ERP Query |
| `padiem_ai.api.quotation.draft` | Quotation Draft Assistant |
| `padiem_ai.api.receivables.get_receivables_summary` | Receivables Summary |
| `padiem_ai.api.delivery_stock.get_delivery_stock_summary` | Delivery & Stock Summary |
| `padiem_ai.api.accountant.get_accountant_package` | Accountant Package Status |
