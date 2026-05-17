# Sprint 3: First Demo Scenario

**Status:** 📋 Planned

**Duration:** 1 sprint (5–7 days)

## Goal

Build an end-to-end demo scenario that shows the core value of Padiem AI ERP to a CEO.

## Demo Scenario

### Scenario Name
"CEO Daily Operations Briefing with AI Quotation Draft"

### User Story
> As a CEO of a small trading company,
> I want to see today's sales status and ask the AI to draft a quotation,
> So that I can make decisions faster and reduce manual work.

### Flow

```
1. CEO logs into Padiem AI ERP dashboard
2. Dashboard shows:
   - Today's orders received
   - Pending quotations
   - Low inventory alerts
   - Recent receivables
3. CEO clicks "AI Briefing"
4. AI generates a daily operations summary:
   - "You received 3 orders today worth ₩4,200,000"
   - "2 quotations are pending customer response"
   - "Item A (SKU-001) is below minimum stock"
5. CEO types: "Draft a quotation for 50 units of Item A to Customer B"
6. AI drafts quotation with:
   - Customer B info auto-filled
   - Item A at standard price
   - Delivery terms
7. CEO reviews, adjusts, and confirms
8. System creates ERPNext Quotation document
9. Activity logged in audit trail
```

## Tasks

### 1. Build CEO Dashboard (Minimal)
- [ ] Simple dashboard page in ERPNext (Web Page or Custom Page)
- [ ] Display key metrics: orders, quotations, inventory, receivables
- [ ] "AI Briefing" button

### 2. Implement AI Briefing
- [ ] Connect to AI provider adapter
- [ ] Gather ERP data for briefing context
- [ ] Generate and display briefing HTML
- [ ] Handle errors gracefully

### 3. Implement AI Quotation Draft
- [ ] Natural language input (text)
- [ ] Parse request: customer, item, quantity
- [ ] Call AI to draft quotation JSON
- [ ] Auto-fill ERPNext Quotation form
- [ ] CEO reviews and confirms
- [ ] On confirm, save as ERPNext Quotation document

### 4. Polish Demo Flow
- [ ] Demo mode with sample data
- [ ] Consistent error handling
- [ ] Fallback when AI provider is unavailable
- [ ] Reset demo data capability

### 5. Test the Full Scenario
- [ ] Run end-to-end test
- [ ] Verify ERPNext document created correctly
- [ ] Verify audit log entries
- [ ] Verify rollback (delete test data)

## Verification Criteria

- [ ] CEO briefing generates with real-time ERP data
- [ ] AI quotation draft creates valid ERPNext Quotation
- [ ] Human approval step works before saving
- [ ] Full flow runs without errors on local setup
- [ ] Demo can be reset for repeated presentations

## Demo Script

```
1. Open browser → Padiem AI ERP Dashboard
2. "Show me today's briefing" → AI generates summary
3. "Draft quotation for 50 units of Item A for Customer B"
4. Review quotation details
5. Click Confirm → Quotation saved in ERPNext
6. Open ERPNext → Quotation list → See the new quotation
```

## Non-Goals (this sprint)

- ❌ Do not deploy to cloud
- ❌ Do not build production UI
- ❌ Do not handle real customer data
- ❌ Do not implement voice input (save for later sprint)
- ❌ Do not implement mobile app
