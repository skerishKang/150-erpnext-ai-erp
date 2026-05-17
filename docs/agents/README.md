# Agent Documentation System

This folder contains all instructions for AI agents working on the Padiem AI ERP project.

## How It Works

- **AGENTS.md** (root) is a short index file. It points here.
- **This folder** (`docs/agents/`) contains all detailed instructions.
- Instructions are organized into numbered folders by topic.

## Reading Order

Always start with [00-index/agent-reading-order.md](00-index/agent-reading-order.md).
It defines what each type of agent must read and in what order.

## Folder Map

| Folder | Contents |
|--------|----------|
| `00-index/` | Project map and agent reading order |
| `01-principles/` | Product identity, business principles, customer targets, non-goals |
| `02-product/` | MVP scope, AI ERP positioning, module map, demo scenarios |
| `03-technical/` | ERPNext strategy, AI providers, cloud deployment, data security |
| `04-operations/` | Git rules, local development, commit policy, test policy |
| `05-prompts/` | Reusable prompts for Vibe coding, CTO handoff, ERPNext installation |

## Rules

1. Never put detailed instructions in the root `AGENTS.md`.
2. All new agent instructions go in the appropriate subfolder here.
3. Update `00-index/project-map.md` when adding new files.
4. Keep each file focused on one topic.
