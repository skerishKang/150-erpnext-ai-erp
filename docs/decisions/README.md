# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for the Padiem AI ERP project.

## What is an ADR?

An Architecture Decision Record is a short document that captures a significant architectural decision, its context, the alternatives considered, and the rationale for the chosen approach.

## Why we record decisions

Decisions are recorded here so that future agents, contributors, and stakeholders:

- Understand *why* the product is built the way it is
- Do not reverse or re-litigate settled strategy questions
- Can quickly onboard without repeating earlier analysis
- Have a clear chain of reasoning when trade-offs arise

## ADR Lifecycle

| Status | Meaning |
|--------|---------|
| **Proposed** | Under discussion, not yet accepted |
| **Accepted** | Decision made and in effect |
| **Deprecated** | Superseded by a later ADR |
| **Superseded** | Replaced by a newer ADR |

## Current ADRs

| # | Title | Status |
|---|-------|--------|
| 0001 | Use ERPNext as initial base | Accepted |
| 0002 | Position product as AI ERP, not automation | Accepted |
| 0003 | Exclude full accounting from MVP | Accepted |
| 0004 | Cloud-first deployment | Accepted |
| 0005 | AI provider abstraction | Accepted |

## How to add a new ADR

1. Copy the format of an existing ADR
2. Assign the next sequential number
3. Fill in: Title, Status, Context, Decision, Consequences
4. Submit as a PR or push directly with a descriptive commit message
