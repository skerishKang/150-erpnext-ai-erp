# ERPNext Docker Lab Plan

## Purpose

The lab folder (`150-erpnext-ai-erp-lab`) is a separate directory for ERPNext Docker experiments.
It is NOT inside the main project repository to keep the main repo clean.

## Folder Structure

```
G:\Ddrive\BatangD\task\workdiary\
├── 150-erpnext-ai-erp/          # Main project repo (documentation, planning)
└── 150-erpnext-ai-erp-lab/      # Lab folder (Docker experiments)
    └── frappe_docker/           # Cloned from github.com/frappe/frappe_docker
        ├── compose.yaml
        ├── example.env
        ├── pwd.yml
        └── overrides/
```

## Why Separate?

1. **Main repo stays clean** — no Docker volumes, no database files, no build artifacts
2. **Lab is disposable** — can delete and reclone without affecting project docs
3. **Git separation** — lab folder is NOT tracked by the main project's git
4. **Experimentation** — safe to break, reset, and retry

## Experiment Plan

### Phase 1: Quick Test (pwd.yml)

**Goal:** Confirm ERPNext runs locally.

```bash
cd G:\Ddrive\BatangD\task\workdiary\150-erpnext-ai-erp-lab\frappe_docker
docker compose -f pwd.yml up -d
docker compose -f pwd.yml logs -f create-site
```

**Expected result:**
- Containers start (backend, frontend, db, redis, websocket, workers, scheduler)
- Site creation completes (~5 minutes)
- Accessible at `http://localhost:8080`
- Login: `Administrator` / `admin`

**Verification:**
- [ ] `docker compose -f pwd.yml ps` shows all services running
- [ ] Browser opens `http://localhost:8080` and shows ERPNext login
- [ ] Login succeeds with Administrator/admin

### Phase 2: Master Data Test

**Goal:** Create basic ERP data.

- [ ] Create sample company
- [ ] Create Customer record
- [ ] Create Supplier record
- [ ] Create Item records (3–5 items)
- [ ] Create Quotation
- [ ] Create Sales Order (from Quotation)

### Phase 3: API Test

**Goal:** Verify ERPNext REST API works.

```bash
# Get auth token
curl -X POST http://localhost:8080/api/method/login \
  -d '{"usr":"Administrator","pwd":"admin"}'

# List customers
curl http://localhost:8080/api/resource/Customer \
  -H "Authorization: token xxx:yyy"

# Create customer via API
curl -X POST http://localhost:8080/api/resource/Customer \
  -H "Authorization: token xxx:yyy" \
  -H "Content-Type: application/json" \
  -d '{"data":{"customer_name":"테스트 고객","customer_type":"Company"}}'
```

**Verification:**
- [ ] API returns JSON responses
- [ ] CRUD operations work on Customer, Item, Quotation
- [ ] Korean text is handled correctly

### Phase 4: Production-like Setup

**Goal:** Test with MariaDB + Redis overrides (closer to production).

```bash
cd G:\Ddrive\BatangD\task\workdiary\150-erpnext-ai-erp-lab\frappe_docker

docker compose \
  -f compose.yaml \
  -f overrides/compose.mariadb.yaml \
  -f overrides/compose.redis.yaml \
  up -d
```

**Verification:**
- [ ] All services start with separate MariaDB and Redis containers
- [ ] ERPNext accessible and functional
- [ ] Data persists after `docker compose down` and `up`

### Phase 5: Custom App Test (Future)

**Goal:** Test installing a custom Frappe app.

- [ ] Create `padiem_ai` custom app scaffold
- [ ] Install app into ERPNext site
- [ ] Verify custom doctype creation
- [ ] Verify custom API endpoint

## Cleanup Commands

```bash
# Stop all containers
docker compose -f pwd.yml down

# Stop and remove all data (full reset)
docker compose -f pwd.yml down -v

# Remove unused Docker resources
docker system prune

# Nuclear option (remove everything Docker-related)
docker system prune -a --volumes
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8080 in use | Change `HTTP_PUBLISH_PORT` in `.env` or stop conflicting service |
| Container won't start | `docker compose logs <service>` to check errors |
| Site creation fails | Wait longer (5–10 min), check `create-site` logs |
| Can't connect | Verify Docker Desktop is running, check `docker ps` |
| Out of disk space | `docker system prune -a --volumes` (deletes all data!) |

## Current Status

- [x] Lab folder created
- [x] frappe_docker cloned (v3.2.0)
- [x] Docker verified (v28.3.2)
- [x] Docker Compose verified (v2.39.1)
- [ ] Phase 1: Quick test (not started)
- [ ] Phase 2: Master data test (not started)
- [ ] Phase 3: API test (not started)
- [ ] Phase 4: Production-like setup (not started)
- [ ] Phase 5: Custom app test (not started)
