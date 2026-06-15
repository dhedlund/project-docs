---
title: Python SDK
type: sdk
status: active
reviewed_confidence: 65
last_reviewed: 2026-06-14
sources:
  - repo: beacon-sdks
    branch: main
    sha: e5f6a7b
    committed: 2026-05-25
    paths:
      - python/
domain: messaging
tags: [sdk]
---

# Python SDK

> The official Python client for the [Messaging API](../api/index.md). It wraps
> the same REST endpoints you'd call by hand — `POST /messages`,
> `GET /messages/{id}` — and adds the ergonomics you'd otherwise rewrite in every
> project: a typed client, retries, pagination, and structured errors.

If you're sending email, SMS, or push from a Python backend, this is the path of
least resistance. You get a small, predictable surface (`client.messages.send(...)`)
instead of hand-rolling HTTP, header plumbing, and retry logic. Under the hood it
talks to the public [Messaging API](../api/index.md), so anything you can do here
you can also do with raw HTTP — the SDK just makes the common cases pleasant and
the sharp edges (idempotency, version pinning, rate limits) safe by default.

The package lives in the `beacon-sdks` repo under `python/`. Model classes are
generated from the API's OpenAPI spec; the helpers around them are hand-written
(see Generated vs hand-written).

## Install & authenticate

```python
# pip install beacon
from beacon import Beacon

client = Beacon(api_key="sk_live_...")
```

The client needs an API key. Keys are environment-scoped bearer tokens — `sk_live_…`
for production, `sk_test_…` for sandbox — created and rotated by an org **owner** or
**admin** in the [dashboard](../../surfaces/dashboard.md). See
[API authentication](../auth.md) for scopes (`messages:send`, `messages:read`,
`webhooks:manage`) and key handling. A key is shown only once at creation; treat it
as a secret.

Don't hard-code the key. Read it from the environment so the same code runs in
sandbox and prod by swapping one variable:

```python
import os
from beacon import Beacon

client = Beacon(api_key=os.environ["BEACON_API_KEY"])
```

??? info "Pointing at sandbox"
    The key prefix selects the environment for billing and routing, but the client
    talks to the production host (`https://api.beacon.example`) by default. To
    exercise the sandbox API explicitly — for example in CI — point the base URL at
    `https://api.sandbox.beacon.example` and use an `sk_test_…` key:

    ```python
    client = Beacon(
        api_key=os.environ["BEACON_API_KEY"],   # sk_test_...
        base_url="https://api.sandbox.beacon.example",
    )
    ```

    Sandbox sends don't reach real recipients, which makes it the right place to
    test webhook handling end to end.

## Quickstart

Send your first message — a templated email — in one call:

```python
msg = client.messages.send(to="user@example.com", channel="email", template="welcome")
print(msg.id, msg.status)   # msg_01H...  queued
```

`send` maps to `POST /messages`. The three required fields mirror the API's
`SendMessage` body: **`to`** (the recipient address), **`channel`**, and
**`template`** (the name of a template defined in
[messaging-service](../../services/messaging-service.md)). You pass a template name,
not raw content — Beacon renders it server-side.

The call returns a `Message` whose `status` starts at `queued`. Delivery is
asynchronous, so a fresh message is almost never `delivered` yet. To find out what
actually happened, either poll the message or — far better for production — subscribe
to [webhooks](../webhooks/index.md) and react to `message.delivered` /
`message.failed`.

```python
# Poll for the current state (GET /messages/{id})
latest = client.messages.get(msg.id)
print(latest.status)   # queued -> sent -> delivered | failed | bounced
```

A message moves through the same `MessageStatus` values the API exposes:
`queued → sent → delivered`, or terminally `failed` / `bounced`. These mirror the
public webhook events one-for-one, so the status you poll and the event you receive
always agree.

### Scheduling a send

Omit `send_at` to send now; pass a timezone-aware `datetime` to schedule for later
(the API field is `sendAt`):

```python
from datetime import datetime, timedelta, timezone

client.messages.send(
    to="user@example.com",
    channel="email",
    template="trial-ending",
    send_at=datetime.now(timezone.utc) + timedelta(days=2),
)
```

### Channels

`channel` accepts `email`, `sms`, or `push`. In practice **email is the live
channel**; `sms` exists but is legacy, so treat non-email channels as opt-in and
confirm with your account before relying on them. The SDK doesn't validate the
channel locally — an unsupported value comes back as an API error, not a client
exception.

## Idempotency

Network calls fail halfway. If you retry a `send` after a timeout, you don't want a
duplicate message going out. The API takes an `Idempotency-Key` header on
`POST /messages` so a retried request with the same key returns the original result
instead of sending again.

The SDK's built-in retries (below) reuse one key across attempts automatically, so
you're already protected against transient failures. For at-most-once semantics
across *your own* retries — say, a job runner that may re-run the whole task — pass a
stable key derived from your domain (an order ID, a job ID):

```python
client.messages.send(
    to="user@example.com",
    channel="email",
    template="receipt",
    idempotency_key=f"receipt-{order.id}",
)
```

Reuse the same key only for what is genuinely the same send. A key collision across
two *different* messages will hand the second caller the first message's result.

## Retries & rate limits

`send`/`get` retry transient failures (network errors, `5xx`, and `429`) with
exponential backoff. The client honours the `Retry-After` header the API returns on
a `429`, so it backs off for exactly as long as the server asks rather than guessing.

Because retries reuse a single idempotency key per logical call, a retried `send`
won't double-send. Reads (`get`) are naturally safe to repeat.

You can tune or disable retries when you'd rather own the policy — for example
inside a job system that already retries:

```python
client = Beacon(api_key=os.environ["BEACON_API_KEY"], max_retries=0)
```

## Listing & pagination

List endpoints return an iterator that fetches pages lazily, so you can loop over
every result without managing cursors yourself:

```python
for message in client.messages.list(status="failed"):
    print(message.id, message.created)
```

Iterate the result directly; the SDK requests the next page only when you reach the
end of the current one. Avoid materializing everything (`list(...)`) on
high-volume accounts — delivery history grows large, and lazy iteration keeps memory
flat.

## Errors

Failed requests raise a typed exception instead of returning an error object, so you
can catch the specific case you care about. Each exception carries the API's
JSON `{code, message}` and the HTTP status:

```python
from beacon import BeaconError, RateLimitError, AuthenticationError

try:
    client.messages.send(to="user@example.com", channel="email", template="welcome")
except RateLimitError as e:
    # already retried with backoff and still throttled
    print("slow down:", e.retry_after)
except AuthenticationError:
    # bad or revoked key, or missing scope
    print("check BEACON_API_KEY and its scopes")
except BeaconError as e:
    # anything else — inspect the structured payload
    print(e.status, e.code, e.message)
```

`BeaconError` is the base class; catch it last as a safety net. The mapping follows
HTTP status: `401`/`403` → `AuthenticationError`, `429` → `RateLimitError`, other
non-2xx → `BeaconError` with the parsed `code`/`message`. A malformed request (an
unknown channel, a missing template) surfaces as a `BeaconError` with the API's
error code — it's rejected cleanly server-side, nothing is half-sent.

## Reacting to delivery outcomes

The SDK sends messages; it does not receive webhooks for you. Delivery is
asynchronous and out-of-order, so the durable way to learn an outcome is to handle
[webhooks](../webhooks/index.md) (`message.delivered`, `message.failed`,
`message.bounced`) and **verify the signature** before trusting the payload.

```python
from beacon.webhooks import verify_signature, WebhookVerificationError

def handle(request):
    try:
        event = verify_signature(
            payload=request.body,
            signature=request.headers["Beacon-Signature"],
            secret=os.environ["BEACON_WEBHOOK_SECRET"],
        )
    except WebhookVerificationError:
        return 400  # stale timestamp or bad signature — drop it

    if event.type == "message.delivered":
        mark_delivered(event.data["message_id"])
```

Two things the [webhooks](../webhooks/index.md) page spells out and your handler must
respect: delivery is **at-least-once** (dedupe on the stable `message_id`, not the
per-attempt `Beacon-Delivery` ID), and **order is not guaranteed** (`delivered` can
arrive before `sent`). Reconcile against current message state rather than event
sequence.

## Version compatibility

The API is versioned by date via the `Beacon-Version` header; the SDK pins a version
per major release, so upgrading the SDK is how you move to a newer API contract.

| SDK version | API version | Notes |
|-------------|-------------|-------|
| 2.x | 2026-05-01+ | current |
| 1.x | 2025-08-01 | security fixes only |

Old API versions are supported for **12 months** after a newer one ships, so a 1.x
client keeps working while you migrate. Pin the SDK in your lockfile and upgrade
deliberately — a major SDK bump can carry a new API date with breaking changes.
Stay on a maintained line: 1.x receives security fixes only and no new features.

??? info "Overriding the API version"
    The SDK sends its pinned `Beacon-Version` for you. You normally shouldn't touch
    it, but if you need to test against a specific dated contract you can override
    the header per-client. Mismatching the SDK's models against a much older or
    newer API date is unsupported — prefer upgrading the SDK.

## Notes & nuances

??? info "Generated vs hand-written"
    Model classes are codegen'd from the OpenAPI spec; the ergonomic helpers
    (retries, pagination) are hand-written. The generated layer (`Message`,
    `MessageStatus`, `SendMessage`, `Error`) tracks the spec exactly, so a field
    added to the API shows up after a regenerate-and-release. The hand-written layer
    — the `Beacon` client, retry/backoff, lazy pagination, the typed exception
    hierarchy, and webhook verification — is where the SDK's behaviour, and its
    tests, live.

??? warning "The SDK only covers Messaging"
    This client wraps the public [Messaging API](../api/index.md). It does **not**
    cover Beacon's other domains — there are no SDK methods for
    [accounts](../../services/accounts-service.md) (orgs/users) or
    [billing](../../services/billing-service.md) (plans/subscriptions/invoices).
    Those are internal services with their own contracts; the public Python surface
    is messaging only.
