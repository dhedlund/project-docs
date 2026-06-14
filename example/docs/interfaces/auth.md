---
title: API authentication
type: auth
status: active
reviewed_confidence: 70
last_reviewed: 2026-06-14
domain: messaging
tags: [api, auth]
---

# API authentication

> How callers authenticate to the [Messaging API](api/index.md).

## API keys

Bearer keys, scoped per environment:

- `sk_live_…` — production; `sk_test_…` — sandbox.
- Send as `Authorization: Bearer <key>`.
- Keys are created and rotated in the [dashboard](../surfaces/dashboard.md) by the
  org **owner** or **admin** (see [Roles & permissions](../access/roles.md)).

## Scopes

| Scope | Grants |
|-------|--------|
| `messages:send` | create messages |
| `messages:read` | read message status |
| `webhooks:manage` | manage webhook endpoints |

## Notes & nuances

??? warning "Key handling"
    Keys are shown once at creation. Treat them as secrets; rotate on exposure.
