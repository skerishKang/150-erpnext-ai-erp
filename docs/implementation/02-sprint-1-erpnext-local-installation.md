# Sprint 1: ERPNext Local Installation

**Status:** 📋 Planned

**Duration:** 1 sprint (5–7 days)

## Goal

Install ERPNext locally or in a dev environment and confirm basic login + company setup.

## Prerequisites

| Requirement | Version/Notes |
|-------------|---------------|
| Docker & Docker Compose | Latest stable |
| Git | Any recent version |
| Disk space | 10 GB+ free |
| RAM | 4 GB+ |
| Network | Internet access for Docker images |

## Installation Path

**Chosen approach:** Docker-based ERPNext installation using the official Frappe Docker Compose setup.

**Rationale:** Docker provides isolation, easy rollback, and environment consistency. Avoids direct system-level Frappe Bench installation which is complex and OS-dependent.

## Tasks

### 1. Prepare Docker Environment
- [ ] Verify Docker installation (`docker --version`, `docker compose version`)
- [ ] Verify Docker daemon is running
- [ ] Allocate sufficient disk and memory for Docker

### 2. Clone ERPNext Docker Repository
- [ ] Choose source: Frappe Docker (`frappe/docker`) or ERPNext Docker (`frappe/erpnext`)
- [ ] Clone to known location
- [ ] Read setup documentation

### 3. Create Installation Checklist
- [ ] Docker Compose configuration review
- [ ] Port mapping: 80/443 for ERPNext, 3306 for DB (internal)
- [ ] Volume mapping for persistent data
- [ ] .env configuration (db root password, admin password)

### 4. Run Installation
- [ ] `docker compose up -d`
- [ ] Wait for containers to initialize
- [ ] Check container logs for errors

### 5. Create Rollback Notes
- [ ] `docker compose down -v` removes data volumes
- [ ] Backup strategy before configuration changes
- [ ] Document what to do if installation fails

### 6. Confirm ERPNext Login
- [ ] Access ERPNext via browser (`http://localhost:8080` or configured port)
- [ ] Login with default Administrator account
- [ ] Confirm dashboard loads without errors

### 7. Confirm Sample Company Setup
- [ ] Navigate to Setup → Company
- [ ] Create a sample company (e.g., "Padiem Demo Corp")
- [ ] Confirm basic master data creation (no customization yet)

## Rollback Notes

| Failure Mode | Rollback Action |
|-------------|----------------|
| Docker Compose fails to start | Check logs, verify port availability, review .env |
| ERPNext login fails | Check `docker compose logs` for frappe-web container errors |
| Database connection error | Verify MariaDB/Postgres container is healthy |
| Site creation fails | Check bench logs in the erpnext container |
| Irrecoverable | `docker compose down -v` → delete volumes → restart clean |

## Verification Criteria

- [ ] ERPNext accessible via `http://localhost:PORT`
- [ ] Administrator login succeeds
- [ ] Sample company "Padiem Demo Corp" created
- [ ] Home/dashboard loads without console errors

## Non-Goals (this sprint)

- ❌ Do not customize ERPNext
- ❌ Do not install custom apps
- ❌ Do not modify source code
- ❌ Do not configure domains or SSL
- ❌ Do not import real customer data
