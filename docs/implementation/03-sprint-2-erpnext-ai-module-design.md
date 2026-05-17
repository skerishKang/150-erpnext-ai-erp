# Sprint 2: ERPNext AI Module Design

**Status:** 📋 Planned

**Duration:** 1 sprint (5–7 days)

## Goal

Design the Padiem AI module architecture, define the AI provider abstraction, create prompt templates, and validate end-to-end data flow for the first demo scenario.

## Prerequisites

- ✅ Sprint 1 complete (ERPNext running locally)
- ✅ Sample company with customers, items, and at least one quotation created
- ✅ ERPNext REST API accessible and tested

## Tasks

### 1. Define AI Module Structure
- [ ] Create custom Frappe app scaffolding (`padiem_ai`)
- [ ] Define app structure: `hooks.py`, `padiem_ai/api/`, `padiem_ai/ai_adapter/`
- [ ] Configure Frappe hooks for scheduled events and API endpoints

### 2. Build AI Provider Adapter
- [ ] Implement abstract base class: `AIProvider`
- [ ] Implement DeepSeek adapter (via OpenRouter or direct API)
- [ ] Implement mock/provider for offline testing
- [ ] Add configuration via Frappe Site Config or custom doctype
- [ ] Implement retry logic, rate limiting, and error handling

### 3. Create Prompt Templates
- [ ] Define template storage (doctype or file-based)
- [ ] Create template for: CEO daily briefing
- [ ] Create template for: quotation draft from description
- [ ] Create template for: sales summary
- [ ] Create template for: inventory alert

### 4. Build ERP Data Retrieval Module
- [ ] Implement data collectors for: Quotation, Sales Order, Delivery Note, Item
- [ ] Build context builder (ERP data → AI prompt context)
- [ ] Validate context size stays within token limits

### 5. Implement AI-Generated Output Handling
- [ ] Define structured output contracts (JSON schema per task)
- [ ] Implement output validator (ensure AI returns valid data)
- [ ] Implement human approval workflow UI concept

### 6. Create Audit Log
- [ ] Design audit log doctype: AI action, user, timestamp, prompt, response, approval
- [ ] Implement audit logging in the AI adapter

## Verification Criteria

- [ ] AI adapter can call DeepSeek and return structured response
- [ ] CEO briefing prompt returns valid summary with real ERP data
- [ ] Quotation prompt can generate draft from item description
- [ ] Audit log records each AI action
- [ ] Mock provider works without internet for development

## API Endpoints (Design)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/method/padiem_ai.api.generate_briefing` | POST | Generate CEO daily briefing |
| `/api/method/padiem_ai.api.draft_quotation` | POST | Draft quotation from description |
| `/api/method/padiem_ai.api.summarize_sales` | POST | Summarize sales period |
| `/api/method/padiem_ai.api.inventory_alert` | POST | Generate inventory alert |

## Non-Goals (this sprint)

- ❌ Do not deploy to cloud yet
- ❌ Do not build front-end CEO dashboard
- ❌ Do not polish UI
- ❌ Do not handle real customer data
