---
title: Email provider
type: integration
status: active
reviewed_confidence: 65
last_reviewed: 2026-06-14
sources:
  - repo: beacon-messaging
    branch: main
    sha: 7a8b9c0
    committed: 2026-05-22
domain: messaging
tags: [integration, messaging]
---

# Email provider

> The third-party email delivery service Beacon sends through. (Services that list it
> in `depends_on` show up under "Depended on by".)

## What we use it for

Actually delivering email messages and receiving delivery/bounce callbacks that feed
our [webhooks](../interfaces/webhooks/index.md).

## Interface

- **Direction** — we POST messages to their API; they POST delivery/bounce events
  back to our ingest endpoint.
- **Auth & secrets** — provider API key, stored in the secrets manager (reference
  only, never in docs).
- **Environments** — a sandbox key that black-holes real delivery.

## Failure modes

Provider 5xx / timeouts → retried per the org's
[retry policy](../options/message-settings.md); exhausted retries become a `failed`
delivery event. A provider-wide outage is the main risk for email throughput.

## Notes & nuances

!!! danger "Suspected dead"
    A second, older email provider's client is still in the tree behind a config flag
    that's been off in all environments for months.
