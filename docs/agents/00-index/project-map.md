# Project Map

Repository structure for Padiem AI ERP.

This map distinguishes current runtime folders from documentation and planned placeholders.

```
150-erpnext-ai-erp/
├── AGENTS.md                    # Agent index
├── README.md                    # Project overview
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
├── docs/
│   ├── agents/                  # Current agent instruction system
│   │   ├── README.md            # How agent docs work
│   │   ├── 00-index/            # Maps and reading order
│   │   ├── 01-principles/       # Product identity, business rules
│   │   ├── 02-product/          # MVP, modules, positioning
│   │   ├── 03-technical/        # ERPNext, AI, cloud, security
│   │   ├── 04-operations/       # Git, dev rules, testing
│   │   └── 05-prompts/          # Reusable prompts
│   ├── product/                 # Current/planned product specs and policies
│   ├── architecture/            # Current/planned technical architecture docs
│   ├── sales/                   # Current/planned sales materials
│   ├── research/                # Current/planned research docs
│   └── implementation/          # Current/planned implementation plans
├── samples/                     # Current/planned sample data and templates
├── prompts/                     # Planned reusable prompts
├── infra/                       # Planned infrastructure config
└── research/                    # Planned raw research materials
```

## Key Files for Agents

| File | Purpose |
|------|---------|
| `AGENTS.md` | Entry point — read this first |
| `docs/agents/00-index/agent-reading-order.md` | Defines what to read next |
| `docs/agents/00-index/project-map.md` | Current repository map |
| `docs/agents/01-principles/product-identity.md` | What this product is |
| `docs/agents/02-product/mvp-scope.md` | What we are building now |
| `docs/agents/03-technical/erpnext-strategy.md` | Why ERPNext |
| `docs/product/CEO_BRIEFING_RECORD_POLICY.md` | CEO briefing record-selection policy |
