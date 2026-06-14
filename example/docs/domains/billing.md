---
title: Billing
type: domain
status: active
reviewed_confidence: 78
last_reviewed: 2026-06-14
tags: [billing]
---

# Billing

> Plans, subscriptions, and invoicing — what an organization pays for and how it's
> charged.

## Capabilities

- **Subscribe & change plan** — see [Plan upgrade](../features/plan-upgrade.md).
- **Track entitlement** — the authority other domains read for what a customer has.

## How it fits together

billing-service owns subscriptions and plans; it reads org/seat data from Accounts
and emits events the rest of the system reacts to.

<!-- Pages that declare `domain: billing` are listed automatically below. -->
