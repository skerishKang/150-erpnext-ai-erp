# Padiem AI ERP

ERPNext-based AI ERP for Korean SMEs.

> **Current status: early ERPNext app/runtime MVP — not production-ready**
>
> The repository contains a read-only ERP summary layer, deterministic CEO briefing, AI provider abstraction, a disabled-by-default DeepSeek implementation, a minimal `/ceo_briefing` route, unit tests, and static validation. A real Frappe/ERPNext bench and site runtime smoke has not yet been completed.

## Product Identity

Padiem AI ERP is an ERP product built on ERPNext. AI is embedded inside ERP workflows; it is not a generic chatbot, automation platform, or autonomous ERP operator.

- **Product:** Padiem AI ERP
- **Base:** ERPNext / Frappe
- **Target:** Korean SMEs with approximately 5–100 employees
- **Initial focus:** quotation, inventory, delivery, receivables, and executive reporting
- **Current implemented slice:** read-only CEO briefing

## Product Principles

1. ERP data and ERP permissions are the source of truth.
2. AI assists ERP work; it does not bypass ERP controls.
3. External AI is disabled by default.
4. The default provider remains `mock` until separately approved.
5. Real customer data, production secrets, backups, and site configuration must never be committed.
6. Accounting, tax filing, payroll, VAT filing, and fully autonomous ERP execution are outside the first-version scope.

## Current Implementation

### ERP read-only summaries

The current briefing context reads or aggregates these ERPNext DocTypes:

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

The runtime summarizes sales, purchasing, inventory, receivables, quotations, deliveries, payments, counts, and warnings.

### CEO briefing

- Deterministic mock briefing generator
- Whitelisted API methods
- Minimal `/ceo_briefing` web route
- Shared all-DocType read permission gate
- Raw context duplication removed from the briefing object
- Safe user-facing error messages

### AI provider layer

| Provider | Current status |
|---|---|
| `mock` | Active safe default; no external call |
| `deepseek` | Client implementation exists; disabled by config guard and not the default |
| `kilocode` | Placeholder |
| `opencodego` | Placeholder |
| `nvidia` | Placeholder |
| `mistral` | Placeholder |
| `ollama` | Placeholder |

DeepSeek requires all of the following before any call is allowed:

- `PA_DIEM_ENABLE_EXTERNAL_AI=true`
- `PA_DIEM_DEEPSEEK_ENABLED=true`
- `PA_DIEM_DEEPSEEK_API_KEY` present

The configured base URL is validated conservatively. HTTPS is required and localhost, private IP ranges, metadata addresses, unexpected ports, and unexpected paths are blocked.

## What Is Not Yet Proven

The following are release blockers, not minor documentation gaps:

- Standard `bench get-app` and `install-app` behavior
- Canonical package/import path in a real site context
- App installation, migration, uninstall, and reinstall
- Real Frappe route and whitelisted API execution
- Actual MariaDB aggregate query behavior
- Company and row-level User Permission enforcement
- Restricted-user runtime behavior
- Reliable distinction between query failure and a real numeric zero
- Supported Frappe, ERPNext, Python, and database versions
- Production-grade external AI data policy and auditing

Related runtime issues:

- [#131 — provision Frappe bench environment](../../issues/131)
- [#130 — run ERPNext/Frappe CEO briefing smoke](../../issues/130)
- [#133 — verify app packaging and standard installation](../../issues/133)

## Current Safety Boundary

Until the P0 release gates are complete:

- Use only local, disposable, or staging ERPNext sites.
- Use synthetic or irreversibly anonymized data.
- Keep the provider on `mock`.
- Do not use production API keys.
- Do not expose the briefing to users who may have restricted company or row-level access.
- Do not treat a successful static test as proof that the app works in ERPNext runtime.
- Do not describe this repository as a finished AI ERP product.

## Repository Structure

```text
.
├── AGENTS.md
├── README.md
├── padiem_ai/
│   ├── setup.py
│   ├── requirements.txt
│   └── padiem_ai/
│       ├── ai/                  # provider registry, config guards, providers
│       ├── api/                 # thin whitelisted API wrappers
│       ├── briefing/            # deterministic briefing generation
│       ├── erp/                 # read-only ERP summary modules
│       ├── public/              # static assets
│       └── www/                 # web route and template
├── tests/                       # standard-library unit tests with Frappe stub
├── docs/
│   ├── agents/                  # agent instructions and project rules
│   ├── architecture/            # target architecture
│   ├── product/                 # product and data policies
│   └── implementation/          # runtime guides, roadmap, release gates
└── .github/workflows/           # static validation
```

## Validation Available Today

GitHub Actions currently runs:

```bash
python -m py_compile <runtime and test Python files>
python -m unittest discover -s tests -p 'test_*.py'
```

The current test suite covers configuration guards, DeepSeek URL validation and prompt construction, mock briefing behavior, permission helper calls, API response shape, and web-route error handling.

These tests use a Frappe stub and do **not** replace a real bench/site runtime test.

See [Runtime Smoke Guide](docs/implementation/RUNTIME_SMOKE_GUIDE.md).

## Installation Status

A verified installation command is intentionally not claimed yet. The repository layout, empty dependency file behavior, and canonical import path must first be validated through [#133](../../issues/133) in the bench environment from [#131](../../issues/131).

After validation, this section must include exact commands for:

- supported Frappe and ERPNext versions
- `bench get-app`
- `bench --site <SITE> install-app padiem_ai`
- migration and update
- uninstall and rollback
- API and web-route smoke

## Improvement Program

### Existing runtime foundation

- [#131 — provision Frappe bench environment](../../issues/131)
- [#130 — run ERPNext/Frappe CEO briefing smoke](../../issues/130)

### P0 — installation, permission, and metric trust

- [#133 — app packaging and standard bench installation](../../issues/133)
- [#134 — Company and User Permission-aware aggregation](../../issues/134)
- [#135 — distinguish query failures from real zero values](../../issues/135)

### P1 — metric policy, AI operations, audit, and quality

- [#136 — document status, period, and currency policy](../../issues/136)
- [#137 — site-level provider settings and external data policy](../../issues/137)
- [#138 — asynchronous briefing execution and accurate metadata](../../issues/138)
- [#139 — persistent AI Briefing Run audit record](../../issues/139)
- [#140 — structured-output schema validation and provider staging test](../../issues/140)
- [#141 — Frappe/ERPNext integration CI and security gates](../../issues/141)

### P2 — repository and product experience

- [#142 — installation, support matrix, license, and release documentation](../../issues/142)
- [#143 — GitHub templates, branch cleanup, and release governance](../../issues/143)
- [#144 — CEO briefing comparison, drill-down, and accessibility](../../issues/144)

### Overall program

- [#145 — move the CEO briefing MVP to ERPNext operations-ready status](../../issues/145)

## Recommended Development Order

```text
#131 bench environment
→ #133 installation/package contract
→ #130 real runtime smoke
→ #134 company and row-level permission boundary
→ #135 metric error model
→ #136 metric status/period/currency policy
→ #141 integration CI
→ #139 persistent run audit
→ #138 asynchronous execution
→ #137 external AI policy and settings
→ #140 schema-validated provider staging
→ #144 product UX
```

## Key Documentation

- [Project Audit — 2026-08-04](docs/PROJECT_AUDIT_20260804.md)
- [Target Architecture](docs/architecture/TARGET_ARCHITECTURE.md)
- [AI and ERP Data Governance](docs/product/AI_DATA_GOVERNANCE.md)
- [CEO Briefing Record Policy](docs/product/CEO_BRIEFING_RECORD_POLICY.md)
- [Stabilization Roadmap](docs/implementation/ROADMAP_20260804.md)
- [Release Gates](docs/implementation/RELEASE_GATES.md)
- [Runtime Smoke Guide](docs/implementation/RUNTIME_SMOKE_GUIDE.md)
- [Contributing](CONTRIBUTING.md)
- [Agent Instructions](AGENTS.md)

## License Status

The app metadata currently declares MIT. A root `LICENSE` file and copyright owner still need to be confirmed under [#142](../../issues/142). Until that is completed, do not infer additional licensing terms from the metadata alone.
