# Data Flow — Padiem AI ERP

## Primary Data Flow

```
ERP Data ──► AI Context Builder ──► AI Provider ──► Generated Output ──► User Review ──► ERP Action
```

## Detailed Flow Diagram

```
┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│          │    │              │    │              │    │          │    │          │    │          │
│  ERPNext │──►│  AI Context  │──►│  AI Provider  │──►│Generated │──►│  User    │──►│  ERPNext │
│  Data    │    │  Builder     │    │  (DeepSeek/  │    │ Briefing │   │  Review  │    │  Action  │
│          │    │              │    │    OpenAI)    │    │ / Draft  │   │          │    │          │
│  • Today's│   │  • Formats   │    │              │    │          │   │  • CEO   │    │  • Create │
│    orders │   │    ERP data  │    │  • LLM call  │    │  • Daily │   │    reads │    │    Quot. │
│  • Pending│   │    for LLM   │    │  • Rate      │    │    brief │   │  • Edits │    │  • Update │
│    quotes │   │  • Adds      │    │    limited   │    │  • Quot. │   │  • Appro-│    │    status │
│  • Stock  │   │    system    │    │  • Retry on  │    │    draft │   │    ves   │    │  • Log    │
│    levels │   │    prompt    │    │    failure   │    │  • Alert │   │  • Rejec-│    │    action │
│  • Receiv-│   │  • Truncates │    │              │    │          │   │    ts    │    │          │
│    ables  │   │    if needed │    │              │    │          │   │          │    │          │
│          │    │              │    │              │    │          │   │          │    │          │
└──────────┘    └──────────────┘    └──────────────┘    └──────────┘   └──────────┘    └──────────┘
       │                                                      │              │              │
       │                                                      │              │              │
       └──────────────────┬───────────────────────────────────┘              │              │
                          │                                                  │              │
                    ┌─────▼──────┐                              ┌─────────────▼─────┐       │
                    │  Audit Log │                              │                   │       │
                    │  Records   │                              │  Human Approval   │       │
                    │  every AI  │                              │  Gate             │       │
                    │  action    │                              │  (mandatory for   │       │
                    │            │                              │  ERP actions)     │       │
                    └────────────┘                              └───────────────────┘       │
                                                                                            │
                                                                  ┌─────────────────────────┘
                                                                  │
                                                          ┌───────▼────────┐
                                                          │   ERP Action    │
                                                          │  (e.g., create  │
                                                          │   Quotation)    │
                                                          └────────────────┘
```

## Flow Types

### Type 1: Read-Only (No ERP Action)

Used for: CEO briefing, sales summary, inventory alerts

```
User clicks "AI Briefing"
    → System gathers ERP data (orders, quotations, inventory)
    → Context builder formats data for AI
    → AI provider generates summary
    → User views briefing
    → No ERP document created
    → All logged to audit
```

### Type 2: Draft + Approval (ERP Action)

Used for: AI quotation draft

```
User types "Draft quotation for 50 units of Item A to Customer B"
    → System parses request (may ask AI to extract intent)
    → System gathers ERP data (customer B info, Item A pricing)
    → Context builder creates prompt
    → AI provider generates quotation draft
    → User reviews draft (can edit fields)
    → User clicks "Confirm" to create ERPNext Quotation
    → System creates Quotation document via Frappe ORM
    → System logs action to audit log
    → User sees confirmation + document link
```

### Type 3: Scheduled (Background)

Used for: Daily briefing email, inventory threshold alerts

```
Scheduler triggers (e.g., every morning at 8:00 AM)
    → System gathers ERP data
    → AI generates briefing/alert
    → Delivered to CEO dashboard
    → Optional: push notification or email
    → Logged to audit
```

## Data Context Size Management

| Data Type | Typical Size | Management |
|-----------|-------------|------------|
| Today's orders | < 1 KB | Include full details |
| Pending quotations | 1–5 KB | Include full details |
| Inventory status | 5–50 KB | Summarize (top X low-stock items) |
| Receivables | 1–10 KB | Include overdue only |
| Full customer master | 100 KB+ | Never include raw; use summary |
| Full item catalog | 500 KB+ | Never include raw; use summary |

**Strategy:** AI context is built on-demand and truncated to fit within provider context limits (typically 8K–32K tokens). Large data sets are summarized server-side before sending to AI.

## Error Handling

| Failure Point | Behavior |
|---------------|----------|
| AI provider unreachable | Fallback to cached briefing; show "AI unavailable" message; log error |
| AI returns invalid JSON | Retry with stricter prompt; if fails, return error to user |
| ERP data fetch fails | Show partial briefing with available data; flag missing sections |
| User rejects AI draft | No ERP action taken; draft discarded; logged to audit |
| AI timeout | Show "taking longer than expected" message; log for monitoring |

## Data Privacy

- ERP data sent to AI provider is **minimal** — only what is needed for the specific action
- No customer passwords, tokens, or credentials are sent to AI providers
- AI provider contract must include **data non-retention** clause
- Sensitive fields (pricing, customer names) can be anonymized in prompts if needed
- Audit log captures all data sent to/received from AI providers (for compliance and debugging)
