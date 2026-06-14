# Beacon plan

> **Fictional reference** — a plan mid-flight, after bootstrap and a few passes.

The rolling plan: *Now* plus the immediately-next item. The durable queue lives in
`backlog.md`. Target ≤ ~200 lines. See `../../../agent_docs/process/loop.md` for how
to update this.

## Where Beacon is

Bootstrapped. Stub pages exist across the layers. Deepened so far:
`billing-service`, `messaging-service`, the `Subscription`, `Delivery event`, and
`Organization` models, the `Plan upgrade` feature, and ADR 0001.
`accounts-service` is still referenced-but-not-documented.

## Now

**Deepen `accounts-service` from reference-only to a full service page, plus the
`User` model it owns.** Definition of done: service page meets the
`audit-checklist.md` service checklist (responsibilities, interface/contract or a
`CONTRACT` backlog entry, owned models, one flow diagram); `User` model meets the
model checklist; both link bidirectionally with `Organization`. Source:
`beacon-accounts`.

## Up next

- Author the `Invoice` and `Plan` models (referenced by `Subscription`; currently
  dangling).

## Last completed

Deepened the `Delivery event` model (MongoDB shape-drift documented) and wrote
ADR 0001 (delivery events in MongoDB). Git log is the canonical history.

## Recent discoveries

(Empty per the loop — discoveries are distilled into the backlog / page callouts.)

## Open questions

- Document `beacon-web` UI components now, or after backend coverage is complete?
  (Leaning: after, so features link down into settled service/model pages.)
