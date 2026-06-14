---
title: MySQL
type: datastore
status: active
reviewed_confidence: 80
last_reviewed: 2026-06-14
engine: MySQL 8
tags: [datastore]
---

# MySQL

> The relational store for accounts and billing — the canonical org, user, plan,
> subscription, and invoice data.

## What lives here

| Holds | Owned by | Notes |
|-------|----------|-------|
| `accounts.organizations` | accounts-service | see [Organization](../models/organization.md) |
| `billing.subscriptions` (+ `active_subscriptions_v` view) | billing-service | see [Subscription](../models/subscription.md) |

## Notes & operations

??? info "Operational notes"
    Single primary with read replicas. Daily backups, 30-day retention.
