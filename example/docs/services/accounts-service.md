---
title: accounts-service
type: service
status: stub
reviewed_confidence: 20
last_reviewed: 2026-06-14
language: java
owned_models:
  - organization
depends_on:
  - mysql
domain: accounts
tags: [accounts]
---

# accounts-service

> **Stub.** Owns organizations and users — the tenant and identity layer. Billing and
> messaging read it as the authority on who exists, org status, and seat counts.
> Java/Spring on MySQL.

This page is a stub: known shape only, not yet deepened (see the `DOC-DEEPEN` entry
in the backlog). What's known so far:

- **Owns:** organizations (see [Organization](../models/organization.md)) and users.
- **Exposes:** `GET /orgs/{id}` (seat count + status), consumed by
  [billing-service](billing-service.md); a suspend endpoint used by
  [Suspend an organization](../features/suspend-organization.md).
- **Does not own:** anything billing- or messaging-related.

To deepen: confirm the full HTTP surface against `beacon-accounts`, add a contract,
and document the `User` model.
