---
title: Add a schema validator to delivery_events
type: decision
status: accepted
date: 2026-06-10
related_services:
  - messaging-service
related_models:
  - delivery-event
supersedes: 0001-delivery-events-in-mongodb
tags: [messaging, storage]
---

# 0002 — Add a schema validator to delivery_events

Supersedes [0001 — Delivery events in MongoDB](0001-delivery-events-in-mongodb.md).

## Context

[ADR 0001](0001-delivery-events-in-mongodb.md) chose MongoDB for the delivery-event
log and accepted "no schema validation" as the cost. In practice the field-presence
drift documented on the [Delivery event](../models/delivery-event.md) page has made
consumers brittle — every reader has to defend against missing fields.

## Decision

Keep delivery events in MongoDB, but add a MongoDB **JSON-schema validator** on
`messaging.delivery_events` that constrains *new* writes. Existing documents are
grandfathered; the validator is not retroactive.

## Consequences

- Stops *new* field drift — new rows are uniform.
- Historical rows still vary, so the "field presence drifts by record age" caveat on
  the Delivery event page still holds for old data (and the page says so).
- The storage choice from 0001 stands; only its no-validation consequence is revised.
