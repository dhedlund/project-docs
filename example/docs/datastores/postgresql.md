---
title: PostgreSQL
type: datastore
status: active
reviewed_confidence: 75
last_reviewed: 2026-06-14
engine: PostgreSQL 16
tags: [datastore]
---

# PostgreSQL

> The relational store for messaging-service's templates and send schedules.

## What lives here

| Holds | Owned by | Notes |
|-------|----------|-------|
| message templates, send schedules | messaging-service | the delivery *log* lives in MongoDB, not here |
