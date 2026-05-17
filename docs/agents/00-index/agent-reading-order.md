# Agent Reading Order

Every agent working in this repository must follow this reading order.

## Step 1: Entry Point

Read `AGENTS.md` in the repository root. It is the index.

## Step 2: Principles (must read before any code or docs work)

1. [01-principles/product-identity.md](../01-principles/product-identity.md) — what this product is
2. [01-principles/business-principles.md](../01-principles/business-principles.md) — business rules
3. [01-principles/customer-target.md](../01-principles/customer-target.md) — who we serve
4. [01-principles/non-goals.md](../01-principles/non-goals.md) — what we are NOT building

## Step 3: Product (understand scope before coding)

1. [02-product/mvp-scope.md](../02-product/mvp-scope.md) — MVP feature list
2. [02-product/ai-erp-positioning.md](../02-product/ai-erp-positioning.md) — why AI ERP, not AI automation
3. [02-product/module-map.md](../02-product/module-map.md) — module structure
4. [02-product/first-demo-scenario.md](../02-product/first-demo-scenario.md) — demo flow

## Step 4: Technical (before implementation)

1. [03-technical/erpnext-strategy.md](../03-technical/erpnext-strategy.md) — ERPNext approach
2. [03-technical/ai-provider-strategy.md](../03-technical/ai-provider-strategy.md) — AI provider plan
3. [03-technical/cloud-deployment-strategy.md](../03-technical/cloud-deployment-strategy.md) — deployment plan
4. [03-technical/data-security-rules.md](../03-technical/data-security-rules.md) — what never to commit

## Step 5: Operations (before committing or pushing)

1. [04-operations/git-rules.md](../04-operations/git-rules.md) — git workflow
2. [04-operations/local-development-rules.md](../04-operations/local-development-rules.md) — local dev setup
3. [04-operations/commit-policy.md](../04-operations/commit-policy.md) — commit messages
4. [04-operations/test-policy.md](../04-operations/test-policy.md) — testing approach

## Step 6: Prompts (when generating code or handoffs)

1. [05-prompts/vibe-coding-rules.md](../05-prompts/vibe-coding-rules.md) — coding behavior
2. [05-prompts/cto-handoff-prompt.md](../05-prompts/cto-handoff-prompt.md) — CTO handoff template
3. [05-prompts/erpnext-installation-agent-prompt.md](../05-prompts/erpnext-installation-agent-prompt.md) — ERPNext install prompt

## Exceptions

- **Quick fixes:** If the task is a small fix, read Step 1 + Step 2 (principles) only.
- **Documentation-only work:** Steps 1–2 are sufficient.
- **Code changes:** Follow all steps.
- **Infrastructure/deployment:** Add Step 4 (technical) emphasis.
