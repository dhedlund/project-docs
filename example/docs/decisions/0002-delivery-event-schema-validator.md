---
title: Add a schema validator to delivery_events
type: decision
status: accepted
date: 2026-06-10
reviewed_confidence: 72
last_reviewed: 2026-06-14
sources:
  - repo: beacon-messaging
    branch: main
    sha: 7a8b9c0
    committed: 2026-05-22
    paths:
      - lib/beacon/messaging/delivery_event.ex
related_services:
  - messaging-service
related_models:
  - delivery-event
supersedes: 0001-delivery-events-in-mongodb.md
tags: [messaging, storage]
---

# 0002 — Add a schema validator to delivery_events

Supersedes [0001 — Delivery events in MongoDB](0001-delivery-events-in-mongodb.md).

> **In one line:** keep delivery events in MongoDB, but put a guardrail on the
> *door* — a MongoDB JSON-schema validator that rejects malformed **new** writes —
> without touching the millions of historical documents already in the collection.

## Context

[ADR 0001](0001-delivery-events-in-mongodb.md) picked MongoDB for the
[delivery-event](../models/delivery-event.md) log and made one deliberate trade:
**no schema enforcement.** That bought cheap, high-volume appends (millions a day)
and the freedom to add fields over time without migrations. The cost — written down
plainly at the time — was that *older records lack fields added later*, and every
reader has to code defensively.

Two years on, that cost has compounded into real pain.

The collection has grown a documented history of field-presence drift. Pull a
delivery event off the wire and what you get depends on **when it was written**:

| Field | Present on | What a naïve reader assumes |
|-------|-----------|-----------------------------|
| `provider_id` | ≥ 2024-03 | "always there" → `nil` on 2023 rows |
| `region` | ≥ 2024-07 | "always there" → `nil` on early-2024 rows |
| `attempts` | most rows | "always an int" → missing on the oldest rows |

Drift across *record age* is unavoidable history — ADR 0001 accepted it and the
[delivery-event model page](../models/delivery-event.md) documents the cutoffs. But
there is a second, worse problem hiding underneath it: nothing stops a **brand-new**
write from being just as inconsistent as an old one. A bug in the writer, a typo in
a `status` string, a forgotten field on a new code path — none of it is caught. The
collection has no opinion about what a valid delivery event looks like, so "correct"
is defined entirely by writer discipline and re-litigated by every consumer on every
read.

Concretely, here is what the absence of a validator costs us:

- **Every consumer reimplements the same defenses.** Reporting jobs, the
  `message.delivered` / `message.failed` emitters in
  [messaging-service](../services/messaging-service.md), and downstream analytics all
  carry their own "default `attempts` to 1, treat absent `region` as unknown,
  re-check `status` is one of the three we expect" boilerplate. That logic drifts
  between consumers, which is how the *same* row gets counted differently in two
  reports.
- **Writer bugs surface late and far away.** A malformed write lands silently and
  only blows up days later in an aggregation or a customer-facing delivery report —
  far from the code that caused it, with no stack trace pointing home.
- **The contract is folklore.** "What fields does a current delivery event have?"
  has no authoritative answer the database can give you. It lives in tribal memory
  and in the model page, both of which can fall out of step with reality.

What we explicitly are **not** trying to do here is rewrite history. The drift on
old documents is real, bounded, and well-understood; back-filling millions of
write-once records is expensive, risky, and buys little. The goal is narrower and
more valuable: **stop the bleeding going forward** so that "new" stops being a
source of surprises.

## Decision

Keep delivery events in MongoDB — the [ADR 0001](0001-delivery-events-in-mongodb.md)
storage choice stands in full. Add a MongoDB **JSON-schema validator** to the
`messaging.delivery_events` collection that constrains **new** writes only.

Three properties define the decision:

1. **Forward-only.** The validator is attached with
   `validationLevel: "moderate"`, which tells MongoDB to validate inserts and
   updates to documents that *already satisfy* the schema, but to **leave existing
   non-conforming documents alone**. Historical rows are grandfathered — they are
   never re-validated and never rejected on read. (We use `moderate` rather than
   `strict` precisely because `strict` would also validate updates to old documents;
   delivery events are write-once, so in practice this difference only matters as a
   safety net.)
2. **Reject, don't warn.** `validationAction: "error"`. A write that violates the
   schema is refused with a `DocumentValidationFailure`, not quietly logged and
   accepted. A loud failure at write time is the entire point — it pins the problem
   to the code that caused it.
3. **Describe the current shape, loosely.** The schema codifies the
   *current* delivery-event shape: the always-present core
   (`message_id`, `org_id`, `status`, `channel`), `status` constrained to
   `{delivered, failed, bounced}`, `channel` to the live value set, and types on the
   age-dependent fields *when present*. It does **not** mandate the age-dependent
   fields (`provider_id`, `region`, `attempts`) — they stay optional so the writer
   keeps its freedom to evolve, and so a future field can be added the same low-cost
   way ADR 0001 wanted.

The validator lives with the rest of messaging-service's storage setup so it ships
and versions alongside the code that writes to the collection — it is part of the
service's owned schema, not a hand-applied database tweak. The
[MongoDB datastore page](../datastores/mongodb.md) and the
[delivery-event model](../models/delivery-event.md) are the two pages that describe
the resulting shape; both should reflect that a validator now exists.

### What the validator looks like

The collection-level validator is roughly this — the **new** door it puts in front
of writes:

```javascript
db.runCommand({
  collMod: "delivery_events",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["message_id", "org_id", "status", "channel"],
      properties: {
        message_id:  { bsonType: "string" },
        org_id:      { bsonType: "string" },
        status:      { enum: ["delivered", "failed", "bounced"] },
        channel:     { enum: ["email", "sms"] },
        provider_id: { bsonType: "string" },   // optional: present ≥ 2024-03
        region:      { bsonType: "string" },    // optional: present ≥ 2024-07
        attempts:    { bsonType: "int" }         // optional: absent ⇒ treat as 1
      }
    }
  },
  validationLevel: "moderate",
  validationAction: "error"
})
```

A few choices worth calling out, because they are easy to get wrong:

- **`required` lists only the universal core.** Those four fields appear on *every*
  document, old and new, so requiring them is safe under `moderate` and meaningful
  going forward. Adding an age-dependent field to `required` would be wrong twice
  over: it would reject legitimately-shaped new writes that don't carry it, and it
  would describe a uniformity the collection has never had.
- **`channel` still permits `sms`.** No new SMS rows are written — the feature is
  retired — but the validator describes the *value set the schema allows*, not
  current traffic, and keeping `sms` valid avoids tripping over the legacy value if
  any code path ever touches it. The "no new SMS" fact stays documented on the
  [delivery-event model](../models/delivery-event.md), not enforced here.
- **`status` is an `enum`, not a free string.** This is the highest-value single
  constraint: a typo'd status (`"deliverd"`) silently poisons every delivery report,
  and now it can't get in.

Here is the behavior you actually get at write time:

```text
// New, well-formed → accepted
{ message_id: "m_1", org_id: "o_7", status: "delivered", channel: "email",
  provider_id: "px_9", region: "us-east", attempts: 1 }            ✅ inserted

// New, typo'd status → rejected loudly, at the source
{ message_id: "m_2", org_id: "o_7", status: "deliverd", channel: "email" }
                                              ✗ DocumentValidationFailure

// Old 2023 document missing provider_id → still readable, never re-checked
{ message_id: "m_0", org_id: "o_3", status: "failed", channel: "sms" }
                                              ✅ untouched (grandfathered)
```

## Consequences

**What gets better.**

- **New field drift stops.** Every row written from now on carries the core four
  with the right types and a valid `status` and `channel`. "Current shape" finally
  has an authority the database can enforce, not just a wiki page.
- **Writer bugs fail fast and local.** A malformed write is rejected with a clear
  `DocumentValidationFailure` at insert time, next to the code that caused it,
  instead of surfacing days later in a skewed report. (Reassuringly: a bad write
  doesn't corrupt anything — it's simply refused.)
- **Consumers can lean on the core a little more.** Readers can now trust that any
  document written after the validator landed has the four core fields with correct
  types and a known `status`. That trims some defensive boilerplate.

**What does not change — read this before you relax your readers.**

- **History still drifts.** The validator is not retroactive. Older documents still
  lack `provider_id`, `region`, and `attempts` exactly as before, and the
  "field presence drifts by record age" caveat on the
  [delivery-event model](../models/delivery-event.md) **still holds for old data.**
  Any consumer that reads across historical ranges must keep its existing defenses
  (default `attempts` to `1`, treat absent `region`/`provider_id` as unknown).
- **Age-dependent fields are still optional even on new writes.** Because they're not
  in `required`, a new document *can* legitimately omit them. Don't read "validator
  added" as "every field is now guaranteed" — only the core four are.
- **The storage decision is unchanged.** This ADR revises exactly one consequence of
  [ADR 0001](0001-delivery-events-in-mongodb.md) — the "no schema validation" cost —
  and nothing else. MongoDB, the two-store split, and the high-volume append model
  all stand.

**New trade-offs we're taking on.**

- **A small write-path cost.** MongoDB evaluates the schema on every insert. For an
  append-only collection at millions/day this is a real-but-minor overhead; the
  schema is intentionally shallow (no deep nesting, no regex) to keep it cheap.
- **The schema is now a thing to maintain.** Add a field to the writer and you must
  add it (as optional) to the validator, or the first write of the new shape gets
  rejected — turning a no-migration change into a two-step one. This is a deliberate
  tax: the validator's value *is* that nothing slips in unannounced. Treat schema
  changes as part of the same change set as the writer change, and keep the
  [delivery-event model page](../models/delivery-event.md) in step.
- **`enum` mistakes bite at deploy time.** If a future legitimate `status` or
  `channel` value is introduced in code but not added to the enum first, its writes
  will be rejected. Order the rollout: widen the validator, then ship the writer.

??? info "Future / cleanup"
    A one-time best-effort backfill of `region` (derived from `provider_id`) on
    historical rows has been discussed but not scheduled — see the same note on the
    [delivery-event model](../models/delivery-event.md). If it ever happens it would
    *narrow* the historical drift but would not change this decision; the validator
    would still be the thing keeping new writes honest. Tightening
    `validationLevel` from `moderate` to `strict` only makes sense after such a
    backfill (and given write-once events, would change little either way).

??? note "Why not a different fix?"
    We weighed three alternatives before landing here.

    - **Migrate the log to PostgreSQL** for real DB-level schema. Rejected: ADR 0001
      chose Mongo deliberately for cheap high-volume appends and migration-free field
      growth; a high-churn append-only relational table reintroduces exactly the
      problems 0001 avoided.
    - **Enforce the shape only in application code** (a shared write wrapper).
      Rejected as the *sole* mechanism: it doesn't stop an out-of-band or
      future-second writer, and it leaves the database with no opinion of its own.
      (The app still validates too — defense in depth — but the collection is now the
      backstop.)
    - **Validate but only warn** (`validationAction: "warn"`). Rejected: a warning
      that's logged and accepted still lets the bad document land, so consumers gain
      nothing they can rely on. Reject-at-the-door is what makes the guarantee real.
