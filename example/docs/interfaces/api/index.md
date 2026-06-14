---
title: Messaging API
type: api
status: active
reviewed_confidence: 75
last_reviewed: 2026-06-14
sources:
  - repo: beacon-messaging
    branch: main
    sha: 7a8b9c0
    committed: 2026-05-22
domain: messaging
tags: [api]
---

# Messaging API

> The public REST API for sending messages and checking their status. Used by
> customer backends and our own [SDKs](../sdks/python.md).

## Basics

- **Base URL / environments** — `https://api.beacon.example` (prod),
  `https://api.sandbox.beacon.example` (sandbox).
- **Auth** — bearer API key; see [Auth](../auth.md).
- **Versioning** — date-pinned via the `Beacon-Version` header; breaking changes ship
  under a new date and old versions are supported for 12 months.
- **Errors** — JSON `{code, message}`; `429` carries `Retry-After`.

## Reference

Rendered from the OpenAPI spec (compiled from `contracts/public-api/`).

<swagger-ui src="openapi.yaml"/>

## Guides

- [Authentication](../auth.md)
- [Webhooks](../webhooks/index.md) — how to get notified of delivery outcomes
- [Python SDK](../sdks/python.md)

## Notes & nuances

??? info "Idempotency"
    `POST /messages` accepts an `Idempotency-Key` header so retries don't double-send.
