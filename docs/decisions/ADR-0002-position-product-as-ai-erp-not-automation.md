# ADR-0002: Position Product as AI ERP, Not Generic AI Automation

**Status:** Accepted

**Date:** 2026-05-16

## Context

The product could be positioned in several ways:

1. **Generic AI automation** — "AI that automates your business processes" (competing with n8n, Zapier, custom GPTs)
2. **AI ERP** — "ERP with AI built in" (competing with Ecount, iU, Duzon, but AI-native)
3. **AI chatbot for ERP** — "Chat with your ERP data" (limited scope, low perceived value)

The Korean SME market has a clear mental model of what "ERP" means and what it costs. "Automation" is perceived as vague, optional, and hard to quantify ROI.

## Decision

Position the product as **Padiem AI ERP** — an AI-native ERP system, not generic automation.

AI must be **embedded inside ERP workflows**, not bolted on as a separate chatbot or automation tool.

## Rationale

- Korean SME decision-makers (CEOs) **understand and budget for ERP**. They do not budget for "AI automation."
- Ecount's success in Korea proves SMEs pay for **ERP as a managed cloud service** — but Ecount lacks AI.
- "AI ERP" differentiates from Ecount, iU, Duzon while staying in a familiar category.
- Embedding AI inside ERP workflows (quotation drafts, sales summaries, inventory alerts) makes AI **visible and valuable** in daily operations.
- Generic automation positioning invites comparison with free tools (n8n, Zapier free tier, custom GPTs).

## Consequences

**Positive:**
- Clear category positioning for sales and marketing
- Higher perceived value and willingness to pay
- Product roadmap remains focused on ERP workflows
- Customers self-select for the right use case

**Negative:**
- Must deliver genuine ERP depth, not just AI on top of spreadsheets
- Requires investment in ERP workflow understanding, not just AI engineering
- Sales cycle may be longer than pure-automation pitch

## Alternatives Considered

| Alternative | Reason against |
|-------------|----------------|
| Pure AI automation platform | Too vague, hard to communicate value, competes with free tools |
| AI chatbot for existing ERPs | Limited perceived value, no recurring ERP revenue |
| AI-powered Excel replacement | Undifferentiated, low price ceiling |

## Related Documents

- [Product Identity](../agents/01-principles/product-identity.md)
- [AI ERP Positioning](../agents/02-product/ai-erp-positioning.md)
- [Sales Positioning](../sales/00-sales-positioning.md)
