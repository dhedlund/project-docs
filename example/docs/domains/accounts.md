---
title: Accounts
type: domain
status: active
reviewed_confidence: 75
last_reviewed: 2026-06-14
tags: [accounts]
---

# Accounts

> Organizations and the users inside them — the tenant and identity layer every other
> domain reads from.

## Capabilities

- **Manage an organization** — its profile, seats, and status.
- **Suspend / reinstate** — see [Suspend an organization](../features/suspend-organization.md).

## How it fits together

accounts-service owns the org and user records; billing and messaging read them but
never write them.

<!-- Pages that declare `domain: accounts` are listed automatically below. -->
