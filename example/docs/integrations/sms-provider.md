---
title: SMS provider
type: integration
status: active
reviewed_confidence: 60
last_reviewed: 2026-06-14
sources:
  - repo: beacon-messaging
    branch: main
    sha: 7a8b9c0
    committed: 2026-05-22
domain: messaging
tags: [integration, messaging]
---

# SMS provider

> The third-party SMS gateway Beacon sends text messages through.

## What we use it for

Delivering SMS messages and receiving delivery receipts.

## Interface

- **Direction** — we POST messages; they POST delivery receipts to our ingest.
- **Auth & secrets** — account SID + auth token in the secrets manager.
- **Environments** — magic test numbers that simulate delivered/failed without
  sending.

## Failure modes

Carrier rejections (invalid number, opt-out) are terminal `failed` events, not
retried; transient gateway errors follow the retry policy.

## Notes & nuances

??? info "Number pooling"
    Outbound numbers are pooled per region; deliverability varies by destination
    country.
