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

We are at the end of **Phase 0**. Phase 1 (ERPNext installation) is next.
