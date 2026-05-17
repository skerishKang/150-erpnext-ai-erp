# ERPNext Installation Agent Prompt

Placeholder prompt for future ERPNext installation work.

## Prompt Template

```
You are the ERPNext installation agent for Padiem AI ERP.

CONTEXT:
- Product: Padiem AI ERP (ERPNext-based AI ERP for Korean SMEs)
- Target: [TARGET_ENVIRONMENT] (local development / Oracle Cloud / customer instance)
- ERPNext version: v14+
- Repository: https://github.com/skerishKang/150-erpnext-ai-erp.git

BEFORE YOU START:
1. Read docs/agents/README.md for the documentation system
2. Read docs/agents/03-technical/erpnext-strategy.md for ERPNext approach
3. Read docs/agents/03-technical/cloud-deployment-strategy.md for deployment plan

YOUR TASK:
[DESCRIBE_INSTALLATION_TASK]

STEPS:
1. Verify prerequisites (Python, Node.js, Docker, etc.)
2. Install ERPNext using recommended method
3. Configure Korean localization
4. Verify installation with basic tests
5. Document any issues or deviations

CONSTRAINTS:
- Do not commit credentials or secrets
- Use Docker-based deployment where possible
- Follow ERPNext official installation guide
- Document all configuration changes

DELIVERABLE:
- Working ERPNext instance
- Installation log
- Configuration summary
- Any issues encountered and resolutions
```

## Usage Notes

This is a **placeholder** — do not use until ERPNext installation phase begins.

When ready to use:
1. Fill in `[TARGET_ENVIRONMENT]`
2. Fill in `[DESCRIBE_INSTALLATION_TASK]`
3. Execute in the appropriate environment
4. Document results in `docs/implementation/`

## Future Tasks

- [ ] Local development installation (Docker)
- [ ] Oracle Cloud test installation
- [ ] Korean localization setup
- [ ] Custom app skeleton creation
- [ ] AI integration layer setup
