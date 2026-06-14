---
title: Roles & permissions
type: roles
status: active
reviewed_confidence: 65
last_reviewed: 2026-06-14
tags: [access]
---

# Roles & permissions

> Who can do what in Beacon. Customer-facing roles live on an organization; internal
> roles belong to Beacon staff.

## Customer roles (per organization)

- **Owner** — full control, including billing and API keys; one per org.
- **Admin** — everything except deleting the org / transferring ownership.
- **Member** — send messages and view delivery; no settings.

## Internal roles (Beacon staff)

- **Support** — read-only org lookup + delivery search ([admin console](../surfaces/admin-console.md)).
- **Ops** — support, plus suspend/reinstate.

## Permission matrix

| Action | Owner | Admin | Member | Support | Ops |
|--------|-------|-------|--------|---------|-----|
| Send a message | ✅ | ✅ | ✅ | — | — |
| Edit message settings | ✅ | ✅ | — | — | — |
| Manage API keys / webhooks | ✅ | ✅ | — | — | — |
| Manage billing / plan | ✅ | — | — | — | — |
| Suspend an org | — | — | — | — | ✅ |
| Org / delivery lookup | own org | own org | own org | any | any |

## Notes & nuances

??? info "Where it's enforced"
    Customer permissions are enforced in accounts-service and the dashboard; internal
    roles in the admin console. App-only checks today — not a separate policy service.
