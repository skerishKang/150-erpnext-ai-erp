# AI Module Architecture

## Overview

The AI module (`padiem_ai`) is a custom Frappe app that provides AI capabilities within ERPNext. It follows a clean layered architecture.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                    CEO Dashboard                         │
│           (Web Page / Frappe Custom Page)                │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                 AI API Endpoints                         │
│     /api/method/padiem_ai.api.*                          │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│              AI Service Layer                             │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Briefing    │  │  Quotation   │  │   Sales      │   │
│  │  Service     │  │  Draft Svc   │  │  Summary Svc  │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
│         │                 │                  │           │
│         └─────────────────┼──────────────────┘           │
│                           │                              │
│         ┌─────────────────▼─────────────────┐            │
│         │      AI Provider Adapter           │            │
│         │  (Abstract Interface)              │            │
│         └──┬──────────┬──────────┬──────────┘            │
│            │          │          │                       │
│  ┌─────────▼──┐ ┌────▼─────┐ ┌──▼──────────┐            │
│  │  DeepSeek  │ │  OpenAI  │ │  Mock/Local │            │
│  │  Adapter   │ │  Adapter │ │  Adapter    │            │
│  └────────────┘ └──────────┘ └─────────────┘            │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │         ERP Data Retrieval Layer                  │    │
│  │  Fetches data from ERPNext doctypes via Frappe    │    │
│  │  ORM, builds context for AI prompts               │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │         Audit Log                                 │    │
│  │  Records: user, action, prompt, response, time    │    │
│  └──────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## Component Details

### 1. AI API Endpoints
Frappe whitelisted methods that the CEO dashboard calls. Each endpoint:
- Receives input from the user (e.g., "Draft quotation for 50 units...")
- Calls the appropriate AI service
- Returns structured result to the dashboard

### 2. AI Service Layer
Business logic for each AI capability:

| Service | Input | Output | ERP Action |
|---------|-------|--------|------------|
| Briefing | None (uses context) | Structured briefing (sales, orders, inventory, receivables) | None (read-only) |
| Quotation Draft | Natural language description | Draft Quotation JSON | Creates ERPNext Quotation on approval |
| Sales Summary | Period (date range) | Sales report with AI analysis | None (read-only) |
| Inventory Alert | None (uses context) | Low-stock items list | None (read-only) |

### 3. AI Provider Adapter
Abstract interface with concrete implementations:

```python
class AIProvider:
    def generate(self, prompt: str, context: dict, schema: dict) -> dict:
        """Send prompt to AI provider and return structured response."""
        pass

    def validate_response(self, response: dict, schema: dict) -> bool:
        """Validate AI response against expected schema."""
        pass
```

- **DeepSeekAdapter:** Calls DeepSeek via OpenRouter API
- **OpenAIAdapter:** Calls OpenAI GPT models
- **MockAdapter:** Returns predefined responses for offline development

### 4. ERP Data Retrieval Layer
Collects data from ERPNext doctypes and builds context:

```python
class BriefingContextBuilder:
    def build(self, company: str) -> dict:
        return {
            "today_orders": self.get_today_orders(company),
            "pending_quotations": self.get_pending_quotations(company),
            "low_stock_items": self.get_low_stock_items(company),
            "overdue_receivables": self.get_overdue_receivables(company),
        }
```

### 5. Audit Log
Every AI interaction is logged:

| Field | Description |
|-------|-------------|
| user | Who triggered the action |
| action | Briefing, draft, summary, alert |
| prompt | Full prompt sent to AI |
| response | Full response from AI |
| approved | Whether human approved |
| erp_document | Created ERPNext document ID (if any) |
| timestamp | When the action occurred |

## Prompt Template Format

```json
{
  "name": "ceo_daily_briefing",
  "version": "1.0",
  "system_prompt": "You are a CEO operations assistant...",
  "user_prompt_template": "Today's ERP data: {{context}}",
  "output_schema": {
    "type": "object",
    "properties": {
      "summary": {"type": "string"},
      "orders": {"type": "array", "items": {"type": "object"}},
      "alerts": {"type": "array", "items": {"type": "string"}}
    }
  },
  "temperature": 0.3,
  "max_tokens": 2000
}
```

## Security

- All AI actions require authenticated Frappe session
- AI provider API keys stored in Frappe Site Config (not in DB or code)
- Human approval required before any ERP document creation
- AI responses validated against schema before use
- Rate limiting on AI API endpoints (configurable)
