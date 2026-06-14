---
title: RabbitMQ
type: datastore
status: active
reviewed_confidence: 72
last_reviewed: 2026-06-14
engine: RabbitMQ 3.13
tags: [datastore, messaging]
---

# RabbitMQ

> The message broker carrying events between services.

## What lives here

| Carries | Producer | Consumer |
|---------|----------|----------|
| `subscription.upgraded` | billing-service | messaging-service |
| `message.delivered` / `message.failed` | messaging-service | (subscribers) |

## Notes & operations

!!! danger "Suspected dead"
    The `legacy.sms_gateway` binding has no producers since SMS was retired.
