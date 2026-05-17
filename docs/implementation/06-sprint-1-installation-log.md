# Sprint 1: Installation Log

**Date:** 2026-05-18
**Status:** Environment verified, Docker ready

## Environment Check Results

### Docker

| Check | Result |
|-------|--------|
| Docker installed | ✅ Docker v28.3.2 (build 578ccf6) |
| Docker Compose | ✅ v2.39.1-desktop.1 |
| Docker daemon | ✅ Running (required Docker Desktop start) |
| Platform | x86_64 |
| CPUs | 12 |
| RAM | ~39 GB |

### WSL

| Check | Result |
|-------|--------|
| WSL available | ✅ |
| Ubuntu-24.04 | ✅ Running |
| docker-desktop | Stopped (using Docker Desktop instead) |

### Lab Folder

| Check | Result |
|-------|--------|
| Lab folder created | ✅ `G:\Ddrive\BatangD\task\workdiary\150-erpnext-ai-erp-lab` |
| frappe_docker cloned | ✅ `150-erpnext-ai-erp-lab\frappe_docker` |
| frappe_docker version | v3.2.0 (latest tag) |
| ERPNext version (example.env) | v16.18.3 |

## frappe_docker Structure

```
frappe_docker/
├── compose.yaml              # Main compose file (base services)
├── example.env               # Environment variables template
├── pwd.yml                   # Quick test compose (Play with Docker)
├── overrides/                # Compose overrides
│   ├── compose.mariadb.yaml  # MariaDB service
│   ├── compose.redis.yaml    # Redis service
│   ├── compose.https.yaml    # HTTPS/Traefik
│   └── ...                   # More overrides
├── images/                   # Dockerfile definitions
├── docs/                     # Documentation
└── development/              # Dev environment tools
```

## Key Files

### compose.yaml

Base services defined:
- `configurator` — initialization (sets DB/Redis config)
- `backend` — Frappe/Gunicorn application server
- `frontend` — Nginx reverse proxy
- `websocket` — Socket.IO for real-time
- `queue-short` — RQ worker (short tasks)
- `queue-long` — RQ worker (long tasks)
- `scheduler` — Frappe scheduler

### example.env

Key defaults:
- `ERPNEXT_VERSION=v16.18.3`
- `DB_PASSWORD=123`
- `HTTP_PUBLISH_PORT=8080` (default)

## Quick Test Plan (pwd.yml)

The fastest way to test ERPNext:

```bash
cd G:\Ddrive\BatangD\task\workdiary\150-erpnext-ai-erp-lab\frappe_docker
docker compose -f pwd.yml up -d
# Wait ~5 minutes for site creation
# Access: http://localhost:8080
# Login: Administrator / admin
```

**Not yet executed — containers not started per instructions.**

## Next Steps

1. Start containers using `pwd.yml` (quick test)
2. Verify ERPNext login at `http://localhost:8080`
3. Create sample company
4. Test basic doctypes (Customer, Item, Quotation)
5. Document results in this file

## Notes

- Docker Desktop must be running before Docker commands work
- The `pwd.yml` is the simplest path — single file, no overrides needed
- Production setup requires `compose.yaml` + `compose.mariadb.yaml` + `compose.redis.yaml`
- Windows path: use Git Bash or WSL for Docker commands
