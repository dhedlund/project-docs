---
title: Plan
type: model
status: stub
reviewed_confidence: 20
last_reviewed: 2026-06-14
owned_by: billing-service
related_models:
  - subscription
tags: [billing]
---

# Plan

> **Stub.** The package an organization pays for — price, billing interval, seat
> limit, and feature set. A [Subscription](subscription.md) references exactly one
> plan via `plan_id`.

This page is a stub: known shape only, not yet deepened (see the `DOC-DEEPEN` entry
in the backlog). To deepen: document the `plans` table, the pricing/interval fields,
and how `seat_limit` flows to [Organization](organization.md), against
`beacon-billing`.
