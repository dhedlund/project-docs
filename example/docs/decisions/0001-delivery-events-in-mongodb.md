---
title: Delivery events in MongoDB
type: decision
status: superseded
date: 2026-06-14
related_services:
  - messaging-service
related_models:
  - delivery-event
tags: [messaging, storage]
---

# 0001 — Delivery events in MongoDB

> **Superseded by [0002](0002-delivery-event-schema-validator.md).** The storage
> choice stands; its no-validation consequence was revised.

## Context

messaging-service writes one [delivery event](../models/delivery-event.md) per send
attempt. Volume is high (millions/day), writes are append-only, reads are mostly
recent-window lookups and aggregate reporting, and the useful set of fields has grown
over time. The service's relational data (templates, schedules) already lives in
PostgreSQL.

## Decision

Store delivery events in **MongoDB**, separate from the relational PostgreSQL data,
rather than adding a high-churn append-only table to PostgreSQL.

## Consequences

- **Positive:** cheap high-volume appends; schema can evolve without migrations as
  new fields are added.
- **Negative / the cost we live with:** no schema enforcement means **older records
  lack fields added later** — the central caveat documented on the
  [delivery-event model](../models/delivery-event.md). Consumers must code
  defensively. Cross-store joins (e.g. event → subscription) are application-side
  only.
