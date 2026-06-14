---
title: Webhooks
type: webhook
status: active
reviewed_confidence: 70
last_reviewed: 2026-06-14
sources:
  - repo: beacon-messaging
    branch: main
    sha: 7a8b9c0
    committed: 2026-05-22
domain: messaging
tags: [webhooks]
---

# Webhooks

> Delivery outcomes Beacon sends to *your* endpoint. (These are customer-facing
> webhooks — distinct from the internal RabbitMQ events between Beacon's services.)

## Event catalog

| Event | When it fires | Payload | Notes |
|-------|---------------|---------|-------|
| `message.sent` | handed to the provider | `{message_id, channel}` | not yet delivered |
| `message.delivered` | provider confirmed delivery | `{message_id, channel, at}` | may arrive much later |
| `message.failed` | retries exhausted | `{message_id, reason}` | terminal |
| `message.bounced` | hard bounce (email) | `{message_id, reason}` | terminal |

Payload schemas live in `contracts/messaging/asyncapi.yaml`.

## Delivery semantics

The reliability contract to design for:

- **At-least-once** — retries and duplicates happen; be **idempotent**. Dedupe on the
  stable `message_id`; the per-attempt delivery ID (header `Beacon-Delivery`) changes.
- **Order is not guaranteed** — `delivered` can arrive before you've processed `sent`.
  Reconcile against current message state, not event sequence.
- **Retries** — exponential backoff for 24h, then the delivery is dropped (visible in
  the dashboard's webhook log).
- **Signing** — every request is signed (`Beacon-Signature`, HMAC over the body +
  timestamp); reject stale timestamps and verify before trusting.

## Subscribing

Register an endpoint and pick events in the [dashboard](../../surfaces/dashboard.md);
test with sandbox sends.

## Notes & nuances

??? info "Internal events vs webhooks"
    `message.delivered` exists twice: as an internal RabbitMQ event
    ([messaging-service](../../services/messaging-service.md)) and as this public
    webhook. They share a name and shape but are different surfaces.
