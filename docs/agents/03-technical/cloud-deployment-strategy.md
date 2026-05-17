# Cloud Deployment Strategy

## Direction

Padiem AI ERP is a **cloud ERP**. No on-premise deployment for initial version.

## Initial Platform

**Oracle Cloud Infrastructure (OCI)** for testing and development.

### Why Oracle Cloud

- Free tier available for testing
- Good price-performance for database workloads
- Korean region available
- ARM-based instances (cost-effective)

## Deployment Architecture (Initial)

```
Internet
    │
    ▼
Reverse Proxy (Nginx)
    │
    ├── ERPNext Application (Frappe/Gunicorn)
    │
    ├── MariaDB Database
    │
    └── AI Service (Python/FastAPI)
            │
            ▼
        External AI Provider (DeepSeek)
```

## Future: Customer-Specific Instances

Each customer gets their own cloud instance:

- Isolated database
- Isolated file storage
- Shared application layer (multi-tenant) or dedicated instances
- Customer-specific AI configuration

### Instance Sizing (Tentative)

| Customer Size | CPU | RAM | Storage |
|---------------|-----|-----|---------|
| Small (5-20 users) | 2 vCPU | 4 GB | 50 GB |
| Medium (20-50 users) | 4 vCPU | 8 GB | 100 GB |
| Large (50-100 users) | 8 vCPU | 16 GB | 200 GB |

## Container Strategy

- Docker for application packaging
- Docker Compose for development
- Kubernetes for production (future)

## Backup Strategy (Planned)

- Database: Daily automated backup
- Files: Daily incremental backup
- Retention: 30 days minimum
