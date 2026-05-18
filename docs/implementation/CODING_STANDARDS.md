# Coding Standards for padiem_ai

This document defines file-size thresholds and module organization rules for the `padiem_ai` application.

## File-Size Thresholds

| Lines | Status | Action Required |
|-------|--------|-----------------|
| >500 | **BLOCKER** | Must split before merge |
| 351-500 | **WARNING** | PR must justify why not split |
| 251-350 | **REVIEW** | Frequent changes trigger module review |

> Note: The check script uses `lines > max_lines` as the failure condition, so files up to and including 500 lines pass.

## App-Owned Code Scope

**Included in size checks:**
- `padiem_ai/padiem_ai/ai/`
- `padiem_ai/padiem_ai/api/`
- `padiem_ai/padiem_ai/briefing/`
- `padiem_ai/padiem_ai/erp/`
- `padiem_ai/padiem_ai/www/`

**Excluded from size checks (vendors/third-party):**
- `frappe/`
- `erpnext/`
- `sites/`
- `env/`
- `node_modules/`
- `.venv/`
- `__pycache__/`

## Module Boundaries

### ai/
AI provider implementations and configuration guards.
- `ai/providers.py` — Provider classes (DeepSeek, Mock, Placeholder)
- `ai/config.py` — Config guard functions
- `ai/registry.py` — Provider lookup and selection

### api/
Thin API endpoint wrappers. No business logic here.
- `api/briefing.py` — CEO briefing endpoint

### briefing/
CEO briefing generation logic.

### erp/
ERP read-only data access. Separate from API response logic.
- `erp/read_only.py` — Core refactoring candidate

### www/
Web controllers and entry points.

## Refactoring Candidates

### 1. `erp/read_only.py`
**Current**: Monolithic ERP data access
**Target**: Domain modules (`erp/sales.py`, `erp/stock.py`, etc.) + facade

### 2. `ai/providers.py`
**Current**: Single file with multiple providers
**Target**: Provider-specific modules (`ai/deepseek.py`, `ai/mock.py`) + facade

### 3. `ai/config.py`
**Current**: Mixed concerns (env reading, status, guards)
**Target**: Separate `ai/env.py`, `ai/status.py`, `ai/guard.py`

## Physical Line Count

We count **physical lines** (actual lines in file), not logical statements. Blank lines and comments count toward the limit.

## Check Script

Run `scripts/check_file_size.py` to verify compliance before PR submission.
