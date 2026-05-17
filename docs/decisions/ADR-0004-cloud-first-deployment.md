# ADR-0004: Cloud-First Deployment

**Status:** Accepted

**Date:** 2026-05-16

## Context

The product needs a deployment model. Options include:

1. **On-premise only** — customer installs on their own infrastructure
2. **Cloud-first** — we host and manage; customer accesses via browser
3. **Hybrid** — both options available

The Korean SME ERP market is dominated by cloud-managed services (Ecount, iU for small businesses). On-premise is still present but declining for SMEs.

## Decision

The product is **cloud-first**.

Initial cloud deployment target is **Oracle Cloud (free tier / low-cost VM)**.

On-premise deployment may be offered later for enterprise customers, but the primary delivery model is managed cloud ERP.

## Rationale

- The business model is **managed cloud ERP**, similar to Ecount's SaaS model.
- Cloud deployment gives us **control over updates, backups, monitoring, and scalability**.
- Oracle Cloud free tier provides a capable ARM VM (4 OCPU, 24 GB RAM) suitable for initial testing and pilot customers.
- Cloud-first enables **usage-based pricing** and **automatic upgrades**.
- Korean SMEs are already comfortable with cloud ERP (Ecount has 700,000+ companies).
- Single deployment model simplifies DevOps and support burden during MVP.

## Consequences

**Positive:**
- Single deployment target reduces DevOps complexity
- Easy to monitor, patch, and upgrade
- Usage analytics and product improvement data
- Predictable hosting cost for pilots

**Negative:**
- Customers requiring on-premise (security policy, data sovereignty) cannot be served initially
- Cloud infrastructure cost must be managed during pilot phase
- Internet dependency for customer access
- Oracle Cloud ARM availability may vary by region

## Deployment Architecture (MVP)

```
Oracle Cloud VM (ARM)
├── Docker Compose
│   ├── ERPNext (Frappe + frontend)
│   ├── MariaDB
│   ├── Redis (for Frappe)
│   └── Nginx (reverse proxy)
├── Backup volume (daily snapshot)
└── Monitoring (basic health check)
```

## Alternatives Considered

| Alternative | Reason against |
|-------------|----------------|
| On-premise only | No recurring revenue model, harder to support, harder to update |
| AWS / Azure | Higher cost for equivalent ARM capacity vs Oracle free tier |
| On-premise + cloud hybrid | Adds DevOps complexity before MVP is validated |

## Related Documents

- [Cloud Deployment Strategy](../agents/03-technical/cloud-deployment-strategy.md)
- [Architecture: Cloud Architecture](../architecture/03-cloud-architecture.md)
