# Agent Coding Rules for 150-erpnext-ai-erp

This repository hosts `padiem_ai` — an AI ERP project built on ERPNext/Frappe.

## Project Context

- **Project**: 150-erpnext-ai-erp / padiem_ai AI ERP
- **Base**: ERPNext + Frappe framework
- **Purpose**: CEO briefing, ERP queries, and AI-assisted business workflows

## Critical Prohibitions

### Core Modifications
- **ERPNext/Frappe core**: DO NOT modify. These are vendored dependencies.
- **Demo data**: Do not modify unless explicitly part of an issue (not this one).

### Security
- **API keys, tokens, `.env`, `site_config`, passwords, backups**: NEVER commit or expose.
- **External AI calls**: Disabled by default. Require explicit enable chain.
- **Default provider**: Keep CEO briefing on `mock` provider. Do not switch to DeepSeek.

### Code Organization
- **File size limit**: 500 physical lines max per file. Merge blocker at 500 lines.
- **Warning threshold**: 350 lines triggers PR explanation requirement.
- **Modularization candidate**: Files over 250 lines with frequent changes need review.

### Architecture Boundaries
- **ERP read-only data access** ≠ **API response logic**. Keep separate.
- **Provider implementation** ≠ **config guard policy**. Keep separate.
- **API endpoints**: Must be thin wrappers. No business logic in routes.

## File Size Rules

| Lines | Action |
|-------|--------|
| 500+ | Merge blocker — must split |
| 350-499 | PR must explain why not split |
| 250-349 | High-change files subject to reviewer review |

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