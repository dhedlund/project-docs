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
domain: messaging
tags: [messaging]
---

# Message settings

> Per-organization sending controls, set in the [dashboard](../surfaces/dashboard.md).
> A few interact in ways a flat list won't show.

## Options

| Option | What it does | Values (default) | Set where / by |
|--------|--------------|------------------|----------------|
| `rate_limit` | max sends per minute | integer (`60`) | dashboard, admin |
| `quiet_hours` | window when sends are held | time range (off) | dashboard, admin |
| `retry_policy` | retries on provider failure | `none` / `standard` / `aggressive` (`standard`) | dashboard, admin |
| `default_channel` | channel when unspecified | `email` / `sms` / `push` (`email`) | dashboard, member |
| `fallback_channel` | channel to try if the primary fails | channel or off (off) | dashboard, admin |

## Interactions

| When… | …this option | behaves as |
|-------|--------------|------------|
| `quiet_hours` active | a scheduled `sendAt` inside the window | held until quiet hours end, not dropped |
| `rate_limit` hit | push channel | ignored — push isn't throttled (see [Send a message](../flows/send-message.md)) |
| `fallback_channel` set | `retry_policy: none` | fallback never triggers — it only fires after the primary's retries are exhausted |
| `fallback_channel` = `default_channel` | — | no-op; the fallback must differ from the primary |

## Notes & nuances

??? warning "Gotchas"
    `quiet_hours` uses the **org's** timezone, not the recipient's — a known
    limitation for orgs with customers across zones.
