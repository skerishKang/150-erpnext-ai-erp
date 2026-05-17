# AI ERP Feature Specification v1

## Document Info

| Item | Value |
|------|-------|
| Version | 1.0 |
| Date | 2026-05-18 |
| Target | Padiem AI ERP First Demo |
| Scope | 6 AI features for Korean SME |
| Status | Draft |

---

## Core Principles

### What This Is

Padiem AI ERP is **not** a chatbot bolted onto ERP. It is an ERP system where AI is a **first-class feature inside the product**. Every AI capability below operates within the ERP UI, reads ERP data directly, and follows ERP workflows.

### What AI Does (v1)

- **Read** ERP data (query, search, filter)
- **Summarize** information (daily briefing, report prep)
- **Draft** documents (quotation, email, report)
- **Alert** on risks (overdue payments, delivery delays)

### What AI Does NOT Do (v1)

- **Modify** ERP data automatically (no auto-save, no auto-post)
- **Approve** workflows (no auto-approve)
- **Send** external communications (no auto-email, no auto-message)
- **Handle** accounting entries (no journal entries, no tax filing)
- **Process** payroll (no salary calculation, no tax withholding)
- **Make** financial decisions (no credit limit changes, no pricing changes)

### Human-in-the-Loop

Every AI output that could affect business decisions requires **explicit human approval** before becoming an ERP record. AI drafts; human decides.

---

## Feature 1: CEO Daily Briefing

### Feature Name

CEO Daily Briefing (CEO 브리핑)

### Customer Value

A CEO running a Korean SME spends 30-60 minutes every morning checking emails, spreadsheets, and ERP dashboards to understand what needs attention today. This feature replaces that with a single, AI-generated summary that highlights what matters: money coming in, orders at risk, and urgent tasks.

### ERPNext Data Used

| DocType | Fields |
|---------|--------|
| Sales Invoice | outstanding_amount, due_date, status, customer |
| Sales Order | delivery_date, status, customer, grand_total |
| Purchase Order | schedule_date, status, supplier, grand_total |
| Delivery Note | status, customer, posting_date |
| Payment Entry | posting_date, paid_amount, party |
| Stock Entry | posting_date, item_code, qty |

### Input

- No user input required
- Auto-generated based on current date
- Can optionally accept a date range

### Output

```
=== CEO Daily Briefing ===
Date: 2026-05-18 (Monday)

[Financial Summary]
- Today's expected receivables: 75,000,000 KRW (Seoul Build Corp)
- Overdue invoices: 1 (total: 45,000,000 KRW)
- Payments received this week: 38,800,000 KRW

[Operations Alert]
- Deliveries due this week: 2
  - SO-2026-005 (Gwangju Design Studio) - due 05/28
  - SO-2026-003 (Incheon Manufacturing) - due 06/05
- Purchase orders pending receipt: 2

[Action Items]
- Follow up: Seoul Build Corp overdue payment (SINV-2026-001)
- Review: Gwangju Design Studio delivery approaching deadline

[AI Note]
Seoul Build Corp has 45M KRW outstanding for 28 days (due 04/20). Consider sending a payment reminder.
```

### Screen Location

- **Primary**: ERPNext Desk homepage widget (top of page)
- **Secondary**: Notification bell (daily morning push)
- **Tertiary**: `/app/ai-briefing` dedicated page

### Human Approval Required

- No approval needed for viewing (read-only summary)
- Approval needed if user asks AI to "send reminder" or "create follow-up task"

### AI Must Not

- Auto-send payment reminders
- Auto-escalate overdue accounts
- Modify invoice or order data
- Share briefing with unauthorized users

### Demo Example

**Demo scenario**: CEO opens ERP at 9 AM, sees daily briefing widget.

**Demo flow**:
1. CEO logs into ERPNext
2. Homepage shows "CEO Daily Briefing" card
3. Card displays: "1 overdue invoice totaling 45M KRW. 1 delivery due this week."
4. CEO clicks "View Details" → expands to full breakdown
5. CEO clicks "Draft Reminder" → AI generates email draft for Seoul Build Corp
6. CEO reviews draft, edits, and clicks "Send" manually

---

## Feature 2: Natural-language ERP Query

### Feature Name

Natural-language ERP Query (자연어 ERP 조회)

### Customer Value

Korean SME employees are not ERP power users. They don't know DocType names, field names, or filter syntax. This feature lets them ask questions in plain Korean and get data back — no training required.

### ERPNext Data Used

| DocType | Example Query |
|---------|---------------|
| Customer | "서울 거래처 목록 보여줘" |
| Supplier | "철강 공급업체 연락처 알려줘" |
| Item | "재고 부족한 품목을 알려줘" |
| Sales Order | "이번 주 납기 예정인 주문 정리해줘" |
| Purchase Order | "아직 입고되지 않은 구매주문을 보여줘" |
| Stock Entry | "어제 창고 반입된 품목 보여줘" |
| Sales Invoice | "미수금 큰 거래처 순으로 정리해줘" |
| Payment Entry | "이번 달 입금 내역 보여줘" |

### Input

- Natural language query in Korean (or English)
- Examples:
  - "이번 달 미수금이 큰 거래처를 알려줘"
  - "Steel Beam 100mm 재고가 얼마야?"
  - "부산 고객사 리스트 보여줘"

### Output

- **Table format** for list queries (sortable, filterable)
- **Summary format** for aggregate queries (number + explanation)
- **Detail format** for single-record queries (field-by-field)
- Each response includes the **source DocType and filters used** (transparency)

### Screen Location

- **Primary**: Global search bar (top of ERPNext, `/app` level)
- **Secondary**: Chat panel (right sidebar, collapsible)
- **Tertiary**: Each module's header area ("Ask about Selling...")

### Human Approval Required

- No approval needed (read-only query)
- If query results in a suggested action (e.g., "create purchase order"), that action requires approval

### AI Must Not

- Return data the user doesn't have permission to see
- Cache or store query results externally
- Execute queries that modify data (DELETE, UPDATE)
- Expose internal ERPNext field names in responses

### Demo Example

**Demo scenario**: Sales manager needs to check overdue payments.

**Demo flow**:
1. Sales manager clicks search bar
2. Types: "이번 달 미수금 큰 거래처 보여줘"
3. AI returns table:
   | Customer | Invoice | Amount | Due Date | Days Overdue |
   |----------|---------|--------|----------|--------------|
   | Seoul Build Corp | SINV-2026-001 | 45,000,000 | 06/20 | - |
   | Busan Tech Solutions | SINV-2026-002 | 25,000,000 | 07/06 | - |
4. Sales manager clicks "Seoul Build Corp" → navigates to Customer page
5. AI shows: "Seoul Build Corp 총 미수금: 45,000,000 KRW"

---

## Feature 3: Quotation Draft Assistant

### Feature Name

Quotation Draft Assistant (견적서 초안 어시스턴트)

### Customer Value

Creating a quotation in ERP requires navigating multiple fields, selecting items, checking prices, and formatting. For a busy sales person, this takes 10-15 minutes per quotation. The AI assistant generates a complete draft from a brief description, saving time and reducing errors.

### ERPNext Data Used

| DocType | Purpose |
|---------|---------|
| Customer | Customer master data, contact info, payment terms |
| Item | Item codes, names, standard rates, UOM |
| Price List | Pricing rules, discounts |
| Quotation | Template structure, required fields |
| Sales Order | Historical orders for repeat customers |

### Input

- Natural language description of what to quote
- Example: "서울건설에 Steel Beam 500미터, LED 조명 30개 견적서 만들어줘"
- Can include: customer name, items, quantities, special notes

### Output

```
=== Quotation Draft ===
Customer: Seoul Build Corp
Date: 2026-05-18
Valid Until: 2026-06-18

Items:
1. Steel Beam 100mm - 500m × 150,000 KRW = 75,000,000 KRW
2. LED Light Fixture - 30 pcs × 120,000 KRW = 3,600,000 KRW

Subtotal: 78,600,000 KRW
Tax (10%): 7,860,000 KRW
Total: 86,460,000 KRW

Payment Terms: Net 30

[Review & Save] [Edit Draft] [Discard]
```

### Screen Location

- **Primary**: Selling module → "New Quotation" page (AI pre-fills form)
- **Secondary**: Chat panel → "Draft Quotation" command
- **Tertiary**: Customer page → "Create Quotation" button with AI assist

### Human Approval Required

- **Always**: Draft must be reviewed before saving as Quotation
- User clicks "Review & Save" → AI populates Quotation form → User confirms → Save
- User can edit any field before saving

### AI Must Not

- Save quotation without human confirmation
- Override price list rules
- Apply unauthorized discounts
- Send quotation to customer automatically
- Create quotations for blocked/inactive customers

### Demo Example

**Demo scenario**: Sales person needs to create a quotation quickly.

**Demo flow**:
1. Sales person opens Selling module
2. Clicks "New Quotation" → sees AI assistant prompt
3. Types: "인천제조에 알루미늄시트 300장, 스테인리스파이프 200미터 견적"
4. AI generates draft with correct items, prices, and customer info
5. Sales person reviews, adjusts quantity, clicks "Save"
6. Quotation QTN-2026-XXX created in ERPNext

---

## Feature 4: Receivables Summary

### Feature Name

Receivables Summary (미수금 요약)

### Customer Value

Managing accounts receivable is critical for SME cash flow. Instead of running complex reports, the AI provides a conversational summary of who owes money, how much, and how overdue — with suggested actions.

### ERPNext Data Used

| DocType | Fields |
|---------|--------|
| Sales Invoice | customer, grand_total, outstanding_amount, due_date, posting_date, status |
| Customer | customer_name, payment_terms, credit_limit |
| Payment Entry | posting_date, paid_amount, party, reference_name |

### Input

- Default: Current month's receivables
- Optional filters:
  - "서울 지역 거래처 미수금"
  - "30일 이상 연체된 건만"
  - "이번 분기 미수금 요약"

### Output

```
=== Receivables Summary ===
As of: 2026-05-18

[Overview]
Total Outstanding: 70,000,000 KRW
Invoices: 2
Overdue (>30 days): 1 (45,000,000 KRW, 28 days overdue)

[By Customer]
1. Seoul Build Corp: 45,000,000 KRW
   - SINV-2026-001: 45M (due 04/20, 30 days terms, 28 days overdue)
   - Last payment: 30M on 04/25 (partial)
   - Recommendation: Send payment reminder

2. Busan Tech Solutions: 25,000,000 KRW
   - SINV-2026-002: 25M (due 07/06, 45 days terms)
   - Status: Current (not yet due)
   - Recommendation: No action needed

[AI Insight]
Seoul Build Corp has consistently paid on time. Current overdue is unusual.
Consider a friendly follow-up call before formal reminder.
```

### Screen Location

- **Primary**: Accounts module → "Receivables Summary" widget
- **Secondary**: CEO Daily Briefing (overdue section)
- **Tertiary**: Customer page → "Receivables" tab with AI summary

### Human Approval Required

- No approval for viewing (read-only)
- Approval needed for: "Send reminder", "Create follow-up task", "Adjust credit limit"

### AI Must Not

- Auto-send payment reminders
- Modify invoice amounts or dates
- Write off bad debts
- Change credit limits
- Share receivables data with unauthorized users

### Demo Example

**Demo scenario**: CFO checks receivables before month-end.

**Demo flow**:
1. CFO opens Accounts module
2. Clicks "Receivables Summary" widget
3. AI displays: "Total outstanding: 70M KRW. Seoul Build Corp has 45M overdue."
4. CFO clicks "Send Reminder" → AI drafts email
5. CFO reviews email, edits tone, clicks "Send"
6. Follow-up task auto-created in ERPNext (with CFO approval)

---

## Feature 5: Delivery and Stock Summary

### Feature Name

Delivery and Stock Summary (배송 및 재고 요약)

### Customer Value

Warehouse managers and sales teams need to know: What's in stock? What's shipping today? What's at risk of delay? Instead of checking multiple reports, this feature provides a single view of delivery and inventory status.

### ERPNext Data Used

| DocType | Fields |
|---------|--------|
| Sales Order | item_code, qty, delivery_date, status, warehouse |
| Delivery Note | item_code, qty, posting_date, status, customer |
| Stock Entry | item_code, qty, source_warehouse, target_warehouse, posting_date |
| Item | item_name, item_group, stock_uom |
| Warehouse | warehouse_name, company |
| Bin | item_code, warehouse, actual_qty, reserved_qty |

### Input

- Default: Today's deliveries and current stock levels
- Optional filters:
  - "Steel Beam 재고 현황"
  - "이번 주 출하 예정 건"
  - "부산 창고 재고 보여줘"
  - "재고 부족한 품목을 알려줘"

### Output

```
=== Delivery & Stock Summary ===
Date: 2026-05-18

[Today's Shipments]
- DN-2026-003: Gwangju Design Studio
  Items: Wood Panel 80ea, LED Fixture 30ea
  Status: Ready to ship

[This Week's Deliveries Due]
- SO-2026-005: Gwangju Design Studio (due 05/28)
  Items: Wood Panel 80, LED Fixture 30
  Stock Status: Sufficient

[Stock Alerts]
- Steel Beam 100mm: 100m remaining (reorder point: 200m)
  → Consider placing purchase order

[Warehouse Summary]
| Warehouse | Items | Total Value |
|-----------|-------|-------------|
| Main Warehouse | 8 | 125,000,000 KRW |
| Busan Center | 1 | 25,000,000 KRW |
```

### Screen Location

- **Primary**: Stock module → "Delivery & Stock Summary" widget
- **Secondary**: Selling module → order fulfillment dashboard
- **Tertiary**: Warehouse page → AI summary tab

### Human Approval Required

- No approval for viewing (read-only)
- Approval needed for: "Create purchase order", "Transfer stock", "Expedite delivery"

### AI Must Not

- Auto-create purchase orders
- Auto-transfer stock between warehouses
- Modify stock levels
- Override reorder rules
- Ship items without proper documentation

### Demo Example

**Demo scenario**: Warehouse manager checks daily operations.

**Demo flow**:
1. Warehouse manager opens Stock module
2. Sees "Delivery & Stock Summary" widget
3. AI shows: "1 shipment ready today. Steel Beam stock low (100m vs 200m reorder point)."
4. Manager clicks "Create PO" → AI drafts purchase order for Steel Beam
5. Manager reviews PO, adjusts quantity, clicks "Save"
6. PO created in ERPNext, linked to supplier Korea Steel Distribution

---

## Feature 6: Accountant-ready Document Package Summary

### Feature Name

Accountant-ready Document Package Summary (회계사 자료 정리 요약)

### Customer Value

At month-end, Korean SMEs need to send invoices, receipts, and supporting documents to their accountant or tax advisor. This typically involves manually collecting PDFs, spreadsheets, and notes. This feature automatically summarizes what's needed and prepares a checklist.

### ERPNext Data Used (v1)

| DocType | Fields |
|---------|--------|
| Sales Invoice | posting_date, customer, grand_total, status, due_date |
| Purchase Invoice | posting_date, supplier, grand_total, status |
| Payment Entry | posting_date, paid_amount, party, mode_of_payment |
| Stock Entry | posting_date, item_code, qty, stock_entry_type |

### Future / Optional (Not v1)

| DocType | Fields |
|---------|--------|
| Journal Entry | posting_date, accounts, total_debit, total_credit |
| Expense Claim | posting_date, employee, total_claimed_amount |

### Input

- Default: Current month's documents
- Optional: "5월 회계사 자료 정리해줘" (specific month)

### Output

```
=== Accountant Document Package ===
Period: 2026-05-01 ~ 2026-05-31

[Sales Summary]
- Sales Invoices issued: 3
- Total sales: 108,800,000 KRW
- Payments received: 2 (38,800,000 KRW)
- Outstanding: 70,000,000 KRW

[Purchase Summary]
- Purchase Orders placed: 3
- Total purchases: 101,000,000 KRW (pending receipt)

[Stock Movements]
- Material Receipts: 3
- Material Issues: 1
- Material Transfers: 1

[Document Checklist]
✓ Sales Invoices (3): SINV-2026-001, SINV-2026-002, SINV-2026-003
✓ Purchase Orders (3): PO-2026-001, PO-2026-002, PO-2026-003
✓ Payment Entries (2): PE-2026-001, PE-2026-002
✓ Stock Entries (5): STE-2026-001 ~ STE-2026-005

[Notes for Accountant]
- Seoul Build Corp partial payment (30M of 75M) — clarify allocation
- No journal entries this month
- No expense claims this month

[Export Options]
[Download PDF Summary] [Export Excel] [Email to Accountant]
```

### Screen Location

- **Primary**: Accounts module → "Month-End Package" button
- **Secondary**: Reports → "Accountant Summary" custom report
- **Tertiary**: CEO Daily Briefing (month-end reminder)

### Human Approval Required

- No approval for viewing/generating summary
- Approval needed for: "Email to Accountant" (review before sending)
- Approval needed for: "Export" (confirm data completeness)

### AI Must Not

- Send documents to accountant automatically
- Modify any accounting entries
- Make tax calculations or filings
- Generate journal entries
- Access payroll or salary data

### Demo Example

**Demo scenario**: Office manager prepares month-end package for accountant.

**Demo flow**:
1. Office manager opens Accounts module
2. Clicks "Month-End Package"
3. AI generates summary with document checklist
4. Manager reviews checklist, confirms all documents present
5. Manager clicks "Export Excel" → downloads summary spreadsheet
6. Manager clicks "Email to Accountant" → AI drafts email with attachments
7. Manager reviews email, adds notes, clicks "Send"

---

## Feature Comparison Matrix

| Feature | Read | Summarize | Draft | Alert | Auto-Save |
|---------|------|-----------|-------|-------|-----------|
| CEO Daily Briefing | ✓ | ✓ | - | ✓ | ✗ |
| Natural-language Query | ✓ | - | - | - | ✗ |
| Quotation Draft Assistant | ✓ | - | ✓ | - | ✗ |
| Receivables Summary | ✓ | ✓ | - | ✓ | ✗ |
| Delivery & Stock Summary | ✓ | ✓ | - | ✓ | ✗ |
| Accountant Package | ✓ | ✓ | - | - | ✗ |

**Legend**: ✓ = AI does this, - = Not applicable, ✗ = Explicitly prohibited

---

## Non-Goals (Explicitly Excluded from v1)

### Accounting Automation

- No automatic journal entries
- No automatic bank reconciliation
- No automatic tax filing
- No automatic depreciation calculation

### Payroll

- No salary calculation
- No tax withholding
- No leave management
- No attendance tracking

### External Communication

- No auto-sending emails
- No auto-sending SMS
- No auto-posting to external services
- No auto-generating tax invoices (세금계산서)

### Data Modification

- No auto-saving any AI-generated content
- No auto-approving workflows
- No auto-updating stock levels
- No auto-changing prices or discounts

---

## Technical Constraints

### AI Provider

- Initial candidate: DeepSeek via OpenAI-compatible provider
- Provider layer must be configurable and vendor-agnostic
- Future providers: Mistral, OpenAI, Claude, Gemini, local models, Ollama-compatible models
- No provider-specific API key or credential should be committed

### Data Privacy

- All AI queries run within ERPNext server context
- No customer data sent to external AI without explicit configuration
- Audit log for all AI interactions
- Role-based access: AI respects ERPNext permission rules

### Performance

- Daily briefing: Generated once per day (cached)
- Query response: < 5 seconds
- Quotation draft: < 10 seconds
- Summary generation: < 15 seconds

### Language

- Primary: Korean
- Secondary: English
- AI understands Korean business terminology
- Output matches user's language preference

---

## Implementation Priority

### Phase 1 (First Demo)

1. **Natural-language ERP Query** — Foundation for all other features
2. **CEO Daily Briefing** — Highest visibility, simplest to implement
3. **Receivables Summary** — Critical for cash flow

### Phase 2 (Second Demo)

4. **Quotation Draft Assistant** — Direct productivity gain
5. **Delivery & Stock Summary** — Operations team value

### Phase 3 (Third Demo)

6. **Accountant Package** — Month-end workflow

---

## Success Criteria

### First Demo Must Show

- [ ] User asks a question in Korean, gets correct ERP data back
- [ ] CEO sees daily briefing with real demo data
- [ ] Receivables summary shows accurate outstanding amounts
- [ ] All AI outputs are read-only (no auto-save)
- [ ] All AI outputs include source transparency (which DocType, which filters)

### Must NOT Show

- [ ] AI modifying any ERP data
- [ ] AI sending any external communication
- [ ] AI accessing data beyond user's permissions
- [ ] Error messages or technical jargon in AI responses

---

**Document Version**: 1.0
**Last Updated**: 2026-05-18
**Author**: Padiem Team
