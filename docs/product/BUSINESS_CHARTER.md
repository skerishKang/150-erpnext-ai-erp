# Padiem AI ERP Business Charter

- Decision date: 2026-09-05
- Portfolio slot: `10`
- Business name: `Padiem AI ERP`
- Business status: `ACTIVE / INCUBATION`
- Product stage: `EARLY MVP → OPERATIONS-READY`
- Production status: `NOT YET`
- Base platform: `ERPNext / Frappe`
- Primary market: Korean SMEs, initially organizations with approximately 5–100 employees
- Promotion authority issue: [#147](../../issues/147)
- Operations-readiness epic: [#145](../../issues/145)

## 1. Business Decision

`150-erpnext-ai-erp` is promoted from an internal development project to an independent PADIEM business line under the portfolio identity **`10. Padiem AI ERP`**.

This is a business and portfolio decision. It is **not** a declaration that the current repository is production-ready. The repository must continue to describe the implementation as an early ERPNext app/runtime MVP until the release gates are proven in a real supported Frappe/ERPNext environment.

## 2. Product Definition

Padiem AI ERP is an ERP product for Korean SMEs built on ERPNext/Frappe. The ERP system is the product; AI is embedded inside ERP workflows to reduce search, reporting, drafting, and monitoring overhead.

Initial business domains include:

- quotation
- sales orders
- purchasing
- inventory
- delivery
- receivables and payments
- executive reporting and CEO briefing

AI capabilities may include:

- natural-language ERP query
- ERP data summarization
- document and communication drafts
- risk, delay, and receivables alerts
- executive briefing

AI must operate within ERP authorization, data-governance, audit, and human-approval boundaries.

## 3. Product Boundary

Padiem AI ERP is not:

- a generic chatbot attached to ERP
- a generic agent platform
- an autonomous accounting or tax system
- a payroll automation product in the first version
- a system that bypasses ERPNext/Frappe permissions
- a system that performs high-impact ERP writes without explicit human approval

The first operations-ready release should prioritize trustworthy read-only intelligence and controlled, reviewable assistance before autonomous actions.

## 4. Position Inside PADIEM

### PADIEM CORE / shared AI technology

PADIEM CORE and shared AI components may provide model routing, RAG, agent, workflow, evaluation, observability, and other reusable capabilities.

These are enabling technology layers. They do not replace the Padiem AI ERP product boundary.

### Padiem AI ERP

Padiem AI ERP owns the customer-facing ERP product experience, ERP data contract, ERP authorization boundary, business metrics, installation lifecycle, operational reliability, and vertical product roadmap.

### 이어온

이어온 remains a separate product centered on organizational memory, people, projects, documents, decisions, and semantic relationships. It should not become a duplicate ERP. Future integration between ERP transactions and organizational context is allowed only through explicit product contracts.

## 5. Commercialization Thesis

The product targets SMEs that already need ERP functions but still depend heavily on manual searching, spreadsheets, repeated reporting, and management-side aggregation.

The initial commercial value proposition is:

> Keep the operational discipline of ERP while making the system substantially easier to query, understand, and act on through embedded AI assistance.

Potential business models may later include hosted subscription, managed deployment, implementation services, and premium AI capabilities. Pricing and packaging are not fixed by this charter and require separate market validation.

## 6. Operations-Readiness Priority

Before broad feature expansion, prove that the product works safely in a real ERPNext/Frappe runtime.

Primary sequence:

```text
#131 Frappe bench environment
→ #133 standard app installation/package contract
→ #130 real ERPNext/Frappe runtime smoke
→ #134 Company and row-level User Permission boundary
→ #135 metric error model: real zero vs query failure
```

After these gates, continue through the P1/P2 program tracked by [#145](../../issues/145).

## 7. Release Boundary

Until P0 release gates are complete:

- use only local, disposable, or staging ERPNext sites
- use synthetic or irreversibly anonymized data
- keep the default provider as `mock`
- do not use production AI credentials
- do not expose briefing data to users whose company or row-level authorization has not been proven
- do not claim production readiness from static/unit tests alone

## 8. Governance

The following records are authoritative for this business inside this repository:

1. [#147 — business promotion and portfolio boundary](../../issues/147)
2. this Business Charter
3. [#145 — operations-readiness execution epic](../../issues/145)
4. README and release-gate documentation
5. implementation code and exact-head CI/runtime evidence

If business status and production status differ, they must remain separately stated. A product may be an active business while still being pre-production.

## 9. Promotion Completion Criteria

Business promotion is considered recorded in GitHub when:

- this charter exists on `main`
- README states the business, product, and production statuses separately
- #147 links the resulting merged commit
- #145 references the promotion decision and P0 execution order

Production readiness remains governed by the technical release gates and is not implied by completion of these documentation steps.
