---
# Organic frontmatter — see templates/model.md for the philosophy.
# REQUIRED:  title · type (webhook) · status
# SUGGESTED: reviewed_confidence · last_reviewed · sources · domain · tags
title: Webhooks
type: webhook
status: unknown
reviewed_confidence:
last_reviewed:
sources:
  # - repo: <name>      # and contracts/webhooks/asyncapi.yaml
  #   branch: main
  #   sha:
  #   committed:
tags: [webhooks]
---

# Webhooks

> What events the platform sends to customers, and how to consume them reliably.
> (Outbound webhooks are *not* the same as internal service events — keep them
> separate.)

## Event catalog

| Event | When it fires | Payload | Notes |
|-------|---------------|---------|-------|
|  |  |  |  |

Payload schemas live in `contracts/webhooks/asyncapi.yaml`.

## Delivery semantics

The reliability contract consumers must design for:

- **At-least-once** — retries and duplicates happen; handlers must be **idempotent**.
  Dedupe on the stable *event ID*; the per-attempt *delivery ID* (header) changes.
- **Order is not guaranteed** — don't assume sequence; reconcile against the current
  resource state when it matters.
- **Retries** — the backoff schedule, max attempts, and what happens after (DLQ?).
- **Signing & verification** — how payloads are signed, the timestamp tolerance, and
  secret rotation.

## Subscribing

How to register an endpoint, choose events, and test in sandbox.

## Notes & nuances
