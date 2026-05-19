# Project Map

Repository structure for Padiem AI ERP.

```
150-erpnext-ai-erp/
├── AGENTS.md                    # Agent index (entry point for AI agents)
├── README.md                    # Project overview
├── padiem_ai/                   # ERPNext app/runtime code
│   └── padiem_ai/
│       ├── ai/                  # AI provider layer and config guards
│       ├── api/                 # API endpoint wrappers
│       ├── briefing/            # CEO briefing generation logic
│       ├── dashboard/           # ERP dashboard page
│       ├── erp/                 # ERP read-only data access
│       ├── www/                 # Web controllers and entry points
│       └── ...                  # Audit, data, page, prompts, public
├── docs/
│   ├── agents/                  # Agent instruction system
│   │   ├── README.md            # How agent docs work
│   │   ├── 00-index/            # Maps and reading order
│   │   ├── 01-principles/       # Product identity, business rules
│   │   ├── 02-product/          # MVP, modules, positioning
│   │   ├── 03-technical/        # ERPNext, AI, cloud, security
│   │   ├── 04-operations/       # Git, dev rules, testing
│   │   └── 05-prompts/          # Reusable prompts
│   ├── product/                 # Product specs (future)
│   ├── architecture/            # Technical architecture (future)
│   ├── sales/                   # Sales materials (future)
│   ├── research/                # Research docs (future)
│   └── implementation/          # Implementation plans (future)
├── prompts/                     # Reusable prompts (future)
├── samples/                     # Sample data and templates (future)
├── infra/                       # Infrastructure config (future)
└── research/                    # Raw research materials (future)
```

## Key Files for Agents

| File | Purpose |
|------|---------|
| `AGENTS.md` | Entry point — read this first |
| `docs/agents/00-index/agent-reading-order.md` | Defines what to read next |
| `docs/agents/01-principles/product-identity.md` | What this product is |
| `docs/agents/02-product/mvp-scope.md` | What we are building now |
| `docs/agents/03-technical/erpnext-strategy.md` | Why ERPNext |
