# Risk Register — Padiem AI ERP

This register documents identified risks, their potential impact, and planned mitigations.

## Risk Table

| # | Risk | Probability | Impact | Mitigation | Owner |
|---|------|-------------|--------|------------|-------|
| R1 | **ERPNext installation complexity** | Medium | High | Use Docker Compose path; document rollback; test on clean environment first | Dev |
| R2 | **Korean localization gaps** | Medium | Medium | Identify gaps early (language, tax, date formats, currency); contribute to ERPNext Korea community or build custom patches | Dev + Product |
| R3 | **Customer expects full accounting (tax filing, VAT, payroll)** | High | Medium | ADR-0003 explicitly excludes full accounting from MVP; set expectations in sales materials and pilot contract | Product + Sales |
| R4 | **Customer confusion: "ERPNext is just Ecount with AI"** | Medium | High | Position as Padiem AI ERP, not "ERPNext"; emphasize AI-native workflows, CEO dashboard, AI draft, daily briefing | Sales + Marketing |
| R5 | **AI hallucination in generated quotations or reports** | High | High | Human approval step before any ERP action; structured output contracts; output validation; clear disclaimer on AI-generated content | Engineering |
| R6 | **Data security — customer data sent to third-party AI provider** | High | High | AI provider contract must include data non-retention clause; offer local model option for sensitive data (via abstraction layer); encrypt data in transit and at rest | Engineering + Legal |
| R7 | **Cloud cost exceeds pilot budget** | Medium | Medium | Start on Oracle Cloud free tier (ARM VM); set cost alerts; monitor usage; define pricing model before scaling | Ops |
| R8 | **Maintenance burden (ERPNext updates, security patches, backups)** | Medium | Medium | Docker-based deployment simplifies updates; automated backup scripts; scheduled maintenance window; monitoring | Ops |
| R9 | **Korean tax law changes** | Low | Medium (post-MVP) | Defer to post-MVP; use accountant-ready document preparation rather than tax filing | Product |
| R10 | **AI provider API changes or price increases** | Medium | Medium | AI provider abstraction layer (ADR-0005) enables switching; negotiate volume pricing if scaling | Engineering |
| R11 | **Customer onboards but does not adopt** | Medium | High | Structured pilot with weekly check-ins; define success metrics before pilot; gather feedback early | Sales + Product |
| R12 | **ERPNext version upgrade breaks customizations** | Low | Medium | Prefer custom apps and hooks over core modifications; test upgrades in staging before applying to production | Dev |

## Risk Matrix

```
Impact
  High    │ R3  R5  R6        R11
          │
  Medium  │ R2  R4  R8  R12   R1  R10
          │
  Low     │ R9                R7
          └──────────────────────────
              Low   Med   High
                    Probability
```

## Trigger Monitoring

| Risk | Trigger | Action |
|------|---------|--------|
| R1 | Docker compose fails on first attempt | Switch to manual Frappe Bench install; document issues |
| R5 | AI generates invalid quotation JSON twice in a row | Tighten prompt; reduce model temperature; add fallback |
| R6 | Customer asks where their data goes | Show data flow diagram; explain AI provider policy; offer local model option |
| R7 | Monthly cloud cost > ₩100,000 | Review resource usage; consider migrating to smaller instance |
| R11 | Customer does not use system for 5+ days in pilot | Proactive check-in; offer training session; simplify onboarding |

## Review Cadence

- Risk register reviewed **every sprint**
- New risks added as discovered
- Closed risks moved to "Observed" section after 3 sprints without recurrence
