# Execution Roadmap — Padiem AI ERP

## Phase Overview

| Phase | Name | Duration (est.) | Deliverable |
|-------|------|-----------------|-------------|
| **0** | Repository and Documentation | ✅ Complete | GitHub repo, AGENTS.md, docs/agents, ADRs, architecture docs |
| **1** | ERPNext Local Installation | Sprint 1 | Working ERPNext login + sample company |
| **2** | ERPNext Basic Company Setup | Sprint 2 | Customers, Items, Quotations, Orders configured |
| **3** | AI Module Design | Sprint 3 | AI provider adapter, prompt templates, draft generation |
| **4** | First Demo Scenario | Sprint 4 | End-to-end demo: voice → quotation → CEO briefing |
| **5** | Oracle Cloud Test Deployment | Sprint 5 | Staging deployment on Oracle Cloud ARM VM |
| **6** | First Customer Proposal and Pilot | Sprint 6 | Pilot customer onboarding and feedback |

## Dependency Graph

```
Phase 0 (docs)
    │
    ▼
Phase 1 (local ERPNext install)
    │
    ▼
Phase 2 (company setup)
    │
    ▼
Phase 3 (AI module design) ──┐
    │                        │
    ▼                        │
Phase 4 (demo scenario) ◄────┘
    │
    ▼
Phase 5 (cloud deployment)
    │
    ▼
Phase 6 (customer pilot)
```

## Gate Criteria

| Phase → Next | Gate |
|-------------|------|
| 0 → 1 | All ADRs written and committed |
| 1 → 2 | Local ERPNext + sample company accessible via browser |
| 2 → 3 | 3+ customer records, 5+ items, sample quotation flow working |
| 3 → 4 | AI provider adapter can call DeepSeek and return structured response |
| 4 → 5 | Demo scenario runs fully on local setup |
| 5 → 6 | Staging environment accessible via domain, customer can visit URL |

## Key Milestones

| Milestone | Target Phase | Description |
|-----------|-------------|-------------|
| M1 | Phase 1 | "CEO can log into ERPNext" |
| M2 | Phase 2 | "CEO can see quotations, orders, inventory" |
| M3 | Phase 3 | "AI can draft a quotation from a voice note" |
| M4 | Phase 4 | "Full demo: voice → quotation → CEO briefing" |
| M5 | Phase 5 | "System running on Oracle Cloud, accessible via browser" |
| M6 | Phase 6 | "First pilot customer using the system" |

## Current Position

We have completed major foundation work through PRs #43, #45, and #47-#61. The project has completed major foundation work and should next validate CEO briefing/import compatibility before Phase 3-4 implementation.

### Completed Work (Through PR #61)

| PR | Description |
|----|-------------|
| #43 | DeepSeek enable guard / config status |
| #45 | AGENTS.md coding rules + file-size guard |
| #47-#61 | ERP read-only modular refactor |

### ERP Read-Only Modular Refactor Details

The `padiem_ai/erp/read_only.py` facade has been split into domain modules:

| Module | Contents |
|--------|----------|
| `read_only_modules/utils.py` | `_count_records()`, `_safe_get_list()` |
| `read_only_modules/sales.py` | `get_sales_summary()`, `get_quotation_summary()`, `get_delivery_summary()` |
| `read_only_modules/inventory.py` | `get_inventory_summary()` |
| `read_only_modules/purchasing.py` | `get_purchase_summary()` |
| `read_only_modules/receivables.py` | `get_receivables_summary()`, `get_payment_summary()` |
| `read_only_modules/context.py` | `get_ceo_briefing_context()` |

**Key structure clarifications:**
- `get_demo_counts()` remains in `read_only.py` (not moved)
- `get_ceo_briefing_context()` moved to `read_only_modules/context.py`
- Public import compatibility maintained via `read_only.py` facade re-export

### DeepSeek Enable Guard Details

- `DeepSeekProvider.health_check()` returns config status only (no external API calls)
- Enable chain requires **all** of: external AI enable flag + DeepSeek enabled flag + configured credentials present
- Default provider remains `mock` (not changed)
- DeepSeek is structurally implemented behind guards, but external runtime use is not yet validated in this roadmap.

### Next Priority Candidates

1. **Roadmap/docs reconciliation completion**
2. **CEO briefing smoke / import compatibility verification**
3. **ERPNext runtime/data validation**
4. **AI ERP demo flow** (voice → quotation → CEO briefing)
5. **Oracle Cloud deployment planning**
6. **First customer pilot/proposal path**

### Historical Context

The original roadmap referenced issues #1-#9, which are now completed/obsolete. Current work (PRs #43, #45, #47-#61) represents later phases that superseded those early tasks.
