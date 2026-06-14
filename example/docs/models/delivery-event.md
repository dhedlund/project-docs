---
title: Delivery event
type: model
status: active
reviewed_confidence: 62
last_reviewed: 2026-06-14
backing_stores:
  - mongo: messaging.delivery_events
owned_by: messaging-service
related_models:
  - subscription
tags: [messaging, events]
---

# Delivery event

> A write-once record of one message send attempt and its outcome. High volume,
> append-only, stored in MongoDB by
> [messaging-service](../services/messaging-service.md). See
> [ADR 0001](../decisions/0001-delivery-events-in-mongodb.md) for why it's in Mongo.

## Business view

*Plain language — safe for non-engineers.*

| Attribute | What it means | Rules / behavior |
|-----------|---------------|------------------|
| Outcome | Whether the message arrived | Delivered, failed, or bounced |
| Channel | How it was sent | Email today; SMS only on old records (retired) |
| When | Time of the attempt | One record per attempt; never updated |
| Org | Which customer it belongs to | Used for per-customer delivery reporting |

## How it maps to storage

This is a **schemaless** MongoDB collection, so "the model" is really the *union of
shapes that have existed over time*. Newer fields simply don't exist on older
documents — that's expected, not corruption. The reference below describes the
**current** shape and flags where older documents differ. Because there's no schema
enforcement, every consumer must code defensively rather than assume a field exists.

---

*Everything below is engineer-facing reference.*

## Document shape

*For a schemaless store, "Present on" replaces nullability — it's the field that
matters most here.*

| Field | Type | Present on | Notes |
|-------|------|-----------|-------|
| `_id` | ObjectId | all | |
| `message_id` | string | all | soft ref to the message |
| `org_id` | string | all | soft ref to [Organization](organization.md) |
| `status` | string | all | `delivered` / `failed` / `bounced` |
| `channel` | string | all | `email`; `sms` only on legacy rows |
| `provider_id` | string | **≥ 2024-03** | missing on older documents |
| `region` | string | **≥ 2024-07** | added later; older docs have none |
| `attempts` | int | most | absent on oldest rows — treat absent as `1` |
| `debug_payload` | object | a few 2023 rows | see suspected dead |

!!! warning "Field presence drifts by record age"
    The single most important fact about this collection: **older documents lack
    fields added later.** Known cutoffs — `provider_id` (before 2024-03), `region`
    (before 2024-07), `attempts` (oldest rows). Filter on existence or default in
    code; never assume universal presence.

## Defaults & derivations

| Field | DB default | App-level default / derivation |
|-------|------------|--------------------------------|
| any field | **none** (MongoDB applies no defaults) | the writer sets every field explicitly at insert |
| `attempts` (when reading old rows) | — | assume `1` if the field is absent |

## Constraints & validation

| Rule | Enforced in | Detail |
|------|-------------|--------|
| Field presence / types | **none** | no schema validator configured on the collection |
| `status` ∈ {delivered, failed, bounced} | **app** | set by the writer; not validated on read |
| Write-once (no updates) | **app** | convention only — nothing prevents an update |

## Relationships

*All logical — MongoDB, so there are no foreign keys.*

| Related model | Via | Cardinality | Enforcement |
|---------------|-----|-------------|-------------|
| Message | `message_id` | many events → one message | **cross-store (none)** |
| [Organization](organization.md) | `org_id` | many events → one org | **cross-store (none)** |

## Notes & nuances

??? note "Deprecated / historical"
    `channel: "sms"` rows exist from the retired SMS feature. No new SMS rows are
    written. Kept for historical reporting.

??? info "Future / cleanup"
    A one-time best-effort backfill of `region` (from `provider_id`) has been
    discussed but not scheduled. A MongoDB schema validator could be added to stop
    *new* drift, but won't fix existing documents.

!!! danger "Suspected dead"
    `debug_payload` appears on a handful of 2023 rows only — looks like a temporary
    debugging field left in by accident. Not written by current code.

## Sources & confidence

Derived from messaging-service's writer code plus sampling the collection across date
ranges. Confidence is moderate (62) precisely because historical shapes are hard to
fully enumerate from code alone.
