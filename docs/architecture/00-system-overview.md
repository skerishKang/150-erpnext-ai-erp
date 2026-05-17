# System Overview — Padiem AI ERP

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Padiem AI ERP System                    │
│                                                          │
│  ┌─────────────────────────┐  ┌──────────────────────┐  │
│  │    ERPNext Base          │  │   Padiem AI Module   │  │
│  │                          │  │                      │  │
│  │  • Customer/Item/Vendor  │  │  • AI Provider       │  │
│  │  • Quotation / SO / DN   │  │    Adapter           │  │
│  │  • Inventory             │  │  • Prompt Templates  │  │
│  │  • Purchase Order        │  │  • ERP Data Context  │  │
│  │  • Receivables           │  │  • Summary/Report    │  │
│  │  • Accounting (future)   │  │  • Quotation Draft   │  │
│  │  • Permissions & Roles   │  │  • Audit Log         │  │
│  └──────────┬──────────────┘  └──────┬───────────────┘  │
│             │                        │                   │
│             └──────────┬─────────────┘                   │
│                        │                                  │
│              ┌─────────▼──────────┐                      │
│              │    CEO Dashboard    │                      │
│              │  (browser/desktop)  │                      │
│              └────────────────────┘                      │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │          AI Provider Abstraction Layer            │    │
│  │  DeepSeek │ OpenAI │ Claude │ Gemini │ Local     │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │           Cloud Deployment (Oracle Cloud)         │    │
│  │  Docker │ ERPNext │ DB │ Backups │ Monitoring     │    │
│  └──────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## Core Components

### 1. ERPNext Base
The operational backbone. Manages all master data and transactions: customers, items, quotations, sales orders, delivery notes, purchase orders, inventory, and receivables.

### 2. Padiem AI Module
Custom Frappe app that adds AI capabilities to ERPNext. Handles AI provider communication, prompt management, data retrieval, and output processing.

### 3. CEO Dashboard
Simplified interface focused on what a CEO needs: daily briefing, key metrics, AI quotation draft, and alert management.

### 4. AI Provider Abstraction Layer
Unified interface to multiple AI providers (see ADR-0005). Allows switching providers without code changes.

### 5. Cloud Deployment
Managed deployment on Oracle Cloud (ARM VM) using Docker Compose. See [Cloud Architecture](03-cloud-architecture.md).

## Key Design Principles

| Principle | Description |
|-----------|-------------|
| **ERP-first** | AI enhances ERP workflows, not the other way around |
| **Human-in-the-loop** | AI generates drafts; humans approve before any ERP action |
| **Provider independence** | No lock-in to any AI vendor |
| **Data privacy** | Customer data is not used for model training; clear data handling policy |
| **Minimal core modification** | Extend ERPNext through custom apps, not core forks |

## User Roles

| Role | Access | AI Features |
|------|--------|------------|
| CEO | Dashboard, reports, AI briefing | Full AI features |
| Operations staff | Quotations, orders, inventory, delivery | AI quotation draft |
| Accountant (external) | Monthly data export | No AI features |
| System admin | User management, configuration | AI provider config, audit log |

## Technology Stack (Planned)

| Layer | Technology |
|-------|-----------|
| ERP Framework | Frappe (Python, JavaScript) |
| ERP Base | ERPNext |
| Database | MariaDB (ERPNext default) |
| AI Module | Python (within Frappe) |
| AI Provider API | REST / OpenAI-compatible |
| Deployment | Docker Compose |
| Cloud | Oracle Cloud Infrastructure (ARM VM) |
| Backup | Automated volume snapshots |
| Domain/SSL | Cloudflare + Let's Encrypt (future) |
