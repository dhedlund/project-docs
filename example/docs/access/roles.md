---
title: Roles & permissions
type: roles
status: active
reviewed_confidence: 65
last_reviewed: 2026-06-14
sources:
  - repo: beacon-web
    branch: main
    sha: 9f8e7d6
    committed: 2026-06-02
  - repo: beacon-accounts
    branch: main
    sha: 4c5d6e7
    committed: 2026-05-28
surfaces:
  - dashboard
  - admin-console
related_services:
  - accounts-service
related_models:
  - organization
related_features:
  - suspend-organization
  - plan-upgrade
tags: [access]
---

# Roles & permissions

> Who can do what in Beacon. There are two separate worlds here: **customer roles**
> that live on a single [organization](../models/organization.md) and govern what
> your own users can do, and **internal roles** held by Beacon staff that reach
> across every org. They never mix — a customer is never staff, and staff never
> appear in your member list.

Most of the time you only care about the first world. If you administer a Beacon
account, skip to [Customer roles](#customer-roles-per-organization) and the
[permission matrix](#permission-matrix). The internal roles section is for Beacon's
own support and operations people working in the [admin console](../surfaces/admin-console.md).

A role is just a named bundle of permissions. Beacon keeps the set deliberately
small — there is no per-feature role builder and no custom roles today. You pick one
of the roles below per user; that's the whole model. The trade-off is simplicity:
fewer roles are easier to reason about and harder to misconfigure, at the cost of
fine-grained control. If you've used a product with twenty overlapping roles and a
permissions spreadsheet, this will feel refreshingly blunt.

## Customer roles (per organization)

These apply to the users *inside* one organization, the ones you invite from
**Settings → Members** in the [dashboard](../surfaces/dashboard.md).
Roles are scoped to that org: being an Owner of org A grants you nothing in org B.
A user who belongs to two orgs carries an independent role in each.

- **Owner** — full control of the org, including billing, plan changes, API keys,
  and the ability to delete the org or hand ownership to someone else. Think of the
  Owner as the account's root user: the buck stops here, especially for anything
  that costs money. **Exactly one per org.** Ownership isn't shared; to change who
  holds it, the current Owner transfers it, which makes the previous Owner an Admin.
- **Admin** — everything an Owner can do *except* the two account-ending actions:
  deleting the org and transferring ownership. An Admin manages day-to-day setup —
  inviting members, rotating [API keys](../interfaces/auth.md), configuring webhooks
  and message settings, sending messages — but can't change the plan or end the
  account. This is the right role for a team lead or a senior engineer who runs the
  integration but shouldn't be touching the invoice.
- **Member** — the working role for people who send messages and watch them land.
  A Member can compose and send, and view the delivery log, but sees no settings:
  no billing, no API keys, no webhooks, no member management. Give this to anyone
  who operates messaging but doesn't administer the account.

The shape here is a deliberate ladder — Member ⊂ Admin ⊂ Owner — so a higher role
can always do everything a lower one can, plus more. There's no role that, say,
manages billing but can't send messages; capabilities only ever add as you climb.

??? info "Why only one Owner?"
    Billing and account deletion are single-throat-to-choke actions, and a sole
    Owner makes accountability unambiguous: there is always exactly one person
    answerable for the plan and the account's existence. The cost is a bus-factor of
    one — if the Owner leaves, someone has to transfer ownership before they go, or
    you'll need Beacon support to help recover the account. Promote a trusted second
    person to Admin early so the transfer is a one-click handoff when the time comes.

## Internal roles (Beacon staff)

These belong to Beacon employees and only exist inside the
[admin console](../surfaces/admin-console.md). They are **cross-org**: a Support or
Ops user can look up *any* customer, which is exactly why their abilities are kept
narrow and read-leaning. No internal role can send a message as a customer or touch
a customer's billing.

- **Support** — read-only. Look up any [organization](../models/organization.md) and
  search [delivery events](../models/delivery-event.md) across orgs to answer "did my
  message send?" questions. Support can see, but not change, customer state.
- **Ops** — everything Support can do, **plus** the ability to suspend and reinstate
  an org (see [Suspend an organization](../features/suspend-organization.md)). This
  is the lever Beacon pulls for non-payment or abuse. It's intentionally an Ops-only
  action, not Support's, so a routine lookup can never accidentally take a customer
  offline.

Like the customer side, this is a ladder: Ops is Support plus the one mutating
action. Suspension is the only customer-state change any internal role can make
through the console today; everything else staff can see is read-only.

## Permission matrix

The roles above in one view. Read a row as "can this role do this thing?": ✅ means
yes, a — means no. The last row is about *scope* rather than yes/no — customer roles
can only ever look up their **own** org, while internal roles can look up **any** org.

| Action | Owner | Admin | Member | Support | Ops |
|--------|-------|-------|--------|---------|-----|
| Send a message | ✅ | ✅ | ✅ | — | — |
| View delivery log | ✅ | ✅ | ✅ | — | — |
| Edit message settings | ✅ | ✅ | — | — | — |
| Manage API keys / webhooks | ✅ | ✅ | — | — | — |
| Invite / manage members | ✅ | ✅ | — | — | — |
| Manage billing / plan | ✅ | — | — | — | — |
| Delete org / transfer ownership | ✅ | — | — | — | — |
| Suspend / reinstate an org | — | — | — | — | ✅ |
| Org / delivery lookup | own org | own org | own org | any | any |

A couple of rows are worth dwelling on:

- **Manage billing / plan** is Owner-only. An Admin runs the integration but cannot
  upgrade, downgrade, or change seats — those flow through billing and so stay with
  the single accountable Owner. (The plan-change flow itself is
  [Plan upgrade](../features/plan-upgrade.md); the entitlements it buys live on the
  [Subscription](../models/subscription.md).)
- **Suspend / reinstate** is the only ✅ that belongs to an internal role and to
  *nobody* on the customer side. A customer can't suspend their own org, and staff
  can't do anything else to it. That narrow intersection is by design.

### How roles map to API scopes

The matrix governs the *dashboard*. The [Messaging API](../interfaces/api/index.md)
is governed separately by **[API key scopes](../interfaces/auth.md)** — a key carries
`messages:send`, `messages:read`, or `webhooks:manage`, independent of any human
role. The connection is at key-creation time: only an **Owner** or **Admin** can mint
or rotate keys, so the role model gates *who hands out* API access even though the key
itself, once issued, acts on its own scopes. A Member who never gets a key has no API
reach; an Admin can issue a `messages:send` key that a script then uses with no human
role at all.

## Notes & nuances

!!! info "Where it's enforced"
    There is **no central policy or authorization service** — Beacon checks
    permissions in the app code of whatever owns the action:

    - **Customer roles** are enforced by the [dashboard](../surfaces/dashboard.md)
      (which hides controls a role can't use) and by
      [accounts-service](../services/accounts-service.md) (Java/Spring), which is the
      authority on org membership and the user's role within an org.
    - **Internal roles** are enforced in the
      [admin console](../surfaces/admin-console.md).
    - **API requests** are gated by [key scopes](../interfaces/auth.md), checked by
      the service handling the request — not by the human role model above.

    Because checks are app-only and spread across surfaces, the matrix on this page
    is the human-readable contract, not a single config you can point at. If you
    change a role's abilities, expect to touch more than one place.

??? warning "Roles are coarse — no custom roles yet"
    Beacon has exactly the five roles above and no role builder. If you need, say,
    "billing access without send access," there's no role for it — the ladder only
    adds capabilities, it doesn't carve them apart. The usual workarounds are to lean
    on the Owner/Admin split for the billing boundary and on per-environment
    [API keys](../interfaces/auth.md) (`sk_test_…` vs `sk_live_…`) for blast-radius
    control. If a customer asks for finer-grained roles, that's a product request,
    not a config change.

??? info "Suspended orgs and roles"
    Suspension acts on the *org*, not on roles. When Ops suspends an org its
    [`status`](../models/organization.md) flips to `suspended` and sends are blocked
    for **everyone** in it — Owner included — regardless of role. Users can still sign
    in and see the dashboard; they just can't send until an Ops user reinstates the
    org. A role grants no exemption from suspension.
