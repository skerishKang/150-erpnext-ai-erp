# Runtime Smoke Guide

This guide defines the runtime smoke checks for Padiem AI ERP after a Frappe/ERPNext bench or staging site is available.

Related issues:

- #130 — run ERPNext/Frappe CEO briefing smoke
- #131 — provision Frappe bench environment for runtime smoke tests

## Status

Static validation and unit tests are already covered by the repository workflow.

Runtime smoke still requires a prepared Frappe/ERPNext site. This document does not prescribe one installation method. A local bench, Docker-based bench, or staging server is acceptable as long as the checks below can be executed.

## Safety rules

- Do not use production API keys.
- Do not print secrets, database passwords, API keys, or environment values.
- Do not call DeepSeek live APIs.
- Do not mutate ERP business data during smoke.
- Do not modify ERPNext/Frappe core.
- Use mock provider behavior unless a separate live-provider test is explicitly approved.

## Required environment

The smoke environment must provide:

- Frappe bench command access.
- An ERPNext/Frappe site.
- The `padiem_ai` app installed or importable in the site context.
- ERPNext DocTypes used by CEO briefing.
- A user/session with read permissions for the required DocTypes.
- A way to test a restricted user or permission-denied path.

## Required DocTypes

CEO briefing permission checks use `CEO_BRIEFING_READ_DOCTYPES`.

Current required DocTypes:

- Customer
- Supplier
- Item
- Quotation
- Sales Order
- Purchase Order
- Stock Entry
- Delivery Note
- Sales Invoice
- Payment Entry
- Warehouse

## Step 1 — repository state

Run from the app checkout:

```bash
git fetch origin
git checkout main
git pull --ff-only
git rev-parse HEAD
git status
```

Expected:

- Branch is `main`.
- Working tree is clean.
- Commit SHA is recorded in the smoke report.

## Step 2 — static validation

Run:

```bash
python -m py_compile $(find padiem_ai/padiem_ai tests -name "*.py")
python -m unittest discover -s tests -p "test_*.py"
```

Expected:

- `py_compile` passes.
- `unittest` passes.
- Expected test count at the time of this guide: 28.

## Step 3 — bench and app installation check

Run commands appropriate to the local environment, for example:

```bash
bench version
bench list-apps
bench --site <SITE_NAME> list-apps
```

Expected:

- Frappe/ERPNext bench is available.
- Target site exists.
- `padiem_ai` is installed or importable for the target site.

Do not paste sensitive site configuration values into reports.

## Step 4 — import smoke in site context

Use bench console or an equivalent site-context command to import:

```python
import padiem_ai.ai.config
import padiem_ai.ai.providers
import padiem_ai.ai.provider_modules.deepseek
import padiem_ai.ai.config_modules.guard
import padiem_ai.erp.permissions
import padiem_ai.erp.read_only
import padiem_ai.api.briefing
import padiem_ai.www.ceo_briefing
```

Expected:

- All imports succeed.
- No external AI call occurs.

## Step 5 — provider/config smoke

In site context:

```python
from padiem_ai.ai.registry import get_default_provider
from padiem_ai.ai.config import get_provider_config_status, get_deepseek_config
from padiem_ai.ai.providers import DeepSeekProvider

provider = get_default_provider()
print(provider.get_provider_name())
print(get_provider_config_status("mock"))
print(get_provider_config_status("deepseek"))
print(DeepSeekProvider().health_check())
print(get_deepseek_config())
```

Expected:

- Default provider is `mock`.
- Mock status is `ok`.
- DeepSeek is disabled unless explicitly configured.
- `DeepSeekProvider.health_check()` reports `external_call: False`.
- `get_deepseek_config()` exposes only key presence booleans, not API key values.

## Step 6 — API smoke

Run in site context:

```python
from padiem_ai.padiem_ai.api.briefing import get_counts, get_ceo_briefing

counts = get_counts()
briefing = get_ceo_briefing()

print(type(counts), counts.keys() if isinstance(counts, dict) else counts)
print(type(briefing), briefing.keys() if isinstance(briefing, dict) else briefing)
print(briefing.get("success"))
print(briefing.get("provider"))
print("data" in briefing)
print("raw_context" in briefing.get("briefing", {}))
```

Expected when permissions and data permit:

- `get_counts()` returns a structured response.
- `get_ceo_briefing()` returns a structured response.
- `success` is `True`.
- Top-level `data` exists.
- `briefing.raw_context` is not duplicated.
- Provider is `mock`.
- `external_call` is `False`.

If this fails, classify the error as one of:

- import failure
- app not installed
- permission failure
- missing DocType
- query/data failure
- unexpected exception

## Step 7 — web route smoke

Open or request:

```text
/ceo_briefing
```

Expected:

- Page renders, or a controlled permission/error message appears.
- Generic exception details are not exposed to the page user.
- Permission error message is safe.
- No external AI call occurs.

## Step 8 — permission smoke

Run both paths if possible.

### User with required read permissions

Expected:

- API/page can read context.
- Response is structured.
- No external AI call occurs.

### User missing at least one required read permission

Expected:

- API/page does not expose ERP context.
- Permission failure is controlled.
- Web page uses safe user-facing message.

## Smoke report template

```text
# Runtime Smoke Report

## 1. Conclusion
- Status: PASS / FAIL / PARTIAL / BLOCKED
- Score:

## 2. Environment
- Commit SHA:
- Branch:
- Working tree:
- Bench available:
- Site identifier: redacted if sensitive
- padiem_ai installed:
- ERPNext/Frappe available:

## 3. Static validation
- py_compile:
- unittest:
- Test count:

## 4. Import smoke
- Result:
- Failed module, if any:

## 5. Provider/config smoke
- Default provider:
- Mock status:
- DeepSeek status:
- DeepSeek health_check external_call:
- API key value exposed: yes/no
- External AI call: yes/no

## 6. API smoke
- get_counts:
- get_ceo_briefing:
- success:
- provider:
- top-level data present:
- briefing.raw_context duplicated:
- error category, if any:

## 7. Web route smoke
- /ceo_briefing:
- safe error message:
- exception detail exposed:

## 8. Permission smoke
- authorized user path:
- restricted user path:
- all required DocTypes checked:

## 9. Blockers
- none, or list with file/function/symptom/cause

## 10. Recommended next action
- close #130
- keep #130 blocked
- create follow-up issue
```
