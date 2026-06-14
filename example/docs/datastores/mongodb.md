---
title: MongoDB
type: datastore
status: active
reviewed_confidence: 70
last_reviewed: 2026-06-14
engine: MongoDB 7
tags: [datastore]
---

# MongoDB

> The high-volume, append-only store for the delivery-event log.

## What lives here

| Holds | Owned by | Notes |
|-------|----------|-------|
| `messaging.delivery_events` | messaging-service | schemaless; see [Delivery event](../models/delivery-event.md) and [ADR 0001](../decisions/0001-delivery-events-in-mongodb.md) |

## Notes & operations

??? info "Operational notes"
    No schema validator configured — hence the field-presence drift documented on
    the delivery-event page.
