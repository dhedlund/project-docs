---
title: Message settings
type: options
status: active
reviewed_confidence: 70
last_reviewed: 2026-06-14
sources:
  - repo: beacon-messaging
    branch: main
    sha: 7a8b9c0
    committed: 2026-05-22
    paths:
      - lib/beacon/messaging/send.ex
      - lib/beacon/messaging/settings.ex
uses_services:
  - messaging-service
uses_models:
  - delivery-event
  - organization
domain: messaging
surfaces:
  - dashboard
tags: [messaging]
---

# Message settings

> Per-organization sending controls, set in the [dashboard](../surfaces/dashboard.md).
> A few interact in ways a flat list won't show.

These five settings shape *how* and *when* your messages go out — without touching
any individual send. You set them once for the whole [organization](../models/organization.md),
and every message that org sends inherits them: the throughput it's allowed, the
hours it stays quiet, what happens when a provider hiccups, and which
channel to use when a send doesn't name one. Think of them as the org-wide policy
that the per-message [send flow](../flows/send-message.md) reads each time it fires.

A few things to keep in mind before the reference tables:

- **Scope is the whole org, not a single send.** There's no per-message override for
  these on the dashboard. A send can specify its own `channel` and `sendAt`, but the
  rate limit, quiet hours, retry policy, and fallback are the org's, applied to
  every message it produces — including the [reactive confirmation](../flows/send-message.md)
  messaging-service sends itself after a `subscription.upgraded` event.
- **They're read live, at fire time.** Like org status, these settings are
  re-evaluated when a message actually fires, not frozen when it was accepted or
  scheduled. Change `quiet_hours` while a message waits in the queue and the *new*
  window applies. This is the same "re-check, don't cache" discipline the
  [send flow](../flows/send-message.md) leans on everywhere.
- **A bad value is rejected, not silently swallowed.** Setting `rate_limit` to a
  non-integer or pointing `fallback_channel` at the same channel as the primary is
  caught at save time with a clear error; it won't quietly corrupt your sending.

## Options

The settings, most-impactful first. `rate_limit` and `quiet_hours` change *whether
and when* a message goes out; `retry_policy` and `fallback_channel` decide what
happens *after* something goes wrong; `default_channel` is a convenience that only
matters when a send omits its channel.

| Option | What it does | Values (default) | Set where / by | Notes |
|--------|--------------|------------------|----------------|-------|
| `rate_limit` | max sends per minute | integer (`60`) | dashboard, admin | Per-org, per-minute ceiling. Email/SMS over the limit **queue and drain**; they don't fail. Push is exempt. |
| `quiet_hours` | window when sends are held | time range (off) | dashboard, admin | Uses the **org's** timezone. Sends due inside the window are **held until it ends**, not dropped. |
| `retry_policy` | retries on provider failure | `none` / `standard` / `aggressive` (`standard`) | dashboard, admin | Re-attempts a send the *provider* refused. Distinct from rate-limit queuing. Gates whether `fallback_channel` can ever fire. |
| `default_channel` | channel when unspecified | `email` / `sms` / `push` (`email`) | dashboard, member | Only consulted when a send doesn't name a channel. `sms` is a [legacy channel](../flows/send-message.md). |
| `fallback_channel` | channel to try if the primary fails | channel or off (off) | dashboard, admin | Fires **only after** the primary's retries are exhausted, so it's inert under `retry_policy: none`. Must differ from the primary. |

### What each one actually does

A short tour, in the same order — read the row above for the shape, here for the why
and the edges.

**`rate_limit` — smooth bursts into a steady stream.** This is a per-org,
per-minute ceiling on sends, defaulting to `60`. Its job is to keep a burst from
overwhelming a downstream provider (and from blowing through provider-side limits
that would bounce your traffic). When an email or SMS send would push the org over
the limit, it doesn't fail — it **queues and drains at the configured rate**, so
the caller sees an accepted send that simply lands slightly later. The one channel
this doesn't touch is **push**, which is exempt; a push send sails through even
mid-burst. That asymmetry is deliberate and shows up again in the
[send flow's](../flows/send-message.md) channel matrix.

**`quiet_hours` — hold sends during off-hours.** Off by default. Set a time range
and any message that would fire inside it is **held until the window closes**, then
released. Nothing is dropped — quiet hours *defer*, they don't reject (contrast
with org suspension, which is a hard stop). The sharp edge here is timezone:
quiet hours are evaluated in the **org's** timezone, not the recipient's, so an org
with customers spread across zones can't express "quiet for each customer locally."
That's a known limitation, not a bug — see the gotcha below.

**`retry_policy` — re-attempt sends a provider refused.** Defaults to `standard`.
This governs what happens when the *provider* rejects or errors on a send (a
transient `503`, a gateway timeout). It's a separate stage from rate-limit
queuing: throttling decides *when* an attempt is made, retries decide *how many
times* to re-attempt one that failed.

| Value | Behavior |
|-------|----------|
| `none` | No retry. The first provider failure is terminal — straight to a `failed` [delivery event](../models/delivery-event.md). |
| `standard` | A bounded set of retries with backoff (the default). |
| `aggressive` | More attempts over a longer window, for orgs that prioritize getting through over giving up fast. |

Two outcomes are worth internalizing: terminal failures (a carrier rejecting an
invalid number, an opt-out) are **never retried regardless of policy** — only
transient errors are (see the [SMS provider](../integrations/sms-provider.md)
notes); and `retry_policy` is the switch that makes `fallback_channel` meaningful,
because the fallback only fires once retries are *exhausted*.

**`default_channel` — the channel for sends that don't name one.** Defaults to
`email`. Most sends specify their channel explicitly (the API and dashboard both
let you choose), so this only kicks in when a send omits it. Note `sms` is a
[legacy channel](../flows/send-message.md) — selectable here, but the modern path
routes SMS through the unified provider, and there's a suspected-dead legacy SMS
branch flagged on the send flow.

**`fallback_channel` — a second channel when the primary gives up.** Off by
default. When set (and *different* from the primary), a send whose primary channel
exhausts its retries is re-attempted on the fallback channel as a **fresh send** —
its own org-status gate, its own [delivery event](../models/delivery-event.md). It
is **not** a per-attempt failover and it is **not** a retry; it's what happens
*after* the retry policy has run out of attempts. Set it to the same channel as the
primary and it's a no-op (rejected at save). Leave `retry_policy` at `none` and the
fallback can never fire, because there's no "retries exhausted" moment to trigger
it.

### Who can set what

The "Set where / by" column above names the lowest role that can change each
setting, all from **Settings → Messaging** in the [dashboard](../surfaces/dashboard.md).
Most settings are **admin**-level; `default_channel` is listed as **member**-level.

!!! warning "Discrepancy: who can edit message settings"
    The source for this page marks `default_channel` as settable by a **member**,
    but [Roles & permissions](../access/roles.md) puts *all* of "Edit message
    settings" at Owner/Admin only — Members can compose, send, and watch the
    delivery log, but see no settings screen. These two statements can't both be
    true as written. The role matrix is the deliberate, human-readable contract, so
    treat Owner/Admin as the safe answer until the `default_channel` permission is
    confirmed against code. Flagged for a maintainer; needs verification.

There are no internal-role (Beacon staff) controls here — Support and Ops never edit
a customer's message settings; see the [roles page](../access/roles.md) for that
boundary.

## Interactions

The part a flat list can't capture: settings that gate, conflict with, or depend on
each other, and which one wins. Read each row as "in *this* situation, *that*
setting behaves as described."

| When… | …this option | behaves as |
|-------|--------------|------------|
| `quiet_hours` active | a scheduled `sendAt` inside the window | held until quiet hours end, not dropped |
| `rate_limit` hit | push channel | ignored — push isn't throttled (see [Send a message](../flows/send-message.md)) |
| `rate_limit` hit | email or SMS channel | queued and drained at the limit — accepted, not failed |
| `fallback_channel` set | `retry_policy: none` | fallback never triggers — it only fires after the primary's retries are exhausted |
| `fallback_channel` = `default_channel` | — | no-op; the fallback must differ from the primary |
| org `suspended` | every setting | moot — the send is rejected (`org_suspended`) before any of these apply |
| `quiet_hours` **and** `rate_limit` both bite | a due send | both defer it: held to the window's end, *then* still subject to the per-minute limit when released |

A couple of these deserve a sentence more:

- **Quiet hours vs. suspension look alike but aren't.** Both can stop a message at
  fire time, but quiet hours **defer** (the message goes out later) while suspension
  **rejects** (the message is dropped with a reason). The
  [send flow's worked scenarios](../flows/send-message.md) walk both side by side.
- **Throttling and retries are different stages, not competitors.** A message can be
  throttled (paced by `rate_limit`) and *then*, when it finally hits the provider,
  fail and fall to `retry_policy`. They stack; neither overrides the other.
- **The order of gates is fixed:** org status → quiet hours → rate limit →
  deliver → (on provider failure) retry policy → (on exhaustion) fallback channel.
  Knowing that order explains most "why didn't my message do X?" questions.

## Worked scenarios

The combinations that actually trip people up, walked end to end.

??? example "A burst of 200 emails with `rate_limit: 60`"
    The first ~60 send within the minute; the rest **queue and drain** at 60/min
    over the following minutes. Every one is *accepted* at call time — none fail
    for being over the limit. If you'd sent these as push instead, all 200 would go
    immediately, because push is exempt from `rate_limit`.

??? example "`fallback_channel: sms` with `retry_policy: none`"
    A primary email send fails at the provider. Because `retry_policy` is `none`,
    the failure is terminal **immediately** — there's no "retries exhausted" moment,
    so the SMS fallback **never fires**. The message ends as a single `failed`
    [delivery event](../models/delivery-event.md). To make the fallback meaningful,
    move `retry_policy` to `standard` or `aggressive`.

??? example "`fallback_channel: sms`, `retry_policy: standard`, primary email keeps failing"
    The email send retries per `standard` policy. Once those retries are
    **exhausted**, the message is re-attempted on SMS as a *fresh* send — it runs
    its own org-status gate and writes its own delivery event. You'll see (at least)
    two delivery events for the one logical message: the failed email and the SMS
    attempt's outcome.

??? example "Scheduled send that lands inside `quiet_hours`"
    `sendAt: 03:00` while `quiet_hours` covers 22:00–06:00 **in the org's
    timezone**. At fire time the message is **held until 06:00**, then released down
    the normal send path (where it's still subject to `rate_limit`). It is not
    dropped. If the org were suspended instead, the same message would be rejected,
    not held — defer vs. reject.

??? example "Org spread across timezones, `quiet_hours` set"
    An org with customers in New York and Tokyo sets `quiet_hours` to its own
    business hours. Because the window is evaluated in the **org's** timezone, a
    Tokyo customer may receive a message at an awkward local hour. There's no
    per-recipient quiet-hours today; this is the known limitation called out below.

## How this connects

- **Where they're applied:** every send reads these in the
  [Send a message](../flows/send-message.md) flow — the channel matrix (push
  exemption), the scheduled/quiet-hours hold, and the throttle-then-retry stages all
  trace back to settings on this page.
- **Where they're set:** the [merchant dashboard](../surfaces/dashboard.md), under
  **Settings → Messaging**.
- **Who can set them:** [Roles & permissions](../access/roles.md) (note the
  `default_channel` discrepancy flagged above).
- **What they act on:** sends produced by
  [messaging-service](../services/messaging-service.md), recorded as
  [delivery events](../models/delivery-event.md); retries interplay with the
  [email](../integrations/email-provider.md) and
  [SMS](../integrations/sms-provider.md) providers' own failure handling.

## Notes & nuances

??? warning "Gotchas"
    `quiet_hours` uses the **org's** timezone, not the recipient's — a known
    limitation for orgs with customers across zones.

    `fallback_channel` is **not** a per-attempt failover and **not** a retry — it
    fires only after `retry_policy` runs out of attempts, so it's silently inert
    whenever `retry_policy` is `none`. If you set a fallback and never see it used,
    check the retry policy first.

    `rate_limit` over-limit sends are **delayed, not dropped** for email/SMS, and
    **don't apply at all** to push. "I hit my rate limit and lost messages" almost
    always means a terminal *provider* failure under `retry_policy: none`, not the
    rate limiter.

??? note "Legacy `sms` channel"
    `sms` remains selectable for `default_channel` and `fallback_channel`, but it's a
    [legacy channel](../flows/send-message.md): modern SMS routes through the unified
    provider, and a suspected-dead legacy SMS branch is flagged on both the
    [send flow](../flows/send-message.md) and
    [messaging-service](../services/messaging-service.md).
