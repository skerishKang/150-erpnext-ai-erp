# Padiem AI ERP

ERPNext-based AI ERP for Korean SMEs.

## What Is This?

Padiem AI ERP is an ERP system — not a generic automation tool.
It is built on ERPNext and enhanced with AI capabilities embedded directly inside ERP workflows.

## Product Identity

- **Product:** Padiem AI ERP
- **Base:** ERPNext
- **Target:** Korean SMEs (manufacturing, distribution, construction, logistics, installation, field operations)
- **Positioning:** AI-powered ERP that eliminates manual work in quotation, stock, delivery, receivables, and reporting

## Current Phase

Padiem AI ERP has moved beyond documentation-only planning into an early ERPNext app/runtime implementation phase.

The repository now includes:

- `padiem_ai/` application code
- AI provider configuration with mock as the safe default
- Config-gated DeepSeek provider implementation
- ERP read-only summary modules for CEO briefing context
- Documentation, implementation plans, and agent instructions

External AI calls are disabled by default and require explicit configuration.
The mock provider remains the default safe provider for development and testing.

ERPNext/Frappe runtime smoke tests require a prepared bench/site environment.
Static validation for the read-only performance migration has been completed, but runtime validation should be performed in an actual ERPNext environment.

## Folder Guide

| Folder | Purpose |
|--------|---------|
| `padiem_ai/` | ERPNext app/runtime code, AI provider layer, and read-only ERP modules |
| `docs/` | All project documentation |
| `docs/agents/` | Agent instruction system (start here for AI agents) |
| `docs/product/` | Product specs and requirements |
| `docs/architecture/` | Technical architecture docs |
| `docs/sales/` | Sales and go-to-market materials |
| `docs/research/` | Market and competitor research |
| `docs/implementation/` | Implementation plans and guides |
| `prompts/` | Reusable prompts |
| `samples/` | Sample data and templates |
| `infra/` | Infrastructure configuration |
| `research/` | Raw research materials |

## Links

- [AGENTS.md](AGENTS.md) — Agent index (start here for AI agents)
- [docs/agents/README.md](docs/agents/README.md) — Agent documentation system overview
