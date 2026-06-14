---
title: Glossary
type: glossary
status: active
reviewed_confidence: 85
last_reviewed: 2026-06-14
tags: [reference]
---

# Glossary

Beacon's shared vocabulary. Define each term once; the canonical page carries the
detail.

### Delivery event

A write-once record of one message send attempt and its outcome. See:
[Delivery event](models/delivery-event.md).

### Dunning

The automated retry-and-notify process after a failed payment, before a subscription
is canceled. See [Subscription](models/subscription.md) (the `past_due` state).

### Organization

A customer account — the top-level tenant that users belong to and that holds a
subscription. See: [Organization](models/organization.md).

### Past due

A [Subscription](models/subscription.md) whose latest payment failed: it enters
dunning, and reverts to active if payment recovers or is canceled if it doesn't.

### Plan

The package an organization pays for; determines price, seat limit, and features. A
subscription references one plan. *(Dedicated page pending — see
[Subscription](models/subscription.md).)*

### Proration

Charging the prorated difference when a plan changes mid-cycle (computed in
billing-service). See [Plan upgrade](features/plan-upgrade.md).

### Seat

One paid-for user slot on a subscription. "Seats in use" counts those actually
assigned to users. See: [Subscription](models/subscription.md).

### Subscription

What an organization is currently paying for: a plan, a billing cycle, and a
lifecycle status. See: [Subscription](models/subscription.md).
