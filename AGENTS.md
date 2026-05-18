# Agent Coding Rules for 150-erpnext-ai-erp

This repository hosts `padiem_ai` — an AI ERP project built on ERPNext/Frappe.

## Project Context

- **Project**: 150-erpnext-ai-erp / padiem_ai AI ERP
- **Base**: ERPNext + Frappe framework
- **Purpose**: CEO briefing, ERP queries, and AI-assisted business workflows

## Critical Repo Rules

### Core Modifications
- **ERPNext/Frappe core**: DO NOT modify. These are vendored dependencies.
- **Demo data**: Do not modify unless explicitly part of an issue.

### Security
- **API keys, tokens, `.env`, `site_config`, passwords, backups**: NEVER commit or expose.
- **External AI calls**: Disabled by default. Require explicit enable chain.
- **Default provider**: Keep CEO briefing on `mock` provider. Do not switch to DeepSeek.

## File-Size / Modularity Rules

| Lines | Action |
|-------|--------|
| >500 | Merge blocker — must split |
| 351-500 | PR must explain why not split |
| 251-350 | High-change files subject to reviewer review |

## Agent Reading Order

1. Read [docs/agents/README.md](docs/agents/README.md) — how this documentation system works
2. Read [docs/agents/00-index/agent-reading-order.md](docs/agents/00-index/agent-reading-order.md) — what to read next
3. Read [docs/agents/00-index/project-map.md](docs/agents/00-index/project-map.md) — repository structure

## Module Boundaries

- `ai/` — AI provider implementations and config guards
- `api/` — Thin API endpoint wrappers
- `briefing/` — CEO briefing generation logic
- `erp/` — ERP read-only data access
- `www/` — Web controllers and entry points

## Refactoring Candidates

1. `erp/read_only.py` → domain modules + facade
2. `ai/providers.py` → provider-specific modules + facade
3. `ai/config.py` → env/config-status/guard separation

## External Reference

Files like `frappe/`, `erpnext/`, `sites/`, `env/`, `node_modules/`, `.venv/` are excluded from size checks and must not be modified.