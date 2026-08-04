# Project Map

Repository structure for Padiem AI ERP.

This map distinguishes current runtime folders from documentation and planned placeholders.

```text
150-erpnext-ai-erp/
├── AGENTS.md                    # Agent index
├── README.md                    # Project overview, current status, and release gates
├── CONTRIBUTING.md              # Development, review, data, and release rules
├── .github/
│   ├── workflows/
│   │   └── static-validation.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── improvement.md
├── padiem_ai/                   # Current ERPNext app/runtime package
│   ├── setup.py                 # Python package setup
│   ├── requirements.txt         # Runtime dependency list
│   └── padiem_ai/
│       ├── ai/                  # AI provider layer and config guards
│       ├── api/                 # API endpoint wrappers
│       ├── briefing/            # CEO briefing generation logic
│       ├── erp/                 # ERP read-only data access modules
│       ├── public/              # Static assets
│       ├── www/                 # Web controllers and entry points
│       └── ...                  # Other ERPNext app files as added
├── tests/                       # Current Frappe-stub unit tests
├── docs/
│   ├── PROJECT_AUDIT_20260804.md # Current audit and risk assessment
│   ├── agents/                  # Current agent instruction system
│   │   ├── README.md            # How agent docs work
│   │   ├── 00-index/            # Maps and reading order
│   │   ├── 01-principles/       # Product identity and business rules
│   │   ├── 02-product/          # MVP, modules, positioning
│   │   ├── 03-technical/        # ERPNext, AI, cloud, security
│   │   ├── 04-operations/       # Git, dev rules, testing
│   │   └── 05-prompts/          # Reusable prompts
│   ├── product/
│   │   ├── CEO_BRIEFING_RECORD_POLICY.md
│   │   └── AI_DATA_GOVERNANCE.md
│   ├── architecture/
│   │   └── TARGET_ARCHITECTURE.md
│   ├── implementation/
│   │   ├── RUNTIME_SMOKE_GUIDE.md
│   │   ├── ROADMAP_20260804.md
│   │   └── RELEASE_GATES.md
│   ├── sales/                   # Current/planned sales materials
│   └── research/                # Current/planned research docs
├── samples/                     # Current/planned synthetic sample data and templates
├── prompts/                     # Planned reusable prompts
├── infra/                       # Planned infrastructure config
└── research/                    # Planned raw research materials
```

## Key Files for Agents

| File | Purpose |
|---|---|
| `AGENTS.md` | Entry point — read this first |
| `README.md` | Current product and implementation status |
| `CONTRIBUTING.md` | Development, data, permission, AI, test, and release rules |
| `docs/agents/00-index/agent-reading-order.md` | Defines what to read next |
| `docs/agents/00-index/project-map.md` | Current repository map |
| `docs/agents/01-principles/product-identity.md` | What this product is |
| `docs/agents/02-product/mvp-scope.md` | What we are building now |
| `docs/agents/03-technical/erpnext-strategy.md` | Why ERPNext |
| `docs/PROJECT_AUDIT_20260804.md` | Verified current-state audit and risks |
| `docs/architecture/TARGET_ARCHITECTURE.md` | Target runtime and trust boundaries |
| `docs/product/AI_DATA_GOVERNANCE.md` | ERP and external AI data policy |
| `docs/product/CEO_BRIEFING_RECORD_POLICY.md` | CEO briefing record-selection policy |
| `docs/implementation/RUNTIME_SMOKE_GUIDE.md` | Real bench/site smoke procedure |
| `docs/implementation/ROADMAP_20260804.md` | Risk-ordered implementation roadmap |
| `docs/implementation/RELEASE_GATES.md` | Evidence required for each release stage |

## Current Runtime Status

Current:

- ERPNext app code
- read-only ERP summary modules
- deterministic mock CEO briefing
- AI provider abstraction and DeepSeek config guard
- API and `/ceo_briefing` route
- static compile and unit tests

Not yet proven:

- standard bench installation
- real Frappe/ERPNext runtime
- Company and row-level aggregate isolation
- production external AI policy
- operations-ready release

See EPIC #145 for the complete release program.
