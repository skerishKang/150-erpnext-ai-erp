# Padiem AI ERP

ERPNext-based AI ERP for Korean SMEs.

## What Is This?

Padiem AI ERP is an ERP system, not a generic automation tool.
It is built on ERPNext and enhanced with AI capabilities embedded directly inside ERP workflows.

## Product Identity

- **Product:** Padiem AI ERP
- **Base:** ERPNext
- **Target:** Korean SMEs
- **Positioning:** AI-powered ERP for quotation, stock, delivery, receivables, and reporting workflows

## Current Phase

Padiem AI ERP has moved beyond documentation-only planning into an early ERPNext app/runtime implementation phase.

The repository currently includes:

- `padiem_ai/` application code
- AI provider configuration with mock as the safe default
- Config-gated DeepSeek provider implementation
- ERP read-only summary modules for CEO briefing context
- Documentation, implementation plans, and agent instructions

External AI calls are disabled by default and require explicit configuration.
The mock provider remains the default safe provider for development and testing.

ERPNext/Frappe runtime smoke tests require a prepared bench/site environment.
Static validation can catch syntax and structural issues, but runtime validation should be performed in an actual ERPNext environment before production use.

## Folder Guide

| Folder | Status | Purpose |
|--------|--------|---------|
| `padiem_ai/` | current runtime | ERPNext app/runtime code, AI provider layer, API wrappers, web route, and read-only ERP modules |
| `docs/` | current docs | Project documentation |
| `docs/agents/` | current docs | Agent instruction system |
| `docs/product/` | current docs | Product specs, requirements, and data-policy documents |
| `docs/architecture/` | current/planned docs | Technical architecture documents |
| `docs/sales/` | current/planned docs | Sales and go-to-market materials |
| `docs/research/` | current/planned docs | Market and competitor research summaries |
| `docs/implementation/` | current/planned docs | Implementation plans and guides |
| `samples/` | current/planned support | Sample data and templates when available |
| `prompts/` | planned | Reusable prompts when added |
| `infra/` | planned | Infrastructure configuration when added |
| `research/` | planned | Raw research materials when added |

## Links

- [AGENTS.md](AGENTS.md) — Agent index
- [docs/agents/README.md](docs/agents/README.md) — Agent documentation system overview
- [docs/product/CEO_BRIEFING_RECORD_POLICY.md](docs/product/CEO_BRIEFING_RECORD_POLICY.md) — CEO briefing record-selection policy
