---
title: Admin console
type: surface
status: active
reviewed_confidence: 55
last_reviewed: 2026-06-14
sources:
  - repo: beacon-web
    branch: main
    sha: 9f8e7d6
    committed: 2026-06-02
audience: internal Beacon staff (ops / support)
tags: [admin]
---

# Admin console

> The internal app Beacon staff use to support customers — look up orgs, inspect
> deliveries, and suspend abusive accounts. Not customer-facing.

## What it offers

- **Org lookup** — find and inspect any [Organization](../models/organization.md).
- **Suspend / reinstate** — see [Suspend an organization](../features/suspend-organization.md).
- **Delivery inspection** — search delivery events across orgs (support).

## Key screens

- **Org detail** — status, plan, recent activity, the suspend action.
- **Delivery search** — cross-org delivery-event lookup.

## Roles

Internal roles only; see [Roles & permissions](../access/roles.md).

## Notes & nuances

!!! danger "Suspected dead"
    A "bulk message replay" tool exists in the console but its endpoint returns 501;
    likely never finished.
