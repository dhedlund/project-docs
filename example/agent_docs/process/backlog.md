# Beacon backlog

> **Fictional reference** — the durable queue behind `plan.md`.

> **RULE — delete-on-completion (no tombstones).** When an item lands, its entry is
> **removed** from this file. The durable record is the git commit + the page
> itself — never a "DONE"/"LANDED" marker left in place. This file is
> forward-looking only.

## Classification

- **`DOC-NEW`** — a needed page that doesn't exist.
- **`DOC-DEEPEN`** — a stub to flesh out.
- **`DOC-VERIFY`** — an existing page that's stale or low-confidence; re-verify
  against source.
- **`DOC-LINK`** — missing/asymmetric cross-links.
- **`CONTRACT`** — TypeSpec/OpenAPI/AsyncAPI work.
- **`FINDING`** — broken/suspicious code surfaced while documenting; needs
  confirmation (and likely an upstream ticket).
- **`OUT`** — explicitly out of scope, named so a cold reader sees the decline.

---

## DOC-NEW

- `accounts-service` full page + `User` model. *(in flight — see `plan.md` Now)*
- `Invoice` model (referenced by `Subscription`).
- `Plan` model (referenced by `Subscription` and billing).
- `beacon-web` feature pages (deferred until backend coverage settles — see plan
  Open questions).

## DOC-VERIFY

- `Subscription` (`reviewed_confidence: 80`) — the pre-2023 `tier` → `plan_id` path
  isn't fully traced; re-verify against `beacon-billing`.
- `Delivery event` (`reviewed_confidence: 62`) — historical document shapes are
  hard to enumerate from code alone; re-sample.

## DOC-LINK

- Generate "Used by features" backlinks on model pages from feature frontmatter
  (derive one direction; don't hand-maintain both). Convergence-pass candidate.

## CONTRACT

- `accounts-service` has no TypeSpec/OpenAPI contract yet — author one so the
  service page can embed it and `billing-service` can verify the `GET /orgs/{id}`
  dependency.
- Establish AsyncAPI backward-compat baselines for the messaging events
  (`asyncapi diff` against a committed baseline).

## FINDING (suspected dead / drift — confirm with source owner)

- `beacon-billing`: the UI sends `coupon_code` on plan upgrade but the service
  ignores it; coupon handling appears to have moved to checkout. Confirm; if dead,
  drop from contract + UI. (See `Plan upgrade` feature callout.)
- `beacon-billing`: `POST /subscriptions/{id}/downgrade` route — no caller found;
  possibly dead. (See `billing-service` callout.)
- `beacon-billing`: `subscriptions.promo_ref` column never written by current code.
  (See `Subscription` callout.)
- `beacon-messaging`: `legacy.sms_gateway` consumer binds a queue with no
  producers since SMS was retired; likely dead. (See `messaging-service` callout.)
- `beacon-messaging`: `delivery_events.debug_payload` on a few 2023 rows only —
  stray debug field. (See `Delivery event` callout.)

## OUT

- Deployment / infra runbooks (scope decision — see `stewardship/product.md`).
- Third-party message-provider internals.

---

## Research threads (anti-coast — dispatch when the above thins)

- **Coverage sweep** over the four repos → new `DOC-NEW` / `DOC-DEEPEN`.
- **Drift audit** of oldest / lowest-confidence pages → `DOC-VERIFY`.
- **Orphan & dead-link lint** → `DOC-LINK`.
- **Dead-path trace** (pick a feature, UI→API→data) → `FINDING`.
- **Glossary / consistency sweep** across pages.
