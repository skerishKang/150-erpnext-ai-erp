# Cloud Architecture — Oracle Cloud Test Deployment

## Target Environment

**Oracle Cloud Infrastructure (OCI)** — ARM-based VM in free tier or low-cost shape.

## Recommended Instance

| Specification | Free Tier | Recommended for Pilot |
|---------------|-----------|----------------------|
| Shape | VM.Standard.A1.Flex | VM.Standard.A1.Flex |
| OCPU | 4 (configurable 1–4) | 4 |
| Memory | 24 GB | 24 GB |
| Storage | 200 GB (boot volume) | 200 GB + 100 GB block volume for DB |
| OS | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |
| Network | 1 public IP, 10 TB/month | Same |

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Oracle Cloud VM                          │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │              Docker Compose Stack                  │    │
│  │                                                    │    │
│  │  ┌──────────────┐  ┌──────────────┐               │    │
│  │  │  Nginx        │  │  ERPNext     │               │    │
│  │  │ (reverse      │◄─┤  Web (port  │               │    │
│  │  │  proxy)       │  │   8080)     │               │    │
│  │  └──────┬───────┘  └──────┬───────┘               │    │
│  │         │                 │                         │    │
│  │         │    ┌────────────▼──────────┐              │    │
│  │         │    │   Frappe Bench        │              │    │
│  │         │    │   (sites, apps)       │              │    │
│  │         │    └────────────┬──────────┘              │    │
│  │         │                 │                         │    │
│  │         │    ┌────────────▼──────────┐              │    │
│  │         └────┤   MariaDB / Postgres  │              │    │
│  │              │   (database)          │              │    │
│  │              └────────────┬──────────┘              │    │
│  │                           │                         │    │
│  │              ┌────────────▼──────────┐              │    │
│  │              │   Redis               │              │    │
│  │              │   (cache/queue)       │              │    │
│  │              └───────────────────────┘              │    │
│  │                                                    │    │
│  │  ┌──────────────────────────────────────────┐      │    │
│  │  │   Backup Volume (daily snapshot)          │      │    │
│  │  │   /mnt/backups/erpnext/                   │      │    │
│  │  └──────────────────────────────────────────┘      │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  Ports open: 80 (HTTP), 443 (HTTPS - future), 22 (SSH)  │
└─────────────────────────────────────────────────────────┘
```

## Staging vs. Production

| Aspect | Staging (First) | Production (Later) |
|--------|-----------------|-------------------|
| Domain | IP-based or subdomain | Custom domain (erp.padiem.ai) |
| SSL | Self-signed or HTTP | Let's Encrypt / Cloudflare |
| Data | Test data only | Real customer data |
| Backup | Manual or daily | Automated with retention policy |
| Monitoring | Basic health checks | Full monitoring + alerts |
| Scaling | Single VM | Multiple VMs / DB replication |

## Deployment Steps (Checklist)

### Phase 1: Provision VM
- [ ] Create Oracle Cloud account (if not exists)
- [ ] Create ARM VM (Ubuntu 22.04, VM.Standard.A1.Flex)
- [ ] Configure security list (ports 22, 80, 443)
- [ ] Set up SSH key access
- [ ] Update system packages
- [ ] Install Docker and Docker Compose

### Phase 2: Deploy ERPNext
- [ ] Clone ERPNext Docker Compose setup
- [ ] Configure environment variables
- [ ] Start stack with `docker compose up -d`
- [ ] Verify all containers healthy
- [ ] Create ERPNext site
- [ ] Configure site with sample company

### Phase 3: Configure Networking
- [ ] Assign public IP (or use reserved IP)
- [ ] Configure DNS (A record to VM IP)
- [ ] Set up Nginx reverse proxy
- [ ] Configure SSL (Let's Encrypt)

### Phase 4: Enable Monitoring
- [ ] Basic uptime monitoring
- [ ] Disk usage alert
- [ ] Container health check
- [ ] Backup success notification

## Backup Strategy

| Data | Frequency | Method | Retention |
|------|-----------|--------|-----------|
| Database (MariaDB) | Daily | `bench backup` or `mysqldump` | 7 days |
| Frappe sites | Daily | Filesystem backup | 7 days |
| Configuration | On change | Git-tracked (Docker Compose + .env) | Permanent |
| Full VM | Weekly | OCI boot volume backup | 4 weeks |

## Cost Estimate (Monthly)

| Item | Free Tier | Paid (Pilot) |
|------|-----------|--------------|
| VM compute | ₩0 (within free tier limits) | ~₩30,000–₩50,000 |
| Block storage (100 GB) | ₩0 (up to 200 GB free) | ~₩10,000 |
| Bandwidth | ₩0 (up to 10 TB/month) | ~₩0 (pilot traffic low) |
| **Total** | **~₩0** | **~₩40,000–₩60,000** |

## Security

- SSH key-only access (no password)
- Firewall: only ports 22, 80, 443 open
- Fail2ban on SSH
- Regular security updates (`unattended-upgrades`)
- Database not exposed to public network (Docker internal network only)
- .env files with secrets not committed to Git
